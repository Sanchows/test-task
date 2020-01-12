# -*- coding: utf-8 -*-

from app import app

from flask import Flask, render_template

@app.route('/')
def index():
    return render_template("index.html", title='Тестовое задание / Python Infrastructure ZiMAD')