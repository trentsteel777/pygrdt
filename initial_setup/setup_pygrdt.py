# Instructions for running
#cd ~/venvs/pygrdt
#source bin/activate
#./manage.py shell < ~/venvs/pygrdt/initial_setup/setup_pygrdt.py

from analysisportal.models import *

wl = Watchlist()
wl.name = 'DEFAULT'
wl.enabled = True
wl.save()

tickersList = ['AAPL', 'ABBV', 'ABC', 'ABCO', 'ABG', 'AEE', 'AFG', 'AGX', 'AJG', 'ALE', 'ALGT', 'ALK', 'ALL', 'AMG', 'AMGN', 'AMP', 'AMSF', 'AMWD', 'ANTM', 'APD', 'APOG', 'ARCH', 'ARW', 'ASTE', 'ATO', 'AVY', 'AXP', 'AYI', 'AZO', 'B', 'BA', 'BANR', 'BC', 'BG', 'BIIB', 'BIVV', 'BLK', 'BMY', 'BPL', 'BRK-B', 'C', 'CACI', 'CASY', 'CB', 'CBM', 'CBS', 'CBT', 'CCK', 'CCL', 'CE', 'CI', 'CNC', 'COF', 'COL', 'COLM', 'CPLA', 'CPS', 'CRI', 'CRUS', 'CTSH', 'CVS', 'DAL', 'DFS', 'DG', 'DIS', 'DLTR', 'DLX', 'DOOR', 'DOW', 'DRI', 'DST', 'DTE', 'DY', 'EBIX', 'EGBN', 'EGRX', 'EIX', 'EME', 'EMN', 'ENS', 'EPR', 'EQM', 'ES', 'EVR', 'EWBC', 'EXP', 'FBHS', 'FL', 'FRC', 'FTV', 'FUN', 'GD', 'GILD', 'GS', 'HA', 'HCA', 'HD', 'HON', 'HRS', 'HUBB', 'HUM', 'HXL', 'HY', 'IBKC', 'IBTX', 'ICE', 'INGR', 'IOSP', 'ITW', 'JBHT', 'JBSS', 'JLL', 'JNJ', 'JPM', 'KALU', 'KMX', 'KSU', 'LAD', 'LAMR', 'LBRDK', 'LCII', 'LDL', 'LEA', 'LEG', 'LH', 'LLL', 'LMT', 'LNC', 'LOPE', 'LOW', 'LRCX', 'LUV', 'LVNTA', 'MAN', 'MASI', 'MHK', 'MMC', 'MMM', 'MMP', 'MMS', 'MO', 'MPC', 'MSI', 'MTX', 'MUSA', 'NCLH', 'NDSN', 'NEE', 'NKE', 'NOC', 'NP', 'NSP', 'NUE', 'NWL', 'OA', 'OC', 'ORLY', 'OSK', 'OXM', 'PATK', 'PCG', 'PFBC', 'PG', 'PH', 'PKG', 'PLCE', 'PLT', 'PNC', 'PRU', 'PVH', 'PX', 'QCOM', 'R', 'RBC', 'RCL', 'RJF', 'ROST', 'RS', 'RTN', 'SAIC', 'SAVE', 'SBNY', 'SCG', 'SEIC', 'SIVB', 'SNA', 'SNX', 'SPGI', 'SPR', 'SRE', 'STI', 'SWK', 'SWKS', 'TAP', 'TCBI', 'TEN', 'THO', 'TJX', 'TSCO', 'TSE', 'TSN', 'TSO', 'TTD', 'TWX', 'TXN', 'UAL', 'UFPI', 'UHS', 'UNH', 'UNP', 'USNA', 'UTX', 'VAC', 'VLO', 'VMI', 'VNO', 'WASH', 'WBA', 'WBC', 'WEC', 'WHR', 'WLK', 'WTFC', 'WWD', 'WYN', 'Y']

for tickerLiteral in tickersList:
	t = Ticker()
	t.ticker = tickerLiteral
	t.watchlist = wl
	t.save()

