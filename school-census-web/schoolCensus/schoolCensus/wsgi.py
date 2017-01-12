import sys

path = '/home/wyounas/punjab-school-census-analysis/school-census-web/schoolCensus/schoolCensus'
if path not in sys.path:
   sys.path.append(path)

from flask_app import app as application