# penpal

### Installation
```shell
virtualenv venv
source venv/bin/activate
pip install requirements.txt
cp penpal/.env.example penpal/.env
python manage.py runserver
```

### Create Postgres Database
```shell
sudo -u postgres psql
```
```sql
create database mydb;
create user myuser with encrypted password 'mypass';
grant all privileges on database mydb to myuser;
```