from flask import Blueprint, render_template, current_app, request, redirect, url_for
import json
import os

views = Blueprint('views', __name__)

# Define the root route (the home page)
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/NDHUTicket', methods=['GET', 'POST'])
def NDHU_ticket():
    if request.method == 'POST':
        user_info = {
        'username': request.form.get('username'), 
        'password': request.form.get('password'), 
        'rentType': request.form.get('rentType'), 
        'court': request.form.get('court'), 
        'timeSelection': request.form.get('timeSelection'),
        'customTime': request.form.get('customTime')}

        print(user_info)
        return redirect(url_for('views.NDHU_ticket'))

    return render_template("NDHUTicket.html")

@views.route('/THSRTicket', methods=['GET'])
def THSR_ticket():
    return render_template("home.html")
