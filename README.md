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
3. Run docker containers: `$ docker-compose up -d`

The application will be available on `http://127.0.0.1:8000/`

## API
Выборка всех пользователей: `http://127.0.0.1:8000/api/users`
<br>
Выборка одного пользователя по его id: `http://127.0.0.1:8000/api/user/id`
