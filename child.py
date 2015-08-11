""" Kid-O  Child class"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Child, connect_to_db, db
from datetime import datetime
import time


class ChildView:

    def __init__(self, child):
        self.temp = 1
        # print "This should be a child profile:", child
        self.pic_url = child.pic_url
        self.first_name = child.first_name
        self.last_name = child.last_name
        self.birth_date = child.birth_date
        self.guardian_type = child.guardian_type
        self.guardian_fname = child.guardian_fname
        self.guardian_lname = child.guardian_lname
        self.doctor_appt = child.doctor_appt
        self.situation = child.situation
        self.home_visit = child.home_visit
        self.latitude = child.latitude
        self.longitude = child.longitude

        # self....
        print "This should be a birthdate", child.birth_date
        # import pdb; pdb.set_trace()

        self.currenttime = datetime.now()
        # print type(child.birth_date.strftime("%Y-%m-%d %I:%M:%S"))
        # print type(self.currenttime)
        print "This should be the current time:", self.currenttime
        self.age = self.currenttime - child.birth_date


        self.age = self.age.days / 365
        print "This should be an age:", self.age

        # self.age = (child.birth_date)
     

    def  getage():

        age = 57

        return "Age: ", age
