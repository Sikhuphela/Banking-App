class BankingApplication:
    def __init__(self):
        self.current_user = None
 
    def register(self):
        username = input("Enter a username: ")
        bank_pin = input("Enter a 4-digit bank pin: ")
        with open('BankData.txt', 'a') as file:
            file.write(f"{username},{bank_pin},0\n")
        print("Registration successful!")
 
    def login(self):
        username = input("Enter your username: ")
        bank_pin = input("Enter your 4-digit bank pin: ")
        with open('BankData.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == username and data[1] == bank_pin:
                    self.current_user = username
                    print("Login successful!")
                    return
        print("Invalid username or bank pin.")
 
    def check_balance(self):
        with open('BankData.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == self.current_user:
                    print(f"Your current balance is: R{data[2]}")
                    break
 
    def update_balance_and_log(self, new_balance, transaction):
        with open('BankData.txt', 'r') as file:
            lines = file.readlines()
        with open('BankData.txt', 'w') as file:
            for line in lines:
                data = line.strip().split(',')
                if data[0] == self.current_user:
                    file.write(f"{data[0]},{data[1]},{new_balance}\n")
                else:
                    file.write(line)
        with open('TransactionLog.txt', 'a') as file:
            file.write(f"{self.current_user},{transaction},{new_balance}\n")
 
    def deposit(self):
        try:
            amount = float(input("How much would you like to deposit? R"))
            if amount <= 0:
                print("Invalid deposit amount.")
                return
            with open('BankData.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if data[0] == self.current_user:
                        new_balance = float(data[2]) + amount
                        self.update_balance_and_log(new_balance, f"Deposit: +R{amount}")
                        print(f"Deposited R{amount}. Current Balance: R{new_balance}")
                        return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
 
    def withdraw(self):
        try:
            amount = float(input("How much would you like to withdraw? R"))
            if amount <= 0:
                print("Invalid withdrawal amount.")
                return
            with open('BankData.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if data[0] == self.current_user:
                        balance = float(data[2])
                        if amount > balance:
                            print("Insufficient balance.")
                            return
                        new_balance = balance - amount
                        self.update_balance_and_log(new_balance, f"Withdrawal: -R{amount}")
                        print(f"Withdrew R{amount}. Current Balance: R{new_balance}")
                        return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
 
    def start(self):
        while True:
            print("Welcome to the Banking Application")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
 
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
                if self.current_user is not None:
                    while True:
                        print("1. Check Balance")
                        print("2. Deposit")
                        print("3. Withdraw")
                        print("4. Exit")
                        trans_choice = input("Choose a transaction: ")
                        if trans_choice == "1":
                            self.check_balance()
                        elif trans_choice == "2":
                            self.deposit()
                        elif trans_choice == "3":
                            self.withdraw()
                        elif trans_choice == "4":
                            break
                        else:
                            print("Invalid transaction choice.")
            elif choice == "3":
                print("Thank you. Goodbye!")
                break
            else:
                print("Invalid choice.")
 
if __name__ == "__main__":
    banking = BankingApplication()
    banking.start()