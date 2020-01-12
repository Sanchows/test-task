# -*- coding: utf-8 -*-

from app import app

from flask import Flask, render_template, flash, redirect, url_for

from app.forms import AddForm

@app.route('/')
def index():
    return render_template("index.html", title='Тестовое задание / Python Infrastructure ZiMAD')


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddForm()
    
    if form.validate_on_submit():
        surname = form.surname.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        flash(f'Добавлен пользователь: "{surname} {first_name} {last_name}"')

        return redirect(url_for('index'))

    return render_template('add.html', title='Добавление пользователя', form=form)