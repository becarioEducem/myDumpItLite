import mysql.connector
import os
import shutil

#Ask for host, user and password
hostname = input("Enter hostname: ")
username = input("Enter username: ")
password = input("Enter password: ")


# Try to Connect to MySQL/MariaDB server
try:
  cnx = mysql.connector.connect(user=username, password=password, host=hostname, database='',ssl_disabled=True)
  # Check if connection was successful
  if cnx.is_connected():
      print('Connection successful!')
      #Get all databases
      cursor = cnx.cursor()
      cursor.execute("SHOW DATABASES")
      databases = cursor.fetchall()
      # Close connection
      cnx.close()
      #Dump all databases
      for database in databases:
        #Connect to the database
        try:
          mydb = mysql.connector.connect(user=username, password=password, host=hostname, database=database[0],ssl_disabled=True)
          print(f"Dumping database: {database[0]}")
          #Make a directory for the database (overwrite if exists)
          if os.path.exists(f"./{database[0]}"): shutil.rmtree(f"./{database[0]}")
          os.mkdir(f"./{database[0]}")
          cursor = mydb.cursor()
          #Get all tables
          cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE != 'VIEW' AND TABLE_SCHEMA = '{database[0]}';")
          tables = cursor.fetchall()
          print(f"Tables: {tables}")
          #Dump all tables
          for table in tables:
            print(f"Dumping table: {table[0]}")
            #Get all rows
            cursor.execute("SELECT * FROM %s" % table[0])
            rows = cursor.fetchall()
            #Dump all rows
            for row in rows:
                with(open(f"./{database[0]}/{table[0]}.txt", "a",encoding="utf-8")) as f:
                    f.write(str(row)+"\n")
          # Close current connection
          mydb.close()
        except mysql.connector.Error as err:
          print(f"Connection failed with username: {username} and password: {password} against database: {database[0]}")
except mysql.connector.Error as err:
    print(f"Connection failed with username: {username} and password: {password}")