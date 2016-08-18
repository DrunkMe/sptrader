import cffi
import os
import sys
import time
import threading
from ctypes import *

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import sptrader
import config
cv = threading.Condition()
login = config.logininfo;
sp = sptrader.SPTrader()
sp.set_login_info(login['host'],
                  login['port'],
                  login['license'],
                  login['app_id'],
                  login['user_id'],
                  "test1")

@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_action(data):
    print(data.Price)
    

@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    cv.acquire()
    print("login")
    print(sp.get_login_status(81))
    sp.api.SPAPI_RegisterTickerUpdate(ticker_action)
    sp.api.SPAPI_SubscribeTicker(
        sp.user,
        b"003888", 0)
    input("Press any key to exit")
    cv.notify()
    cv.release()


cv.acquire()
print(sp.login(login_actions))
cv.wait()
cv.release()
sp.logout()
