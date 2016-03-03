#!/usr/bin/env python
import os
import sys

try:
  virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
  python_version = "python"+str(sys.version_info[0])+"."+str(sys.version_info[1]) 
  os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib', python_version, 'site-packages')
  virtualenv = os.path.join(virtenv, 'bin','activate_this.py')
  if(sys.version_info[0] < 3):
    execfile(virtualenv, dict(__file__=virtualenv))
  else:
    exec(open(virtualenv).read(), dict(__file__=virtualenv))
    
except IOError:
  pass


#  main():
from telegrambot.bot import Bot
bot = Bot()
bot.start_webhook_server()
