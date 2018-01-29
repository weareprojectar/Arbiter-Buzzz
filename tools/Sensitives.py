## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/12
## @Details 장고 서버를 실행하기 위한 sensitives.pickle 파일 핸들링

import os, pickle


class Sensitives(object):
    def __init__(self, start_path):
        self.start_path = start_path
        self.sensitives = {'SECRET_KEY': '',
                           'IP_ADDRESS': '',
                           'DB_NAME': '',
                           'DB_USER': '',
                           'DB_PW': '',
                           'DEBUG': '',
                           'APP_STATUS': ''}
        self.data = None

    def setup(self):
        pickle_file = self.start_path + '/sensitives.pickle'
        if os.path.exists(pickle_file):
            print('Sensitives.pickle file already exists, edit each values through "set"')
        else:
            self.sensitives['SECRET_KEY'] = input('SECRET_KEY: ')
            self.sensitives['IP_ADDRESS'] = input('IP_ADDRESS: ')
            self.sensitives['DB_NAME'] = input('DB_NAME: ')
            self.sensitives['DB_USER'] = input('DB_USER: ')
            self.sensitives['DB_PW'] = input('DB_PW: ')
            self.sensitives['DEBUG'] = bool(input('DEBUG (True/False): '))
            self.sensitives['APP_STATUS'] = input('APP_STATUS (dev/prod): ')
            self.save(True)

    def open(self):
        pickle_file = open(self.start_path + '/sensitives.pickle', 'rb')
        self.data = pickle.load(pickle_file)
        print('Data loaded')

    def check(self):
        if self.data == None:
            self.open()
        for key, val in self.data.items():
            if type(val) == bool:
                val = str(val)
            print(key + ': ' + val)

    def set(self, key, val):
        if self.data == None:
            self.open()
        if key == 'DEBUG':
            self.data[key] = bool(int(val))
        else:
            self.data[key] = str(val)
        print('Successfully set ' + key + ' as ' + str(val))

    def save(self, initial=False):
        pickle_file = open(self.start_path + '/sensitives.pickle', 'wb')
        if initial:
            pickle.dump(self.sensitives, pickle_file)
        else:
            pickle.dump(self.data, pickle_file)
        print('Data saved')
