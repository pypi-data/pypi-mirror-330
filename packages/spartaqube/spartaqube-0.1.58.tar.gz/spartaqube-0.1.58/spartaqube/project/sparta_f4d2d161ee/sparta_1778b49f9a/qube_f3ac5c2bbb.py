import os
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_eb690246e5 import qube_eb690246e5
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_b5bdbf9d8b import qube_b5bdbf9d8b
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_8bfd8c6f08 import qube_8bfd8c6f08
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_4aef200d59 import qube_4aef200d59
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_eb690246e5()
		elif A.dbType==1:A.dbCon=qube_b5bdbf9d8b()
		elif A.dbType==2:A.dbCon=qube_8bfd8c6f08()
		elif A.dbType==4:A.dbCon=qube_4aef200d59()
		return A.dbCon