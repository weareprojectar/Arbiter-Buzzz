source ~/.bashrc

# make virtual environment of python
mkvirtualenv buzzz

# move directory to arbiter 
cd /home/arbiter

python << END
import pickle
file = open('sensitives.pickle','wb')
sen = {'IP_ADDRESS':'45.32.59.138', 'DB_NAME':'arbiter', 'DB_PW':'makeitpopAR!1','DBUG':True,'SECRET_KEY':'tf=&jg*c#l1675$sy0eni!6sr7xz(isd=9#h$q)e+@*tkmdol1'}

pickle.dump(sen, file)
file.close()
END


sudo apt-get install python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
pip install -r requirements.txt


sudo apt-get install supervisor
sudo service supervisor start
systemctl status supervisor
sudo supervisorctl status

cd /etc/supervisor/confd

touch celerybeat.conf
touch celery.conf

sudo apt-get install rabbitmq-server
systemctl status rabbitmq-server
