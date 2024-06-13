from flask import Blueprint, render_template, current_app, url_for, flash, request, redirect
import json
import os
from .utility.ndhu_submit import submit_reservation

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
        'date': request.form.get('date').replace("-", "/"), 
        'timeSelection': request.form.get('timeSelection'),
        'customTime': request.form.get('customTime')}

        state = submit_reservation({
            "username":user_info['username'], "password":user_info['password']}, 
            user_info['rentType'], 
            user_info['court'], 
            user_info['date'], 
            user_info['timeSelection'], 
            user_info['customTime'])
        
        if state == True:
            flash('成功：登記場地已經完成！', 'success')
        else:
            flash('錯誤：有地方出錯喔...', 'danger') 

        return redirect(url_for('views.NDHU_ticket'))

    return render_template("NDHUTicket.html")

@views.route('/THSRTicket', methods=['GET', 'POST'])
def THSR_ticket():
    if request.method == 'POST':
        user_info = {
        'ID': request.form.get('ID'), 
        'startStation': request.form.get('startStation'), 
        'destinationStation': request.form.get('destinationStation'),
        'typesofticket': request.form.get('typesofticket'), 
        'typesofCar': request.form.get('typesofCar'),
        'date': request.form.get('date').replace("-", "/"),
        'time': request.form.get('time'),
        'fare': {
            "fullFare": request.form.get('fullFare'), 
            "halfFare": request.form.get('halfFare'),
            "disabledFare": request.form.get('disabledFare'),
            "seniorFare": request.form.get('seniorFare'),
            "studentFare": request.form.get('studentFare'),
            },
        'ticketTypeSelection': request.form.get('ticketTypeSelection'),
        'customTicket': request.form.get('customTicket'),
        }

        print(user_info)
        return redirect(url_for('views.THSR_ticket'))

    return render_template("THSRTicket.html")
