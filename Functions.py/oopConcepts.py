from abc import ABC, abstractmethod  # Importing Abstract Base Class module

# 🟢 ABSTRACTION: Creating an abstract base class for bank accounts
class BankAccount(ABC):  
    def __init__(self, account_holder, balance=0):  # 🟡 ARGUMENTS (account_holder), DEFAULT ARGUMENT (balance)
        """ENCAPSULATION: Protecting balance from direct access"""
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute (Encapsulation)

    def deposit(self, amount):
        """Deposit money into the account"""
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount} successfully!")
        else:
            print("Invalid deposit amount!")

    def withdraw(self, amount):
        """Withdraw money while ensuring sufficient balance"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew ${amount} successfully!")
        else:
            print("Insufficient balance or invalid amount!")

    def get_balance(self):  
        """ENCAPSULATION: Getter method to access private balance"""
        return self.__balance

    @abstractmethod
    def calculate_interest(self):  
        """ABSTRACTION: Forcing all subclasses to implement this method"""
        pass

    def show_details(self):  
        """POLYMORPHISM: This method will be overridden by child classes"""
        print(f"Account Holder: {self.account_holder}, Balance: ${self.__balance}")

# 🟢 INHERITANCE: SavingsAccount is a child class of BankAccount
class SavingsAccount(BankAccount):  
    def __init__(self, account_holder, balance=0, interest_rate=5):  # 🟡 KEYWORD ARGUMENTS (interest_rate)
        """Initialize Savings Account with an interest rate"""
        super().__init__(account_holder, balance)  # Calling Parent Constructor
        self.interest_rate = interest_rate  # Additional attribute

    def calculate_interest(self):  
        """POLYMORPHISM: Different implementation of calculate_interest"""
        interest = self.get_balance() * (self.interest_rate / 100)
        return f"Interest earned: ${interest:.2f}"

    def show_details(self):  
        """POLYMORPHISM: Overriding the parent class method"""
        print(f"Savings Account Holder: {self.account_holder}, Balance: ${self.get_balance()}, Interest Rate: {self.interest_rate}%")

# 🟢 INHERITANCE: CurrentAccount is a child class of BankAccount
class CurrentAccount(BankAccount):  
    def __init__(self, account_holder, balance=0, overdraft_limit=500):  # 🟡 KEYWORD ARGUMENTS (overdraft_limit)
        """Initialize Current Account with overdraft limit"""
        super().__init__(account_holder, balance)  
        self.overdraft_limit = overdraft_limit  # Additional attribute

    def withdraw(self, amount):  
        """POLYMORPHISM: Overriding withdraw method to allow overdraft"""
        if amount <= (self.get_balance() + self.overdraft_limit):
            print(f"Withdrew ${amount} successfully (Using Overdraft)!")
        else:
            print("Withdrawal exceeds overdraft limit!")

    def calculate_interest(self):  
        """POLYMORPHISM: Different implementation for current account"""
        return "No interest for Current Account"

    def show_details(self):  
        """POLYMORPHISM: Overriding the parent class method"""
        print(f"Current Account Holder: {self.account_holder}, Balance: ${self.get_balance()}, Overdraft Limit: ${self.overdraft_limit}")

# 🟢 CREATING OBJECTS & DEMONSTRATING OOP CONCEPTS
savings = SavingsAccount("Alice", balance=1000, interest_rate=4)  
current = CurrentAccount(account_holder="Bob", balance=2000, overdraft_limit=1000)  

# 🟢 PERFORMING TRANSACTIONS
savings.deposit(500)  # Deposit money
savings.withdraw(300)  # Withdraw money

current.deposit(700)
current.withdraw(2500)  # Using overdraft

# 🟢 POLYMORPHISM: SHOWING DETAILS
savings.show_details()  
current.show_details()  

# 🟢 ABSTRACTION: IMPLEMENTING THE ABSTRACT METHOD
print(savings.calculate_interest())  
print(current.calculate_interest())  # Should return "No interest for Current Account"
