# test-task

## Screenshots
`http://127.0.0.1/`:
![](https://sun9-32.userapi.com/c855536/v855536779/1d494e/fdpWw1MLkcQ.jpg "screenshot http://127.0.0.1/")

`http://127.0.0.1/?page=2`:
![](https://sun9-67.userapi.com/c855536/v855536779/1d4944/N2XjYHqY5eU.jpg "screenshot http://127.0.0.1/?page=2")

`http://127.0.0.1/add`:
![](https://sun9-4.userapi.com/c855536/v855536779/1d493a/be5LIObQ9_s.jpg "screenshot http://127.0.0.1/add")

## Setup
1. Clone the repository: `$ git clone https://github.com/Sanchows/test-task.git`
2. `$ cd test-task/`
3. Create a virtual environment: `$ python3 -m virtualenv env`
4. Activate a virtual environment: `$ source env/bin/activate`
5. `$ pip install -r requirements.txt`
6. Download redis:`$ sudo apt update && sudo apt install redis-server`
7. Set the "systemd" value of the "supervised" parameter in the /etc/redis/redis.conf (for Ubuntu 18.04): `$ sudo nano /etc/redis/redis.conf`
8. Restart redis.service: `$ sudo systemctl restart redis.service`
9. Add environment variable: `$ export FLASK_APP=my_app.py`
10. Run Celery: `$ celery -A app.routes.celery worker --loglevel=info`
11. New terminal `Ctrl+Shift+T`
12. Run a web-app: `$ flask run`

The application will be available on http://127.0.0.1:5000/

## REST API
Выборка всех пользователей: `http://127.0.0.1:5000/api/users`
Выборка одного пользователя по его id: `http://127.0.0.1:5000/api/user/id`