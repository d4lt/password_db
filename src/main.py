import mysql.connector as mysql
import sys


 #!                                                         loggin in
db = None
setted = False
while not setted:
    default_config = (input("Use the default configuration? (Y/N)")).strip()
    if default_config.lower() == "y":
        default_config = True
        setted = True
    elif default_config.lower() == "n":
        default_config = False
        setted = True
    else:
        print("Please just put Y or N on the input")

while db is None:
    try:
        if default_config:

            db_password = (input("Database password: ")).strip()
            db = mysql.connect(
                host="localhost",
                user="root",
                password = db_password,
                database = "Passwords_DB"
            )

        else:

            db_name = (input("Database name: ")).strip()
            db_host = (input("Database host: ")).strip()
            db_user = (input("Database user: ")).strip()
            db_password = (input("Database password: ")).strip()

            db = mysql.connect(
                host="localhost",
                user="root",
                password = db_password,
                database = "Passwords_DB"
            )

    except Exception as e:
        print(f"Something went wrong.\nOr you just typed the wrong password.\n\nLog: {e}")



cursor = db.cursor()

# **                                           -------------Main Menu-------------
def main():

    while True:
        menu = (input("Menu:\n\n    Add a password. [add]\n    Update a password. [update]\n    See a password. [see]\n    Delete a password. [delete]\n    Exit. [exit]\n\n")).strip()

        if menu == 'add' or menu == 'update' or menu == 'delete' or menu == 'see':
            break
        elif menu == 'exit':
            sys.exit()
        else:
            print("\nPlease enter a option in the menu.")
        
    if menu == "add":
        print("\n\n\nNOTE: In the host name, type in the most literal way possible.\ne.g: 'GitHub'is the exact name of the site\n\n")
        host = (input("What is the host of your password ?: ")).strip()
        email = (input("What is the email of your password ?: ")).strip()
        password = (input("What is the password that you want to add?: ")).strip()
        add(host, email,  password)
        main()

    elif menu == "update":
        print("\n\n\nNOTE: In the host name, type in the most literal way possible.\ne.g: 'GitHub'is the exact name of the site\n\n")
        host = (input("What is the host of the password to update ?: ")).strip()
        email = (input("What is the email of the password to update ?: ")).strip()
        password = (input("Please, type the new password: ")).strip()
        update(host, email, password)
        main()
        
    elif menu == "see":
        print("\n\n\nNOTE: In the host name, type in the most literal way possible.\ne.g: 'GitHub'is the exact name of the site\n\n")
        host = (input("What is the host of the password ?: ")).strip()
        email = (input("What is the email of the password ?: ")).strip()
        see(host, email)
        main()

    elif menu == "delete":
        print("\n\n\nNOTE: In the host name, type in the most literal way possible.\ne.g: 'GitHub'is the exact name of the site\n\n")
        host = (input("What is the host of the password to be deleted ?: ")).strip()
        email = (input("What is the email of the password to be deleted ?: ")).strip()
        delete(host, email)
        main()


# **                                      -----------Functionalities-----------

# check if the host_name exists
def checkif_exists(hostname, email):
    cursor.execute(
        f"SELECT EXISTS (SELECT Host, Email FROM  passwords WHERE passwords.Host = '{hostname}' and passwords.Email = '{email}');"
    )
    for i in cursor:
        exists = i[0]

    return exists
    


def add(host, email, password):

    exists = checkif_exists(host, email)

    if exists:
        print(f"""A password for the host: "{host}" and email: "{email}" already exists.""")
        main()  # returns to the Menu
        return

    cursor.execute(
        f"INSERT INTO passwords (Host, Email, Password) VALUES ('{host}', '{email}', '{password}');"
        )
    db.commit()
    
    print("Password added.\n\n\n")


def update(host, email, password):

    exists = checkif_exists(host, email)

    if not exists:
        print("That password does not exists. \n\n\n")
        main()
        return


    cursor.execute(
        f"UPDATE passwords SET Password = '{password}' WHERE Host = '{host}' AND Email = '{email} ;"
    )
    db.commit()

    print(f"{host} password updated.\n\n\n")


def see(host, email):
    exists = checkif_exists(host, email)

    if not exists:
        print("Such host does not exists.\n Or you just typed the wrong name.\n\n\n")
        main()
        return

    cursor.execute(
        f"SELECT * FROM passwords WHERE passwords.Host = '{host}' AND passwords.Email = '{email}';"
    )

    for i in cursor:
        print(f"\n\nHost: {i[0]}\nEmail: {i[1]}\nPassword: {i[2]}\n\n\n")


def delete(host, email):
    exists = checkif_exists(host, email)

    if not exists:
        print("Such host does not exists.\n Or you just typed the wrong name.\n\n\n")
        main()
        return
    
    cursor.execute(
        f"DELETE FROM passwords WHERE passwords.Host = '{host}' AND passwords.Email = '{email}';"
    )

    db.commit()

    print(f"\n\nThe password of {host} from the email  {email} has been deleted.\n\n\n")

    #!                                          -----------Program Execution-----------

if __name__ == '__main__':
    main()
