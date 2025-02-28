import pandas as pd
import requests as req
import hashlib
import base64
import json
import time
import threading as mt
import websocket as wb
import ssl

class GreekAPI:
    def __init__(self, user,s_pwd, pwd,procli,ac_no):
        self.username = user
        self.session_pwd = s_pwd
        self.userpwd = pwd
        self.gscid = self.username
        self.session_id = None
        self.ws_apollo = None
        self.procli=procli
        self.url_session_token ='http://greekapi.greeksoft.in:3001'
        self.is_secure=False
        self.is_base64 = True
        self.rest_ip = "dev.greeksoft.in"
        self.rest_port = "3333"
        self.session_token = self.get_session_token()
        self.ac_no=ac_no
        if self.is_secure :
            self.ssl_verify = False
            self.wbhd = "https://"
            self.wshd = "wss://"
        else:
            self.ssl_verify = False
            self.wbhd = "http://"
            self.wshd = "ws://"
        self.gcid=self.getlogininfo()
    def base64_to_json(self, coded_string):
        string = base64.b64decode(coded_string).decode('utf-8')
        return json.loads(string)

    def get_session_token(self):
        url = f'{self.url_session_token}/auth/greek/sessiontoken'
        myobj = {
            "username": str(self.username),
            "password": str(self.session_pwd),
            "validFor": str("1d")
        }

        response = req.post(url, json=myobj)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the session token from the response
        session_token = response.json().get('sessionToken')

        return session_token

    def json_to_base64(self, string):
        string = json.dumps(string)
        coded_string = base64.b64encode(string.encode('utf-8'))
        coded_string = repr(coded_string)[2:-1]
        return coded_string

    def get_url(self,servicename):
        svcname = servicename
        url = self.wbhd+self.rest_ip+ ":"+self.rest_port+"/"+svcname
        return url
    def token_broadcast(self,tokenno, assettype):
        gcid=self.getlogininfo()
        params = {
            "request": {
                "data": {
                    "token": tokenno,
                    "assetType": assettype,
                    "gscid": str(self.username),
                    "gcid": str(gcid),
                },
                "svcName": "getQuoteForSingleSymbol_V2",
                "svcGroup": "Markets"
            }
        }
        params = self.json_to_base64(params)
        stoken = self.session_token
        headers = { "Authorization":""+str(stoken) ,"charset": "utf-8", "Content-Type": "application/json" }
        svcname = "getQuoteForSingleSymbol_V2"
        url_neworder = self.get_url(svcname)
        y1 =  req.post(url_neworder,data=params,headers=headers ,verify=self.ssl_verify )
        y1 = y1.text
        z1 = self.base64_to_json(y1)
        df_broadcast_response = pd.json_normalize(z1['response'])
        return df_broadcast_response

    def getlogininfo(self):
        svcname = "getLoginInfo"
        url_getlogininfo = self.get_url(svcname)
        stoken = self.session_token
        headers = { "Authorization":""+str(stoken) ,"charset": "utf-8", "Content-Type": "application/json" }
        svc_req = {
            "request": {
                "svcVersion": "1.0.0",
                "svcGroup": "Login",
                "svcName": "getlogininfo",
                "assetType": "",
                "data": {
                    "gscid": str(self.username)
                }
            }
        }
        if self.is_base64 :
            svc_req = self.json_to_base64(svc_req)
        svc_res =  req.request("POST",url=url_getlogininfo,data=svc_req,headers=headers,verify=False )
        if self.is_base64 :
            svc_res = svc_res.text
            svc_res = self.base64_to_json(svc_res)
        # print(svc_res)
        gcid = svc_res['response']['data']['gcid']
        return gcid

    def jlogin_new(self):
        url_jloginnew = f"http://{self.rest_ip}:{self.rest_port}/jloginNew"
        pwdhash = hashlib.md5(self.userpwd.encode()).hexdigest()
        svc_req = {
            "request": {
                "data": {
                    "gscid": str(self.username),
                    "deviceDetails": "",
                    "deviceType": "0",
                    "pass": str(pwdhash),
                    "transPass": "",
                    "userType": "Customer",
                    "brokerid": "1",
                    "passType": "0",
                    "version_no": "1.0.1.10",
                    "encryptionType": "1"
                },
                "svcName": "jloginNew",
                "svcGroup": "Login"
            }
        }

        if self.is_base64:
            svc_req = self.json_to_base64(svc_req)

        headers = {"Authorization": self.session_token, "charset": "utf-8", "Content-Type": "application/json"}
        svc_res = req.post(url_jloginnew, data=svc_req, headers=headers, verify=False)
        if self.is_base64:
            svc_res = self.base64_to_json(svc_res.text)

        session_id = svc_res['response']['sessionId']
        self.session_id=session_id
        websocket_broadcast_ip = svc_res['response']['data']['Apollo_IP']
        websocket_broadcast_port = svc_res['response']['data']['Apollo_Port']
        websocket_order_ip = svc_res['response']['data']['Iris_IP']
        return session_id, websocket_broadcast_ip, websocket_broadcast_port, websocket_order_ip

    def Net_Position_Details_strategywise(self):
        svcname = "getStrategyNameWiseNetPositionDetail?"
        url_neworder = self.get_url(svcname)
        #ord_status = req.get(f"{url_neworder}/{ord_id}")
        text = "gscid={}".format(str(self.username))

        # text = text.replace('"', '')
        # info = json_to_base64(text)
        coded_string = base64.b64encode(text.encode('utf-8'))
        coded_string = repr(coded_string)[2:-1]
        info = url_neworder + coded_string


        # params = {
        #     "request": {
        #         "FormFactor": "M",
        #         "data": {
        #             "gcid": str(gcid),
        #             "gscid": str(username)
        #         },
        #         "svcGroup": "portfolio",
        #         "svcVersion": "1.0.0",
        #         "streaming_type": str(svcname),
        #         "request_type": "subscribe"
        #     }
        # }
        # params = json_to_base64(params)
        stoken = self.session_token
        headers = { "Authorization":""+str(stoken) ,"charset": "utf-8", "Content-Type": "application/json" }
        y1 =  req.request("GET", info, headers=headers ,verify=self.ssl_verify )
        y1 = y1.text
        z1 = self.base64_to_json(y1)
        response = z1

        return response

    def send_apollo_resp(self):
        jln = self.jlogin_new()
        session_id = jln[0]
        # bgcid=self.get_gscid_and_stoken()
        gcid=self.gcid
        print(session_id)
        # session_id = jln['response']['sessionId']
        ws_apollo = wb.create_connection(f"ws://{self.rest_ip}:3032", sslopt={"cert_reqs": ssl.CERT_NONE})
        self.ws_apollo=ws_apollo
        apollo_login_req = {"request": {"data": {"gscid": str(self.username),"gcid": str(gcid),"sessionId": str(session_id),"device_type": "0"},"response_format": "json","request_type": "subscribe","streaming_type": "login"}}
        apollo_login_req = self.json_to_base64(apollo_login_req)
        ws_apollo.send( apollo_login_req )
        apollo_login_res = ws_apollo.recv()
        apollo_login_res = self.base64_to_json(apollo_login_res)
        print("Apollo Login Response:", apollo_login_res)


        t1 = mt.Thread( target=self.heartbeat_req)
        t1.start()



    def heartbeat_req(self):
        gcid=self.gcid
        ws_apollo = wb.create_connection(f"ws://{self.rest_ip}:3032", sslopt={"cert_reqs": ssl.CERT_NONE})

        apollo_hb_req = {"request": {"data": {"gcid": str(gcid),"sessionId": str(self.session_id) },"response_format": "json","request_type": "subscribe","streaming_type": "HeartBeat"}}
        apollo_hb_req = self.json_to_base64(apollo_hb_req)
        while True:
            ws_apollo.send( apollo_hb_req )
            time.sleep(20)

    def thread_function(self,stop_event):
        while not stop_event.is_set():
            apollo_res = self.base64_to_json(self.ws_apollo.recv())
            service_name = apollo_res['response']['svcName']
            streaming = apollo_res['response']['streaming_type']
            if service_name == 'Broadcast' and streaming == 'marketPicture':
                token = apollo_res['response']['data']['symbol']
                # if s1_nifty["symbol"] == token:
                # print("HI")
                # "hi"

    def subscribe_token(self, token):
        apo_login=self.send_apollo_resp()
        gcid=self.gcid
        self.gscid=self.username
        if self.gscid and self.session_id and len(token)<=50:
            for tkn in token:
                s1_nifty = {"symbol": str(tkn)}
                apollo_subscribe_req_n = {
                    "request": {
                        "data": {
                            "symbols": [s1_nifty]
                        },
                        "response_format": "json",
                        "gscid": str(self.username),
                        "gcid": gcid,  # Assuming gcid is the same as gscid for this example
                        "request_type": "subscribe",
                        "streaming_type": "marketPicture"
                    }
                }
                apollo_subscribe_req_n = self.json_to_base64(apollo_subscribe_req_n)
                self.ws_apollo.send(apollo_subscribe_req_n)
                print(f"Subscribed to token: {tkn}")
        else:
            print("Cannot subscribe. Session ID or GCID is not set.")

    def unsubscribe_token(self,token):
        gcid=self.gcid
        username=self.username
        if gcid and username:
            s1_nifty = {"symbol": str(token)}
            apollo_unsubscribe_req_n={
                "request": {
                    "data": {
                        "symbols": [
                            {
                                "symbol": [s1_nifty]
                            }
                        ]
                    },
                    "response_format": "json",
                    "gscid": str(self.username),
                    "gcid": gcid,
                    "request_type": "unsubscribe",
                    "streaming_type": "marketPicture"
                }
            }
            apollo_unsubscribe_req_n = self.json_to_base64(apollo_unsubscribe_req_n)
            self.ws_apollo.send(apollo_unsubscribe_req_n)
            return f"UnSubscribed to token: {token}"


    def get_apollo_resp(self,token,req_data):
        subs=self.subscribe_token(token)
        while True:
            apollo_res = self.ws_apollo.recv()
            apollo_res = self.base64_to_json(apollo_res)
            service_name = apollo_res['response']['svcName']
            streaming = apollo_res['response']['streaming_type']
            if service_name == 'Broadcast' and streaming == 'marketPicture':
                # print("Market Picture Data:", apollo_res['response']['data'])
                tkn=apollo_res['response']['data']['symbol']
                sym=apollo_res['response']['data']['name']
                ltp=apollo_res['response']['data']['ltp']
                ltt=apollo_res['response']['data']['ltt']
                bid=apollo_res['response']['data']['bid']
                ask=apollo_res['response']['data']['ask']
                depth=apollo_res['response']['data']['level2']
                app_res=apollo_res['response']['data']
                if req_data =='depth':
                    yield tkn,sym,depth,ltt
                elif req_data =='ask/bid':
                    yield tkn,sym,bid,ask,ltt
                elif req_data=='allresp':
                    yield app_res
                else:
                    yield tkn,sym,ltp,ltt
                # time.sleep(0.5)


    def place_order(self,tokenno,symbol,lot,qty,price,buysell,ordtype,trigprice,strategyname):
        gcid=self.gcid
        params = {
            "request": {
                "data": {
                    "trigger_price": str(trigprice),
                    "gtoken": str(tokenno),
                    "side": str(buysell),
                    "gcid": str(gcid),
                    "validity": "0",
                    "price": str(price),
                    "exchange": "NSE",
                    "disclosed_qty": "0",
                    "tradeSymbol": str(symbol),
                    "lot": str(lot),
                    "iprocli":str(self.procli),
                    "order_type": str(ordtype),
                    "product": "0",
                    "qty": str(qty),
                    "corderid": "3",
                    "amo": "0",
                    "AccountNumber":str(self.ac_no),
                    "is_restapi":"1",
                    "gtdExpiry": 0,
                    "is_post_closed": "0",
                    "is_preopen_order": "0",
                    "isSqOffOrder": "false",
                    "offline": "0",
                    "strategyName":str(strategyname),
                    "strategyNo":"124"
                },
                "response_format": "json",
                "request_type": "subscribe",
                "streaming_type": "NewOrderRequest"
            }
        }

        if self.procli != "1":
            # Remove 'AccountNumber' and 'is_restapi' from the data dictionary if procli is not "1"
            del params["request"]["data"]["AccountNumber"]
            del params["request"]["data"]["is_restapi"]

        params = self.json_to_base64(params)
        stoken = self.session_token
        headers = { "Authorization":""+str(stoken) ,"charset": "utf-8", "Content-Type": "application/json" }
        svcname = "NewOrderRequest"
        url_neworder = self.get_url(svcname)
        y1 =  req.post(url_neworder,data=params,headers=headers ,verify=self.ssl_verify )
        y1 = y1.text
        z1 = self.base64_to_json(y1)
        df_order_response = pd.json_normalize(z1['response'])
        return df_order_response


    def close_connection(self):
        if self.ws_apollo:
            self.ws_apollo.close()
            print("WebSocket connection closed.")
