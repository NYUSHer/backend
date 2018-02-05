import pymysql.cursors

# Configure MySQL
"""
# Local
CONFIG = pymysql.connect(host='192.168.64.2',
                         user='root',
                         password='',
                         db='NYUSHer',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
"""
CONFIG = pymysql.connect(host='nyusher.nya.vc',
                         port=6660,
                         user='root',
                         password='maxeeisgood',
                         db='NYUSHer',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
