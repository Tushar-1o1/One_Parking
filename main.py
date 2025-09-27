import time
import datetime
from decimal import Decimal




# To Empty_Slots
def slots(mycur,mydb):
    Total_Slots=100
    try :
        mycur.execute("SELECT COUNT(*) FROM Daily_Parking")
        result=mycur.fetchone()[0]
        Empty_Slots=Total_Slots-result
        return Total_Slots,Empty_Slots
    except Exception as e :
        print(e)
        return Total_Slots,None


        
# To calculate price
def price(Entry_Time, Exit_Time,mycur,mydb,vehicle_type):
    duration = Exit_Time - Entry_Time
    in_min = duration.total_seconds() / 60
    mycur.execute("SELECT Price FROM PARKING_PRICE WHERE Vehicle_Type LIKE %s", ('%' + vehicle_type + '%',))
    result = mycur.fetchone()
    if result is None:
        raise ValueError(f"No pricing data found for vehicle type: {vehicle_type}")
    per_min = result[0]
    charge = round(per_min * Decimal(str(in_min)), 2)
    return charge, in_min



# Convert mysql time to python time
def timedelta_to_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return datetime.time(hour=hours, minute=minutes, second=seconds)



# For check out
def vehicle_Out(mycur, mydb):
    Number_Plate = input("Enter Number Plate : ")
    Exit_Time = datetime.datetime.now().time()
    Date = datetime.datetime.now().date()

    try:
        mycur.execute("""
            SELECT Entry_Time, Date, Vehicle_Type 
            FROM Parking_Log 
            WHERE Number_Plate = %s AND Exit_Time IS NULL
        """, (Number_Plate,))
        result = mycur.fetchone()

        if result is None:
            print("Vehicle never entered ")
            return

        entry_time, entry_date, vehicle_type = result

        if isinstance(entry_time, datetime.timedelta):
            entry_time = timedelta_to_time(entry_time)

        Entry_DateTime = datetime.datetime.combine(entry_date, entry_time)
        Exit_DateTime = datetime.datetime.combine(Date, Exit_Time)

        charge, minutes = price(Entry_DateTime, Exit_DateTime, mycur, mydb, vehicle_type)

        print("Duration: ", round(minutes, 2), "minutes")
        print("Charges: ₹", charge)

        mycur.execute("""
            UPDATE Parking_Log
            SET Exit_Time=%s, Price_Paid=%s
            WHERE Number_Plate=%s
        """, (Exit_Time, charge, Number_Plate))

        mycur.execute("DELETE FROM Daily_Parking WHERE Number_Plate=%s", (Number_Plate,))

        mydb.commit()

    except Exception as e:
        print("Error during vehicle exit:", e)




# For check in    
def vehicle_In(mycur, mydb):
    Vehicle_Name=input("Enter Vehicle Name : ")
    Vehicle_Type=input("Enter Vehicle Type : ")
    Number_Plate=input("Enter Number Plate : ")
    Entry_Time=datetime.datetime.now().time()
    Date = datetime.datetime.now().date()
    try :
        mycur.execute("SELECT STATUS FROM NCRB WHERE NUMBER_PLATE = %s",(Number_Plate,))
        record=mycur.fetchone()
        if record:
            print("""ALERT.......
                     CRIMINAL RECORD FOUND
                    """)
            call()
            return False
        else :
            mycur.execute("""
                    INSERT INTO Daily_Parking (Vehicle_Name, Vehicle_Type, Number_Plate, Entry_Time, Exit_Time)
                    VALUES (%s, %s, %s, %s, NULL)
            """, (Vehicle_Name, Vehicle_Type, Number_Plate, Entry_Time))
            mycur.execute("""
                    INSERT INTO Parking_Log (Vehicle_Name, Vehicle_Type, Number_Plate, Entry_Time, Exit_Time,Date,Price_Paid)
                    VALUES (%s, %s, %s, %s, NULL, %s, NULL)
            """,(Vehicle_Name, Vehicle_Type, Number_Plate, Entry_Time, Date))
            mydb.commit()
            print("Vehicle with number plate {} entered successfully...".format(Number_Plate))

            return True
    except Exception as e:
        print("error in vehicle entry....")
        return False
    



#For all vehicles information
def vehicles_Info(mycur, mydb):
    try:
        mycur.execute("SELECT * FROM Daily_Parking")
        result=mycur.fetchall()

        if result:
            print("\nAll Vehicle Information:\n" + "-"*50)
            for row in result:
                print("  Vehicle Name   : ",row[0])
                print("  Vehicle Type   : ",row[1])
                print("  Number Plate   : ",row[2])
                print("  Entry Time     : ",row[3])
                print("  Exit Time      : ",row[4] if row[4] else "Still Parked")
                print("-" * 50)
        else:
            print("No record found for this number plate or the parking is empty.")
            
    except Exception as e:
        print("Error in finding vehicle:", e)



#View a particular record
def view_particular_rec(mycur,mydb):
    Number_Plate=input("Enter number plate number : ")
    try:
        mycur.execute("SELECT * FROM Parking_Log WHERE Number_Plate = %s", (Number_Plate,))
        row=mycur.fetchone()
        if row:
            print("  Vehicle Name   : ",row[1])
            print("  Vehicle Type   : ",row[2])
            print("  Number Plate   : ",row[3])
            print("  Entry Time     : ",row[4])
            print("  Exit Time      : ",row[5] if row[5] else "Still Parked")
            print("  Date           : ",row[6])
            print("  Price Paid     : ","₹",row[7] if row[7] else "N/A")
            print("-" * 50)
        else :
            print("No record found for number plate : ", number_plate)
    except Exception as e:
        print("Error fetching record : ", e)



#Edit a record
def edit_record(mycur,mydb):
    Number_Plate=input("Enter number plate number : ")
    try:
        mycur.execute("SELECT * FROM Parking_Log WHERE Number_Plate = %s", (Number_Plate,))
        result=mycur.fetchone()
        if result:
            Vehicle_Name=input("Enter New Vehicle Name : ")
            Vehicle_Type=input("Enter New Vehicle Type : ")
            mycur.execute("UPDATE Parking_Log SET Vehicle_Name=%s, Vehicle_Type=%s WHERE Number_Plate=%s",(Vehicle_Name,Vehicle_Type,Number_Plate))
            mycur.execute("UPDATE Daily_Parking SET Vehicle_Name=%s, Vehicle_Type=%s WHERE Number_Plate=%s",(Vehicle_Name,Vehicle_Type,Number_Plate))
            mydb.commit()
        else :
            print("No record found for number plate:", Number_Plate)
    except Exception as e:
        print("Error editing record : ", e)



#Edit Pricing
def price_edit(mycur,mydb):
    try :
        mycur.execute("SELECT * FROM PARKING_PRICE")
        result=mycur.fetchall()
        if result:
            print("-" * 60)
            print("S_No  |","Vehicle Type            |", "Pricing in ₹")
            print("-" * 60)
            for row in result:
                print("(",row[0],", ",row[1],", ₹",row[2],")")
            print("-" * 60)
            S_No=int(input("Enter S_No = "))
            Price = float(input("Enter New Price = "))
            try :
                mycur.execute("UPDATE PARKING_PRICE SET Price = %s WHERE S_No = %s",(Price,S_No))
                print("Price Updated....\n")
                mydb.commit()
            except Exception as e:
                print(e)
        else :
            print("Empty")
    except Exception as e:
        print("Error while editing : ", e)

#Contact Nearest Police Station
def call():
    print("Police station has been contacted..........")






