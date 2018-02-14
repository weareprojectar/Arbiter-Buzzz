# Root user Setting
echo -e "makeitpopweAR!1\nmakeitpopweAR!1" | passwd root

# Arbiter User Setting
adduser arbiter
usermod -aG sudo arbiter
groups arbiter

# Firewall Setting
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
sudo ufw allow 8000

# Download PostgreSQL & setting
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

# DB SETTING
su -c "psql -c \"CREATE DATABASE arbiter;\"" postgres
su -c "psql -c \"CREATE USER arbiter WITH PASSWORD 'makeitpopweAR!1';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET client_encoding TO 'utf8';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET default_transaction_isolation TO 'read committed';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET timezone TO 'UTC';\"" postgres
su -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE arbiter TO arbiter;\"" postgres
su -c "psql -c \"\du\"" postgres

### PostgreSQL localhost setting
cd /etc/postgresql/9.5/main
vim +":%s/#listen_addresses = 'localhost'/#listen_addresses = '*'/g | wq" postgresql.conf

cd /etc/postgresql/9.5/main
vim +"%s/127.0.0.1\/32/0.0.0.0\/0   /g | %s/::1\/128/::\/0/g | wq" pg_hba.conf

echo one
sudo systemctl start postgresql.service
echo two
sudo systemctl enable postgresql.service
echo three
sudo systemctl status postgresql.service
echo four
sudo systemctl restart postgresql.service
echo done!

# clone arbiter datas for configure
rm -r /home/arbiter
mkdir /home/arbiter
cd /home/arbiter
git clone https://github.com/weareprojectar/Arbiter-Buzzz.git .
cd ~

export LC_ALL=C
sudo apt-get install python3-pip
echo pip3 install.....
sudo -H pip3 install --upgrade pip

echo setuptools install......
sudo pip3 install setuptools

echo install virtualenv and virtualenvwrapper........
sudo -H pip3 install virtualenv virtualenvwrapper


cd ~
mkdir ~/.virtuanenvs
echo "export WORKON_HOME=~/home/venv" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo execute next program! you must reboot!
reboot


