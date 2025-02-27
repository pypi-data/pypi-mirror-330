import time
from project.logger_config import logger
def sparta_ca2f19de62():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_ca2f19de62()
def sparta_089ece8230(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_1ee815affd():sparta_089ece8230(False)