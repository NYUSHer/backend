import pymysql.cursors

# Configure MySQL
CONFIG = pymysql.connect(host='192.168.64.2',
                         user='root',
                         password='',
                         db='NYUSHer',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)