import sys

path = '/home/wyounas/punjab-school-census-analysis/school-census-web/schoolCensus'
if path not in sys.path:
   sys.path.append(path)

from autoapp import app as application