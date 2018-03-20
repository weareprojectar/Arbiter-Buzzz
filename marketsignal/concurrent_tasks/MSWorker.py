from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
import os, time
import pandas as pd
import numpy as np

from marketsignal.concurrent_tasks.Processor import Processor
from marketsignal.concurrent_tasks.Indexer import Indexer
from marketsignal.concurrent_tasks.Scorer import Scorer
from marketsignal.concurrent_tasks.MSHomeProcessor import MSHomeProcessor

DATA_PATH = os.getcwd() + '/tmp'
CLOSE_PATH = os.getcwd() + '/data/close'
VOLUME_PATH = os.getcwd() + '/data/volume'


class MSWorker:

    def __init__(self):
        print('Initializing Marketsignal Worker')

    def step_one(self):
        p = Processor() # before any updates from keystone, calculate 4 years indexes
        print('Making data for OHLCV: base data')
        p.make_base_data()

    def step_two(self):
        i = Indexer()
        i.size_type_of_stock()
        i.style_type_of_stock()
        i.calc_size_index()
        i.calc_style_index()
        i.calc_industry_index()

    def step_three(self):
        p = Processor()
        print('Making data for Index: index data')
        p.make_index_data()

    def step_four(self):
        for task_name in ['index']:
            s = Scorer(task_name)
            s.save_mom_volt_cor_vol()
            s.calculate_score_ratings()

    def step_five(self):
        ms = MSHomeProcessor()
        ms.save_data()
        ms.make_rank_data()
