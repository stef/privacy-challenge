#!/root/env/bin/python
import sys
sys.path.insert(0, "/home/sal/env")
sys.path.insert(0, "/home/sal/corp.gov")

activate_this = '/home/sal/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from webapp import app as application
#application.run(debug=True)
