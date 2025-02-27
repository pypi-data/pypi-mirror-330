_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_6e115c4929.sparta_f56af70853.qube_45072a23ee as qube_45072a23ee
from project.sparta_6e115c4929.sparta_f56af70853.sparta_44a112063b.qube_1470c4d881 import AerospikeConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_26843c6200.qube_5ba35cd536 import CassandraConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_c05c575b26.qube_2624aacdb4 import ClickhouseConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_fa7136dd01.qube_022edd2d14 import CouchdbConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_be2227b6c7.qube_613768f6ab import CsvConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_640fd8fa4a.qube_4298406579 import DuckDBConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_3c55d0e418.qube_11132b3542 import JsonApiConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_0e765d1844.qube_670587029f import InfluxdbConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_e9bd1abdff.qube_e842ea4ebf import MariadbConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_281579d66a.qube_26b4dcd443 import MongoConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_3c20820e13.qube_22fad20e75 import MssqlConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_e387b9cba4.qube_0b06c79d65 import MysqlConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_c1f10e5ea5.qube_85aa7bb62a import OracleConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_1c1a2035a3.qube_1008464dc4 import ParquetConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_99df609dd9.qube_34480ecf4e import PostgresConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_3e8dfb6a0d.qube_ce12eaf872 import PythonConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_7bc0cb45b1.qube_7a004c087e import QuestDBConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_6635ec85a6.qube_d9cf0c444d import RedisConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_ae15f91c3b.qube_78815221cb import ScylladbConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_2a9024a43b.qube_34b165f21a import SqliteConnector
from project.sparta_6e115c4929.sparta_f56af70853.sparta_c60954a9ce.qube_0b7d7f20dc import WssConnector
from project.logger_config import logger
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_45072a23ee.sparta_12f25002c5(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_60630cfd0f(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)