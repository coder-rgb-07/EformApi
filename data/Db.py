from common.logger import logger
import pyodbc as Database
from dataclasses import dataclass, fields
from data.Entity import *
from Config import Debug
import os


class Db:

    def __init__(self):
        self.conn = None
        try:
            if Debug:
                # Development database configuration
                driver = os.getenv('DB_DEV_DRIVER', 'ODBC Driver 17 for SQL Server')
                server = os.getenv('DB_DEV_SERVER', '')
                database = os.getenv('DB_DEV_DATABASE', '')
                username = os.getenv('DB_DEV_USERNAME', '')
                password = os.getenv('DB_DEV_PASSWORD', '')
                
                if not all([server, database, username, password]):
                    raise ValueError(
                        "Development database environment variables are required: "
                        "DB_DEV_SERVER, DB_DEV_DATABASE, DB_DEV_USERNAME, DB_DEV_PASSWORD. "
                        "Please set them in your .env file or environment variables."
                    )
            else:
                # Production database configuration
                driver = os.getenv('DB_PROD_DRIVER', 'ODBC Driver 18 for SQL Server')
                server = os.getenv('DB_PROD_SERVER', '')
                database = os.getenv('DB_PROD_DATABASE', '')
                username = os.getenv('DB_PROD_USERNAME', '')
                password = os.getenv('DB_PROD_PASSWORD', '')
                
                if not all([server, database, username, password]):
                    raise ValueError(
                        "Production database environment variables are required: "
                        "DB_PROD_SERVER, DB_PROD_DATABASE, DB_PROD_USERNAME, DB_PROD_PASSWORD. "
                        "Please set them in your .env file or environment variables."
                    )
            
            serverInfo = self.__DbServerInfo(driver, server, database, username, password)
            DSN = (
                f'DRIVER={{{serverInfo.dirver}}};'
                f'SERVER={serverInfo.server};DATABASE={serverInfo.database};'
                f'UID={serverInfo.username};PWD={serverInfo.password};'
            )
            self.conn = Database.connect(DSN)
            logger.debug("Db connection successful.")
        except Database.Error as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise e

    # SELECT TOP 1 p.StaffId, LoginName, e.EmailAddress
    def getStaffEmail(self, agentId):
        """获取员工邮箱地址"""
        sql = f"""
        SELECT TOP 1 p.StaffId, LoginName, e.EmailAddress
        FROM (StaffProviderProposalPortal p INNER JOIN StaffEmail e ON e.StaffId = p.StaffId)
        WHERE e.typecode = 'W' AND p.LoginName = '{agentId}'
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                staff = StaffInfoDb(
                    StaffId=row[0],
                    LoginName=row[1],
                    EmailAddress=row[2]
                )
                cursor.close()
                logger.info(
                    f'员工信息: StaffId={staff.StaffId}, LoginName={staff.LoginName}, EmailAddress={staff.EmailAddress}')
                return staff
            cursor.close()
            return None
        except Exception as e:
            logger.error(f'获取员工邮箱失败: {str(e)}')
            return None

    @dataclass
    class __DbServerInfo:
        dirver: str
        server: str
        database: str
        username: str
        password: str
