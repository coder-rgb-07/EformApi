import logging
import os
from pathlib import Path
import http.client
import logging
import os
import sys
from pathlib import Path
import http.client
from datetime import datetime as dt


def getProjectRootPath():
    if getattr(sys, 'frozen', False):  # 判断是否是打包环境
        return os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # common
        return os.path.dirname(current_dir)  # 根据实际层级调整次数,FwdAmgAdviserEmailTransfer


def setup_logger():
    # http.client.HTTPConnection.debuglevel = 1

    # 动态计算日志目录
    base_dir = getProjectRootPath()
    log_dir = os.path.join(base_dir, 'logs')
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    t = dt.now().strftime("%Y%m%d-%H%M%S")
    log_file_path = os.path.join(log_dir, f'log_{t}.txt')

    # Insert an empty line at the beginning of the log file
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write('\n')

    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


logger = setup_logger()
