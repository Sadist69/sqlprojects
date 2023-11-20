import random 
import mariadb
from datetime import datetime


##passwords
auser="admin"
apass="1234"
uuser="user"
upass="1234"


# Connect to the database
conn = mariadb.connect(
    host="localhost",
    user="root",
    password="1234"

)
cursor = conn.cursor()
cursor.execute("create database if not exists hospital;")
cursor.execute("use hospital;")
cursor.execute("create table if not exists patients(name varchar(32),age int(2),gender varchar(10),patient_id int(5),reason varchar(50),datee date,timee time );")
cursor.execute("create table if not exists bills(patient_id int(5),amount int(12));") 

# Admin login
def admin_login():
    while True:
        try:
            print("_"*50)
            d="\nADMIN LOGIN PORTAL"
            print(d.center)
            x=input("\nTo Continue Further Press Y TO exit Press X : ")
            if x=='y' or x=='Y': 
                username = input("\t \t Enter admin username: ")
                password = input("\t \tEnter admin password: ")
                if username==auser and password==apass :
                    admin_menu()
                else:
                    print(" \n Invalid credentials")
            else:
                print("Exittting...")
                break
                
        except Exception as e:
            print(".......Error Occured Try Again......")
            continue
        
            

# User login
def user_login():
    while True:
        try:
            c="\nUSER LOGIN PORTAL"
            print("_"*50)
            print(c.center)
            x=input("\nTo Exit Press X Or Y TO Continue : ")
            if x=='y' or x=='Y':

                username = input("\t\tEnter username: ")
                password = input("\t\tEnter password: ")
                #cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                if username==uuser and password==upass:
                    user_menu()
                else:
                    print("\nInvalid User Credentials")
            else:
                break
        except Exception as e:
            print("......Enter Correct Input......")
            continue
# Admin menu
def admin_menu():
    while True:
     try:
        db="\nWELCOME ADMIN"
        print(db.center)
        print("══════════════════════"*3)
        print(" \n Admin Menu:")
        print("══════════════════════"*3)
        print("\t\t1. Add patient")
        print("\t\t2. Update patient status")
        print("\t\t3. Discharge patient")
        print("\t\t4. Process bill")
        print("\t\t5. Show Patients")
        print("\t\t6. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            add_patient()
        elif choice == '2':
            update_patient_status()
        elif choice == '3':
            discharge_patient()
        elif choice == '4':
            process_bill()
        elif choice == '5':
            show_patients()
        elif choice=='6':
            break
        else:
            print("\n \tInvalid choice")
            continue
     except:
            print("......Try again......")
            continue

# User menu
def user_menu():
 while True: #loop to avoid interrupt
  try:
    print("══════════════════════"*3)  
    print(" \nUser Menu:")
    print("══════════════════════"*3)
    print("\t\t1. View patient status")
    print("\t\t2. View bill amount")
    print("\t\t3. Exit")
    choice = input("\n Enter choice: ")
    if choice == '1':
        view_patient_status()
    elif choice == '2':
        view_bill_amount()
    elif choice == '3':
        break
    else:
       print("\n Invalid choice")
       continue
  except Exception as e:
      print("\n\n........Please enter valid input.......")
      continue
  finally:
      conn.commit()   
#~~~~~~~~~~~~~~~~~aADMIN PORTAL CODE STARTS HERE `~~~~~~~~~~~~` 

# Add new patient
def add_patient():
 while True:
  try:
    a="\nPATIENT REGISTRATION PORTAL"
    print("_"*50)
    print(a.center)
    name = input("\t\tEnter patient name: ")
    age = int(input("\t\tEnter patient age: "))
    gender = input("\t\tEnter patient gender: ")
    patient_id=random.randint(2000,6000)
    #curent date , time
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
        
    id1=patient_id
    reason = input("\n \tEnter patient diagnosis: ")
    cursor.execute("INSERT INTO patients (name, age, gender,patient_id,reason,datee,timee) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, age, gender,patient_id,reason,current_date,current_time))
    
    print(f"              Patient added successfully   ID - {id1}       ")
    r=input("\n Enter Y to add more X to exit.")
    if r=='Y':
        continue
    else:
        break
  except Exception as e:
      print("\n \tAn Error occured Try again")
      continue
  finally:
      conn.commit()
      
      
# Update patient status
def update_patient_status():
    while True:
        try:
            b="\nPATIENT DIAGNOSIS PORTAL"
            print("_"*50)
            print(b.center)
            patient_id = int(input("\t\tEnter patient ID: "))
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient=cursor.fetchone()
            if patient:
                reason  = input("\t\tEnter new diagnosis: ")
                cursor.execute("UPDATE patients SET reason=%s WHERE patient_id=%s", (reason, patient_id))
                print(f"\n \tPatient status updated successfully for patient id {patient_id}")
            else:
                print("\n Patient dosen't Match, please try again....")
        except Exception as e:
            print(f"\nAn Error Occured : {e}")
            continue
        finally:
            conn.commit()
# Discharge patient
def discharge_patient():
    while True:
        try:
            print("_"*50)
            dd="\nPATIENT DISCHARGE PORTAL"
            print(dd.center)
            patient_id = int(input("\t\tEnter patient ID: "))
            id2=patient_id
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient=cursor.fetchone()
            if patient:
                cursor.execute("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
                print(f"\n\t\tPatient {id2} discharged successfully")
                r=input("\n \tEnter Y to proceed X to exit.")
                if r=='y' or r=='Y':
                    continue
                else:
                    break
            else:
                print("Patient Not Found... Try again!")
        except Exception as e:
            print("Error Occured Try again")
            continue
        finally:
          conn.commit()

# Process bill
def process_bill():
    while True:
        try:
            patient_id = int(input("\t\tEnter patient ID: "))
            amount = float(input("\t\tEnter bill amount: "))
            cursor.execute("INSERT INTO bills (patient_id, amount) VALUES (%s, %s)", (patient_id, amount))
            print("\n \tBill processed successfully")
            r=input("\n \tEnter Y to add more X to exit : ")
            if r=='Y':
                continue
            else:
                print("\n Exitting...")
                break
        except Exception as e:
            print("......Error Occured Try again......")
            continue
        finally:
           conn.commit()
           
           
           
#~~~~~~~~~~~~~~ USER PORTAL CODE STARTS HERE ~~~~~~~~~~~~~~~


# View patient status
def view_patient_status():
    while True:
        try:
            print("_"*50)
            d="\n WELCOME USER"
            print(d.center)
            patient_id = int(input("\t\tEnter patient ID: "))
            '''cursor.execute("SELECT reason FROM patients WHERE patient_id=%s", (patient_id,))
            #status = cursor.fetchone()
            reason=cursor.fetchone()
            if reason:
                print(f"                Patient diagnosis: {reason[0]}       ")
            else:
                print("\nPatient not found")
                '''
            cursor.execute(f"SELECT patient_id, name, age, reason, datee, timee FROM patients WHERE patient_id = {patient_id}")
            patient_data=cursor.fetchone()
            if patient_data:
                print(f"\t\tPatient ID: {patient_data[0]}")
                print(f"\t\tName: {patient_data[1]}")
                print(f"\t\tAge: {patient_data[2]}")
                print(f"\t\tAdmit Reason: {patient_data[3]}")
                print(f"\t\tDate Of Admit: {patient_data[4]}")
                print(f"\t\tTime Of Admit: {patient_data[5]}")
                
            else:
                print(f"\nNo patient found with ID: {patient_id}")
                      
            r=input("\n Enter Y to search more X to exit : ")
            if r=='Y'or r=='y':
                continue
            else:
                break
        except Exception as e:
            print(".......Error Occured Try again.......")
            continue
        
        
# View bill amount
def view_bill_amount():
    while True:
        try:
            patient_id = int(input("\n \tEnter patient ID: "))
            cursor.execute("SELECT amount FROM bills WHERE patient_id=%s", (patient_id,))
            #cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            #patient=cursor.fetchone()
            #cursor.execute("SELECT patient_id, amount FROM bills WHERE patient_id = %s",(patient_id))
            amount = cursor.fetchone()
            if amount:
                print(f" \n Bill amount: ₹{amount[0]} only. ")
            else:
                print("\nBill not found")
            x=input("\n\tEnter Y to Continue further Or X to Exit : ")     
            if x=='y' or x=='Y':
                continue
            else:
                break   
        except:
            print("\n.......Error Occurred Try Again....")
            continue

    
##### Show pateint option
def show_patients():
    try:
        di="\n \n \n WELCOME ADMIN"
        print("_"*50)
        print(di.center)
        cursor.execute("SELECT patient_id,name,datee,timee FROM patients")
        row=cursor.fetchall()
        #cursor.execute("SELECT patient_id,name,COUNT(patient_id) FROM patients ORDER BY; ")
        #cursor.execute("SELECT patient_id, name,COUNT(patient_id) FROM patients GROUP BY patient_id, name")
        #res=cursor.fetchall()
        print(" ══════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        if not row:
            print("\nNo data present")
        else:
            print("PATIENT ID \t NAME \t DATE \t         TIME ")                                               
            
            for rows in row:
                print(f"{rows[0]}\t\t{rows[1]},\t{rows[2]},\t{rows[3]}")
    except Exception as e:
        print("Try again....")
    

# Main menu
def main_menu():
    while True:
        try:
            print("══════════════════════"*3)
            print("\n Hospital Management System: \n ")
            print("══════════════════════"*3)
            print("\t\t1. Admin login")
            print("\t\t2. User login")
            print("\t\t3. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
             admin_login()
            elif choice == '2':
                user_login()
            elif choice == '3':
                break
            else:
                print("Invalid choice")
        except:
            print("......Try Again......")

# Initialize the application
main_menu()
# Close the database connection
conn.close()
