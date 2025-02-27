import os
from project.sparta_a3a543928a.sparta_e2e7d1248d.qube_d738852946 import qube_d738852946
from project.sparta_a3a543928a.sparta_e2e7d1248d.qube_278306d85a import qube_278306d85a
from project.sparta_a3a543928a.sparta_e2e7d1248d.qube_a4bb464dfd import qube_a4bb464dfd
from project.sparta_a3a543928a.sparta_e2e7d1248d.qube_748d7a8a36 import qube_748d7a8a36
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_d738852946()
		elif A.dbType==1:A.dbCon=qube_278306d85a()
		elif A.dbType==2:A.dbCon=qube_a4bb464dfd()
		elif A.dbType==4:A.dbCon=qube_748d7a8a36()
		return A.dbCon