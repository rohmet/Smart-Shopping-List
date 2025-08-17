from flask import Flask, render_template, Blueprint

route = Blueprint( 'route',__name__)

@route.route('/')
def home():
    return render_template('index.html')
