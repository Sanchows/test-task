from pymongo import MongoClient

client = MongoClient(host='mongo', port=27017)
db = client['test_task']

def insert(user):
    try:
        users = db.users
        users.insert_one(user)
    except Exception as e:
        raise
    else:
        return user['_id']

def find():
    try:
        users = db.users
        result = users.find()

    except Exception as e:
        raise
    else:
        return list(result)

def find_by_id(user_id):
    try:
        users = db.users
        user = users.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise
    else:
        return user


def update_path_to_image(user_id, path, path_resized):
    try:
        db.users.update_one({"_id": user_id}, {"$set": {"photo.path": path}})
        db.users.update_one({"_id": user_id}, {"$set": {"photo.path_resized": path_resized}})
    except:
        raise
    else:
        pass