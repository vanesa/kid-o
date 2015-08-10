""" Kid-O  Child class"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Child, connect_to_db, db
import datetime
import time


class ChildView:

    def __init__(self, child):
        self.temp = 1
        # print "This should be a child profile:", child
        self.pic_url = child.child_pic_url
        # self....
        print "This should be a birthdate", child.birth_date
        # self.age = time.strptime(child.birth_date, "%Y-%m-%d %I:%M:%S")
        self.age = (child.birth_date)

        print "This should be an age:", self.age

    def  getage():

        age = 57

        return "Age: ", age