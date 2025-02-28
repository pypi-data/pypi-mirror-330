import time
from project.sparta_484a14773c.sparta_b7c52b6e7f.qube_5d3c8fd317 import EngineBuilder
from project.logger_config import logger
class MysqlConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mysql');A.connector=A.build_mysql()
	def test_connection(A):
		B=False
		try:
			if A.connector.is_connected():A.connector.close();return True
			else:return B
		except Exception as C:logger.debug(f"Error: {C}");return B