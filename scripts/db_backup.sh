# Backing up Django DB

### 1. BM
su arbiter -c "psql -c \"\copy stockapi_bm (date, name, index, volume, individual, foreigner, institution) to '/home/arbiter/backup/bm.csv' delimiter ',';\""
