_E='service'
_D='is_terminated'
_C='utf-8'
_B='response'
_A='res'
import json,io,base64,os,cloudpickle,pandas as pd
from project.logger_config import logger
def sparta_fbb0c3b4a5(file_path,text):
	A=file_path
	try:
		B='a'if os.path.exists(A)and os.path.getsize(A)>0 else'w'
		with open(A,B,encoding=_C)as C:
			if B=='a':C.write('\n')
			C.write(text)
		logger.debug(f"Successfully wrote/appended to {A}")
	except Exception as D:logger.debug(f"Error writing to file: {D}")
class ReceiverKernel:
	def __init__(A,ipython_kernel,socket_zmq):A.ipython_kernel=ipython_kernel;A.socket_zmq=socket_zmq
	def send_response(C,identity,response_dict,request_dict=None):
		B=request_dict;A=response_dict
		if B is not None:A.update(B)
		A[_D]=True;C.socket_zmq.send_multipart([identity,json.dumps(A).encode()])
	def terminate(A,identity):B={_A:1,_E:'break-loop',_D:True,_B:1};A.send_response(identity,B)
	def process_request(A,identity,request_dict):
		R='value';Q='name';P='kernel_variable';O='cellId';N='cmd';I='json_data';D=identity;B=request_dict;A.ipython_kernel.set_zmq_identity(D);A.ipython_kernel.set_zmq_request(B);C=B[_E]
		if C=='execute_code':G=B[N];A.ipython_kernel.execute_code(G,websocket=A.socket_zmq)
		elif C=='execute_shell':G=B[N];E=json.loads(B[I]);A.ipython_kernel.execute_shell(G,websocket=A.socket_zmq,cell_id=E[O])
		elif C=='execute':G=B[N];E=json.loads(B[I]);A.ipython_kernel.execute(G,websocket=A.socket_zmq,cell_id=E[O])
		elif C=='activate_venv':S=B['venv_name'];A.ipython_kernel.activate_venv(S);A.terminate(D)
		elif C=='deactivate_venv':A.ipython_kernel.deactivate_venv();A.terminate(D)
		elif C=='get_kernel_variable_repr':J=B[P];T=A.ipython_kernel._method_get_kernel_variable_repr(kernel_variable=J);F={_A:1,_B:T};A.send_response(D,F,B)
		elif C=='get_workspace_variable':J=B[P];U=A.ipython_kernel._method_get_workspace_variable(kernel_variable=J);V=base64.b64encode(cloudpickle.dumps(U)).decode(_C);F={_A:1,_B:V};A.send_response(D,F,B)
		elif C=='reset_kernel_workspace':A.ipython_kernel.reset_kernel_workspace();A.terminate(D)
		elif C=='list_workspace_variables':W=A.ipython_kernel.list_workspace_variables();F={_A:1,_B:W};A.send_response(D,F,B)
		elif C=='set_workspace_variable':E=json.loads(B[I]);A.ipython_kernel._method_set_workspace_variable(name=E[Q],value=json.loads(E[R]));A.terminate(D)
		elif C=='set_workspace_variables':
			H=cloudpickle.loads(base64.b64decode(B['encoded_dict']))
			for(K,L)in H.items():A.ipython_kernel._method_set_workspace_variable(K,L)
			A.terminate(D)
		elif C=='set_workspace_variable_from_datasource':E=json.loads(B[I]);H=json.loads(E[R]);X=pd.DataFrame(H['data'],columns=H['columns'],index=H['index']);A.ipython_kernel._method_set_workspace_variable(name=E[Q],value=X);A.terminate(D)
		elif C=='get_kernel_memory_size':Y=A.ipython_kernel.get_kernel_memory_size();F={_A:1,_B:Y};A.send_response(D,F,B)
		elif C=='set_workspace_cloudpickle_variable':
			M=base64.b64decode(B['cloudpickle_kernel_variables']);M=cloudpickle.loads(M)
			for(K,L)in M.items():Z=io.BytesIO(L);a=cloudpickle.load(Z);A.ipython_kernel._method_set_workspace_variable(K,a)
			A.terminate(D)
		elif C=='get_cloudpickle_kernel_all_variables':b,c=A.ipython_kernel.cloudpickle_kernel_variables();F={_A:1,_B:json.dumps({'picklable':base64.b64encode(cloudpickle.dumps(b)).decode(_C),'unpicklable':base64.b64encode(cloudpickle.dumps(c)).decode(_C)})};A.send_response(D,F,B)