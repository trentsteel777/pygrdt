# Instructions for running
# Start a django shell (python manage.py shell)
# Run the below command in there to execute this file
# exec(open("./initial_setup/setup_pygrdt").read())


#Source.objects.get_or_create(name="Website")
from analysisportal.models import *

wl = Watchlist()
wl.name = 'DEFAULT'
wl.enabled = True
wl.save()

t = Ticker()
t.ticker = 'AAPL'
t.watchlist = wl
t.save()
