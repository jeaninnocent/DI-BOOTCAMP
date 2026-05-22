class BankAccount:
    def __init__(self, username, password, initial_balance=0):
        # Part III additions
        self.username = str(username)
        self.password = str(password)
        self.authenticated = False
        
        # Part I
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.balance = initial_balance

    def authenticate(self, username, password):
        """Part III: Authenticates the user."""
        if self.username == username and self.password == password:
            self.authenticated = True
            return True
        return False

    def deposit(self, amount):
        """Part I & III: Adds to balance if authenticated and amount is positive."""
        if not self.authenticated:
            raise PermissionError("Action denied: You must be authenticated to deposit.")
        
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Deposit amount must be a positive integer.")
            
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Part I & III: Deducts from balance if authenticated and amount is positive."""
        if not self.authenticated:
            raise PermissionError("Action denied: You must be authenticated to withdraw.")
            
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive integer.")
            
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
            
        self.balance -= amount
        return self.balance


class MinimumBalanceAccount(BankAccount):
    def __init__(self, username, password, initial_balance=0, minimum_balance=0):
        # Part II: Initialize parent class, then add specific attribute
        super().__init__(username, password, initial_balance)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        """Part II: Overrides withdraw to enforce minimum balance."""
        if not self.authenticated:
            raise PermissionError("Action denied: You must be authenticated to withdraw.")
            
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive integer.")
            
        if (self.balance - amount) < self.minimum_balance:
            raise ValueError(f"Transaction denied. A minimum balance of {self.minimum_balance} must be maintained.")
            
        self.balance -= amount
        return self.balance


class ATM:
    def __init__(self, account_list, try_limit):
        """Part IV: Validates accounts and try limits before starting."""
        # Validate account list
        if not all(isinstance(acc, (BankAccount, MinimumBalanceAccount)) for acc in account_list):
            raise TypeError("Error: account_list must only contain BankAccount or MinimumBalanceAccount instances.")
        self.account_list = account_list

        # Validate try limit (catch exception and default to 2 as instructed)
        try:
            if not isinstance(try_limit, int) or try_limit <= 0:
                raise ValueError("try_limit must be a positive integer.")
            self.try_limit = try_limit
        except ValueError as e:
            print(f"Warning: {e} Defaulting try_limit to 2.")
            self.try_limit = 2

        self.current_tries = 0
        self.show_main_menu()

    def show_main_menu(self):
        while True:
            print("\n" + "="*20)
            print("🏧 WELCOME TO THE ATM")
            print("="*20)
            print("1. Log in")
            print("2. Exit")
            choice = input("Select an option (1-2): ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.log_in(username, password)
            elif choice == '2':
                print("Thank you for using our ATM. Goodbye!")
                break
            else:
                print("Invalid selection. Please try again.")

    def log_in(self, username, password):
        while self.current_tries < self.try_limit:
            for account in self.account_list:
                if account.authenticate(username, password):
                    self.current_tries = 0  # Reset tries upon successful login
                    print(f"\n✅ Login successful! Welcome, {username}.")
                    self.show_account_menu(account)
                    return True
            
            # If no match is found
            self.current_tries += 1
            tries_left = self.try_limit - self.current_tries
            print("\n❌ Invalid username or password.")
            
            if self.current_tries < self.try_limit:
                print(f"You have {tries_left} tries remaining.")
                username = input("Enter username: ")
                password = input("Enter password: ")
            else:
                print("🚨 Maximum login attempts reached. Shutting down program for security.")
                exit()  # Shuts down the entire program as requested

    def show_account_menu(self, account):
        while True:
            print("\n--- Account Menu ---")
            print(f"Current Balance: ${account.balance}")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Log out")
            choice = input("Select an option (1-3): ")

            if choice == '1':
                try:
                    amount = int(input("Enter amount to deposit (integer only): "))
                    account.deposit(amount)
                    print(f"✅ Successfully deposited ${amount}.")
                except ValueError as e:
                    print(f"⚠️ Error: {e}")
            
            elif choice == '2':
                try:
                    amount = int(input("Enter amount to withdraw (integer only): "))
                    account.withdraw(amount)
                    print(f"✅ Successfully withdrew ${amount}. Please take your cash.")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            
            elif choice == '3':
                account.authenticated = False  # De-authenticate for security
                print("Logging out... Returning to main menu.")
                break
            else:
                print("Invalid selection. Please try again.")


# ==========================================
# TEST SCRIPT (To test your code locally)
# ==========================================
if __name__ == "__main__":
    # Create some accounts
    acc1 = BankAccount("john_doe", "pass123", 500)
    acc2 = MinimumBalanceAccount("jane_smith", "secure456", 1000, 200)

    # Group them in a list
    my_accounts = [acc1, acc2]

    # Initialize the ATM (This will automatically trigger the main menu)
    my_atm = ATM(my_accounts, try_limit=3)