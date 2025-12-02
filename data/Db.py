from common.logger import logger
import pyodbc as Database
from dataclasses import dataclass, fields
from data.Entity import *
from Config import Debug


class Db:

    def __init__(self):
        self.conn = None
        try:
            serverInfo = self.__DbServerInfo('ODBC Driver 17 for SQL Server', 'amg-crm-dev.database.windows.net,1433',
                                             'amg-crm-dev', 'amgadmin', 'Amg4726723') if (
                Debug) else self.__DbServerInfo('ODBC Driver 18 for SQL Server', 'awm-prod-00.database.windows.net',
                                                'crm', 'app_user', 'pine@pple12')
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
