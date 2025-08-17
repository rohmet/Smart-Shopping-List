from flask import Flask, render_template, Blueprint, request
from app.services import shopping_category_recommendation

route = Blueprint( 'route',__name__)

@route.route('/', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        user_input = request.form['shopping_list']
        recommendations = shopping_category_recommendation(user_input)
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html')