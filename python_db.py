import mysql.connector
import getpass
import random
import hashlib

#connect to specific database
def connect_to_database(database):
    connection = mysql.connector.connect(host="localhost", user="root", passwd="", database=database)
    print("successfuly connected to {}".format(database))
    return connection

#get id for specific user
def get_user_id(connection, name, email):
    mycursor = connection.cursor()
    query = "select id from users where name = '{}' and email = '{}'".format(name, email)
    mycursor.execute(query)
    result = mycursor.fetchone()
    return result[0]

#generate code for verification 
def generate_verification_code(connection, user_id):
    mycursor = connection.cursor()
    random_num = random.randint(0, 100)
    #print(random_num)
    vc = hashlib.md5(str(random_num).encode())
    code = vc.hexdigest()
    #save the code in verification table
    query = "insert into verification_code(vc, user_id) values(%s, %s)"
    vals = (code, user_id)
    mycursor.execute(query, vals)
    connection.commit()
    return code

def get_user_verification_code(mycursor, user_id):
    query = "select vc from verification_code where user_id = '{}'".format(user_id)
    #val = (user_id)
    mycursor.execute(query)
    res = mycursor.fetchone()
    return res[0]

    
def verify_user(connection, user_id):
    mycursor = connection.cursor()
    query = "update users set verified = %s where id = %s"
    vals = (1, user_id)
    mycursor.execute(query, vals)
    connection.commit()

def login(connection, user_name, password):
    mycursor = connection.cursor()
    query = "select * from users where name = '{}' and password = '{}'".format(user_name, password)
    mycursor.execute(query)
    result = mycursor.fetchone()
    user_id = result[0]
    if(result):
        print("Welcome {}".format(result[1]))
        
        if(result[4] == 0):
            print("Your account is not verified yet! Would you like to verify it ?")
            action = int(input("Press 1 to verify, Press 2 to skip:"))
            if(action == 1):
                #get user verification code
                code = get_user_verification_code(mycursor, user_id)
                user_code = input("Please enter the following code: {}\n".format(code))
                if(user_code == code):
                    verify_user(connection, user_id)
                    print("Congratulations!! your account is verified now")   

    else:
        print("Username or Password might be error!")        


def register(connection, user_name, email, password):
    mycursor = connection.cursor()
    query = "insert into users(name, email, password) values(%s, %s, %s)"
    val = (user_name, email, password)
    mycursor.execute(query, val)
    connection.commit()
    print(mycursor.rowcount, "record inserted.")


def main():
    connection = connect_to_database("python_course")  
    while(True):
        print('''Welcome to the useres application\nIf you want to register press 1\nIf you want to login press 2''')
        action = int(input("Enter your choice:"))
        if(action == 1):
            name = input("Please enter your name:")
            email = input("Please enter your email:")
            password = input("Please enter your password:")
            register(connection, name, email, password)
            user_id = get_user_id(connection, name, email)
            vc = generate_verification_code(connection, user_id)
            print('''You are not verified yet\nIf you want to verify your account please this code {}'''.format(vc))
            code = input('Verification Code:')
            if(code == vc):
                verify_user(connection, user_id)
                print("Congratulations!! your account is verified now")
            else:
                break    
            connection.close()
            break
        elif(action == 2):
            name = input("Please enter your name:")
            password = getpass.getpass("Please enter your password:")
            login(connection, name, password)
            connection.close()
            break

main()