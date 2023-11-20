import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import random
import string
import sqlite3

class BankingApplication:
    def __init__(self):
        self.current_user = None
        self.current_balance = 0
        self.conn = sqlite3.connect('your_database_file.db')
        self.create_tables()

    def create_tables(self):
        # Create the users table if it doesn't exist
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    bank_pin TEXT NOT NULL,
                    password TEXT NOT NULL,
                    balance REAL DEFAULT 0
                )
            ''')

    def generate_password(self):
        password_length = 8
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(password_length))

    def register(self, username, bank_pin, password):
        with self.conn:
            self.conn.execute('INSERT INTO users (username, bank_pin, password, balance) VALUES (?, ?, ?, 0)',
                              (username, bank_pin, password))

    def login(self, username, bank_pin, password):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM users WHERE username=? AND bank_pin=? AND password=?',
                                       (username, bank_pin, password))
            data = cursor.fetchone()
            if data:
                self.current_user = username
                return True
            return False

    def check_balance(self):
        with self.conn:
            cursor = self.conn.execute('SELECT balance FROM users WHERE username=?', (self.current_user,))
            self.current_balance = cursor.fetchone()[0]

    def deposit(self, amount):
        with self.conn:
            cursor = self.conn.execute('SELECT balance FROM users WHERE username=?', (self.current_user,))
            current_balance = cursor.fetchone()[0]
            new_balance = current_balance + amount
            self.conn.execute('UPDATE users SET balance=? WHERE username=?', (new_balance, self.current_user))
            self.current_balance = new_balance

    def withdraw(self, amount):
        with self.conn:
            cursor = self.conn.execute('SELECT balance FROM users WHERE username=?', (self.current_user,))
            current_balance = cursor.fetchone()[0]
            if current_balance >= amount:
                new_balance = current_balance - amount
                self.conn.execute('UPDATE users SET balance=? WHERE username=?', (new_balance, self.current_user))
                self.current_balance = new_balance

    def record_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('TransactionLog.txt', 'a') as file:
            file.write(f"{timestamp} - {self.current_user} - {transaction_type} - Amount: R{amount}\n")

    def update_password(self, username, new_password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE users SET password=? WHERE username=?', (new_password, username))
            self.conn.commit()

    def forgot_password(self, username):
        with self.conn:
            cursor = self.conn.execute('SELECT password FROM users WHERE username=?', (username,))
            data = cursor.fetchone()
            if data:
                return data[0]
            return None

    def __del__(self):
        self.conn.close()


class BankingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking Application")
        self.master.geometry("800x600")  # Set the size of the main window
        self.banking_app = BankingApplication()
        self.master.configure(bg='light blue')

        # Create a LabelFrame for better organization
        self.label_frame = tk.LabelFrame(self.master, text="Welcome to the Midnight Coders \n "" \n Banking Application", font= ('broadway', 20, 'bold'), padx=70, pady=70)
        self.label_frame.pack(padx=70, pady=70)

        # Create widgets inside the LabelFrame
        self.label = tk.Label(self.label_frame, text="Select an option:", font=('broadway,12'))
        self.label.pack(pady=10)

        self.register_button = tk.Button(self.label_frame, text="Register", command=self.register, width=20)
        self.register_button.pack(pady=10)
        self.register_button.configure(bg='pink')

        self.login_button = tk.Button(self.label_frame, text="Login", command=self.login, width=20)
        self.login_button.pack(pady=10)
        self.login_button.configure(bg='pink')

        self.forgot_password_button = tk.Button(self.label_frame, text="Forgot Password", command=self.forgot_password, width=20)
        self.forgot_password_button.pack(pady=10)
        self.forgot_password_button.configure(bg='pink')

        self.exit_button = tk.Button(self.label_frame, text="Exit", command=self.master.destroy, width=20)
        self.exit_button.pack(pady=10)
        self.exit_button.configure(bg='pink')

    def register(self):
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("500x400")  # Set the size of the register window
        register_window.configure(bg='light blue')  # Corrected the method name

        # Username
        username_label = tk.Label(register_window, text="Enter a username:", font=("Arial", 12))
        username_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.username_entry = tk.Entry(register_window, font=("Arial", 10))
        self.username_entry.pack(pady=10)  # Added padding in the y-direction for spacing

        # PIN
        pin_label = tk.Label(register_window, text="Enter a 4-digit bank PIN:", font=("Arial", 12))
        pin_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.pin_entry = tk.Entry(register_window, show="*", font=("Arial", 10))
        self.pin_entry.pack(pady=10)  # Added padding in the y-direction for spacing
        register_button = tk.Button(register_window, text="Register", command=self.perform_registration, width=15)
        register_button.pack(pady=10)


    def perform_registration(self):
        username = self.username_entry.get()
        bank_pin = self.pin_entry.get()

        if not bank_pin.isdigit() or len(bank_pin) != 4:
            messagebox.showerror("Registration Error", "Invalid PIN. Please enter a 4-digit number.")
            return

        if not username:
            messagebox.showerror("Registration Error", "Please enter a username.")
            return

        password = self.banking_app.generate_password()
        self.banking_app.register(username, bank_pin, password)
        messagebox.showinfo("Registration", f"Registration successful!\nYour password is: {password}")
        self.master.deiconify()  # Show main window

    def login(self):
        self.master.withdraw()  # Hide main window
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.geometry("500x400")  # Set the size of the login window
        login_window.configure(bg='lightblue')

        username_label = tk.Label(login_window, text="Enter your username:", font=("Arial", 10))
        username_label.pack()

        self.username_entry = tk.Entry(login_window, font=("Arial", 12))
        self.username_entry.pack()

        pin_label = tk.Label(login_window, text="Enter your 4-digit bank pin:", font=("Arial", 10))
        pin_label.pack()

        self.pin_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
        self.pin_entry.pack()

        password_label = tk.Label(login_window, text="Enter your password:", font=("Arial", 10))
        password_label.pack()

        self.password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
        self.password_entry.pack()

        login_button = tk.Button(login_window, text="Login", command=self.perform_login, width=15)
        login_button.pack(pady=10)

    def perform_login(self):
        username = self.username_entry.get()
        bank_pin = self.pin_entry.get()
        password = self.password_entry.get()
        if self.banking_app.login(username, bank_pin, password):
            messagebox.showinfo("Login", "Login successful!")
            self.show_transaction_options()
        else:
            messagebox.showerror("Login Error", "Invalid username, bank pin, or password.")
            self.master.deiconify()  # Show main window

    def show_transaction_options(self):
        self.master.withdraw()  # Hide main window
        transaction_window = tk.Toplevel(self.master)
        transaction_window.title("Transactions")
        transaction_window.geometry("500x400")  # Set the size of the transaction window
        transaction_window.configure(bg='light blue')

        check_balance_button = tk.Button(transaction_window, text="Check Balance", command=self.check_balance, width=20)
        check_balance_button.pack(pady=10)
        check_balance_button.configure(bg='pink')

        deposit_button = tk.Button(transaction_window, text="Deposit", command=self.open_deposit_window, width=20)
        deposit_button.pack(pady=10)
        deposit_button.configure(bg='pink')


        withdraw_button = tk.Button(transaction_window, text="Withdraw", command=self.open_withdraw_window, width=20)
        withdraw_button.pack(pady=10)
        withdraw_button.configure(bg='pink')

        exit_button = tk.Button(transaction_window, text="Exit", command=self.master.destroy, width=20)
        exit_button.pack(pady=10)
        exit_button.configure(bg='pink')

    def check_balance(self):
        self.banking_app.check_balance()
        messagebox.showinfo("Balance", f"Your current balance is: R{self.banking_app.current_balance}")

    def open_deposit_window(self):
        deposit_window = tk.Toplevel(self.master)
        deposit_window.title("Deposit")
        deposit_window.geometry("300x200")  # Set the size of the deposit window
        deposit_window.configure(bg='light blue')

        # Create labels with font
        amount_label = tk.Label(deposit_window, text="How much would you like to deposit? R", font=("Arial", 12))
        amount_label.pack(pady=10)

        # Create an entry for the user to input the amount
        amount_entry = tk.Entry(deposit_window, font=("Arial", 12))
        amount_entry.pack(pady=10)

        # Create a button to submit the deposit
        deposit_button = tk.Button(deposit_window, text="Deposit",
                                   command=lambda: self.perform_deposit(amount_entry.get()), width=15)
        deposit_button.pack(pady=10)
        deposit_button.configure(bg='pink')

    def perform_deposit(self, amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Invalid deposit amount.")
                return

            self.banking_app.deposit(amount)
            self.banking_app.record_transaction("Deposit", amount)
            self.check_balance()
            messagebox.showinfo("Deposit", f"Deposited R{amount}. Current Balance: R{self.banking_app.current_balance}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def open_withdraw_window(self):
        withdraw_window = tk.Toplevel(self.master)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("300x200")  # Set the size of the withdraw window
        withdraw_window.configure(bg='light blue')

        # Create labels with font
        amount_label = tk.Label(withdraw_window, text="How much would you like to withdraw? R", font=("Arial", 12))
        amount_label.pack(pady=10)

        # Create an entry for the user to input the amount
        amount_entry = tk.Entry(withdraw_window, font=("Arial", 12))
        amount_entry.pack(pady=10)

        # Create a button to submit the withdrawal
        withdraw_button = tk.Button(withdraw_window, text="Withdraw",
                                    command=lambda: self.perform_withdraw(amount_entry.get()), width=15)
        withdraw_button.pack(pady=10)
        withdraw_button.configure(bg='pink')

    def perform_withdraw(self, amount_str):
        try:
            amount = float(amount_str)
            if amount < 10 or amount % 1 != 0:
                messagebox.showerror("Error",
                                     "Invalid withdrawal amount. Please enter a whole number greater than or equal to R10.")
                return

            if amount > self.banking_app.current_balance:
                messagebox.showerror("Error",
                                     "Withdrawal amount exceeds the current balance. Please enter another amount.")
                return

            self.banking_app.withdraw(amount)
            self.banking_app.record_transaction("Withdrawal", amount)
            self.check_balance()
            messagebox.showinfo("Withdraw",
                                f"Withdrew R{int(amount)}. Current Balance: R{self.banking_app.current_balance}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def forgot_password(self):
        username = simpledialog.askstring("Forgot Password", "Enter your username:")
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        result = self.banking_app.forgot_password(username)
        if result:
            messagebox.showinfo("Password Reset", f"Your new password is: {result}")
        else:
            messagebox.showerror("Error", "Username not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()