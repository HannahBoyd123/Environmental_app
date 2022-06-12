import mysql.connector

def _connect_to_db(db_name: str):
    cnx = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='&Potato98&',
                                  auth_plugin='mysql_native_password',
                                  database=db_name)
    return cnx