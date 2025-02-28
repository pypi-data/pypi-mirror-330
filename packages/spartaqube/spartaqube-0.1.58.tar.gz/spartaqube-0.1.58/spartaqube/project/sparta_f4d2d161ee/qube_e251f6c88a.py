import time
from project.logger_config import logger
def sparta_552d613e25():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_552d613e25()
def sparta_21306052cc(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_944bd4c250():sparta_21306052cc(False)