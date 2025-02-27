_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_c75c2106f3():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f4d62af2f9(objectToCrypt):A=objectToCrypt;C=sparta_c75c2106f3();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9711a2545d(apiAuth):A=apiAuth;B=sparta_c75c2106f3();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2c9648dbd1(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_202c18b1de(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2c9648dbd1(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_fefdaec140(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2c9648dbd1(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_9eefce8ebe(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f0afb90554(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_9eefce8ebe(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_527b03b9ba(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_9eefce8ebe(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_61a7c5c5be(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5e6a777318(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_61a7c5c5be(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c107049039(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_61a7c5c5be(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_5e8643b5e0():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_8ee6529fea(objectToCrypt):A=objectToCrypt;C=sparta_5e8643b5e0();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c79a8ad4d1(objectToDecrypt):A=objectToDecrypt;B=sparta_5e8643b5e0();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)