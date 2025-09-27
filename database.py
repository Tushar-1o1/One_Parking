import mysql.connector
import time
def connect():
    try:
        paswd=input("Enter the login password : ")
        mydb=mysql.connector.connect(host="localhost",
                                     user="root",
                                     password=paswd,
                                     database="PARKING")
        mycur=mydb.cursor()
        print(51*"*","login successfully",51*"*")

        mycur.execute("""
                    CREATE TABLE IF NOT EXISTS PARKING_PRICE(
                    S_No INT PRIMARY KEY,
                    Vehicle_Type VARCHAR(40),
                    Price DECIMAL(10,2)
                    )
        """)

        mycur.execute("SELECT COUNT(*) FROM PARKING_PRICE")
        count = mycur.fetchone()[0]
        if count == 0:
            mycur.execute("""
                        INSERT INTO PARKING_PRICE(S_No, Vehicle_Type, Price) VALUES
                        (1, 'Motorcycle / Scooter / Bike', 10.00),
                        (2, 'Car / Hatchback / Sedan', 15.00),
                        (3, 'SUV / MUV / Van', 20.00),
                        (4, 'Pickup Truck / Mini LCV', 20.00),
                        (5, 'Bus / Tempo Traveller', 30.00),
                        (6, 'Truck / Commercial Vehicle', 35.00)
            """)
        
        mycur.execute("""
                    CREATE TABLE IF NOT EXISTS Daily_Parking(
                    Vehicle_Name VARCHAR(30),
                    Vehicle_Type VARCHAR(30),
                    Number_Plate VARCHAR(20) PRIMARY KEY,
                    Entry_Time TIME,
                    Exit_Time TIME
                    );
        """)

        mycur.execute("""
                    CREATE TABLE IF NOT EXISTS Parking_Log(
                    S_No INT AUTO_INCREMENT PRIMARY KEY,
                    Vehicle_Name VARCHAR(30),
                    Vehicle_Type VARCHAR(30),
                    Number_Plate VARCHAR(20) NOT NULL,
                    Entry_Time TIME,
                    Exit_Time TIME,
                    Date DATE,
                    Price_Paid DECIMAL(10,2)
                    )
                    
        """)
        mydb.commit()
        return True,mycur,mydb
    except mysql.connector.Error as err:
        print("Invalid Credentials:", err)
        time.sleep(2)
        return False,None,None

