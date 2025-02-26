import tos 
import os
from typing import List, Dict
import io
from PIL import Image
import json 
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def _valid_tos_path(path):
    """
    Check if the given path is a valid Terms of Service (TOS) file path.

    Args:
    path (str): The path to be checked.

    Returns:
    bool: True if the path is a valid TOS file path, False otherwise.
    """
    if not path.startswith("tos://"):
        raise ValueError(f"tos path should start with 'tos://'")
        
    if path.endswith("/"):
        raise ValueError(f"tos path should not end with '/'")
    return True

def _split_tospath(path):
    """
    Split the given TOS file path into its components.

    Args:
    path (str): The TOS file path to be split.

    Returns:
    tuple: A tuple containing the bucket name, prefix, and file name.
    """
    path = path.replace("tos://", "")
    path = path.split("/")
    bucket_name = path[0]
    prefix = "/".join(path[1:-1])
    file_name = path[-1]
    return bucket_name, prefix, file_name
    
    
def check_tos_file_exists(tos_filepath, config):
    """
    Check if the Terms of Service (TOS) file exists at the specified filepath.

    Args:
    tos_filepath (str): The filepath of the TOS file. Example: tos://bucket_name/prefix/file_name/
    config (dict): A dictionary containing configuration settings.

    Returns:
    bool: True if the file exists, False otherwise.

    Raises:
    ValueError: If the tos_filepath is empty or None.
    """
    _valid_tos_path(tos_filepath)
    bucket_name, prefix, file_name = _split_tospath(tos_filepath)
    client = tos.TosClientV2(config['ak'], config['sk'], config['endpoint'], config['region'])
    
    truncated = True
    continuation_token = ''
    while truncated:
        try:
            result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token, max_keys=1000)
        except tos.exceptions.TosServerError as e:
            print(f"Error listing objects: {e}")
            return False
        for item in result.contents:
            if item.key.endswith(file_name):
                return True
        truncated = result.is_truncated
        continuation_token = result.next_continuation_token
    return False
    # Check if the file exists
    
def list_all_files_under_tos_dir(tos_dir, config, save2txt = False, custom_save_path = None):
    """
    List all files under the given prefix in the specified bucket.

    Args:
    tos_dir (str): The directory path in the
    """
    output_list = []
    if not tos_dir.startswith("tos://"):
        raise ValueError(f"tos dir should start with 'tos://'")
    if not tos_dir.endswith("/"):
        raise ValueError(f"tos dir should end with '/'")
    bucket_name, prefix, _ = _split_tospath(tos_dir)
    prefix = f"{prefix}/"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        # 1. 列举根目录下文件和子目录
        is_truncated = True
        count = 0
        next_continuation_token = ''
        while is_truncated:
            count += 1
            print(f"{count * 1000} objects have been found!", end="\r")
            out = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=next_continuation_token)
            # print(out, out.__dict__)
            is_truncated = out.is_truncated
            next_continuation_token = out.next_continuation_token

            # contents中返回了根目录下的对象
            for content in out.contents:
                output_list.append(content.key)
        print()
        print("All files have been listed!")
        
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
        print('fail with server error, code: {}'.format(e.code))
        # request id 可定位具体问题，强烈建议日志中保存
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
        
    out = list(filter(lambda x: not x.endswith("/"), output_list))
    print(f"Total number of files: {len(out)}")
    if save2txt:
        if custom_save_path is None:
            save_path = "all_files.txt"
        else:
            save_path = custom_save_path
        write_list_to_txt(out, save_path)
    return out
    
def list_all_subdirs_under_prefix(tos_dir, config, save2txt = False, custom_save_path = None):
    """
    List all subdirectories under the given prefix in the specified bucket.

    Args:
    tos_dir (str): The directory path in the bucket. Example: tos://bucket_name/prefix/
    config (dict): A dictionary containing configuration settings.
    save2txt (bool, optional): Whether to save the subdirectories to a text file. Defaults to False.
    custom_save_path (str, optional): The custom path to save the text file. Defaults to None.

    Returns:
    list: A list of subdirectories under the given prefix.

    Raises:
    ValueError: If the tos_dir is empty or None.
    """
    if not tos_dir.startswith("tos://"):
        raise ValueError(f"tos dir should start with 'tos://'")
    if not tos_dir.endswith("/"):
        raise ValueError(f"tos dir should end with '/'")
    output_list = []
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        bucket_name, prefix, file_name = _split_tospath(tos_dir)
        prefix = f"{prefix}/"
        # 1. 列举根目录下文件和子目录
        is_truncated = True
        count = 0
        next_continuation_token = ''
        while is_truncated:
            count += 1
            print(f"{count * 1000} objects have been found!", end="\r")
            out = client.list_objects_type2(bucket_name, delimiter="/", prefix=prefix, continuation_token=next_continuation_token)
            # print(out, out.__dict__)
            is_truncated = out.is_truncated
            next_continuation_token = out.next_continuation_token

            for file_prefix in out.common_prefixes:
                output_list.append(file_prefix.prefix)
        print()
        print("All subdirs have been listed!")
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
        print('fail with server error, code: {}'.format(e.code))
        # request id 可定位具体问题，强烈建议日志中保存
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
    print(f"Total number of subdirs: {len(output_list)}")
    
    if save2txt:
        if custom_save_path is None:
            save_path = "all_dirs.txt"
        else:
            save_path = custom_save_path
        write_list_to_txt(output_list, save_path)
    
    return output_list


def uid2pil_img(bucket_name, uid, viewIdx, img_format, config, specified_tos_img_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    PIL.Image: The image fetched from the TOS storage.

    Raises:
    ValueError: If the img does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_img_dir is None:
        if bucket in ["v1", "v3"]:
            tos_img_prefix = "rendering/cam72"
        else:
            tos_img_prefix = "data/rendering/cam72"
    else:
        if not specified_tos_img_dir.endswith("/"):
            raise ValueError(f"specified_tos_img_dir should end with '/'")
        if not specified_tos_img_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_img_dir should start with 'tos://'")
        bucket_name, tos_img_prefix, _ = _split_tospath(specified_tos_img_dir)


    object_key = f"{tos_img_prefix}/{uid}/View{viewIdx}_FinalColor.{img_format}"
    full_img_path = f"tos://{bucket_name}/{object_key}"
    if not check_tos_file_exists(full_img_path, config):
        raise ValueError(f"Image does not exist in TOS storage: {full_img_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    if not data:  # Check if data is empty
        raise ValueError(f"Empty data fetched for UID: {uid}, Object Key: {object_key}")
    bytes_io = io.BytesIO(data)
    image = Image.open(bytes_io)
    return image


def uid2camera_info(bucket_name, uid, config, specified_tos_img_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    str : camera info

    Raises:
    ValueError: If the camerainfo txt does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_img_dir is None:
        if bucket in ["v1", "v3"]:
            tos_img_prefix = "rendering/cam72"
        else:
            tos_img_prefix = "data/rendering/cam72"
    else:
        if not specified_tos_img_dir.endswith("/"):
            raise ValueError(f"specified_tos_img_dir should end with '/'")
        if not specified_tos_img_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_img_dir should start with 'tos://'")
        bucket_name, tos_img_prefix, _ = _split_tospath(specified_tos_img_dir)
        
    object_key = f"{tos_img_prefix}/{uid}/camera_info.txt"
    full_txt_path = f"tos://{bucket_name}/{object_key}"
    full_txt_path = f"tos://{bucket_name}/{object_key}"
    if not check_tos_file_exists(full_txt_path, config):
        raise ValueError(f"Camera info does not exist in TOS storage: {full_txt_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    if not data:  # Check if data is empty
        raise ValueError(f"Empty data fetched for UID: {uid}, Object Key: {object_key}")
    bytes_io = io.BytesIO(data)
    camera_info = bytes_io.read().decode('utf-8')
    return camera_info


def uid2mesh(bucket_name, uid, file_type, config, specified_tos_glb_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    PIL.Image: The image fetched from the TOS storage.

    Raises:
    ValueError: If the img does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_glb_dir is None:
        if bucket in ["v1", "v3"]:
            tos_glb_prefix = "glb_models"
        else:
            tos_glb_prefix = "data/glb_models"
    else:
        if not specified_tos_glb_dir.endswith("/"):
            raise ValueError(f"specified_tos_glb_dir should end with '/'")
        if not specified_tos_glb_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_glb_dir should start with 'tos://'")
        bucket_name, tos_glb_prefix, _ = _split_tospath(specified_tos_glb_dir)

    object_key = f"{tos_glb_prefix}/{uid}.{file_type}"
    full_glb_path = f"tos://{bucket_name}/{object_key}"
    if not check_tos_file_exists(full_glb_path, config):
        raise ValueError(f"Mesh does not exist in TOS storage: {full_glb_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    bytes_io = io.BytesIO(data)
    # mesh = trimesh.load(bytes_io, file_type='glb', force='scene')
    return bytes_io

def save_tensor(tensor_buffer, tos_save_path, config):
    # buffer = io.BytesIO()
    # torch.save(feature, buffer)
    tensor_buffer.seek(0)
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=tensor_buffer)
        # print(f"Tensor embedding for UID {uid} successfully uploaded to {self.bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading tensor embedding: {e}")


def save_dict_to_tos_json(data_dict, tos_save_path):
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    # Convert dictionary to JSON string
    json_data = json.dumps(data_dict)
    
    # Create a BytesIO buffer to hold the JSON content
    buffer = io.BytesIO()
    buffer.write(json_data.encode())  # Write the JSON string as bytes to the buffer
    
    # Seek to the beginning of the buffer before uploading
    buffer.seek(0)
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=buffer)
    except Exception as e:
        print(f"Error uploading json: {e}")

def save_string(str_data, tos_save_path, config):
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"

    # Use StringIO to hold the string data
    stream = io.StringIO()
    
    # Write the string data to the in-memory stream
    stream.write(str_data)
    
    # Get the string content of the stream (although it's already in memory)
    string_data = stream.getvalue()

    # Upload the string data as content to the cloud storage
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=string_data)
    except Exception as e:
        print(f"Error uploading str: {e}")
    stream.close()

def _set_tosutil_config(config):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")

    if not os.path.exists("~/.tosutilconfig"):
        print("tosutil has not been set!")
        config_set_command_str = f"{config['tosutil_path']} config \
                                    -i {config['ak']} \
                                    -k {config['sk']} \
                                    -e {config['endpoint']} \
                                    -re {config['region']}"
        config_result = subprocess.run(config_set_command_str, shell=True, capture_output=True, text=True)
        print(config_result)
        print("-----------------------------------------------")

def download_dir(tos_dir, local_dir, config, jobs=96, chunk_jobs=96):
    transfer_command_str = f'{config['tosutil_path']} cp \
                        -r -flat -u -p {jobs} -j {chunk_jobs} \
                        "{tos_dir}" "{local_dir}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error downloading {tos_dir} to {local_dir}: {result.stderr}")
    return result.returncode


def download_file(tos_path, local_path, config, jobs=96, chunk_jobs=96):
    transfer_command_str = f'{config['tosutil_path']} cp \
                            -u -p {jobs} -j {chunk_jobs} \
                            "{tos_path}" "{local_path}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)   
    if os.path.exists(local_path):
        return 0
    else:
        print(f"Error downloading {tos_path} to {local_path}: {result.stderr}")
        return -1

def download_file_from_tos2local(tos_parent_dir, uids, file_type, local_dir, config, jobs=96, chunk_jobs=96):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    _set_tosutil_config(config)
    tos_parent_dir = tos_parent_dir.strip("/")
    results = []
    with tqdm(total=len(uids)) as pbar:
        with ThreadPoolExecutor() as executor:
            future_to_path = {}
            for uid in uids:
                tos_path = f"{tos_parent_dir}/{uid}.{file_type}"
                save_path = f"{local_dir}/{uid}.{file_type}"
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                future_to_path[executor.submit(download_file, tos_path, save_path, config, jobs=jobs, chunk_jobs=chunk_jobs)] = uid
            # future_to_path = {executor.submit(download_file_from_tos2local, bucket_name, tos_path): tos_path for tos_path in paths}
            for future in as_completed(future_to_path):
                uid = future_to_path[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'{uid} generated an exception: {exc}')
                else:
                    results.append((uid, result))
                pbar.update(1)

    fail_list = []
    for result in results:
        if result[1] != 0:
            fail_list.append(result[0])
    print(f"{len(fail_list)} download are unsuccessful!")
    if fail_list:
        write_list_to_txt(fail_list, "fail_download.txt")
    return results


def download_dirs_from_tos2local(tos_parent_dir, uids, local_dir, config, jobs=96, chunk_jobs=96):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    _set_tosutil_config(config)
    tos_parent_dir = tos_parent_dir.strip("/")
    results = []
    with tqdm(total=len(uids)) as pbar:
        with ThreadPoolExecutor() as executor:
            future_to_path = {}
            for uid in uids:
                save_dir = f"{os.path.join(local_dir, uid)}/"
                tos_target_dir = f"{tos_parent_dir}/{uid}/"
                os.makedirs(local_dir, exist_ok=True)
                future_to_path[executor.submit(download_dir, tos_target_dir, save_dir, config, jobs=jobs, chunk_jobs=chunk_jobs)] = uid           
            # future_to_path = {executor.submit(download_file_from_tos2local, bucket_name, tos_path): tos_path for tos_path in paths}
            for future in as_completed(future_to_path):
                uid = future_to_path[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'{uid} generated an exception: {exc}')
                else:
                    results.append((uid, result))
                pbar.update(1)
                
    fail_list = []
    for result in results:
        if result[1] != 0:
            fail_list.append(result[0])
    print(f"{len(fail_list)} download are unsuccessful!")
    if fail_list:
        write_list_to_txt(fail_list, "fail_download.txt")
    return results
    
    

def save_dict_to_json(data: Dict, file_path: str):
    import json
    with open(file_path, 'w') as json_file:
        # Write the dictionary to the file as JSON
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Dict has been successfully saved to {file_path}")

def write_list_to_txt(uid_list: List, file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(uid_list))
    print(f"List has been successfully saved to {file_path}")
    