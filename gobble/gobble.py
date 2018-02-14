import os
from kiwoom import Kiwoom
from processtracker import ProcessTracker, timeit

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import os, time
import simplejson as json
import _pickle as pickle
from pathlib import Path

TR_REQ_TIME_INTERVAL = 3.8

class Gobble(ProcessTracker):

    @timeit
    def __init__(self):
        super().__init__() # initialize ProcessTracker
        self.starting()
        self.app = QApplication(["kiwoom.py"])
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    @timeit
    def step_one_kiwoom(self):
        self.step_one()
        for market_type in ["0", "10"]:
            pickle_name = "kospi-dict.pickle" if market_type == "0" else "kosdaq-dict.pickle"
            code_list = self.kiwoom.get_code_list_by_market(market_type)
            name_list = [self.kiwoom.get_master_code_name(code) for code in code_list]
            market_dict = dict(zip(code_list, name_list))
            pickle_out = open("./data/" + pickle_name, "wb")
            pickle.dump(market_dict, pickle_out)
            pickle_out.close()
        self.step_one_finish()

    def set_tasks(self, market_type=None):
        if market_type == None:
            kospi_in = open("./data/kospi-dict.pickle", "rb")
            self.kospi_task = pickle.load(kospi_in)
            kosdaq_in = open("./data/kosdaq-dict.pickle", "rb")
            self.kosdaq_task = pickle.load(kosdaq_in)
        elif market_type == 'kospi':
            kospi_in = open("./data/kospi-dict.pickle", "rb")
            self.kospi_task = pickle.load(kospi_in)
            self.kosdaq_task = {}
        elif market_type == 'kosdaq':
            self.kospi_task = {}
            kosdaq_in = open("./data/kosdaq-dict.pickle", "rb")
            self.kosdaq_task = pickle.load(kosdaq_in)

    def _get_total_stock_num(self):
        kospi_len = len(list(self.kospi_task.keys()))
        kosdaq_len = len(list(self.kosdaq_task.keys()))
        return kospi_len + kosdaq_len

    def _buysell_skip_codes(self):
        os.chdir("./data/stock/kospi-buysell")
        kospi_list = [json.split(".")[0] for json in os.listdir()]
        os.chdir("../../../")
        os.chdir("./data/stock/kosdaq-buysell")
        kosdaq_list = [json.split(".")[0] for json in os.listdir()]
        os.chdir("../../../")
        return kospi_list + kosdaq_list

    def req_buysell(self, start):
        done_list = self._buysell_skip_codes()
        total_stock_num = self._get_total_stock_num() - len(done_list)
        code_looped = 0
        total_time = 0

        # get code list (0: KOSPI, 10: KOSDAQ)
        for market_type in [0, 10]:
            if market_type == 0:
                market = "kospi"
                task = self.kospi_task
            elif market_type == 10:
                market = "kosdaq"
                task = self.kosdaq_task

            for code, name in task.items():
                if code in done_list:
                    continue
                ts = time.time()
                try:
                    self._initialize_buysell_data(code, market, start)
                except:
                    print(code + ", " + name + " buysell save skipped due to error")
                te = time.time()
                time_took = te - ts
                total_time += time_took
                code_looped += 1
                avg_time_took = total_time/code_looped
                stocks_left = total_stock_num - code_looped
                time_left = avg_time_took * stocks_left
                print(str(stocks_left) + " stocks left to save")
                print(str(time_left) + " seconds left to finish whole request")
                print("---------------------------------------------------")

    def _initialize_buysell_data(self, code, market, start):
        global TR_REQ_TIME_INTERVAL

        kiwoom = self.kiwoom
        name = kiwoom.get_master_code_name(code)
        time.sleep(TR_REQ_TIME_INTERVAL)
        print(code + ": " + name + " buysell data initializing")
        kiwoom.prepare_data()
        print("update data dict created")

        for buysell in [1, 2]:
            if buysell == 1:
                kiwoom.set_buysell_state("buy")
            elif buysell == 2:
                kiwoom.set_buysell_state("sell")

            # opt10059 TR 요청
            kiwoom.set_input_value("일자", time.strftime('%Y%m%d'))
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
                if current_date <= int(start):
                    print("loop breaking b/c " + str(current_date) + " lower than " + str(start))
                    break
                time.sleep(TR_REQ_TIME_INTERVAL)
            if buysell == 1:
                print("BUY data saved, ready for DB")
            elif buysell == 2:
                print("SELL data saved, ready for DB")

        length = kiwoom.data.shape[0]
        code_list = [code]*length
        name_list = [name]*length
        kiwoom.data['code'] = code_list
        kiwoom.data['name'] = name_list
        cols = Labels = ["date", "code", "name","close_price", "individual", "foreign_retail", "institution", "financial", "insurance", "trust",
                        "etc_finance", "bank", "pension", "private", "nation", "etc_corporate", "foreign", "buysell"]
        kiwoom.data = kiwoom.data[cols]
        path= ".\\data\\stock\\" + market + "-buysell\\"
        file_name = code + ".csv"
        kiwoom.data.to_csv(os.path.join(path,file_name))
        print(code + ": " + name + " buysell data successfully saved")

    def update_buysell(self):
        pass
