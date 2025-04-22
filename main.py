def banking_menu():
    print("\nPlease choose an option below")
    print("1. Sign in")
    print("2. login")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check your balance")
    print("6.EXIT")
import mysql.connector

def sign_in():
    username = input("Create a username ")
    password = input('Create a password ')
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            user="root",       
            password="10Bluepizz@",  
            database="bank"
        )
        cursor = connection.cursor()

        query = "INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)"
        values = (username, password, 0) 

        cursor.execute(query, values)
        connection.commit()

        print('Account has been created succesfully!')

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def login(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="10Bluepizz@", 
            database="bank"
        )
        cursor = connection.cursor()

        # Query to fetch the user data
        query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()  # Fetch one user matching the criteria

        if user:
            print("Login successful!")
            return user[0]  # Return the user_id (first element of the tuple)
        else:
            print("Invalid username or password")
            return None  # Return None if login fails

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
from decimal import Decimal

def deposit(user_id, deposit_amount):
    try:
        # Convert deposit_amount to a Decimal to avoid type mismatch
        deposit_amount = Decimal(deposit_amount)

        connection = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="10Bluepizz@", 
            database="bank"
        )
        cursor = connection.cursor()

        # Get the current balance
        cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        current_balance = cursor.fetchone()[0]

        # Convert current_balance to Decimal to ensure type consistency
        current_balance = Decimal(current_balance)

        # Calculate the new balance
        new_balance = current_balance + deposit_amount

        # Update the user's balance in the database
        update_balance_query = "UPDATE users SET balance = %s WHERE id = %s"
        cursor.execute(update_balance_query, (new_balance, user_id))

        # Record the transaction in the transactions table
        transaction_query = "INSERT INTO transactions (user_id, amount, transaction_type) VALUES (%s, %s, %s)"
        cursor.execute(transaction_query, (user_id, deposit_amount, 'Deposit'))

        connection.commit()
        print(f"Deposit successful! New balance: {new_balance}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    user_id = None  # Track the logged-in user

    while True:
        banking_menu()
        choice = input("Enter your choice: ")

        if choice == '1':  # Sign in
            sign_in()

        elif choice == '2':  # Login
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = login(username, password)  # Save the user_id upon successful login
            if user_id:
                print("Login successful!")
            else:
                print("Login failed. Try again.")

        elif choice == '3':  # Deposit
            if user_id:  # If the user is logged in
                try:
                    deposit_amount = float(input("Enter the amount to deposit: "))
                    if deposit_amount > 0:
                        deposit(user_id, deposit_amount)
                    else:
                        print("Please enter a valid deposit amount.")
                except ValueError:
                    print("Invalid input. Please enter a valid number for the deposit.")
            else:
                print("Please log in first.")

        elif choice == '6':  # Exit
            print('Thanks for using the banking app. Goodbye!')
            break
        else:
            print('Option not implemented yet. Please choose something else for now.')
main()