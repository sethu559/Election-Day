import mysql.connector
import re
import smtplib
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="election"
)

mycursor = mydb.cursor()

def insert_voter(id, voter_name, age, candidate_name):
    try:
        sql = "INSERT INTO voter_list (id, voter_name, age, candidate_name) VALUES (%s, %s, %s, %s)"
        values = (id, voter_name, age, candidate_name)
        mycursor.execute(sql, values)
        mydb.commit()
        print(f"Dear {voter_name}, Your response was successfully saved!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def view_list():
    try:
        mycursor.execute("SELECT * FROM voter_list")
        result = mycursor.fetchall()
        for voter in result:
            print(voter)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def send_mail():
    try:
        gmail = input("Enter Your Mail: ")
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("cssethupathy@gmail.com", "ktax lhul drby xrti") 
        t = datetime.datetime.now()
        message = f"You voted successfully on {t} Time"
        s.sendmail("cssethupathy@gmail.com", gmail, message)
        s.quit()
        print("Mail sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")

def main():
    print("\n***********Welcome to Our Website**************")
    print("\n***********Vote for Your leader*************")
    print("1. Voting Menu")
    print("2. Exit")
    choice = (input("Enter your choice: "))
    
    if choice == 1:
        with open("voter_name.txt", "r") as f:
            name = f.read()
        voter_name = input("Enter your Name: ")
        x = re.search(voter_name, name)
        if x:
            print(f"Yes, {voter_name}, you are in this ward.")
        else:
            print("You are not in this ward.")

        age = int(input("Enter Your Age: "))
        if age >= 18:
            print("You are Eligible to Vote!")   
        else:
            print("You are not Eligible to Vote!")

        with open("candidate.txt",'r') as f:
            can = f.read()
        print("Candidate lists=[vijay,ajith,kamal]")
        candidate_name = input("Enter your candidate name: ")
        x = re.search(candidate_name, can)
        if x:
            print(f"You voted for {candidate_name}.")
            insert_voter(None, voter_name, age, candidate_name)
        else:
            print("This candidate doesn't exist!")

        send_mail()

    elif choice == 2:
        print("Exiting program.")
    else:
        print("Invalid choice. Please select option 1 or 2.")


    mycursor.close()
    mydb.close()
    


main()