import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="ed",
    passwd="Se!nf3ld1",
    database="ccc"
)

mycursor = mydb.cursor()


mycursor.execute("CREATE TABLE IF NOT EXISTS clients(\
id INT AUTO_INCREMENT PRIMARY KEY,\
name1 VARCHAR(255),\
name2 VARCHAR(255),\
phone INTEGER,\
email VARCHAR(255),\
username VARCHAR(255),\
password VARCHAR(255),\
Pet VARCHAR(255),\
notes VARCHAR(255))")



mydb.commit()

print(mycursor.rowcount, "record inserted.")

