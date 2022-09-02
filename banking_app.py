# Things to do:

### Add a transaction system to the customer service
### Complete the already employee seciton

import json as j
import datetime
import os
import random

employee_file = "employee_data_set.json"
customer_file = "customer_data_set.json"
ID_filename = "ID.json"
Transaction_id_file = "Customer_transaction_id_file.json"

# Using the Employee and customer as an objects in order to use its unique features and obey the DRY 
class Employee:
    def __init__(self, firstname, lastname, age, branch, rule):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.branch = branch
        self.rule = rule

    def req_employee_detail(self):
        dic01 = {
            'firstname':self.firstname,
            'lastname':self.lastname,
            'age':self.age,
            'branch':self.branch,
            'rule':self.rule
        }
        return dic01
    def req_employee_file(self):
        pass

# This objetc is to define a customer, and also use its features through the program
class Customer():
    def __init__(self, firstname, lastname, age, username):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.username = username
        
    

    def req_customer_detail(self):
        dic01 = {
            'firstname':self.firstname,
            'lastname':self.lastname,
            'age':self.age,
        }
        return dic01

# to determine the categoty of the client
def determination():
    print("Customer-->(1)")
    print("Employee-->(2)") 
    Q1 = input('Enter your enquiry number:') 
    if Q1=='1':
        return customer_determination()
    elif Q1=='2':
        return logging_employee()
    else:
        print('Enquiry not recognised please try again!')
        return determination()
    
# Logging the employee to their correct side
def logging_employee():
    print('Already an employee-->(1)')
    print('New employee-->(2)')
    Q = input('Enter:')
    if Q=='1':
        pass
    elif Q=='2':
        return new_emp()
    else:
        return logging_employee()  # An error occures when using the while loop to return the client to determination when they make the third mistake  

# starting to register a new employee:
def new_emp():
    try:
        age = int(input('Enter your age:'))
    except ValueError:
        print('please enter your age in integer form.')
        return new_emp()
    firstname = input('Enter your firstname:')
    lastname = input('Enter your lastname:')
    branch = input('Enter your working branch:')
    rule = input('Enter your rule:')
    firstname02 = firstname.lower()
    lastname02 = lastname.lower()
    branch02 = branch.lower()
    rule02 = rule.lower() 
    return username_new_emp(firstname02, lastname02, branch02, rule02, age)

# This is to get the username of the new employee:
def username_new_emp(firstname, lastname, branch, rule, age):
    username = input("Enter your username:")
    if os.path.exists(employee_file):
        with open(employee_file) as f:
            load = j.load(f)
        load = dict(load)
        usernames = load.keys()
        if username in usernames:
            print('Please try another username!')
            return username_new_emp(firstname, lastname, branch, rule, age)
        else:
            employee = Employee(firstname, lastname, branch, rule, age)
            value = dict(employee.req_employee_detail())
            load.update({username: value})
            with open(employee_file, 'w')as f2:
                j.dump(load, f2)
            return password_new_emp(username, firstname, lastname)
    else:
        employee= Employee(firstname, lastname, age, branch, rule)
        value = dict(employee.req_employee_detail())
        dic = dict({username:value})
        with open(employee_file, 'w')as f3:
            j.dump(dic, f3)
        return password_new_emp(username, firstname, lastname)

# This secition sets the password for the new employee in order to be used later on when trying to enter the system.           
def password_new_emp(username, firstname, lastname):
    print('Do not consist your name or lastname in the password!')
    password1 = input('Enter your password:')
    password2 = input('Re-enter your password:')
    if password1==password2:
        password3=password1.lower()
        if firstname in password3:
            if lastname in password3:
                print('Remove your firstname and lastname')
                return password_new_emp(username, firstname, lastname)
            else:
                print('remove your firstname!')
                return password_new_emp(username, firstname, lastname)
        elif lastname in password3:
            print("Remove your lastname!")
            return password_new_emp()
        else:
            if os.path.exists(employee_file):
                with open(employee_file)as f:
                    load = j.load(f)
                load = dict(load)
                load[username].update({'password':password1})
                with open(employee_file, 'w')as f2:
                    j.dump(load, f2)
            else:
                print('Sorry and error has occured!')
                return determination()

    else:
        print("Passwords dont match!")
        return password_new_emp(username, firstname, lastname)
    return generating_id(username)

# This section will generate a unique ID for each employee in which will faciliatate the recognistion of the employees ID.
def generating_id(username):
    ID = random.randint(1000, 9999)
    if os.path.exists(ID_filename):
        with open(ID_filename)as f:
            load = j.load(f)
        load = dict(load)
        if ID in load['ID']:
           return generating_id()
        else:
            load['ID'].append(ID)
            with open(ID_filename, 'w')as f2:
                j.dump(load, f2)
            with open(employee_file)as f3:
                dic = j.load(f3)
            dic = dict(dic)
            dic[username].update({'ID':ID})
            with open(employee_file, 'w')as f4:
                j.dump(dic, f4)
            print('All has been set, Welcome!')
    else:
        load02 = {
            "ID":[ID]
        }
        with open(ID_filename, 'w')as f5:
            j.dump(load02, f5)
        with open(employee_file)as f6:
            load03 = j.load(f6)
        load03 = dict(load03)
        load03[username].update({"ID":ID})
        with open(employee_file, 'w')as file:
            j.dump(load03, file)
        print("All has been set, Welcome!")


def already_emp_login(): 
    print('Welcome employee!')
    print()
    if os.path.exists(employee_file):
        with open(employee_file)as f:
            load = j.load(f)
        load = dict(load)
        usernames = load.keys()
        username = input('Enter your username:')
        password = input('Enter your password:')
        if username in usernames:
            password_confirm = load[username]["password"]
            ID_confirm = load[username]['ID']
            if password==password_confirm:
                def id_confirm(ID_confirm):
                    try:
                        ID = int(input('Enter your ID:'))
                        if ID==ID_confirm:
                            print("Welcome to your account:")
                            return already_employee_features(username)
                    except ValueError:
                        print("Your ID is an integer value!")
                        return id_confirm(ID_confirm)
                return id_confirm(ID_confirm)    
            else:
                print("Account not been found!")
                return already_emp_login()
        else:
            print("Account not been found! ")
            return already_emp_login()


def already_employee_features(username):
    print("Deposit Money-->(1)") 
    print("Remove account-->(2)")
    print("Recover password-->(3)")
    print("Show balance-->(4)")
    print("Open account-->(5)")
    print("Transact money-->(6)")
    service = input("Input the service code:")
    if service=='1':
        pass
    elif service=='2':
        pass
    elif service=='3':
        pass
    elif service=='4':
        pass
    elif service=='5':
        pass
    elif service=='6':
        pass
    else:
        print("Please enter one of the services above!")
        return already_employee_features(username)

# This part leads the clients to their correct and desired service!
def customer_determination():
    print("New customer-->(1)")
    print("Already customer-->(2)")
    print("To exit, type 'exit'")
    Question = input('Enter your enquiry:')
    if Question=='1':
        return new_customer()
    elif Question=='2':
        return already_customer()
    elif Question=='exit':
        return determination()
    else:
        print("Enquiry not recognised!")
        return customer_determination()

# This part creates and receives the details for the new customers joining the serivice!
def new_customer():
    try:
        age = int(input('Enter your age:'))
    except ValueError:
        print("Enter the age as an integer!")
        return new_customer()
    firstname = input('Enter your firstname:')
    lastname = input('Enter your lastname:')
    firstname02 = firstname.lower()
    lastname02 = lastname.lower()

    return customer_username(age, firstname02, lastname02)

# This part is the continue of the previous section for completing the new customers account
def customer_username(age, firstname, lastname):
    username = input("Enter your username:")
    if os.path.exists(customer_file):
        with open(customer_file)as f:
            load = j.load(f)
        load = dict(load)
        usernames = load.keys()
        if username in usernames:
            print("please try another username!")
            return customer_username(age, firstname, lastname)
        else:
            customer = Customer(firstname, lastname, age, username)
            load.update({username:customer.req_customer_detail()})
            with open(customer_file, 'w')as f2:
                j.dump(load, f2)
            return customer_password(username, firstname, lastname)
    else:
        dic_customer = {
            username:{
                'firstname':firstname,
                'lastname':lastname,
                'age':age,
            }
        }
        with open(customer_file, 'w')as f3:
            j.dump(dic_customer, f3)
        return customer_password(username, firstname, lastname)

# This is the final part for creating the customers account and it completes the process by opening the files
def customer_password(username, firstname, lastname):
    print("Don't include your firstname or lastname in the password!")
    password1 = input('Enter your password:')
    password02 = input('Re-enter your password:')
    if password1==password02:
        password03=password02.lower()
        if firstname in password03:
            if lastname in password03:
                print('Remove your firstname and lastname!')
                return customer_password(username, firstname, lastname)
            else:
                print("Remove your firstname!")
                return customer_password(username, firstname, lastname)
        else:
            key_word = input('Enter a key word to be remebered:')
            if os.path.exists(customer_file):
                with open(customer_file)as f:
                    load = j.load(f)
                load = dict(load)
                load[username].update({'password':password02})
                load[username].update({'Key_word':key_word})
                with open(customer_file, 'w')as f2:
                    j.dump(load, f2)
                path = 'C:\\Users\\ALI\\Desktop\\Visualstudio'
                path02 = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
                add_file = f'{username}_add.txt'
                remove_file = f'{username}_remove.txt'
                statement = f'{username}_statement.txt'
                os.chdir(path)
                newfolder = f'{username}'
                os.makedirs(newfolder)
                os.chdir(path02)
                open(add_file, 'x')
                open(remove_file, 'x')
                open(statement, 'x')                
                os.chdir(path)
                return generating_transaction_id(username)
            else:
                print("An error has occured!")
                return determination()
    else:
        print("Your passwords doesn't match!")
        return customer_password(username, firstname, lastname)

# This section has assigend a specific transaction ID to the customer so when a money was going to be transferred into their account, the other user will use this particular id in order to deposit the money
def generating_transaction_id(username):
    transaction_ID = random.randint(10000, 99999)
    if os.path.exists(Transaction_id_file):
        with open(Transaction_id_file)as f:
            load = j.load(f)
        load = dict(load)
        transaction_IDs = load['ID']
        if transaction_ID in transaction_IDs:
            return generating_transaction_id(username)
        else:
            load["ID"].append(transaction_ID)
            with open(Transaction_id_file, 'w')as f2:
                j.dump(load, f2)
            if os.path.exists(customer_file):
                with open(customer_file)as f3:
                    dic01 = j.load(f3)
                dic01 = dict(dic01)
                dic01[username].update({f"transaction_ID":transaction_ID})
                with open(customer_file, 'w')as f4:
                    j.dump(dic01, f4)
                print('All has been set but please remember your transaction ID for future use!')
                print(f"Your transaction ID is: {transaction_ID}")
            else:
                print('An error has occured! 1')
                return determination()
    else:
        dic02 = {
            "ID":[transaction_ID]
        }
        with open(Transaction_id_file, 'w')as f5:
            j.dump(dic02, f5)
        if os.path.exists(customer_file):
            with open(customer_file)as f6:
                data = j.load(f6)
            data = dict(data)
            data[username].update({"transaction_ID":transaction_ID})
            with open(customer_file, 'w')as f7:
                j.dump(data, f7)
            print('All has been set but please remember your transaction ID for future use!')
            print(f"Your transaction ID is: {transaction_ID}")
        else:
            print('An error has occured! 2')
            return determination()   

# This part provies service to the ones who are already customers in this system    
def already_customer():
    username = input('Enter your username:')
    password = input('Enter your password:')
    if os.path.exists(customer_file):
        with open(customer_file)as f:
            load = j.load(f)
        load = dict(load)
        usernames = load.keys()
        if username in usernames:
            password_confirm = load[username]['password']
            if password==password_confirm:
                return customer_service(username, password)
            else:
                print("Username or password doesnt match!")
                return already_customer()
        else:
            print("account not found!")
            return already_customer()

# This section, allows the customers to be despersed and be transfered to the sections they want to go to do their enquiries after entering the correct login details in already_customer()
def customer_service(username, password):
    print("Deposit money--(1)")
    print('Remove money-->(2)')
    print('Forgot password-->(3)') 
    print('Get statement-->(4)')   
    print('Remove account-->(5)')
    print('show balance-->(6)')
    print("Transfer money-->(7)")
    print('If you want to exit the service, please type \'exit\'')
    print()

    Question = input('Enter your enquiry:')
    if Question=='1':
        return deposit_money(username, password)
    elif Question=='2':
        return remove_money(username, password)
    elif Question=='3':
        return forgot_password(username, password)
    elif Question=='4':
        return get_statement(username)
    elif Question=='5':
        return remove_account(username, password)
    elif Question=='6':
        print(f'balance: {check_balance(username, password)}')
    elif Question=='7':
        pass
    elif Question=='exit':
        return customer_determination()
    else:
        print('Enquiry not recognised!')
        return customer_service(username, password)

# This section deposits money by inputing the amount and then adds it to the designated folder and file
def deposit_money(username, password):
    try:
        amount = int(input("Enter the amount:"))
        path = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
        add_file_name = f"{username}_add.txt"
        statement_file_name = f"{username}_statement.txt"
        os.chdir(path)
        with open(add_file_name, 'a')as f:
            f.write(f'{amount}\n')
        x = datetime.datetime.now()
        with open(statement_file_name, 'a')as f2:
            f2.write(f'+{amount}, {x.strftime("%c")}\n')
        print("Your money has been deposited!")
        print("Do you want to deposit any more money? y/n")      
        Question =input('Enter:')
        if Question=='y':
            return deposit_money(username, password)
        elif Question=='n':
            return customer_service(username, password)
        else:
            print("resonse not recognised!")
            return customer_service(username, password)  
     
    except ValueError:
        print("Please enter an integer amount!")
        return deposit_money(username)

# This section removes the money from the balance if there is enough money to be removed
def remove_money(username, password):
    try:
        x = datetime.datetime.now()
        add_list1 = []
        add_list2 = []
        add_list3 = []
        remove_list1 = []
        remove_list2 = []
        remove_list3 = []
        amount = int(input('Enter:'))
        path = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
        add_file = f'{username}_add.txt'
        remove_file = f'{username}_remove.txt'
        statement_file = f'{username}_statement.txt'
        os.chdir(path)
        if os.path.exists(add_file):
            with open(add_file)as f:
                adds = f.readlines()
            if len(adds)==0:
                print("You dont have any money to remove!")
                return determination()
            else:
                for add_num1 in adds:
                    add_list1.append(add_num1[:-1])
                for add_num2 in add_list1:
                    add_list2.append(int(add_num2))
                add_test_balance = 0
                for add_num3 in add_list2:
                    add_test_balance= add_test_balance+add_num3
                    add_list3.append(add_test_balance)
                    total_deposit = add_list3[-1]
        else:
            print("An error has occured on finding the relevant section of your account!")
            return determination()
        if os.path.exists(remove_file):
            with open(remove_file)as f2:
                removes = f2.readlines()
            if len(removes)==0:
                total_remove = 0
                balance = total_deposit-total_remove
                if amount>balance:
                    print('You dont have enough balance for this money remove!')
                    return remove_money(username)
                elif amount<=balance:
                    if os.path.exists(remove_file):
                        with open(remove_file, 'a')as f3:
                            f3.write(f'{amount}\n')
                    else:
                        print("An error has occured on finding the relevant section of your account!")
                        return determination()
                    if os.path.exists(statement_file):
                        with open(statement_file, 'a')as f4:
                            f4.write(f'-{amount}, {x.strftime("%c")}\n')
                        print('Your money has been removed!')
                        return customer_service(username, password)
                    else:
                        print("An error has occured on finding the relevant section of your account!")
                        return determination()
            else:
                for remove_num1 in removes:
                    remove_list1.append(remove_num1[:-1])
        
                for remove_num2 in remove_list1:
                    remove_list2.append(int(remove_num2))
        
                remove_test_balance = 0
                for remove_num3 in remove_list2:
                    remove_test_balance = remove_test_balance+remove_num3
                    remove_list3.append(remove_test_balance)
                total_remove = remove_list3[-1]
                balance = total_deposit-total_remove
                if amount>balance:
                    print("You dont have enough balance!")
                    return remove_money(username)
                elif amount<=balance:
                    if os.path.exists(remove_file):
                        with open(remove_file, 'a')as f3:
                            f3.write(f'{amount}\n')
                        
                    else:
                       print("An error has occured on finding the relevant section of your account!")
                       return determination()
                    if os.path.exists(statement_file):
                        with open(statement_file, 'a')as f4:
                            f4.write(f'-{amount}, {x.strftime("%c")}\n')
                        print('your money has been removed!')
                        return customer_service(username, password)
                    else:
                        print("An error has occured on finding the relevant section of your account!")
                        return determination()
    except ValueError:
        print("Please enter an integer amount!")
        return remove_money(username, password)

# This section will recover the password by inputing some detailes from the user then it will ask for the new password and then updates the system
def forgot_password(username, password):
    Key= input("Enter the key name to recover your password:")
    with open(customer_file)as f:
        load = j.load(f)
    load = dict(load)
    key_confirm = load[username]['Key_word'] 
    firstname = load[username]['firstname']
    lastname = load[username]['lastname']
    def recover_password():
        print("Dont include your name or lastname in the password!")
        new_password1 = input('Enter the new password:')
        new_password2 = input('Re-enter the password:')
        if new_password2==new_password1:
            new_password3 = new_password1.lower()
            if firstname in new_password3:
                if lastname in new_password3:
                    print('Remove your name and lastname!')
                    return recover_password()
                else:
                    print('Dont include your firstname or lastname!')
            elif lastname in new_password3:
                print('Dont include your firstname or lastname!')
                return recover_password()
            else:
                if os.path.exists(customer_file):
                    with open(customer_file)as f2:
                        load02 = j.load(f2)
                    load02 = dict(load02)
                    load02[username]['password']=new_password2
                    with open(customer_file, 'w')as f3:
                        j.dump(load02, f3)
                    print("The new password has been set!")
                    return customer_service(username, password)
                else:
                    print("An error has occured!")
                    return determination()
        else:
            print("passwords dont match!")
            print()
            return recover_password()
    if Key==key_confirm:
        return recover_password()
    else:
        print("The key term donsn't match!")
        return forgot_password(username, password)

# This section will output the statement of all deposit and removals by their correct dates
def get_statement(username):
    path = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
    file_name = f'{username}_statement.txt'
    os.chdir(path)
    with open(file_name)as f:
        text = f.readlines()
    print(text)

# This section will show the balance of the account by reading the history of the files and by subtracting the total removes from the total adds to represnt the final account balance.
def check_balance(username, password):
    path = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
    add_file = f'{username}_add.txt'
    remove_file = f'{username}_remove.txt' 
    os.chdir(path)
    add_list1 = []
    add_list2 = []
    add_list3 = []
    remove_list1 = []
    remove_list2 = []
    remove_list3 = []
    if os.path.exists(add_file):
        with open(add_file)as f:
            adds = f.readlines()
        if len(adds)==0:
            no_balance = 0
            return no_balance
        else:
            for add_num1 in adds:                         
                add_list1.append(add_num1[:-1])
            for add_num2 in add_list1:
                add_list2.append(int(add_num2))
            add_test_balance = 0
            for add_num3 in add_list2:
                add_test_balance = add_test_balance+add_num3
                add_list3.append(add_test_balance)
            total_deposit = add_list3[-1]
    else:
        print('An error has occured!')
        return determination()
    if os.path.exists(remove_file):
        with open(remove_file)as f2:
            removes = f2.readlines()
        for remove_num1 in removes:
            remove_list1.append(remove_num1[:-1])
        for remove_num2 in remove_list1:
            remove_list2.append(int(remove_num2))
        
        remove_test_balance = 0
        for remove_num3 in remove_list2:
            remove_test_balance = remove_test_balance+remove_num3
            remove_list3.append(remove_test_balance)
        total_remove = remove_list3[-1]
        balance = total_deposit - total_remove
        return balance
    else:
        print('An error has occured!')
        return determination()

# This section will removes the account from customer file history and all the respective files and folder after ensuring the user has removed all their money from their account before closing the account!
def remove_account(username, password):
    
    main_path =f"C:\\Users\\ALI\\Desktop\\Visualstudio"
    password = input('Enter your password:')
    os.chdir(main_path)
    if os.path.exists(customer_file):
        with open(customer_file)as f:
            load = j.load(f)
        load = dict(load)
        password_confirm = load[username]['password']
    else:
        print("An error has occured! 00")
        return determination()

    if password==password_confirm:
        key = input("Enter the key word:")
        key_confirm = load[username]['Key_word']
        if key==key_confirm:
            balance = check_balance(username, password)
            if balance==0:
                Questiion = input('Are you sure you want to remove your account? (y/n)--->')
                if Questiion=='y':
                    path = f"C:\\Users\\ALI\\Desktop\\Visualstudio\\{username}"
                    
                    add_file = f'{username}_add.txt'
                    remove_file = f'{username}_remove.txt'
                    statement_file = f'{username}_statement.txt'
                    os.chdir(path)
                    if os.path.exists(add_file):
                        os.remove(add_file)
                    else:
                        print("An error has occured 01")
                        return determination()
                    if os.path.exists(remove_file):
                        os.remove(remove_file)
                    else:
                        print("An error has occured 02")
                        return determination()
                    if os.path.exists(statement_file):
                        os.remove(statement_file)
                    else:
                        print("An error has occured 03")
                        return determination()
                    os.chdir(main_path)
                    os.rmdir(username)
                    if os.path.exists(customer_file):
                        with open(customer_file)as f2:
                            load2 = j.load(f2)
                        load2 = dict(load2)
                        del load2[username]
                        with open(customer_file, 'w')as f3:
                            j.dump(load2, f3)
                        print('Your account has been removed!')
                        return determination()
                    else:
                        print("An error has occured! 04")
                        return determination()
    
                elif Questiion=='n':
                    print("Thank you for not removing your account!")
                    return determination()

                else:
                    print('Response not recognised!')
                    return remove_account(username, password)
            else:
                print(f"you stil have {balance} in your account!")
                print(f"You need to remove {balance} from your account!")
                return remove_money(username, password)
                
        else:
            print("Your key word doesnt match please try again!")
            return remove_account(username, password)
    else:
        print("Your password doesnt match!")
        return remove_account(username, password)

def transfer_money(username):
    pass

determination()

