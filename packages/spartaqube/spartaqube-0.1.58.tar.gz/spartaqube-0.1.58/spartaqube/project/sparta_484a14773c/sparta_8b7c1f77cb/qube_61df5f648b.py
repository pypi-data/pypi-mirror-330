_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_1b23781713():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_252766026d(objectToCrypt):A=objectToCrypt;C=sparta_1b23781713();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_80c4d6d286(apiAuth):A=apiAuth;B=sparta_1b23781713();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_26ef4354c6(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_c18f177957(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_26ef4354c6(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a85f9218ab(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_26ef4354c6(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_71fa5ab04a(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_effa50f9a5(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_71fa5ab04a(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_1f314c8df7(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_71fa5ab04a(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_fd2dcd9e3a(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_4fb3c59b2a(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_fd2dcd9e3a(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c04e43795c(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_fd2dcd9e3a(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_4e21b961f0():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e5ad020573(objectToCrypt):A=objectToCrypt;C=sparta_4e21b961f0();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_da287ede29(objectToDecrypt):A=objectToDecrypt;B=sparta_4e21b961f0();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)