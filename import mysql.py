import mysql.connector

def test_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Change this to your MySQL username
            password=""  # Enter your MySQL password
        )
        if connection.is_connected():
            print("✅ Connected to MySQL successfully!")
    except mysql.connector.Error as error:
        print("❌ Failed to connect:", error)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

test_connection()
