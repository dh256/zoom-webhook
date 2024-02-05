'''
Used to generate signature of a webhook message
Needed for Postman testing of sending a webhook message 

Set SECRET_TOKEN env variable to Zoom's app webhook secret token
'''
from cryptography.hazmat.primitives import hashes, hmac
import json
import os

def main():
    message = 'v0:1705957624:{"event","meeting.started":"payload",{"account_id","J5_UemqcQPahWZOOzlseYA":"object",{"duration",0:"start_time","2024-01-22T21:07:04Z":"timezone","Europe/London":"topic","David Hanley\'s Personal Meeting Room":"id","3666557080":"type",4:"uuid","+ZpcwOiwS/SjzWQktIYbbg==":"host_id","fHw2iBkBQHWwLe-pKbmGrw"}}:"event_ts",1705957624046}'
    print(message)
    key = bytes(os.environ['SECRET_TOKEN'],'utf-8')
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(bytes(message,'utf-8'))
    signature = f'v0={h.finalize().hex()}'
    print(signature)
    

if __name__ == '__main__':
    main()