import os
import sys
import pyzipper
from common.File import File


import os
import pyzipper

import os
import pyzipper

def zip_folder_with_password(folder_path, zip_path, password):
    """
    使用 AES-256 加密压缩文件夹
    :param folder_path: 源文件夹路径
    :param zip_path: 输出 ZIP 文件路径
    :param password: ZIP 文件密码
    """
    try:
        # 获取文件夹中所有文件的路径
        files = []
        for root, dirs, file_names in os.walk(folder_path):
            for file_name in file_names:
                # print("file_name = "+file_name)
                file_path = os.path.join(root, file_name)
                files.append((file_path, os.path.relpath(file_path, folder_path)))

        if not files:
            print(f"警告: 文件夹 '{folder_path}' 为空，没有文件被压缩。")
            return

        # 创建带有 AES-256 加密的 ZIP 文件
        with pyzipper.AESZipFile(
            zip_path,
            'w',
            compression=pyzipper.ZIP_DEFLATED,
            encryption=pyzipper.WZ_AES  # 使用 AES 加密
        ) as zip_file:
            zip_file.setpassword(password.encode('utf-8'))  # 设置密码
            zip_file.aes_key_size = 256  # 指定 AES 密钥长度为 256 位
            for file_path, arcname in files:
                zip_file.write(file_path, arcname=arcname)

    except FileNotFoundError:
        print(f"错误: 文件夹路径 '{folder_path}' 不存在。")
    except PermissionError:
        print(f"错误: 无法访问文件夹路径 '{folder_path}'。")
    except Exception as e:
        print(f"发生未知错误: {e}")


password = "your_password"  # 设置密码


base_folder = File.getProjectRootPath()
output_folder = "test"
zip_file_name = "your_output.zip"

# foler test path
folder_to_zip = os.path.join(base_folder, output_folder)

# 使用 os.path.join 或 pathlib.Path 构建路径，确保跨平台兼容性
zip_file_path = os.path.join(base_folder, output_folder, zip_file_name)




print(f"Folder {folder_to_zip} compressed to {zip_file_path} with password {password}")
zip_folder_with_password(folder_to_zip, zip_file_path, password)
