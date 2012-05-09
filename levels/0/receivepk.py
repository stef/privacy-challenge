#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    This file is part of parltrack

#    parltrack is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    parltrack is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with parltrack  If not, see <http://www.gnu.org/licenses/>.

# (C) 2012 by Stefan Marsiske, <stefan.marsiske@gmail.com>

from email.parser import Parser
from email.utils import collapse_rfc2231_value
import pgpdump, base64, sys, re

sendere=re.compile(r'(.*) {1,}<(\S*@\S*)>')

msg=Parser().parse(sys.stdin)
sender=collapse_rfc2231_value(msg.get('from'))
m=sendere.match(sender)
if m:
    print m.groups()

for part in msg.walk():
    print part.get_content_type()
    if part.get_content_type()=='text/plain':
        res=[]
        # cut of preamble
        inblock=False
        lines=part.get_payload().split('\n')
        i=0
        while i<len(lines):
            if not inblock:
                if lines[i].strip()=='-----BEGIN PGP PUBLIC KEY BLOCK-----':
                    inblock=True
                    i+=2
            else:
                if lines[i].strip()=='-----END PGP PUBLIC KEY BLOCK-----':
                    break
                res.append(lines[i])
            i+=1
        data=base64.b64decode(''.join(res))
        pgp_data=pgpdump.BinaryData(data)
        packets = list(pgp_data.packets())
        print packets
        # check deadrop for gpgme handling of keys
