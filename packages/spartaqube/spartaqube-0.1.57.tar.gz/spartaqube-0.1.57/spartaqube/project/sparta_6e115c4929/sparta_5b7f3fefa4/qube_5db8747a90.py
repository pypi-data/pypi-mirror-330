import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_e223501ed5():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_6ff79361b9(userId):A=sparta_e223501ed5();B=os.path.join(A,userId);return B
def sparta_03bd8fc590(notebookProjectId,userId):A=sparta_6ff79361b9(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_aa60349a6e(notebookProjectId,userId):A=sparta_6ff79361b9(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_90a1989cd7(notebookProjectId,userId,ipynbFileName):A=sparta_6ff79361b9(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_2b405fcb9a(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_03bd8fc590(B,C);G=sparta_6ff79361b9(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_8dc306f2a4(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_2b405fcb9a(A,B);C=f"{A}.zip";D=sparta_6ff79361b9(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}