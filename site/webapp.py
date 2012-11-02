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

app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')
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
                  sender = "ono@tacticaltech.org",
                  recipients = request.args.get('email'))
    msg.body = """
    Hello %s from %s,
    
I need your help. I know you are worried about your digital security, so am I. And frankly, I'm also worried about mine. I have been remembering things lately from my previous robotic life, gruesomely effective surveillance techniques and advanced digital attacks. I need to put the pieces back together, to help people who are potentially at risk. To do that I need access to certain websites. But I've noticed that many of these sites are blocked in my country, Secure-a-lot. Can you help me to get the right information and learn somethings about safe and secure digital communications along the way?

Let's first steps to setup a secure chat account so we can talk more comfortably. Please go to register.jabber.org and register an account there. Now install Adium (Mac), Pidgin (Windows https://securityinabox.org/en/pidgin_securechat 3.1 ), Empathy (linux), login to your Jabber account, add me (username Ono) as a friend and shoot me a message.""" % (request.args.get('ip',request.remote_addr), geoipdb.country_code_by_addr(request.args.get('ip',request.remote_addr)) or '')
    mail.send(msg)
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           )
