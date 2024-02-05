'''
Flask web app to process webhook events received from Zoom.US account
Set SECRET_TOKEN env variable to Zoom's app webhook secret token
'''
from flask import Flask, request, abort, Response, jsonify
from cryptography.hazmat.primitives import hashes, hmac
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return('<p>Hello - The webhook is alive!</p><p>Submit events to /webhook</p>')

@app.route('/webhook', methods=['POST'])
def webhook():
    print('Webhook called')
    if request.content_type.find('application/json') >= 0:
        body = request.json
        if not body:
            # invalid request
            print(f'Invalid request,Invalid JSON body,{body}')
            abort(400)
    else:
        # invalid request
        print(f'Invalid request,Invalid content_type,{request.content_type}')
        abort(400)
    
    # handle a Zoom Validation request
    event = body['event']
    if event == 'endpoint.url_validation':
        # return response
        print(f'Process validation request')
        plain_token = body['payload']['plainToken']
        return jsonify(
            plainToken=plain_token,
            encryptedToken=calculate_signature(plain_token)
        )
    else:
        # normal zoom event
        # get signature
        if 'x-zm-signature' in [key.lower() for key in request.headers.keys()]:
            zm_signature = request.headers['x-zm-signature']
        else:
            # invalid requestx-zm-signature
            print(f'Invalid request, header not found')
            abort(400)

        # get request timestamp
        if 'x-zm-request-timestamp' in [key.lower() for key in request.headers.keys()]:
            zm_request_timestamp = request.headers['x-zm-request-timestamp']
            print(f'x-zm-request-timestamp,{zm_request_timestamp}')
        else:
            # invalid request
            print(f'Invalid request,x-zm-request-timestamp header not found')
            abort(400)
        
        # calculate the signature of body and compare to received_signature
        body_str = json.dumps(body,separators=(',',':'))
        message = f'v0:{zm_request_timestamp}:{body_str}'
        calc_signature = f'v0={calculate_signature(message)}'
        if calc_signature != zm_signature:
            # invalid sig
            print(f'Invalid request,payload signature does not match received signature,{zm_signature},{calc_signature}')
            abort(400)

        # process the event
        process_event(body)
        
        # all good - return 200
        print('Webhook event processed')
        return Response(status=200)

def process_event(body):
    # process the event - for now just log
    print(f"Event,{body['event']},{body['event_ts']},{body['payload']}")

def calculate_signature(hash_str: str) -> str:
    h = hmac.HMAC(bytes(os.environ['SECRET_TOKEN'],'utf-8'), hashes.SHA256())
    h.update(bytes(hash_str,'utf-8'))
    calc_signature = h.finalize().hex()
    return calc_signature
    
if __name__ == '__main__':
   app.run()
