import pymysql.cursors

LOGIN_ERR = "001"
REG_ERR = "002"
TOKEN_INVALID = "101"
EMAIL_ERR = "102"
UID_ERR = "103"

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
