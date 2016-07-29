import sys, os
sys.path.insert (0,'/var/www/zippy-gig')
os.chdir("/var/www/zippy-gig")
from zippy_gig import app as application
