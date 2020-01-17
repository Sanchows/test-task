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
        return user['_id']

def find():
    try:
        users = db.users
        a = users.find()
    except Exception as e:
        raise
    else:
        return list(a)

def update_path_to_image(user_id, path):
    try:
        print(dir(db.users))
        db.users.update_one({"_id": user_id}, {"set": {"photo.path": path}})
    except:
        raise
    else:
        pass