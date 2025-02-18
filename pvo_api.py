import logging
import time
import requests

class PVOutputApi:

    def __init__(self, system_id, api_key):
        self.m_system_id = system_id
        self.m_api_key = api_key

    def add_status(self, d, t, v1, v2, v3, v4, v5, v6, c1, n, v7, v8, v9, v10, v11, v12, m1):
        
        payload = {}
        payload['d'] = d
        payload['t'] = t
        payload['v1'] = v1
        payload['v2'] = v2
        
        if v3 is not None:
            payload['v3'] = v3
        
        if v4 is not None:        
            payload['v4'] = v4
        
        if v5 is not None:        
            payload['v5'] = v5
        
        if v6 is not None:        
            payload['v6'] = v6
        
        if c1 is not None:        
            payload['c1'] = c1
        
        if n is not None:        
            payload['n'] = n
        
        if v7 is not None:        
            payload['v7'] = v7
        
        if v8 is not None:        
            payload['v8'] = v8
        
        if v9 is not None:        
            payload['v9'] = v9
        
        if v10 is not None:        
            payload['v10'] = v10
        
        if v11 is not None:        
            payload['v11'] = v11
        
        if v12 is not None:        
            payload['v12'] = v12
        
        if m1 is not None:        
            payload['m1'] = m1
            
        self.call("https://pvoutput.org/service/r2/addstatus.jsp", payload)

    def call(self, url, payload):
    
        logging.info(payload)

        headers = {
            'X-Pvoutput-Apikey' : self.m_api_key,
            'X-Pvoutput-SystemId' : self.m_system_id,
            'X-Rate-Limit': '1'
        }

        for i in range(1, 4):
            try:
                r = requests.post(url, headers=headers, data=payload, timeout=10)
                if 'X-Rate-Limit-Reset' in r.headers:
                    reset = round(float(r.headers['X-Rate-Limit-Reset']) - time.time())
                else:
                    reset = 0
                if 'X-Rate-Limit-Remaining' in r.headers:
                    if int(r.headers['X-Rate-Limit-Remaining']) < 10:
                        logging.info("Only {} requests left, reset after {} seconds".format(
                            r.headers['X-Rate-Limit-Remaining'],
                            reset))
                if r.status_code == 403:
                    logging.info("Forbidden: " + r.reason)
                    time.sleep(reset + 1)
                else:
                    r.raise_for_status()
                    break
            except requests.exceptions.RequestException as arg:
                logging.info(r.text or str(arg))
            time.sleep(i ** 3)
        else:
            logging.error("Failed to call PVOutput API")