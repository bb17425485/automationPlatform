# wsgi setting

#activate_this=r'D:\Envs\acc\Scripts\activate_this.py'

#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0,r"C:\Python\automationPlatform")

from autoFlask import app

application = app