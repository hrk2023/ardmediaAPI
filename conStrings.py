import os
from pymongo import MongoClient
try:
    DPASS=os.environ.get('DPASS')
    DUSER=os.environ.get('DUSER')
except:
    print('DATABASE CONNECTION VARIABLES NOT SET')
conn="mongodb+srv://admin:Nydqqzuy1324@cluster0.spqyy.mongodb.net/"
client=MongoClient(conn)
db1=client.adrmedia