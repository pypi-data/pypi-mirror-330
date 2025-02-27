_L='is_git_repository'
_K='You need to create a notebook first (you can save this notebook with CTRL+ALT+S first)'
_J='url'
_I='name'
_H='scm'
_G='An unexpected error occurred, please try again'
_F=None
_E=False
_D='errorMsg'
_C='projectPath'
_B=True
_A='res'
import os,re,time,json,shutil,git
from asyncio import subprocess
from re import S
from dateutil import parser
from subprocess import Popen,PIPE
from django.contrib.humanize.templatetags.humanize import naturalday
from project.logger_config import logger
def sparta_369d1135a6(path):
	try:A=git.Repo(path).git_dir;return _B
	except git.exc.InvalidGitRepositoryError:return _E
def sparta_a9b925de6f(json_data,user_obj):
	A=json_data['notebookProjectId'];B,C=qube_f10fc8419f.get_notebookProjectObj(A,user_obj)
	if B is not _F:return _B
	return _E
def sparta_8fc546c8f3(remoteBranchToTrack):A=Popen(f"git branch -u {remoteBranchToTrack}",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);B=A.stdout.readline();logger.debug('realtime_output 1');logger.debug(B);A=Popen(f"git config push.default upstream",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);logger.debug('realtime_output 2');logger.debug(B)
def sparta_681333af51(func):
	def A(json_data,user_obj):
		B=user_obj;A=json_data
		if not sparta_a9b925de6f(A,B):return{_A:-1,_D:_K}
		return func(A,B)
	return A
def sparta_cf69b58623(func):
	def A(webSocket,json_data,user_obj):
		B=user_obj;A=json_data
		if not sparta_a9b925de6f(A,B):return{_A:-1,_D:_K}
		return func(webSocket,A,B)
	return A
def sparta_45f7da42e9(repo,user_obj):
	C='user';A=user_obj;D=A.email;E=f"{A.first_name.capitalize()} {A.last_name.capitalize()}"
	with repo.config_writer()as B:B.set_value(C,_I,E);B.set_value(C,'email',D)
def sparta_594d2a5e71(webSocket,json_data,user_obj):
	A=json_data;logger.debug('sqEditorGitClone');logger.debug(A);F=A[_C];G=A['bCreateRepoAtPath'];K=A['folder_name'];H=A['file_path'];I=A['cloneUrl'];C=F
	if G:C=H
	J=os.path.dirname(os.path.realpath(__file__));os.chdir(C);D=Popen(f"git clone {I} --progress",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);os.chdir(J);E=_E
	while _B:
		B=D.stdout.readline()
		if'Receiving objects:'in B:E=_B,
		if B==''and D.poll()is not _F:break
		if B:webSocket.send(text_data=json.dumps({_A:2,'msg':B}))
	if E:return{_A:1}
	else:return{_A:-1,_D:'An error occurred'}
def sparta_1957671909(json_data,user_obj):
	A=json_data;B=A[_C];I=A.get('bAddGitignore',_E);J=A.get('bAddReadme',_E);C=Popen(f"git init",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B,cwd=B);F=[]
	for G in C.stdout:logger.debug('Git create repo txt');logger.debug(G,end='');F.append(G.strip())
	C.stdout.close();C.wait();H=os.path.dirname(__file__)
	if I:
		D=os.path.join(H,'.default_gitignore');E=os.path.join(B,'.gitignore')
		try:shutil.copy(D,E)
		except:pass
	if J:
		D=os.path.join(H,'.default_readme');E=os.path.join(B,'README.md')
		try:shutil.copy(D,E)
		except:pass
	return{_A:1,'output':'\n'.join(F)}
def sparta_94eb688f8a(json_data,user_obj):
	F=user_obj;B=json_data;logger.debug('sqEditorGitAddRemoteOrigin json_data');logger.debug(B);C=B[_C];G=sparta_369d1135a6(C)
	if G:
		H=B['remoteUrl'];I=B['remoteName'];A=git.Repo(C);sparta_45f7da42e9(A,F);J=A.create_remote(I,url=H);A=git.Repo(C);sparta_45f7da42e9(A,F)
		for D in A.remotes:D.fetch()
		for D in A.remotes:
			if J==D:
				E=D.refs
				if len(E)>0:K=E[len(E)-1];L=os.path.dirname(os.path.realpath(__file__));os.chdir(C);sparta_8fc546c8f3(K);os.chdir(L)
	return{_A:1}
def sparta_58c77e7082(json_data,user_obj):
	A=json_data;logger.debug('git_load_available_track_remote json_data');logger.debug(A);B=A[_C];F=sparta_369d1135a6(B)
	if F:
		G=A[_H];C=git.Repo(B);sparta_45f7da42e9(C,user_obj);D=[]
		for E in C.remotes:
			if G==E.config_reader.get(_J):
				for H in E.refs:D.append({_I:H.name})
	return{_A:1,'available_branches':D}
def sparta_702254ea58(json_data,user_obj):
	A=json_data;logger.debug('*******************************************');logger.debug('git_set_track_remote json_data');logger.debug(A);B=A[_C];D=sparta_369d1135a6(B)
	if D:G=A[_H];E=A['remoteBranchToTrack'];C=git.Repo(B);sparta_45f7da42e9(C,user_obj);H=C.head.ref.name;F=os.path.dirname(os.path.realpath(__file__));os.chdir(B);sparta_8fc546c8f3(E);os.chdir(F)
	return{_A:1}
@sparta_681333af51
def sparta_ff90bb711e(json_data,user_obj):return{_A:1}
def sparta_0f8b4ac55b(json_data,user_obj):
	B=json_data[_C];C=sparta_369d1135a6(B)
	if C:A=git.Repo(B);sparta_45f7da42e9(A,user_obj);D=A.active_branch;E=D.tracking_branch().remote_name;F=A.remote(name=E);F.pull(allow_unrelated_histories=_B)
	return{_A:1}
def sparta_9fafedfb50(json_data,user_obj):
	B=json_data[_C];C=sparta_369d1135a6(B)
	if C:A=git.Repo(B);sparta_45f7da42e9(A,user_obj);D=A.active_branch;E=D.tracking_branch().remote_name;F=A.remote(name=f"{E}");F.push()
	return{_A:1}
def sparta_42fc68ca7e(json_data,user_obj):
	A=json_data[_C];C=sparta_369d1135a6(A)
	if C:
		B=git.Repo(A);sparta_45f7da42e9(B,user_obj)
		for D in B.remotes:D.fetch()
	return{_A:1}
def sparta_6349087e2b(json_data,user_obj):A=json_data[_C];B=sparta_369d1135a6(A);return{_A:1,_L:B}
def sparta_24bb56babf(json_data,user_obj):
	Y='time_sort';O='is_git_repo';G='sha'
	def N(commit):A=commit;B=time.strftime('%Y-%m-%d %H:%M',time.localtime(A.committed_date));C=naturalday(parser.parse(str(B)));return{'author':A.committer.name,'author_name':A.author.name,'time':C,Y:B,G:A.hexsha,'message':A.message,'summary':A.summary}
	def B(folder_path):
		j='remotes_arr';i='commits_ahead_arr';h='commits_behind_arr';g='is_ahead';f='is_behind';W='branch';H=folder_path;P=sparta_369d1135a6(H);logger.debug(f"is_git_repository > {H}");logger.debug(P)
		if P:
			A=git.Repo(H);F=[];Z=[]
			for a in A.references:
				b=a.name;Z.append(b)
				for k in A.iter_commits(rev=b):B=N(k);B[W]=a.name;B[f]=0;B[g]=0;F.append(B)
			F=sorted(F,key=lambda d:d[Y],reverse=_B);I=A.head.ref.name;K=[];L=[]
			if len(A.remotes)>0:
				c=A.active_branch;Q=_F;D=c.tracking_branch()
				if D is not _F:
					M=c.tracking_branch().name;logger.debug(f"current_branch > {I}");logger.debug(f"remote_branch > {M}");logger.debug('branch.tracking_branch()');logger.debug(D);logger.debug(dir(D));logger.debug(D.path);logger.debug('Remote Name');logger.debug(D.remote_name);Q=D.remote_name;l=D.config_reader();logger.debug('remote_branch_url');logger.debug(l)
					try:
						m=A.iter_commits(f"{I}..{M}")
						for n in m:B=N(n);K.append(B)
						logger.debug(h);logger.debug(K)
					except Exception as R:logger.debug('Exception behind');logger.debug(R)
					try:
						o=A.iter_commits(f"{M}..{I}")
						for p in o:B=N(p);L.append(B)
						logger.debug(i);logger.debug(L)
					except Exception as R:logger.debug('Exception Ahead');logger.debug(R)
					for S in K:
						T=S[G]
						for E in F:
							if E[W]==f"{M}"and E[G]==T:E[f]=1;break
					for S in L:
						T=S[G]
						for E in F:
							if E[W]==I and E[G]==T:E[g]=1;break
			U=[]
			for J in A.remotes:
				d=_E;logger.debug('----------------------------');logger.debug('this_remote');logger.debug(J);logger.debug(dir(J))
				if Q is not _F:
					if Q==J.name:d=_B
				V=J.config_reader.get(_J);q=os.path.splitext(os.path.basename(V))[0];C=re.search('@[\\w.]+',V)
				if C is not _F:
					C=str(C.group())
					if C.startswith('@'):C=C[1:]
				else:C=''
				U.append({_I:J.name,_H:V,'repo_name':q,'domain':C,'is_tracking':d})
			logger.debug(j);logger.debug(U);e=_E
			if X==H:e=_B
			return{_A:1,'is_base_directory':e,'folder':H,O:P,'commits_arr':F,'branches':Z,'current_branch':I,j:U,h:K,i:L}
	X=json_data[_C];A=B(X)
	if A is not _F:A[O]=_B;return A
	else:return{_A:1,O:_E}
def sparta_2c57e450e4(json_data,user_obj):
	H='path';G='file';C=json_data[_C];I=sparta_369d1135a6(C)
	if I:
		B=git.Repo(C);sparta_45f7da42e9(B,user_obj);D=[]
		for A in B.index.diff(_F):D.append({G:A.a_path,'change_type':A.change_type,'is_deleted':A.deleted_file,H:A.a_path})
		E=[]
		for F in B.untracked_files:E.append({G:F,H:F})
		return{_A:1,'changed_files_arr':D,'untracked_files_arr':E}
	return{_A:1}
def sparta_e433888c1f(json_data,user_obj):
	B=json_data;C=B[_C];D=B['gitMsg'];E=sparta_369d1135a6(C)
	if E:A=git.Repo(C);sparta_45f7da42e9(A,user_obj);A.git.add(all=_B);A.git.commit('-m',D)
	return{_A:1}
@sparta_681333af51
def sparta_9e121222a2(json_data,user_obj):return{_A:1}
def sparta_5c1a75e950(json_data,user_obj):
	A=json_data;logger.debug('Delete Remoete');logger.debug(A);C=A[_C];E=sparta_369d1135a6(C)
	if E:
		B=git.Repo(C);sparta_45f7da42e9(B,user_obj);F=A[_H]
		for D in B.remotes:
			if F==D.config_reader.get(_J):B.delete_remote(D);break
	return{_A:1}
def sparta_f7ea628463(json_data,user_obj):return{_A:1}
def sparta_602b8ec5e5(json_data,user_obj):
	D=json_data;E=D[_C];C=D['newBranchName'];F=sparta_369d1135a6(E)
	if F:
		A=git.Repo(E);sparta_45f7da42e9(A,user_obj);B=[A for A in A.branches if A.name==C]
		if len(B)==0:G=A.active_branch;B=A.create_head(C);B.checkout();A.git.push('--set-upstream','origin',B);G.checkout();A.git.checkout(C);return{_A:1}
		else:return{_A:-1,_D:'A branch with this name already exists'}
	return{_A:-1,_D:_G}
def sparta_ec21abb866(json_data,user_obj):
	A=json_data;B=A[_C];D=A['branch2Checkout'];E=sparta_369d1135a6(B)
	if E:
		C=git.Repo(B);sparta_45f7da42e9(C,user_obj)
		try:C.git.checkout(D);return{_A:1}
		except Exception as F:return{_A:-1,_D:str(F)}
	return{_A:-1,_D:_G}
def sparta_05242ff03c(json_data,user_obj):
	B=json_data;C=B[_C];D=B['branch2Merge'];F=sparta_369d1135a6(C)
	if F:
		A=git.Repo(C);sparta_45f7da42e9(A,user_obj);E=A.head.ref.name
		if E==D:return{_A:-1,_D:'Please choose another branch'}
		try:A.git.checkout(D);A.git.merge(E);return{_A:1}
		except Exception as G:return{_A:-1,_D:str(G)}
	return{_A:-1,_D:_G}
def sparta_5ff64fa1b7(json_data,user_obj):
	D=json_data;A=D[_C];B=D['branch2Delete'];F=sparta_369d1135a6(A)
	if F:
		E=git.Repo(A);sparta_45f7da42e9(E,user_obj);G=E.head.ref.name
		if G==B:return{_A:-1,_D:'You cannot delete the active branch. Please checkout to another branch before deleting this one'}
		try:H=os.path.dirname(os.path.realpath(__file__));os.chdir(A);C=Popen(f"git branch -d {B}",stdout=PIPE,stderr=PIPE,bufsize=1,universal_newlines=_B,shell=_B);I=C.stderr.readlines();C=Popen(f"git push origin --delete {B}",stdout=PIPE,stderr=PIPE,bufsize=1,universal_newlines=_B,shell=_B);I=C.stderr.readlines();os.chdir(H);return{_A:1}
		except Exception as J:return{_A:-1,_D:str(J)}
	return{_A:-1,_D:_G}
def sparta_52b3751ae6(json_data,user_obj):
	F='diff_output';A=json_data;logger.debug('sqEditorGitLoadFilesDiff');logger.debug(A);B=A[_C];G=A['filePath'];H=A['fileType'];C=sparta_369d1135a6(B);logger.debug(_L);logger.debug(C)
	if C:D=git.Repo(B);sparta_45f7da42e9(D,user_obj);E=D.git.diff();logger.debug(F);logger.debug(E);return{_A:1,F:E}
	return{_A:-1,_D:_G}