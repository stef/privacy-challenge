# This file is part of saving-secure-a-lot
#
#  saving-secure-a-lot is free software: you can redistribute it and/or
#  modify it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3 of
#  the License, or (at your option) any later version.
#
#  saving-secure-a-lot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public
#  License along with saving-secure-a-lot If not, see
#  <http://www.gnu.org/licenses/>.
#
# (C) 2012- by Stefan Marsiske, <s@ctrlc.hu>

from flask import Flask, request, render_template, redirect, url_for, make_response, send_from_directory
from flask_mail import Mail, Message
from common import cfg
from forms import RegistrationForm, LoginForm
from lepl.apps.rfc3696 import Email
import os, random, itertools, hmac, hashlib, json
from game import get_val, second, add_state, get_state

basepath=os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')
app.config.update(
	DEBUG=True,
	MAIL_FAIL_SILENTLY = False,
	#EMAIL SETTINGS
	MAIL_SERVER='localhost',
	MAIL_PORT=8825,
	)
mail = Mail(app)

with open('%s/secret' % basepath,'r') as f:
    secret=f.read().strip()

@app.context_processor
def context():
    global cfg, query
    return {'cfg'   : cfg
           ,'query' : ''
           ,'path'  : request.path
           }

@app.route('/')
def index():
  return render_template('base.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.route('/product-sheets/atlas-ctx4.pdf')
def productsheet():
  if request.cookies['login']:
      print 'asdf'
      return send_from_directory(app.static_folder, 'productsheet.pdf')
  return render_template('base.html')

@app.route('/myproducts')
def myproducts():
  if request.cookies['login']:
      prefix = request.url_root.split('/')[2].split('.')[0]
      if prefix == "localhost:5000":
          prefix = "asdf"
      keyid=get_val('corp.cf.zone',":%s" % prefix, second)[:-(len(prefix)+1)]
      rec=json.loads(get_state(keyid, 'corp-userdata') or '')
      return render_template('myproducts.html', serno=rec['serno'])
  return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        prefix = request.url_root.split('/')[2].split('.')[0]
        if prefix == "localhost:5000":
            prefix = "asdf"
        keyid=get_val('corp.cf.zone',":%s" % prefix, second)[:-(len(prefix)+1)]
        rec=json.loads(get_state(keyid, 'corp-userdata') or '')
        if(form.email.data==rec['email'] and form.password.data==rec['password']): # fuck yeah plaintext passwords ftw!
            add_state(keyid, 'corp-login', '')
            response = make_response(redirect('/'))
            response.set_cookie('login', True)
            return response
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.email.data,
        #            form.password.data)
        t1 = Email()
        recp=form.email.data
        if t1(recp):
            prefix = request.url_root.split('/')[2].split('.')[0]
            if prefix == "localhost:5000":
                prefix = "asdf"
            keyid=get_val('corp.cf.zone',":%s" % prefix, second)[:-(len(prefix)+1)]
            add_state(keyid, 'corp-userdata', json.dumps({'name':form.name.data,
                                                          'email':form.email.data,
                                                          'country':form.country.data,
                                                          'address':form.address.data,
                                                          'company':form.company.data,
                                                          'dept':form.dept.data,
                                                          'pos':form.pos.data,
                                                          'serno':form.serno.data,
                                                          'password':form.password.data,
                                                          }))
            #flash("Thanks for registering, you will receive further instruction at %s." % recp)
            msg = Message("registration successful, welcome at Corporation.",
                          sender = "donotreply@corporation.cf",
                          recipients = [recp])
            msg.body = render_template('welcome.txt', name=form.name.data, host=request.url_root.split('/')[2])
            mail.send(msg)
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           #,host         = int(cfg.get('server', 'host'))
           )
