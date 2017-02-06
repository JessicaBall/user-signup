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
import cgi
import re

#main handler HTML boilerplate
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""

#mainhandler build page
params = dict(username = "", email = "", error_username = "", error_password = "", error_verify = "", error_email = "")

def build_page(self, params):
    uname_label = "<label for='username'>Username</label>"
    uname_input = "<input name='username' type='text' value='{0}'>".format(params.get('username'))
    uname_error = "<label for='username' class='error'>{0}</label>".format(params.get('error_username'))

    pwd_label = "<label for='password'>Password</label>"
    pwd_input = "<input name='password' type='password' value=''>"
    pwd_error = "<label for='password' class='error'>{0}</label>".format(params.get('error_password'))

    vfypwd_label = "<label for='verify'>Verify</label>"
    vfypwd_input = "<input name= 'verify' type='password' value=''>"
    vfypwd_error = "<label for='verify' class='error'>{0}</label>".format(params.get('error_verify'))

    email_label = "<label for='email'>Email (optional)</label>"
    email_input = "<input name='email' type='email' value='{0}'>".format(params.get('email'))
    email_error = "<label for='email' class='error'>{0}</label>".format(params.get('error_email'))

    submit = "<input type='submit'/>"

    form = ("<form method='post'>" + uname_label + uname_input + uname_error + '<br>'
     + pwd_label + pwd_input + pwd_error + '<br>' + vfypwd_label + vfypwd_input + vfypwd_error + '<br>'
     + email_label + email_input + email_error + '<br>' + submit + "</form>")

    header  = "<h2>Signup</h2>"

    return page_header + header + form + page_footer

#welcome handler build page
def build_welcomepage(content):
    welcome_page_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
    </head>
    <body>
    """

    welcome_page_footer = """
    </body>
    </html>
    """
    return welcome_page_header + content + welcome_page_footer

#global escape function
def escapeHtml(input):
    return cgi.escape(input, quote=True)

#regular expresions
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile (r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

#signup mainhandler
class MainHandler(webapp2.RequestHandler):
    def get(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        username = ""
        email = ""

        content = build_page("",params)
        self.response.write(content)

    def post(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        username = ""
        email = ""


        is_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params['username'] = username
        params['email'] = email

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            is_error = True

        if not valid_password(password):
            params['error_password'] = "That isn't a valid password."
            is_error = True

        elif password != verify:
            params['error_verify'] = "Those passwords don't match."
            is_error = True

        if not valid_email(email):
            params['error_email'] = "Please enter a valid e-mail."
            is_error = True

        if not is_error:
            username_welcome = username
            self.redirect("/welcome?username={0}".format(username_welcome))
        else:
            content = build_page("",params)
            self.response.write(content)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username_welcome = self.request.get("username")
        escaped_username = escapeHtml(username_welcome)

        content = """
                <h1>
                    Welcome, """ + escaped_username + """!
                </h1>
            """

        self.response.write(build_welcomepage(content))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler),
], debug=True)
