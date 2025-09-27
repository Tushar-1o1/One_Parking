import hashlib
import time
import main


def hash_password_sha224(password):
    return hashlib.sha224(password.encode()).hexdigest()


def open_file():
    try :
        with open("admin.txt","r") as fr:
            Ap=fr.read().strip()
            return Ap
    except Exception:
        print("File Missing...")
    
    
try:
    def admin(flag,mycur,mydb):
        print("-" * 123)
        admin_pass=input("Enter Admin Password : ")
        hashed_pass = hash_password_sha224(admin_pass)
        stored=open_file()
        
        if hashed_pass == stored:
            while flag :
                print(55*"="+"ADMIN  PANEL"+55*"=")
                print("1---> To View a Paticular")
                print("2---> To Edit a Record")
                print("3---> To Edit Pricing")
                print("4---> Exit The Admin panel")
                choice=int(input("Enter Your Choice : "))
                if choice==1 :
                    main.view_particular_rec(mycur,mydb)
                elif choice==2 :
                    main.edit_record(mycur,mydb)
                elif choice==3:
                    main.price_edit(mycur,mydb)
                elif choice==4 :
                    print(50*"*"+"Exiting Admin Panel In"+50*"*")
                    for i in range(5,0,-1):
                        print(i,end="..",flush=True)
                        time.sleep(1)
                    flag=False
                else :
                    print("Wrong choice")
        else :
            print("Access Denied (please enter correct password)")
            time.sleep(5)
except Exception :
    print(Exception)
