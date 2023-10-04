from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app, db
from app.models import User, Wine

jwt = JWTManager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return render_template('login.html')

@app.route('/wines', methods=['GET'])
@jwt_required()
def list_wines():
    wines = Wine.query.all()
    return render_template('wines.html', wines=wines)

@app.route('/wines/add', methods=['GET', 'POST'])
@jwt_required()
def add_wine():
    if request.method == 'POST':
        flash('Wine added successfully')
        return redirect(url_for('list_wines'))
    return render_template('add_wine.html')

@app.route('/wines/delete/<int:wine_id>', methods=['POST'])
@jwt_required()
def delete_wine(wine_id):
    flash('Wine deleted successfully')
    return redirect(url_for('list_wines'))

@app.route('/wines/<int:wine_id>', methods=['GET'])
@jwt_required()
def view_wine(wine_id):
    wine = Wine.query.get(wine_id)
    return render_template('wine_details.html', wine=wine)
