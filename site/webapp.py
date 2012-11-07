#!/usr/bin/env python

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

from flask import Flask, request, render_template
from flask_mail import Mail, Message
from common import cfg
from pygeoip import GeoIP
import os

basepath=os.path.dirname(os.path.abspath(__file__))
geoipdb = GeoIP('%s/GeoIP.dat' % basepath)
geoipcdb = GeoIP('%s/GeoIPCity.dat' % basepath)

app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')
app.config.update(
	#DEBUG=True,
	MAIL_FAIL_SILENTLY = False,
	#EMAIL SETTINGS
	MAIL_SERVER='localhost',
	MAIL_PORT=8825,
	#MAIL_USE_SSL=True,
	#MAIL_USERNAME = 'you@google.com',
	#MAIL_PASSWORD = 'GooglePasswordHere'
	)
mail = Mail(app)

@app.context_processor
def contex():
    global cfg, query
    return {'cfg'   : cfg
           ,'query' : ''
           ,'path'  : request.path
           }

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'
                           ,vendor=request.user_agent.platform
                           ,ip=request.args.get('ip',request.remote_addr)
                           )

@app.route('/signup', methods=['GET'])
def signup():
    msg = Message("save secure-a-lot",
                  sender = "ono@vps598.greenhost.nl",
                  recipients = [request.args.get('email')])
    from=(geoipcdb.record_by_addr(request.args.get('ip',request.remote_addr)) or {}).get('city','')
    if not from:
       from=(geoipdb.country_name_by_addr(request.args.get('ip',request.remote_addr)) or ''))
    msg.body = render_template('welcome.txt',
                               ip=request.args.get('ip',request.remote_addr),
                               country=from)
    mail.send(msg)
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           #,host         = int(cfg.get('server', 'host'))
           )
