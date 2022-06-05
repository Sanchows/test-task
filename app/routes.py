# -*- coding: utf-8 -*-

import os
import api

from app import app
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import AddForm
from app import db

import cv2

from celery import Celery

celery = Celery(broker='redis://redis:6379', backend='redis://redis:6379')

@app.route('/')
def index():
    users = db.find()

    TOTAL_USERS = len(users) # всего пользователей в бд
    TOTAL_ON_PAGE = 5 # количество юзеров на одной странице
    request_page = request.args.get('page') # запрос на вывод номера страницы
    DEFAULT_PAGE = 1 # по дефолту первая страница

    if request_page:
        try:
            page = int(request_page)
        except:
            page = DEFAULT_PAGE
    else:
        page = DEFAULT_PAGE

    pages = [1] + [i+2 for i in range((TOTAL_USERS-1)//TOTAL_ON_PAGE)] # список номеров страниц
    if not page in pages:
        page = DEFAULT_PAGE

    return render_template(
        "index.html",
        current_page=page,
        pages=pages,
        TOTAL_ON_PAGE=TOTAL_ON_PAGE,
        users=users[(page-1)*TOTAL_ON_PAGE:((page-1)*TOTAL_ON_PAGE)+TOTAL_ON_PAGE], # срез юзеров, в зависимости от страницы
        title='Тестовое задание'
    )

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validation_image(file):
    errors = {}
    file_data = {}

    MAX_FILE_SIZE = 10 * 1024 * 1024 + 1

    filename = file.filename.split('.', -1)[0]
    file_extension = file.filename.split('.', -1)[-1].lower()

    file_bytes = file.read(MAX_FILE_SIZE)
    errors["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
    errors["file_extension_error"] = not allowed_file(file.filename) 
    
    if not errors['file_size_error'] and not errors['file_extension_error']:
        # file.save(f"{os.getcwd()}/app/static/upload_images/{file.filename}")
        file_data = {
            'filename': filename,
            'file_extension': file_extension,
            'path': '',
            'path_resized': '',
            'file_bytes': file_bytes,
        }

    return errors, file_data


@celery.task(name='image.Downscale')
def save_resized_image(filename):
    image = cv2.imread(f"{os.getcwd()}/app/static/upload_images/{filename}", cv2.IMREAD_UNCHANGED)
    width = image.shape[1] # ширина 529
    height = image.shape[0] # высота 303

    ALLOW_WIDTH = 200
    ALLOW_HEIGHT = 200

    if width > ALLOW_WIDTH:
        excess = width - ALLOW_WIDTH
        excess_percent = excess * 100 / width
        width = ALLOW_WIDTH

        height = height - int(height * excess_percent/100)
    
    if height > ALLOW_HEIGHT:
        excess = height - ALLOW_HEIGHT
        excess_percent = excess * 100 / height
        height = ALLOW_HEIGHT

        width = width - int(width * excess_percent / 100)

    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    abs_path_to_resized = f"{os.getcwd()}/app/static/resized_images/{filename}"
    
    cv2.imwrite(abs_path_to_resized, resized)


def save_file(user_id, file):
    path_to_file = f"{os.getcwd()}/app/static/upload_images/{user_id}.{file['file_extension']}"
    
    with open(path_to_file, 'wb') as new_file:
        new_file.write(file['file_bytes'])

    filename_resized = f"{user_id}.{file['file_extension']}"
    task = save_resized_image.delay(f"{user_id}.{file['file_extension']}")
    path_to_resized_image = f"static/resized_images/{filename_resized}"

    db.update_path_to_image(user_id, 
        f"static/upload_images/{user_id}.{file['file_extension']}",
        path_to_resized_image,
    )

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddForm()
    
    if form.validate_on_submit():
        
        surname = form.surname.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        file = form.file.data
        
        file_errors, file_data = validation_image(file)
        
        if True in file_errors.values():
            if file_errors["file_size_error"]:
                flash(f'Ошибка. Размер файла превышает 10МБ !')            
            if file_errors["file_extension_error"]:
                flash(f'Ошибка. Расширение файла не соответствует: .jpg, .jpeg, .png')
            return render_template('add.html', title='Добавление пользователя', form=form)

        user = {
            "surname": surname,
            "first_name": first_name,
            "last_name": last_name,
            "photo": file_data
        }
        
        try:
            user_id = db.insert({
                    "surname": surname,
                    "first_name": first_name,
                    "last_name": last_name,
                    "photo": {
                        'filename': file_data['filename'],
                        'file_extension': file_data['file_extension'],
                        'path': file_data['path'],
                        'path_resized': file_data['path_resized'],
                    }
                } 
            )
        except:
            flash(f'Пользователь не создан. Произошла ошибка в базе данных.')
            return render_template('add.html', title='Добавление пользователя', form=form)
        
        save_file(user_id, user['photo'])

        flash(f'Добавлен пользователь: "{surname} {first_name} {last_name}"')
        return redirect(url_for('index'))

    return render_template('add.html', title='Добавление пользователя', form=form)