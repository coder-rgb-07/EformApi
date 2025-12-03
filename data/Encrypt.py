from enum import Enum
import os
import subprocess
import shutil
from pathlib import Path
from common.logger import logger
from common.File import File
import json


class Encrypt:
    class FileMode(Enum):
        IN = 'In'
        OUT = 'Out'

    def __init__(self):
        pass

    def _find_java_executable(self):
        """
        Find Java executable path.
        Checks JAVA_HOME, common installation paths, and PATH.
        
        Returns:
            str: Path to java.exe or 'java' if found in PATH
            
        Raises:
            FileNotFoundError: If Java cannot be found
        """
        import shutil
        
        # 1. Check JAVA_HOME environment variable
        java_home = os.getenv('JAVA_HOME')
        if java_home:
            java_path = os.path.join(java_home, 'bin', 'java.exe')
            if os.path.exists(java_path):
                logger.info(f"Found Java at JAVA_HOME: {java_path}")
                return java_path
        
        # 2. Check common Java installation paths on Windows
        common_paths = [
            r'C:\Program Files\Java\jdk-25\bin\java.exe',
            r'C:\Program Files\Java\jdk-21\bin\java.exe',
            r'C:\Program Files\Java\jdk-17\bin\java.exe',
            r'C:\Program Files\Java\jdk-11\bin\java.exe',
            r'C:\Program Files\Java\jdk-8\bin\java.exe',
            r'C:\Program Files (x86)\Java\jdk-25\bin\java.exe',
            r'C:\Program Files (x86)\Java\jdk-21\bin\java.exe',
            r'C:\Program Files (x86)\Java\jdk-17\bin\java.exe',
        ]
        
        for java_path in common_paths:
            if os.path.exists(java_path):
                logger.info(f"Found Java at common path: {java_path}")
                return java_path
        
        # 3. Check if 'java' is in PATH
        java_in_path = shutil.which('java')
        if java_in_path:
            logger.info(f"Found Java in PATH: {java_in_path}")
            return java_in_path
        
        # 4. If nothing found, raise error
        error_msg = (
            "Java not found. Please either:\n"
            "1. Set JAVA_HOME environment variable\n"
            "2. Add Java to your system PATH\n"
            "3. Install Java from https://www.oracle.com/java/technologies/downloads/"
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    def encryptParam(self, data):
        """
        加密参数。
    
        使用临时文件和Java程序加密给定的数据。
    
        参数:
        data (dict): 需要加密的数据。
    
        返回:
        str: 加密后的数据。
    
        异常:
        Exception: 如果加密失败，抛出异常。
        """
    
        # 获取用于输入和输出的临时文件名
        fileNameIn = self.getTempFile(Encrypt.FileMode.IN)
        fileNameOut = self.getTempFile(Encrypt.FileMode.OUT)
    
        # 把data写入in文件
        with open(fileNameIn, 'w') as f:
            json.dump(data, f)
    
        # 查找Java可执行文件
        java_exe = self._find_java_executable()
        
        # 构建Java命令
        command = [
            java_exe,
            '-cp', f'{File.getExeProjectRootPath()}/lib/springBootDemo123.jar',
            '-Dloader.main=com.fwd.mis.fna.util.amgencstr',
            'org.springframework.boot.loader.PropertiesLauncher',
            fileNameIn,
            fileNameOut
        ]
        # powershell: java -cp $env:PROJECT_ROOT/lib/springBootDemo123.jar -Dloader.main=com.fwd.mis.fna.util.amgencstr org.springframework.boot.loader.PropertiesLauncher $fileNameIn $fileNameOut
        # java -cp springBootDemo123.jar -D"loader.main=com.fwd.mis.fna.util.amgencstr" org.springframework.boot.loader.PropertiesLauncher .\in.txt .\out.txt
        logger.info(f"Current Working Directory: {os.getcwd()}")
        logger.info(f"Full Command: {' '.join(command)}")
    
        # 执行Java命令，捕获输出和错误
        try:
            result = subprocess.run(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                timeout=30  # 30秒超时
            )
            
            # 记录Java程序的输出
            if result.stdout:
                logger.info(f"Java stdout: {result.stdout}")
            if result.stderr:
                logger.warning(f"Java stderr: {result.stderr}")
            
            if result.returncode != 0:
                error_msg = f"encryptParam Java程序执行失败！退出码: {result.returncode}"
                if result.stderr:
                    error_msg += f"\n错误信息: {result.stderr}"
                if result.stdout:
                    error_msg += f"\n输出信息: {result.stdout}"
                logger.error(error_msg)
                raise Exception(error_msg)
            else:
                logger.info("encryptParam Java 程序执行成功！")
        except subprocess.TimeoutExpired as e:
            error_msg = f"encryptParam Java程序执行超时（30秒）"
            logger.error(error_msg)
            raise Exception(error_msg)
        except FileNotFoundError as e:
            error_msg = f"encryptParam 找不到Java程序。请确保Java已安装并在PATH中。错误: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"encryptParam 执行Java程序时发生异常: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 检查输出文件是否存在
        if not os.path.exists(fileNameOut):
            error_msg = f"加密输出文件不存在: {fileNameOut}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 读取out文件
        encryptPayload = None
        try:
            with open(fileNameOut, 'r', encoding='utf-8') as f:
                encryptPayload = f.read().strip()
        except Exception as e:
            error_msg = f"读取加密输出文件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 检查是否为空
        if not encryptPayload or len(encryptPayload) == 0:
            error_msg = f"加密失败！输出文件为空: {fileNameOut}"
            logger.error(error_msg)
            logger.error(f"输入文件内容: {open(fileNameIn, 'r', encoding='utf-8').read()}")
            raise Exception(error_msg)
        
        logger.info(f"加密成功，输出长度: {len(encryptPayload)} 字符")
        return encryptPayload

    def decryptParam(self, data):
        """
        解密给定的参数数据。
        
        该方法首先将输入的数据保存到一个临时文件中，然后调用解密方法将加密数据解密到另一个临时文件，
        最后读取解密后的数据并将其解析为JSON格式返回。
        
        参数:
        - data: 待解密的加密数据，以字符串形式提供。
        
        返回:
        - 解密后的数据，以JSON格式返回。
        """
    
        # 获取用于输入和输出的临时文件名
        fileNameIn = self.getTempFile(Encrypt.FileMode.IN)
        fileNameOut = self.getTempFile(Encrypt.FileMode.OUT)
    
        # 将加密数据写入临时输入文件
        with open(fileNameIn, 'w') as f:
            f.write(data)
        # logger.info(f"保存加密数据到文件 {fileNameIn}")
    
        # 调用解密方法，将加密数据解密到输出文件
        self.__decryptParam(fileNameIn, fileNameOut)
        # 从输出文件中读取解密后的数据
        with open(fileNameOut, 'r') as f:
            decryptPayload = f.read()
        # logger.info(f"解密数据 {decryptPayload}")
    
        # 将解密后的数据解析为JSON格式并返回
        json_data = json.loads(decryptPayload)
        return json_data

    def __decryptParam(self, fileNameIn, fileNameOut):
        """
        解密参数文件。
    
        本函数负责将给定的加密参数文件解密为明文文件。它通过调用Java程序（JAR文件）来执行解密操作，
        并确保所有路径操作和命令执行都是安全和跨平台的。
    
        参数:
        fileNameIn (str): 输入文件名（加密的参数文件）。
        fileNameOut (str): 输出文件名（解密后的明文文件）。
    
        返回:
        bool: 解密成功返回True，否则抛出异常。
        """
    
        # 1. 规范化路径输入（兼容绝对路径和相对路径）
        project_root = Path(File.getExeProjectRootPath()).resolve()  # 确保为绝对路径
    
        # 2. 安全拼接路径（自动处理路径分隔符）
        input_path = (project_root / fileNameIn).resolve()
        output_path = (project_root / fileNameOut).resolve()
        jar_path = (project_root / "lib" / "TestDecrypt.jar").resolve()
    
        # 3. 验证路径有效性
        if not jar_path.exists():
            raise FileNotFoundError(f"JAR文件不存在: {jar_path}")
        if not input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        if not output_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {output_path}")
        # output_path.parent.mkdir(parents=True, exist_ok=True)  # 自动创建输出目录
    
        # 4. 查找Java可执行文件
        java_exe = self._find_java_executable()
        
        # 5. 构建跨平台命令（处理空格和特殊字符）
        command = [
            java_exe,
            '-jar',
            str(jar_path),  # 强制转换为字符串k
            str(input_path),  # 显式添加引号
            str(output_path)  # 兼容含空格路径
        ]
    
        # 5. 调试输出（关键！）
        # print("[DEBUG] 完整命令:", ' '.join(command))
        # print("[DEBUG] 输入文件是否存在:", input_path.exists())
        # print("[DEBUG] 输出目录权限:", os.access(output_path.parent, os.W_OK))
    
        # 6. 执行命令（捕获错误信息）
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False  # Windows需要shell=True解析引号
        )
    
        # 7. 错误处理
        if result.returncode != 0:
            print("=== 错误详情 ===")
            print(result.stderr)
            logger.error(result.stderr)
            raise RuntimeError(f"JAR执行失败，退出码: {result.returncode}")
        return True

    def getTempFile(self, mode: FileMode):
        """
        根据指定模式获取临时文件的路径。
    
        参数:
        mode (FileMode): 文件模式，决定文件名前缀。
    
        返回:
        str: 临时文件的路径。
    
        异常:
        Exception: 如果模式无效，则抛出异常。
        """
        # 初始化时间变量，用于生成唯一文件名
        time = 1
        # time = File.getCurrentTimeFormatted()  # 获取当前格式化时间，本行代码被注释掉了
    
        # 根据模式决定文件名
        if mode == self.FileMode.IN:
            fileName = f'in_{time}.txt'
        elif mode == self.FileMode.OUT:
            fileName = f'out_{time}.txt'
        else:
            raise Exception('Invalid mode')  # 模式无效时抛出异常
    
        temp_folder = File.getTempFolderPath()  # 获取临时文件夹路径
        p = os.path.join(temp_folder, fileName)  # 构造文件路径
    
        # 如果文件存在，清空文件内容
        if os.path.exists(p):
            with open(p, 'w') as file:
                file.truncate(0)  # 清空文件内容
    
        # 如果文件不存在，创建文件
        if not os.path.exists(p):
            with open(p, 'w') as file:
                file.write('')  # 写入空字符串以创建文件
    
        return p  # 返回文件路径
