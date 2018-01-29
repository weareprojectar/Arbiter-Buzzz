## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/17
## @Details tools의 프로세스를 트래킹하는 유틸리티 함수 모음

import time

def timeit(method):
    """decorator for timing processes"""
    def timed(*args, **kwargs):
        ts = time.time()
        method(*args, **kwargs)
        te = time.time()
        print("Process took " + str(te-ts) + " seconds")
    return timed
