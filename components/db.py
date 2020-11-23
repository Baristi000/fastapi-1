import mysql.connector

from core.config import settings

#open mysql connection
def connection():
    cnx = mysql.connector.connect(host=settings.MYSQL_SERVER,
                                user=settings.MYSQL_USER,
                                password=settings.MYSQL_PASSWORD,
                                database=settings.MYSQL_DB)
    return cnx

#execute query 
def query_exec(q:str):
    cnx = connection()
    cursor = cnx.cursor()
    cursor.execute(q)
    if q.split()[0].upper()=="SELECT":
        data = cursor.fetchall();
        res = []
        for r in data:
            row = {}
            for i in range(len(cursor.description)):
                row.update({(cursor.description[i][0]):r[i]})
            res.append(row)    
        cnx.close()
        cursor.close()
        return(res)
    else:
        cnx.commit()
        cnx.close()
        cursor.close()
