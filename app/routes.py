# -*- coding: utf-8 -*-

import os
from app import app
from flask import Flask, render_template, flash, redirect, url_for
from app.forms import AddForm
from app import db

@app.route('/')
def index():
    users = db.find()
    
    return render_template("index.html", users=users, title='Тестовое задание / Python Infrastructure ZiMAD')

def validation_image(file):
    errors = {}
    file_data = {}

    MAX_FILE_SIZE = 10 * 1024 * 1024 + 1
    VALID_FILES = ('jpg', 'jpeg', 'png')

    filename = file.filename.split('.', -1)[0]
    file_extension = file.filename.split('.', -1)[-1].lower()

    file_bytes = file.read(MAX_FILE_SIZE)
    errors["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
    errors["file_extension_error"] = not file_extension in VALID_FILES 
    
    if not errors['file_size_error'] and not errors['file_extension_error']:
        # file.save(f"{os.getcwd()}/app/static/upload_images/{file.filename}")
        file_data = {
            'filename': filename,
            'file_extension': file_extension,
            'path': '',
            'file_bytes': file_bytes,
        }

    return errors, file_data

def save_file(user_id, file):
    with open(f"{os.getcwd()}/app/static/upload_images/{user_id}.{file['file_extension']}", 'wb') as new_file:
        new_file.write(file['file_bytes'])
    
    db.update_path_to_image(user_id, f"static/upload_images/{user_id}.{file['file_extension']}")

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
            user_id = db.insert(user)
        except:
            flash(f'Пользователь не создан. Произошла ошибка в базе данных.')
            return render_template('add.html', title='Добавление пользователя', form=form)
        
        save_file(user_id, user['photo'])

        flash(f'Добавлен пользователь: "{surname} {first_name} {last_name}"')
        return redirect(url_for('index'))

    return render_template('add.html', title='Добавление пользователя', form=form)