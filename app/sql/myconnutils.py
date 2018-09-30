import pymysql.cursors  
 
# Function return a connection.
def getConnection():
     
    # You can change the connection arguments.
    db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',                             
                                 db='APPSOCIAL',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return db
