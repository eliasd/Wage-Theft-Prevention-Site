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

    def post(self):
        f_template = env.get_template('finlog.html')

        # Generating Signout Link
        user=users.get_current_user()
        signout_greeting = ('%s (<a href="%s">Log Out</a>)') % (user.nickname(), users.create_logout_url('/'))

        #Request the Wage Variables
        clock_in_hour = self.request.get('time_in_hour')
        clock_in_minute = self.request.get('time_in_min')
        clock_out_hour = self.request.get('time_out_hour')
        clock_out_min = self.request.get('time_out_min')
        break_time_length = self.request.get('break_time_length')
        marital_status = int(self.request.get('marital_status'))





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/finlog',FinancialLogHandler)
], debug=True)
