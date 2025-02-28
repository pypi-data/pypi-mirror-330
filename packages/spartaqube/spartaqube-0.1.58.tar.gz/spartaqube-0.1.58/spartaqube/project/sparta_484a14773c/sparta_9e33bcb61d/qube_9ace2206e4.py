_m='makemigrations'
_l='app.settings'
_k='DJANGO_SETTINGS_MODULE'
_j='python'
_i='thumbnail'
_h='previewImage'
_g='isPublic'
_f='isExpose'
_e='password'
_d='lumino_layout'
_c='developer_venv'
_b='lumino'
_a='Project not found...'
_Z='You do not have the rights to access this project'
_Y='backend'
_X='stdout'
_W='npm'
_V='luminoLayout'
_U='hasPassword'
_T='is_public_developer'
_S='has_password'
_R='is_expose_developer'
_Q='static'
_P='frontend'
_O='manage.py'
_N='developerId'
_M='description'
_L='slug'
_K='project_path'
_J='developer_id'
_I='developer'
_H='developer_obj'
_G='name'
_F='projectPath'
_E=None
_D='errorMsg'
_C=False
_B='res'
_A=True
import re,os,json,stat,importlib,io,sys,subprocess,platform,base64,traceback,uuid,shutil
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_b786689d5b
from project.models_spartaqube import Developer,DeveloperShared
from project.models import ShareRights
from project.sparta_484a14773c.sparta_88433fd91c import qube_353c7b61a4 as qube_353c7b61a4
from project.sparta_484a14773c.sparta_174d7f1491 import qube_de9f73339e as qube_de9f73339e
from project.sparta_484a14773c.sparta_b7c52b6e7f.qube_c3c81d82c4 import Connector as Connector
from project.sparta_484a14773c.sparta_8bb3408009 import qube_f97f36df45 as qube_f97f36df45
from project.sparta_484a14773c.sparta_5aa07280e6.qube_2b5480aafc import sparta_45043f35a3
from project.sparta_484a14773c.sparta_0b1182bbde import qube_be549b6d29 as qube_be549b6d29
from project.sparta_484a14773c.sparta_0b1182bbde import qube_fbed11d623 as qube_fbed11d623
from project.sparta_484a14773c.sparta_cf2c26801e.qube_3818061d71 import sparta_f3e34e8081
from project.sparta_484a14773c.sparta_5aa07280e6.qube_1b962f541a import sparta_f0e24d00e7,sparta_fa8168e869
from project.logger_config import logger
def sparta_ef7df956ed():
	A=['esbuild-darwin-arm64','esbuild-darwin-x64','esbuild-linux-x64','esbuild-windows-x64.exe'];C=os.path.dirname(__file__);A=[os.path.join(C,'esbuild',A)for A in A]
	def D(file_path):
		A=file_path
		if os.name=='nt':
			try:subprocess.run(['icacls',A,'/grant','*S-1-1-0:(RX)'],check=_A);logger.debug(f"Executable permissions set for: {A} (Windows)")
			except subprocess.CalledProcessError as B:logger.debug(f"Failed to set permissions for {A} on Windows: {B}")
		else:
			try:os.chmod(A,stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH);logger.debug(f"Executable permissions set for: {A} (Unix/Linux/Mac)")
			except Exception as B:logger.debug(f"Failed to set permissions for {A} on Unix/Linux: {B}")
	for B in A:
		if os.path.exists(B):D(B)
		else:logger.debug(f"File not found: {B}")
	return{_B:1}
def sparta_3758e8bd51(user_obj):
	A=qube_353c7b61a4.sparta_0fac479d2e(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_3a814bb14f(project_path):
	G='template';A=project_path
	if not os.path.exists(A):os.makedirs(A)
	D=A;H=os.path.dirname(__file__);E=os.path.join(sparta_b786689d5b()['django_app_template'],_I,G)
	for F in os.listdir(E):
		C=os.path.join(E,F);B=os.path.join(D,F)
		if os.path.isdir(C):shutil.copytree(C,B,dirs_exist_ok=_A)
		else:shutil.copy2(C,B)
	I=os.path.dirname(os.path.dirname(H));J=os.path.dirname(I);K=os.path.join(J,_Q);L=os.path.join(K,'js',_I,G,_P);B=os.path.join(D,_P);shutil.copytree(L,B,dirs_exist_ok=_A);return{_K:A}
def sparta_d8eba59d63(json_data,user_obj):
	B=user_obj;A=json_data[_F];A=sparta_45043f35a3(A);F=Developer.objects.filter(project_path=A).all()
	if F.count()>0:
		C=F[0];G=sparta_3758e8bd51(B)
		if len(G)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=C)|Q(is_delete=0,user=B,developer__is_delete=0,developer=C))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=C)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if not H:return{_B:-1,_D:'Chose another path. A project already exists at this location'}
	if not isinstance(A,str):return{_B:-1,_D:'Project path must be a string.'}
	try:A=os.path.abspath(A)
	except Exception as E:return{_B:-1,_D:f"Invalid project path: {str(E)}"}
	try:
		if not os.path.exists(A):os.makedirs(A)
		K=sparta_3a814bb14f(A);A=K[_K];return{_B:1,_K:A}
	except Exception as E:return{_B:-1,_D:f"Failed to create folder: {str(E)}"}
def sparta_e36380baf4(json_data,user_obj):A=json_data;A['bAddGitignore']=_A;A['bAddReadme']=_A;return qube_fbed11d623.sparta_f63c92e4f2(A,user_obj)
def sparta_ffd07e43b2(json_data,user_obj):return sparta_474079b762(json_data,user_obj)
def sparta_dd36258d52(json_data,user_obj):
	K='%Y-%m-%d';J='Recently used';D=user_obj;F=sparta_3758e8bd51(D)
	if len(F)>0:A=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0)|Q(is_delete=0,user=D,developer__is_delete=0)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
	else:A=DeveloperShared.objects.filter(Q(is_delete=0,user=D,developer__is_delete=0)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
	if A.count()>0:
		C=json_data.get('orderBy',J)
		if C==J:A=A.order_by('-developer__last_date_used')
		elif C=='Date desc':A=A.order_by('-developer__last_update')
		elif C=='Date asc':A=A.order_by('developer__last_update')
		elif C=='Name desc':A=A.order_by('-developer__name')
		elif C=='Name asc':A=A.order_by('developer__name')
	G=[]
	for E in A:
		B=E.developer;L=E.share_rights;H=_E
		try:H=str(B.last_update.strftime(K))
		except:pass
		I=_E
		try:I=str(B.date_created.strftime(K))
		except Exception as M:logger.debug(M)
		G.append({_J:B.developer_id,_G:B.name,_L:B.slug,_M:B.description,_R:B.is_expose_developer,_S:B.has_password,_T:B.is_public_developer,'is_owner':E.is_owner,'has_write_rights':L.has_write_rights,'last_update':H,'date_created':I})
	return{_B:1,'developer_library':G}
def sparta_7aaa8e6fed(json_data,user_obj):
	B=user_obj;E=json_data[_N];D=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
	if D.count()==1:
		A=D[D.count()-1];E=A.developer_id;F=sparta_3758e8bd51(B)
		if len(F)>0:C=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:C=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		if C.count()==0:return{_B:-1,_D:_Z}
	else:return{_B:-1,_D:_a}
	C=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
	if C.count()>0:G=datetime.now().astimezone(UTC);A.last_date_used=G;A.save()
	return{_B:1,_I:{'basic':{_J:A.developer_id,_G:A.name,_L:A.slug,_M:A.description,_R:A.is_expose_developer,_T:A.is_public_developer,_S:A.has_password,_c:A.developer_venv,_K:A.project_path},_b:{_d:A.lumino_layout}}}
def sparta_8c9392587f(json_data,user_obj):
	G=json_data;B=user_obj;E=G[_N]
	if not B.is_anonymous:
		F=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
		if F.count()==1:
			A=F[F.count()-1];E=A.developer_id;H=sparta_3758e8bd51(B)
			if len(H)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			else:D=DeveloperShared.objects.filter(Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			if D.count()==0:return{_B:-1,_D:_Z}
		else:return{_B:-1,_D:_a}
	else:
		I=G.get('modalPassword',_E);logger.debug(f"DEBUG DEVELOPER VIEW TEST >>> {I}");C=has_developer_access(E,B,password_developer=I);logger.debug('MODAL DEBUG DEBUG DEBUG developer_access_dict');logger.debug(C)
		if C[_B]!=1:return{_B:C[_B],_D:C[_D]}
		A=C[_H]
	if not B.is_anonymous:
		D=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
		if D.count()>0:J=datetime.now().astimezone(UTC);A.last_date_used=J;A.save()
	return{_B:1,_I:{'basic':{_J:A.developer_id,_G:A.name,_L:A.slug,_M:A.description,_R:A.is_expose_developer,_T:A.is_public_developer,_S:A.has_password,_c:A.developer_venv,_K:A.project_path},_b:{_d:A.lumino_layout}}}
def sparta_1b00b9ff12(json_data,user_obj):
	I=user_obj;A=json_data;N=A['isNew']
	if not N:return sparta_e5ddbd722f(A,I)
	C=datetime.now().astimezone(UTC);J=str(uuid.uuid4());G=A[_U];E=_E
	if G:E=A[_e];E=qube_de9f73339e.sparta_e5b6a49be4(E)
	O=A[_V];P=A[_G];Q=A[_M];D=A[_F];D=sparta_45043f35a3(D);R=A[_f];S=A[_g];G=A[_U];T=A.get('developerVenv',_E);B=A[_L]
	if len(B)==0:B=A[_G]
	K=slugify(B);B=K;L=1
	while Developer.objects.filter(slug=B).exists():B=f"{K}-{L}";L+=1
	H=_E;F=A.get(_h,_E)
	if F is not _E:
		try:
			F=F.split(',')[1];U=base64.b64decode(F);V=os.path.dirname(__file__);D=os.path.dirname(os.path.dirname(os.path.dirname(V)));M=os.path.join(D,_Q,_i,_I);os.makedirs(M,exist_ok=_A);H=str(uuid.uuid4());W=os.path.join(M,f"{H}.png")
			with open(W,'wb')as X:X.write(U)
		except:pass
	Y=Developer.objects.create(developer_id=J,name=P,slug=B,description=Q,is_expose_developer=R,is_public_developer=S,has_password=G,password_e=E,lumino_layout=O,project_path=D,developer_venv=T,thumbnail_path=H,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_f3e34e8081());Z=ShareRights.objects.create(is_admin=_A,has_write_rights=_A,has_reshare_rights=_A,last_update=C);DeveloperShared.objects.create(developer=Y,user=I,share_rights=Z,is_owner=_A,date_created=C);return{_B:1,_J:J}
def sparta_e5ddbd722f(json_data,user_obj):
	G=user_obj;B=json_data;L=datetime.now().astimezone(UTC);H=B[_N];I=Developer.objects.filter(developer_id__startswith=H,is_delete=_C).all()
	if I.count()==1:
		A=I[I.count()-1];H=A.developer_id;M=sparta_3758e8bd51(G)
		if len(M)>0:J=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=M,developer__is_delete=0,developer=A)|Q(is_delete=0,user=G,developer__is_delete=0,developer=A))
		else:J=DeveloperShared.objects.filter(is_delete=0,user=G,developer__is_delete=0,developer=A)
		N=_C
		if J.count()>0:
			T=J[0];O=T.share_rights
			if O.is_admin or O.has_write_rights:N=_A
		if N:
			K=B[_V];U=B[_G];V=B[_M];W=B[_f];X=B[_g];Y=B[_U];C=B[_L]
			if A.slug!=C:
				if len(C)==0:C=B[_G]
				P=slugify(C);C=P;R=1
				while Developer.objects.filter(slug=C).exists():C=f"{P}-{R}";R+=1
			D=_E;E=B.get(_h,_E)
			if E is not _E:
				E=E.split(',')[1];Z=base64.b64decode(E)
				try:
					a=os.path.dirname(__file__);b=os.path.dirname(os.path.dirname(os.path.dirname(a)));S=os.path.join(b,_Q,_i,_I);os.makedirs(S,exist_ok=_A)
					if A.thumbnail_path is _E:D=str(uuid.uuid4())
					else:D=A.thumbnail_path
					c=os.path.join(S,f"{D}.png")
					with open(c,'wb')as d:d.write(Z)
				except:pass
			logger.debug('lumino_layout_dump');logger.debug(K);logger.debug(type(K));A.name=U;A.description=V;A.slug=C;A.is_expose_developer=W;A.is_public_developer=X;A.thumbnail_path=D;A.lumino_layout=K;A.last_update=L;A.last_date_used=L
			if Y:
				F=B[_e]
				if len(F)>0:F=qube_de9f73339e.sparta_e5b6a49be4(F);A.password_e=F;A.has_password=_A
			else:A.has_password=_C
			A.save()
	return{_B:1,_J:H}
def sparta_fde411ba16(json_data,user_obj):
	E=json_data;B=user_obj;F=E[_N];C=Developer.objects.filter(developer_id__startswith=F,is_delete=_C).all()
	if C.count()==1:
		A=C[C.count()-1];F=A.developer_id;G=sparta_3758e8bd51(B)
		if len(G)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if H:K=E[_V];A.lumino_layout=K;A.save()
	return{_B:1}
def sparta_a803d74bec(json_data,user_obj):
	A=user_obj;G=json_data[_N];B=Developer.objects.filter(developer_id=G,is_delete=_C).all()
	if B.count()>0:
		C=B[B.count()-1];E=sparta_3758e8bd51(A)
		if len(E)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=E,developer__is_delete=0,developer=C)|Q(is_delete=0,user=A,developer__is_delete=0,developer=C))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=A,developer__is_delete=0,developer=C)
		if D.count()>0:F=D[0];F.is_delete=_A;F.save()
	return{_B:1}
def has_developer_access(developer_id,user_obj,password_developer=_E):
	J='debug';I='Invalid password';F=password_developer;E=developer_id;C=user_obj;logger.debug(_J);logger.debug(E);B=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all();D=_C
	if B.count()==1:D=_A
	else:
		K=E;B=Developer.objects.filter(slug__startswith=K,is_delete=_C).all()
		if B.count()==1:D=_A
	logger.debug('b_found');logger.debug(D)
	if D:
		A=B[B.count()-1];L=A.has_password
		if A.is_expose_developer:
			logger.debug('is exposed')
			if A.is_public_developer:
				logger.debug('is public')
				if not L:logger.debug('no password');return{_B:1,_H:A}
				else:
					logger.debug('hass password')
					if F is _E:logger.debug('empty passord provided');return{_B:2,_D:'Require password',_H:A}
					else:
						try:
							if qube_de9f73339e.sparta_2dd5e7e055(A.password_e)==F:return{_B:1,_H:A}
							else:return{_B:3,_D:I,_H:A}
						except Exception as M:return{_B:3,_D:I,_H:A}
			elif C.is_authenticated:
				G=sparta_3758e8bd51(C)
				if len(G)>0:H=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
				else:H=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
				if H.count()>0:return{_B:1,_H:A}
			else:return{_B:-1,J:1}
	return{_B:-1,J:2}
def sparta_ca550c9f9e(json_data,user_obj):A=sparta_45043f35a3(json_data[_F]);return sparta_f0e24d00e7(A)
def sparta_af3597400e(json_data,user_obj):A=sparta_45043f35a3(json_data[_F]);return sparta_fa8168e869(A)
def sparta_32343b2cff():
	try:
		if platform.system()=='Windows':subprocess.run(['where',_W],capture_output=_A,check=_A)
		else:subprocess.run(['command','-v',_W],capture_output=_A,check=_A)
		return _A
	except subprocess.CalledProcessError:return _C
	except FileNotFoundError:return _C
def sparta_05f0c67e00():
	try:A=subprocess.run('npm -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run([_W,'-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_d8950d64bf():
	try:A=subprocess.run('node -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run(['node','-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_ac15e77830(json_data,user_obj):
	A=sparta_45043f35a3(json_data[_F]);A=os.path.join(A,_P)
	if not os.path.isdir(A):return{_B:-1,_D:f"The provided path '{A}' is not a valid directory."}
	B=os.path.join(A,'package.json');C=os.path.exists(B);D=sparta_32343b2cff();return{_B:1,'is_init':C,'is_npm_installed':D,'npm_version':sparta_05f0c67e00(),'node_version':sparta_d8950d64bf()}
def sparta_474079b762(json_data,user_obj):
	A=sparta_45043f35a3(json_data[_F]);A=os.path.join(A,_P)
	try:C=subprocess.run('npm init -y',shell=_A,capture_output=_A,text=_A,check=_A,cwd=A);logger.debug(C.stdout);return{_B:1}
	except Exception as B:logger.debug('Error node npm init');logger.debug(B);return{_B:-1,_D:str(B)}
def sparta_453e88aa6b(json_data,user_obj):
	A=json_data;logger.debug('NODE LIS LIBS');logger.debug(A);D=sparta_45043f35a3(A[_F])
	try:B=subprocess.run('npm list',shell=_A,capture_output=_A,text=_A,check=_A,cwd=D);logger.debug(B.stdout);return{_B:1,_X:B.stdout}
	except Exception as C:logger.debug('Exception');logger.debug(C);return{_B:-1,_D:str(C)}
from django.core.management import call_command
from io import StringIO
def sparta_28e307a0c4(project_path,python_executable=_j):
	E=python_executable;B=project_path;A=_C
	try:
		H=os.path.join(B,_O)
		if not os.path.exists(H):A=_A;return _C,f"Error: manage.py not found in {B}",A
		F=os.environ.copy();F[_k]=_l;E=sys.executable;I=[E,_O,_m,'--dry-run'];C=subprocess.run(I,cwd=B,text=_A,capture_output=_A,env=F)
		if C.returncode!=0:A=_A;return _C,f"Error: {C.stderr}",A
		G=C.stdout;J='No changes detected'not in G;return J,G,A
	except FileNotFoundError as D:A=_A;return _C,f"Error: {D}. Ensure the correct Python executable and project path.",A
	except Exception as D:A=_A;return _C,str(D),A
def sparta_28e7762803():
	A=os.environ.get('VIRTUAL_ENV')
	if A:return A
	else:return sys.prefix
def sparta_2cf9430181():
	A=sparta_28e7762803()
	if sys.platform=='win32':B=os.path.join(A,'Scripts','pip.exe')
	else:B=os.path.join(A,'bin','pip')
	return B
def sparta_380686e4e3(json_data,user_obj):
	A=sparta_45043f35a3(json_data[_F]);A=os.path.join(A,_Y,'app');F,B,C=sparta_28e307a0c4(A);D=1;E=''
	if C:D=-1;E=B
	return{_B:D,'has_error':C,'has_pending_migrations':F,_X:B,_D:E}
def sparta_20443edb7c(project_path,python_executable=_j):
	D=python_executable;C=project_path
	try:
		H=os.path.join(C,_O)
		if not os.path.exists(H):return _C,f"Error: manage.py not found in {C}"
		F=os.environ.copy();F[_k]=_l;D=sys.executable;G=[[D,_O,_m],[D,_O,'migrate']];logger.debug('commands');logger.debug(G);B=[]
		for I in G:
			A=subprocess.run(I,cwd=C,text=_A,capture_output=_A,env=F)
			if A.stdout is not _E:
				if len(str(A.stdout))>0:B.append(A.stdout)
			if A.stderr is not _E:
				if len(str(A.stderr))>0:B.append(f"<span style='color:red'>Stderr:\n{A.stderr}</span>")
			if A.returncode!=0:return _C,'\n'.join(B)
		return _A,'\n'.join(B)
	except FileNotFoundError as E:return _C,f"Error: {E}. Ensure the correct Python executable and project path."
	except Exception as E:return _C,str(E)
def sparta_3e99759990(json_data,user_obj):
	A=sparta_45043f35a3(json_data[_F]);A=os.path.join(A,_Y,'app');B,C=sparta_20443edb7c(A);D=1;E=''
	if not B:D=-1;E=C
	return{_B:D,'res_migration':B,_X:C,_D:E}
def sparta_c323d0bfee(json_data,user_obj):return{_B:1}
def sparta_a092675301(json_data,user_obj):return{_B:1}
def sparta_0f0d786085(json_data,user_obj):return{_B:1}
def sparta_4d046715e8(json_data,user_obj):logger.debug('developer_hot_reload_preview json_data');logger.debug(json_data);return{_B:1}
def sparta_9e3bedaf81(json_data,user_obj):
	C='baseProjectPath';A=json_data;D=sparta_45043f35a3(A[C]);E=os.path.join(os.path.dirname(D),_Y);sys.path.insert(0,E);import webservices as B;importlib.reload(B);F=A['service'];G=A.copy();del A[C]
	try:return B.sparta_c763753217(F,G,user_obj)
	except Exception as H:return{_B:-1,_D:str(H)}