import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from abc import ABC, abstractmethod
from functools import reduce

# Abstract Class (Abstraction)
class BankAccount(ABC):
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self._balance = balance  # Encapsulation: Protected variable
        self.transactions = []

    @abstractmethod
    def interest_rate(self):
        pass  # Abstract method

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.transactions.append(amount)
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.transactions.append(-amount)  # Negative for withdrawals
        else:
            print("Insufficient funds or invalid amount.")

    def get_balance(self):
        return self._balance

    def get_transactions(self):
        return self.transactions

# Inheritance: Savings and Checking Accounts
class SavingsAccount(BankAccount):
    def interest_rate(self):
        return 0.04  # 4% interest

class CheckingAccount(BankAccount):
    def interest_rate(self):
        return 0.02  # 2% interest

# Creating Bank Accounts
acc1 = SavingsAccount("Alice", 500)
acc2 = CheckingAccount("Bob", 300)

# Simulated transactions
acc1.deposit(100)
acc1.deposit(200)
acc1.withdraw(50)
acc1.deposit(300)
acc1.withdraw(150)

acc2.deposit(400)
acc2.withdraw(100)
acc2.deposit(250)

# Lambda Function: Convert transactions to absolute values
transaction_amounts = list(map(lambda x: abs(x), acc1.get_transactions() + acc2.get_transactions()))
print("Transaction Amounts:", transaction_amounts)

# Compute Mean and Standard Deviation
mean = np.mean(transaction_amounts)
std_dev = np.std(transaction_amounts)
print(f"Mean Transaction: {mean}, Standard Deviation: {std_dev}")

# Define Probability Density Function (PDF)
x_values = np.linspace(min(transaction_amounts), max(transaction_amounts), 100)
pdf_values = norm.pdf(x_values, mean, std_dev)

# Plot PDF
plt.plot(x_values, pdf_values, label="Transaction PDF")
plt.xlabel("Transaction Amount")
plt.ylabel("Probability Density")
plt.title("Probability Density Function (PDF) of Transactions")
plt.legend()
plt.show()

# Filtering transactions above a threshold using filter()
high_value_transactions = list(filter(lambda x: x > mean + std_dev, transaction_amounts))
print("High-Value Transactions:", high_value_transactions)

# Using reduce() to compute total transaction volume
total_transaction_volume = reduce(lambda x, y: x + y, transaction_amounts)
print("Total Transaction Volume:", total_transaction_volume)

# Probability of a transaction being greater than $300
prob_greater_than_300 = 1 - norm.cdf(300, mean, std_dev)
print(f"Probability of a transaction being > $300: {prob_greater_than_300:.4f}")
