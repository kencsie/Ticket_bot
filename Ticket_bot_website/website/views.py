from flask import Blueprint, render_template, current_app, request, redirect, url_for
import json
import os

views = Blueprint('views', __name__)

# Define the root route (the home page)
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/NDHUTicket', methods=['GET'])
def NDHU_ticket():
    return render_template("NDHUTicket.html")

@views.route('/THSRTicket', methods=['GET'])
def THSR_ticket():
    return render_template("home.html")
