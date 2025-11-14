from random import randint
# from kavenegar import *
from uuid import uuid4
import os
import random
# from decouple import config
#========================================================
def create_random_code(count):
    count-=1
    return randint(10**count,10**(count+1)-1)
#========================================================
# def send_sms(mobile,message):
#     api = KavenegarAPI('534B346952654446314B38566B6E462B327469775A4D7844562B50313077353679676B36667A6E716D67733D')
#     try:
#         params = { 'sender' : '2000660110', 'receptor': mobile, 'message' :message }
#         response = api.sms_send(params)
#     except:
#         pass
#========================================================
class UploadFile:
    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix
    
    def upload_to(self,instance,filename):
        filename, ext =os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
#========================================================
def generate_tracking_code(length=8):
    return ''.join(random.choices('0123456789', k=length))
#========================================================

