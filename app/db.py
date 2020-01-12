from pymongo import MongoClient

client = MongoClient(host='localhost', port=27017)
db = client['test_task']

def insert(user):
    try:
        users = db.users
        users.insert_one(user)
    except Exception as e:
        raise
    else:
        print(f"DB: {user} succesfully inserted.")