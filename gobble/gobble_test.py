from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time

from kiwoom import Kiwoom

TR_REQ_TIME_INTERVAL = 3.8
START = '20000101'

# starting app
app = QApplication(['kiwoom.py'])
kiwoom = Kiwoom()
kiwoom.comm_connect()

tasks = {}
# retrieving kospi, kosdaq codes
for market_type in ['0', '10']:
    code_list = kiwoom.get_code_list_by_market(market_type)
    name_list = [kiwoom.get_master_code_name(code) for code in code_list]
    market_dict = dict(zip(code_list, name_list))
    if market_type == '0':
        tasks['kospi'] = market_dict
    elif market_type == '10':
        tasks['kosdaq'] = market_dict

# requesting data from kiwoom server
# for market_type in [0, 10]:
#     if market_type == 0:
#         market = 'kospi'
#     elif market_type == 10:
#         market = 'kosdaq'

# test kosdaq buysell data
for code, name in tasks['kosdaq'].items():
    print(code, name)
    kiwoom.prepare_data()

    for buysell in [1, 2]:
        if buysell == 1:
            kiwoom.set_buysell_state('buy')
        elif buysell == 2:
            kiwoom.set_buysell_state('sell')

        today_date = time.strftime('%Y%m%d')

        # opt10059 TR 요청
        kiwoom.set_input_value("일자", today_date)
        kiwoom.set_input_value("종목코드", code)
        kiwoom.set_input_value("금액수량구분", 2)
        kiwoom.set_input_value("매매구분", buysell)
        kiwoom.set_input_value("단위구분", 1)
        kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")
        time.sleep(TR_REQ_TIME_INTERVAL)
        print("first request sent in successfully")

        while kiwoom.remained_data == True:
            kiwoom.set_input_value("일자", time.strftime('%Y%m%d'))
            kiwoom.set_input_value("종목코드", code)
            kiwoom.set_input_value("금액수량구분", 2)
            kiwoom.set_input_value("매매구분", buysell)
            kiwoom.set_input_value("단위구분", 1)
            kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0101")
            print("requesting...")
            current_date = kiwoom.get_date()
            print("date loop is on: ", str(current_date))
            if current_date <= int(START):
                print("loop breaking b/c " + str(current_date) + " lower than " + str(START))
                break
            time.sleep(TR_REQ_TIME_INTERVAL)

        if buysell == 1:
            print("BUY data saved, ready for DB")
        elif buysell == 2:
            print("SELL data saved, ready for DB")

    print(kiwoom.data)
    break
