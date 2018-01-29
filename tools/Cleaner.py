## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/12
## @Details 파일들을 정리하고 간단한 처리

import os, glob

from arbiter.settings import INSTALLED_APPS


class Cleaner(object):
    def __init__(self, start_path):
        self.start_path = start_path
        self.apps = [app for app in INSTALLED_APPS if 'django' not in app and 'rest_framework' not in app]

    def clean_migrations(self):
        for app in self.apps:
            os.chdir(self.start_path + '/' + app + '/migrations/')
            print(os.getcwd())
            mig_f = glob.glob('0*')
            for f in mig_f:
                print(f + ' deleted')
                os.remove(f)
