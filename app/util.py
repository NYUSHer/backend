import pymysql.cursors

LOGIN_ERR = "001"
REG_ERR = "002"
TOKEN_INVALID = "101"
EMAIL_ERR = "102"
UID_ERR = "103"


def query_mod(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()


def query_fetch(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
    finally:
        connection.close()
    return result
