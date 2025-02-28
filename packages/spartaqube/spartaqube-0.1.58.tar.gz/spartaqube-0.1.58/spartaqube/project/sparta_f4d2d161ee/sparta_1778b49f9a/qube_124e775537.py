import os
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_b5bdbf9d8b import qube_b5bdbf9d8b
from project.sparta_f4d2d161ee.sparta_1778b49f9a.qube_eb690246e5 import qube_eb690246e5
from project.logger_config import logger
class db_custom_connection:
	def __init__(A):A.dbCon=None;A.dbIdManager='';A.spartAppId=''
	def setSettingsSqlite(B,dbId,dbLocalPath,dbFileNameWithExtension):G='spartApp';E=dbLocalPath;C=dbId;from bqm import settings as F,settingsLocalDesktop as H;B.dbType=0;B.spartAppId=C;A={};A['id']=C;A['ENGINE']='django.db.backends.sqlite3';A['NAME']=str(E)+'/'+str(dbFileNameWithExtension);A['USER']='';A['PASSWORD']='2change';A['HOST']='';A['PORT']='';F.DATABASES[C]=A;H.DATABASES[C]=A;D=qube_eb690246e5();D.setPath(E);D.setDbName(G);B.dbCon=D;B.dbIdManager=G;logger.debug(F.DATABASES)
	def getConnection(A):return A.dbCon
	def setAuthDB(A,authDB):A.dbType=authDB.dbType