import time
import main
import database as db
import admin


flag,mycur,mydb=db.connect()

def reset_cursor(mycur, mydb):
    try:
        mycur.fetchall()
    except:
        pass
    mycur.close()
    return mydb.cursor(buffered=True)



try :
    Total_Slots,Empty_Slots=main.slots(mycur,mydb)
except Exception as e:
    print(" ")

terminal_width=60

while (flag and Empty_Slots>0):
    mycur=reset_cursor(mycur,mydb)
    print()
    print(50*"="+"Parking Management Menu"+49*"=")
    print("Total Slots: " + str(Total_Slots) + " | Available: " + str(Empty_Slots))
    print("-" * 122)
    print("1 ---> Vehicle Entry (Check-In)")
    print("2 ---> Vehicle Exit (Check-Out)")
    print("3 ---> Show Parked Vehicles")
    print("4 ---> To Enter Admin Panel")
    print("5 ---> Exit Program")
    choice = int(input("Enter your choice: "))
    if (choice==1):
        success = main.vehicle_In(mycur, mydb)
        if success:
            Empty_Slots -= 1
    elif (choice==2):
        Empty_Slots=Empty_Slots+1
        main.vehicle_Out(mycur, mydb)
    elif (choice==3):
        main.vehicles_Info(mycur, mydb)
    elif (choice==4):
        print(51*"."+"Entering Admin Panel"+51*".")
        admin.admin(flag,mycur,mydb)
    elif (choice==5):
        print(49*"*"+"Ending Code Execution IN"+49*"*")
        for i in range(5,0,-1):
            print(i,end="..",flush=True)
            time.sleep(1)
        flag=0
    else:
        print("Wrong Choice","."*20)

