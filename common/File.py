import os
import sys
from datetime import datetime as dt
import shutil
import pyzipper
from common.logger import logger


class File:

    @staticmethod
    def __isExeFile():
        return getattr(sys, 'frozen', False)

    # get temp folder path, return path, if not exist ,create in root path
    # use createFolder
    @staticmethod
    def getTempFolderPath():
        folderName = 'temp'
        return File.__createFolder(folderName)

    # get FwdDocFiles folder path, return path, if not exist,create in root path
    # use createFolder
    @staticmethod
    def getFwdDocFilesFolderPath():
        folderName = 'FwdDocFiles'
        return File.__createFolder(folderName)

    # get LocalData folder path, return path, if not exist,create in root path
    # use createFolder
    @staticmethod
    def getLocalDataFolderPath():
        folderName = 'LocalData'
        return File.__createFolder(folderName)

    # return full path
    @staticmethod
    def __createFolder(folderName):
        root_path = File.getProjectRootPath()
        folderPath = os.path.join(root_path, folderName)
        os.makedirs(folderPath, exist_ok=True)
        return folderPath

    @staticmethod
    def createFolderUnder(folderName, path=None):
        if path is None:
            raise ValueError("路径不能为空")

        folderPath = os.path.join(path, folderName)
        os.makedirs(folderPath, exist_ok=True)
        return folderPath

    # delete file by the path
    def deleteFile(file_path):
        try:
            # 检查文件是否存在
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' has been deleted.")
            else:
                print(f"File '{file_path}' does not exist.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def getProjectRootPath():
        if getattr(sys, 'frozen', False):  # 判断是否是打包环境
            # return sys._MEIPASS  # PyInstaller打包后的临时资源目录
            return os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # common
            return os.path.dirname(current_dir)  # 根据实际层级调整次数,FwdAmgAdviserEmailTransfer

    @staticmethod
    def getExeProjectRootPath():
        if getattr(sys, 'frozen', False):  # 判断是否是打包环境
            return sys._MEIPASS  # PyInstaller打包后的临时资源目录
            # return os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # common
            return os.path.dirname(current_dir)  # 根据实际层级调整次数,FwdAmgAdviserEmailTransfer


    @staticmethod
    def getCurrentTimeFormatted():
        # return dt.now().strftime("%Y%m%d-%H%M%S.%f")
        return dt.now().strftime("%Y%m%d-%H%M%S")

    @staticmethod
    def removeRedundantFilesIn(log, folderPath):
        if os.path.exists(folderPath) and os.path.isdir(folderPath):
            file_paths = [os.path.join(folderPath, filename)
                          for filename in os.listdir(folderPath)]
            files = [f for f in file_paths if os.path.isfile(
                f) or os.path.islink(f)]
            if len(files) >= 5:
                files.sort(key=lambda x: os.path.getmtime(x))
                files_to_delete = files[:5]
                for file_path in files_to_delete:
                    try:
                        os.unlink(file_path)
                        log.info(f'Deleted {file_path}.')
                    except Exception as e:
                        log.info(f'Failed to delete {file_path}. Reason: {e}')
            else:
                # print('The number of files is 10 or less. No need to delete the oldest ones.')
                pass
        else:
            # print(f'The folder {folder_path} does not exist.')
            pass

    @staticmethod
    def removeAllFilesIn(docFolderPath):
        """
        Remove all files within the specified folder.

        Args:
            docFolderPath (str): The path to the folder from which all files will be removed.
        """
        # Check if the folder contains any files or directories
        if os.listdir(docFolderPath):
            # Iterate through all items in the folder
            for filename in os.listdir(docFolderPath):
                # Construct the full path of the item
                file_path = os.path.join(docFolderPath, filename)
                # Check if the item is a file
                if os.path.isfile(file_path):
                    # Remove the file
                    os.remove(file_path)

    def remove_folder_and_contents(folder_path):
        # 检查文件夹是否存在
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # 删除文件夹及其中的所有内容
                shutil.rmtree(folder_path)
                print(f"Folder '{folder_path}' and all its contents have been deleted.")
            except Exception as e:
                print(f"Error occurred while deleting folder: {e}")
        else:
            print(f"Folder '{folder_path}' does not exist.")

    @staticmethod
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
                    logger.info("file_name = " + file_name)
                    file_path = os.path.join(root, file_name)
                    files.append((file_path, os.path.relpath(file_path, folder_path)))

            if not files:
                logger.error(f"警告: 文件夹 '{folder_path}' 为空，没有文件被压缩。")
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
            logger.error(f"错误: 文件夹路径 '{folder_path}' 不存在。")
        except PermissionError:
            logger.error(f"错误: 无法访问文件夹路径 '{folder_path}'。")
        except Exception as e:
            logger.error(f"发生未知错误: {e}")
