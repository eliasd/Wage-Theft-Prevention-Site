#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.api import users
import logging
from datastore_obj import User
from time_calc_funct import time_calc

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('main.html')

        #
        user = users.get_current_user()
        if user:
            greet = ('Welcome, %s! (<a href="%s">sign out</a>)') % (user.nickname(), users.create_logout_url('/'))
        else:
            greet = ('<a href="%s">Sign in or register</a>.' ) % (users.create_login_url('/finlog'))

        greetingdict = {'greeting':greet}
        self.response.write(main_template.render(greetingdict))

class FinancialLogHandler(webapp2.RequestHandler):
    def get(self):
        f_template = env.get_template('finlog.html')

        # Generating Signout Link
        user=users.get_current_user()
        signout_greeting = ('%s (<a href="%s">Log Out</a>)') % (user.nickname(), users.create_logout_url('/'))

        # Financial Log Dictionary
        financial_log_dict = {'signout':signout_greeting}

        self.response.write(f_template.render(financial_log_dict))

    def post1(self):
        f_template = env.get_template('finlog.html')

        # Generating Signout Link
        user=users.get_current_user()
        signout_greeting = ('%s (<a href="%s">Log Out</a>)') % (user.nickname(), users.create_logout_url('/'))

        #Request the Wage Variables
        clock_in_hour = int(self.request.get('time_in_hour'))
        clock_in_min = int(self.request.get('time_in_min'))
        time_of_day_in = (self.request.get('time_of_day_in'))

        clock_out_hour = int(self.request.get('time_out_hour'))
        clock_out_min = int(self.request.get('time_out_min'))
        time_of_day_out = (self.request.get('time_of_day_out'))

        break_time_length = int(self.request.get('break_time_length'))
        marital_status = int(self.request.get('marital_status'))
        userID = user.user_id()

        #Total Time Worked:
        time_worked = time_calc(clock_in_hour,clock_out_hour,clock_in_min,clock_out_min,time_of_day_in,time_of_day_out)

        total_tax = 0
        if marital_status == 2:
            total_tax = 6.20 + 1.45 + 0.90
        else:
            total_tax = 6.20 + 1.45 + 0.90 + 1.315

        # Check if user is in database: if not create datastore element; otherwise simply modify
        query_result = User.query(User.user_id==userID).get()
        if query_result and query_result.user_id == userID:
            query_result.time_worked = query_result.time_worked + time_worked
            query_result.put()
        else:
            (User(user_id=userID,time_worked=time_worked,marital_status=marital_status,total_california_tax=total_tax)).put()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/finlog',FinancialLogHandler)
], debug=True)
