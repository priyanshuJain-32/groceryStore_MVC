from flask import Blueprint, render_template, request, redirect, url_for, flash
# from ./instance import database.sqlite3 as db
# import sys, os
# path = os.path.abspath("instance")
# sys.path.append(path)
# import database as db

from . import db
from .models import Users
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():

	if request.method == 'GET':
		return render_template('login.html')

	user_name_ = request.form.get('user_name')
	password_ = request.form.get('password')

	user = Users.query.filter_by(user_name=user_name_).first()
	# Condition checks if the user_name and password are there in database.
	
	if ((not user) or (not (password_==user.password))):
		flash('Incorrect login details. Please try again.')
		return redirect(url_for('auth.login'))
	
	login_user(user)
	return redirect(url_for('main.product_page'))


@auth.route('/admin_login', methods=['GET','POST'])
def admin_login():
	if request.method == 'GET':
		return render_template('admin_login.html')

	user_name_ = request.form.get('user_name')
	password_ = request.form.get('password')

	user = Users.query.filter_by(user_name=user_name_).first()
	# Condition checks if the user_name and password are there in database.
	
	if ((not user) or (not (password_==user.password))):
		flash('Incorrect login details. Please try again.')
		return redirect(url_for('auth.admin_login'))

	if user.role != 'admin':
		flash('You are not an Admin. Please login as a User.')
		return redirect(url_for('auth.login'))
	
	login_user(user)
	return redirect(url_for('main.list_category'))


@auth.route('/signup', methods=['GET','POST'])
def signup():
	
	# If the signup page is requested then render the signup page
	if request.method=='GET':
		return render_template('signup.html')
	
	# Else take the input from the signup page and save them into variables
	name_ = request.form.get('first_name')
	user_name_ = request.form.get('user_name')
	password_ = request.form.get('password')
	repeat_password_ = request.form.get('repeat_password')

	# If a user with same user_name already exists render the signup page again with a flash message
	user = Users.query.filter_by(user_name = user_name_).first()
	
	if user:
		flash('User name already exists, Please try again.')
		return redirect(url_for('auth.signup'))

	if password_!=repeat_password_:
		flash('Password did not match the repeated password. Please try again.')
		return redirect(url_for('auth.signup'))

	# Create the new_user and commit to the database

	new_user = Users(name=name_, user_name=user_name_, password=password_, role="user")
	db.session.add(new_user)
	db.session.commit()
	flash('Signup is successful. Proceed to login')
	return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
	# return 'Logout'
	logout_user()
	return redirect(url_for('main.home'))