# -*- coding: utf-8 -*-

import os
from app import app
from flask import Flask, render_template, flash, redirect, url_for
from app.forms import AddForm
from app import db

@app.route('/')
def index():
    return render_template("index.html", title='Тестовое задание / Python Infrastructure ZiMAD')

def _upload_image(file):
    upload_errors = {}

    MAX_FILE_SIZE = 10 * 1024 * 1024 + 1
    VALID_FILES = ('jpg', 'jpeg', 'png')

    filename = file.filename
    file_extension = filename.split('.', -1)[-1].lower()

    file_bytes = file.read(MAX_FILE_SIZE)
    upload_errors["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
    upload_errors["file_extension_error"] = not file_extension in VALID_FILES 
    
    if not upload_errors['file_size_error'] and not upload_errors['file_extension_error']:
        with open(f"{os.getcwd()}/app/uploads/{filename}", 'wb') as new_file:
            new_file.write(file_bytes)
        # file.save(f"{os.getcwd()}/app/uploads/{file.filename}")

    return upload_errors

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddForm()
    
    if form.validate_on_submit():
        surname = form.surname.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        file = form.file.data
        
        upload_errors = _upload_image(file)
        
        if upload_errors["file_size_error"]:
            flash(f'Ошибка. Размер файла превышает 10МБ !')
            return render_template('add.html', title='Добавление пользователя', form=form)

        if upload_errors["file_extension_error"]:
            flash(f'Ошибка. Расширение файла не соответствует: .jpg, .jpeg, .png')
            return render_template('add.html', title='Добавление пользователя', form=form)

        user = {
            "surname": surname,
            "first_name": first_name,
            "last_name": last_name,
        }
        try:
            db.insert(user)
        except:
            flash(f'Пользователь не создан. Произошла ошибка в базе данных.')
            return render_template('add.html', title='Добавление пользователя', form=form)

        flash(f'Добавлен пользователь: "{surname} {first_name} {last_name}"')
        return redirect(url_for('index'))

    return render_template('add.html', title='Добавление пользователя', form=form)