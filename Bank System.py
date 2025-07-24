from getpass import getpass

# For Tables
import pandas as pd
from tabulate import tabulate

# For Data Storage
import json

# For Date and Time usage
import datetime
import time

# For Password Validation
import re


#  ************ Class BankSystem contains User Registration and Login for both User and Admin and Admin Functionalities **************

class Banksystem():


    def __init__(self,users):
        self.users = users

    # User Registration

    def register_user(self):
        print(" ___ REGISTRATION ___ \n")
        self.name = input("Name :")
        self.username = input("Username  :")
        while self.username in users['active_users'].keys():
            print("*** Username unavailable ! Try another ***")
            self.username = input("Username  :")
        while True:
            self.password = input("Create a strong password: ")
            m = re.match('^(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%^&+=!]).{6,25}$',self.password)
            if m :
                print("Password accepted !")
                break
            else:
                print(" Try again...!!!\n Password must be 6–25 characters long,\n include at least 1 uppercase, 1 number, and 1 special character.")
        self.retype = input("Retype password  :")
        while self.password != self.retype:
            print("Passwords mismatch")
            self.password = input("Password  :")
            self.retype = input("Retype password  :")

        print(" REGISTERED SUCCESSFULLY !!!  \n")
        time.sleep(1)
        account_number = users['next_account_id']
        users['active_users'].update({self.username:{'name':self.name,
                                     'password':self.password,
                                     'account_id':account_number,
                                     'balance':0,
                                     'transactions':[]}
                      })
        users['next_account_id'] +=1
        update_users(self.users)

   #  User Login

    def login_user(self):
        print(" ___ LOGIN ___ \n")
        self.uname = input("Username :")
        if self.uname != 'admin':
            while self.uname not in users['active_users'].keys() and self.uname !='admin':
                print("User not found ! Register to login ")
                try:
                    print("1. Try again")
                    print("2. Register")
                    print("3. Exit")

                    choice = int(input("enter your choice :"))
                    if choice == 1:
                        self.uname = input("Username :")
                        if self.uname in users['active_users'].keys():
                            break
                        else:
                            continue
                    elif choice == 2:
                        self.register_user()
                        main_menu()
                        break
                    elif choice == 3:
                        main_menu()
                        break
                    else:
                        print("Invalid choice...Enter a number from 1-3")
                except Exception:
                    print("Invalid input... Enter a number from 1-3")

        password = input("Password :")
        counter = 3
        if self.uname !='admin':
            while password != users['active_users'][self.uname]['password']:
                print(f"*** Incorrect password {counter} attempts left***")
                if counter != 0 :
                    password = input("Password :")
                    counter -= 1
                else :
                    print("Log in attempt failed")
                    return
            else:
                print("Logged in successfully !")
                time.sleep(1)
                bankuser = BankAccount(self.uname,users)
                bankuser.user_menu()
        else:
            while password != users['admin']['password']:
                print(f"*** Incorrect password {counter} attempts left***")
                if counter != 0:
                    password = input("Password :")
                    counter -= 1
                else:
                    print("Log in attempt failed")
                    return
            else:
                print("Logged in successfully !")
                time.sleep(1)
                self.admin_menu()

    # Display Admin Menu

    def admin_menu(self):
        session_active = True
        while session_active :
            print("\n ___ Welcome Admin !!! ___\n")
            print("1. View User Accounts")
            print("2. Delete a User Account")
            print("3. Recover Deleted Account")
            print("4. Change Password")
            print("5. Log out")
            try:
                choice = int(input("enter your choice :"))
                if choice == 1 :
                    self.view_user_accounts()
                    time.sleep(0.5)
                elif choice == 2 :
                    self.delete_user_account()
                    time.sleep(0.5)
                elif choice == 3:
                    self.recover_deleted_account()
                    time.sleep(0.5)
                elif choice == 4:
                    print("PASSWORD : ",users['admin']['password'])
                    print("_______________________")
                    change_password('admin')
                    time.sleep(0.5)
                elif choice == 5:
                    session_active = False
                    print("\n Logging out...\n".upper())
                    time.sleep(1)
                    return
                else:
                    print("invalid choice , enter a number between 1-5")
                    time.sleep(0.5)
            except:
                print("invalid input , enter a number between 1-5")
                time.sleep(0.5)

    # Display User Accounts for admin

    def view_user_accounts(self):

        print("    *** ACCOUNT HOLDERS DETAILS ***\n")
        print(" ----- ACTIVE ACCOUNT HOLDERS -----")
        user_data = {uname: details for uname, details in users['active_users'].items()}
        if len(user_data)==0:
            print("\nNo User Accounts !!!")
            time.sleep(0.5)
            return
        df = pd.DataFrame(user_data)
        df = df.T
        print(tabulate(df, headers='keys', tablefmt='pretty'))

    # User Account deletion

    def delete_user_account(self):

        print(" \n---- DELETE AN ACCOUNT ----\n")
        usernames=[]
        for username in users['active_users'].keys():
            usernames.append(username)
        if len(usernames) == 0:
            print("\nNo User Accounts to delete !")
            time.sleep(0.5)
            return
        else:
            print(" *** Available User Accounts ***")
            for names in usernames:
                print(names)
        del_user = input("\nEnter Username :")
        if del_user in users['active_users'].keys():
            data = {del_user : users['active_users'][del_user]}
            df = pd.DataFrame(data)
            df = df.T
            print(tabulate(df, headers='keys', tablefmt='pretty'))
            print()
            print("Please confirm to delete the account :")
            print("1. Yes")
            print("2. No")
            confirm_del = input("Enter your choice : ")
            if confirm_del == '1' or confirm_del == 'yes':
                vals= users['active_users'].pop(del_user)
                print(f"\n**** User Account '{vals['name']}' with Account id - {vals['account_id']} is deleted successfully !!! ****")
                users['deleted_users'].update(data)
                update_users(self.users)

            elif confirm_del == '2' or confirm_del == 'no':
                return
            else:
                print("Invalid choice \n")
                time.sleep(0.5)
                return
        else:
            print("Username doesn't exists !!!")
            time.sleep(0.5)
            return

    # Revive Deleted Account

    def recover_deleted_account(self):
        print(" ****** RECOVER DELETED ACCOUNT *******\n")
        deleted_users = {uname: details for uname, details in users['deleted_users'].items()}
        if len(deleted_users) == 0:
            print("No Deleted Accounts !!!")
            time.sleep(0.5)
            return
        df = pd.DataFrame(deleted_users)
        df = df.T
        print("DELETED ACCOUNTS")
        print()
        print(tabulate(df, headers='keys', tablefmt='pretty'))
        print()
        recover_acc = input("Enter username to recover : ")
        print()
        if recover_acc in users['deleted_users'].keys():
            print("Recovering Account Details :")
            print("Name :",users['deleted_users'][recover_acc]['name'])
            print("Account Number:",users['deleted_users'][recover_acc]['account_id'])
            print()
            print("Are you sure to recover this account :")
            print("1. Yes")
            print("2. No")
            confirm_recover = input("Enter your choice : ")
            if confirm_recover == '1' or confirm_recover == 'yes':
                val = users['deleted_users'].pop(recover_acc)
                recover_data = {recover_acc : val}
                users['active_users'].update(recover_data)
                update_users(self.users)
                print("----- ACCOUNT RESTORED SUCCESSFULLY !!! -----")
                return
            elif confirm_recover == '2' or confirm_recover == 'no':
                print("Going back to menu...")
                return
            else:
                print("Invalid choice \n")
                time.sleep(0.5)
                return
        else:
            print("Username doesn't exists !!!")
            time.sleep(0.5)
            return

#                            **** / End of class BankSystem  / ****



#                 *************  BankAccount class for User Operations   ******************8

class BankAccount:
    def __init__(self,uname,users):
        self.users = users
        self.uname = uname
    min_balance = 500       # BankAccount Variable (Minimum Balance of an account)

    # Display User Menu

    def user_menu(self):
        while True:
            print("\n *******  Welcome ", self.users['active_users'][self.uname]['name'].upper(), "!!! *******")
            time.sleep(0.5)
            print("1. Deposit money")
            print("2. Withdraw money")
            print("3. View Account Balance")
            print("4. View Transaction History")
            print("5. Edit my details")
            print("6. Log out")

            try:
                choice = int(input("enter your choice: \n"))

                if choice == 1 :
                    self.deposit_money()
                    time.sleep(1)
                elif choice == 2:
                    self.withdraw_money()
                    time.sleep(1)
                elif choice == 3:
                    self.view_balance()
                    time.sleep(1)
                elif choice == 4:
                    self.view_transactions()
                    time.sleep(1)
                elif choice == 5:
                    self.edit_user_details()
                    time.sleep(1)
                elif choice == 6:
                    print("\n Logging out...\n".upper())
                    time.sleep(1)
                    break
                else:
                    print("Invalid choice ... Enter a number between 1-6")
                    time.sleep(0.5)
            except:
                print("Invalid choice . Enter a digit")
                time.sleep(0.5)

    # Money Deposit

    def deposit_money(self):
        print("___ MONEY DEPOSIT ___")
        while True:
            try:
                dep_amount = int(input("Enter amount to deposit: "))
                if dep_amount > 0:
                    users['active_users'][self.uname]['balance'] += dep_amount
                    dep_time = datetime.datetime.now()
                    print(f"Rs.{dep_amount} is deposited !!! \n")
                    balance_now = users['active_users'][self.uname]['balance']
                    users['active_users'][self.uname]['transactions'].append(
                        {"Date": dep_time.strftime("%x"),
                         "Time":dep_time.strftime("%X"),
                         "Amount": dep_amount ,
                         "Transaction":"Credit",
                         "Balance":balance_now})
                    update_users(self.users)
                    break
                else:
                    print("Invalid amount !!! Amount should be above Rs.0  \n")
                    time.sleep(0.5)
            except:
                print("Invalid amount !!! Enter a digit \n")
                time.sleep(0.5)

    # Money Withdrawal

    def withdraw_money(self):
        print("\n___ MONEY WITHDRAWAL ___")
        if int(users['active_users'][self.uname]['balance']) == 0:
            print("Withdrawal not possible with No Balance !!!")
            return
        while True:
            try:
                withdraw_amount = int(input("Enter amount to withdraw: "))
                if int(users['active_users'][self.uname]['balance']) < self.min_balance :
                    print("Minimum balance , Withdrawal not possible !")
                elif withdraw_amount > (int(users['active_users'][self.uname]['balance']) - self.min_balance):
                    print("Withdrawal not possible , amount exceeded minimum balance limit !")
                elif withdraw_amount > 0:
                    users['active_users'][self.uname]['balance'] -= withdraw_amount
                    withdraw_time = datetime.datetime.now()
                    print(f"Rs.{withdraw_amount} is withdrawed !!! \n")
                    balance_now = users['active_users'][self.uname]['balance']
                    users['active_users'][self.uname]['transactions'].append(
                        {"Date": withdraw_time.strftime("%x"),
                         "Time": withdraw_time.strftime("%X"),
                         "Amount": withdraw_amount,
                         "Transaction": "Debit",
                         "Balance":balance_now})
                    update_users(self.users)
                    break
                elif withdraw_amount == 0:
                    print("Withdraw amount can't be Rs.0")
                    time.sleep(0.5)
                else:
                    print("Invalid amount !!! Enter a rupee value above Rs.0")
                    time.sleep(0.5)
            except:
                print("Invalid amount !!! Enter a rupee value")
                time.sleep(0.5)

    # Display Account Balance

    def view_balance(self):
        print("\n ___ ACCOUNT BALANCE ___")
        print("Your current balance is")
        print(f" ** Rs.{users['active_users'][self.uname]['balance']:.2f} ** ")

    # Display Transactions of the User

    def view_transactions(self):
        print("\n ___ACCOUNT TRANSACTIONS___\n")

        if len(users['active_users'][self.uname]['transactions'])==0:
            print("*** No Recent Transactions ***")
        else:
            data =users['active_users'][self.uname]['transactions']
            df = pd.DataFrame(data,index= range(1,len(data)+1))
            print(tabulate(df, headers='keys', tablefmt='pretty'))

    # Change User's Name and Password

    def edit_user_details(self):
        while True:
            print("\n _____EDIT MY DETAILS_____")
            print("Name : ",users['active_users'][self.uname]['name'])
            print("Password : ",users['active_users'][self.uname]['password'])
            print("--------------------------------")
            print("1. Change Name")
            print("2. Change Password")
            print("3. Exit")
            try:
                choice = int(input("enter your choice :"))

                if choice == 1:

                    # Change User's Name

                    new_name = input("___Enter new name___ :")
                    print("Please confirm to change the name :")
                    print("1. Yes")
                    print("2. No")
                    confirm_change = input("Enter your choice : ")
                    if confirm_change == '1' or confirm_change == 'yes':
                        users['active_users'][self.uname]['name'] = new_name
                        update_users(self.users)
                        print(" *** NAME CHANGED !!! ***")
                        return
                    elif confirm_change == '2' or confirm_change == 'no':
                        return
                    else:
                        print("Invalid Choice !!!")
                        return

                elif choice == 2:
                    # Change User's Password
                    change_password(self.uname)
                    return

                elif choice == 3:
                    print("Going back to menu... !!!")
                    time.sleep(0.3)
                    return
                    # break
                else:
                    print("Enter a number between 1-3")
            except:
                print("Invalid choice ...Try again !")



#                        ****/  End of class BankAccount  /****


# To load data from users.json file or create a new file with admin data

def get_users():
    try:
        with open("users.json",'r') as f:
            return json.load(f)
    except:
        with open("users.json", 'w+') as f:
            admin_deeds = {"next_account_id": 1001,
                           "admin": {
                                "name": "Admin",
                                "password": "Admin@123" },
                           "active_users":{},
                           "deleted_users":{}
                           }
            json.dump(admin_deeds,f,indent=4)
        with open("users.json",'r') as f:
            return json.load(f)

# To update users dict to users.json file

def update_users(users):
    with open("users.json",'w') as f:
        json.dump(users,f,indent=4)

# To change password for both Users and Admin

def change_password(username):

    print("--- CHANGE PASSWORD ---\n")
    new_pass = input("Enter the new password :")
    retype_new = input("Re-type new password :")
    while new_pass != retype_new:
        print("Passwords mismatch !")
        new_pass = input("Enter the new password :")
        retype_new = input("Re-type new password :")
    print("Please confirm to change the password :")
    print("1. Yes")
    print("2. No")
    confirm_change = input("Enter your choice : ")
    if confirm_change == '1'or confirm_change== 'yes':
        if username == 'admin':
            users['admin']['password'] = new_pass
        else:
            users['active_users'][username]['password'] = new_pass
        update_users(users)
        print(" *** PASSWORD CHANGED !!! ***")
        return
    elif confirm_change == '2' or confirm_change =='no':
        return
    else:
        print("Invalid choice \n")
        time.sleep(0.5)
        return

# Entry Point of the Code

users = get_users()                # Loading or creating admin data
user = Banksystem(users)           # Instantiating BankSystem class

def main_menu():
    session_active = True
    while session_active:
        try:
            print("************ BANK MANAGEMENT SYSTEM **********")
            print("1. Register ")
            print("2. Login")
            print("3. Exit")
            choice = int(input("Enter your choice :"))
            if choice == 1:
                user.register_user()
            elif choice == 2:
                user.login_user()
            elif choice == 3:
                print("\n ****** Exiting !!! ******".upper())
                session_active= False
                quit()
            else:
                print("Invalid choice , enter a number between 1-3")
        except Exception:
            print("Invalid input ")

main_menu()       # Calls main_menu until final exit