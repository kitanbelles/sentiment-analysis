import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="otaladesuyi",
    password='phanmium'
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE twitterdb")
print(mydb)