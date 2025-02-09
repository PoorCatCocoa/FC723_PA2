"""
Pseudocode:
    deposit:		#add the balance
        balance += amount

    withdraw:		#withdraw the balance
        if (balance - amount) < -1500:
            error
        else:
            balance -= amount

    transfer:		#transfer the balance to the target account
        if (balance - amount) < -1500:
            error
        else:
            balance -= amount
            target_account.deposit(amount)

    lock():		#account locked status
        locked = True

    freeze():		#account is locked due to multiple failed login attempts
        failed_attempts += 1
        if failed_attempts >= 3:
            lock()

    twos_complement:		#convert the value to two's complement
        if value < 0:
        value = (1 << bit_width) + value

        value -= (1 << bit_width)

    create_account:		#create a new account
        if username in accounts:
            error
        else:
            creat Account

    get_account:		#get the account and check the password
        account = Account(username)
        if account && account.password == password:
            if account.is_locked:
                error
        elif account && account.password != password:
            freeze()
        else:
            error

"""
class Account:		#class about the change of the money and status
	def __init__(self, username, password, balance: float =.0):
		self.username = username
		self.password = password
		self.balance = self.twos_complement(int(balance * 100), 32)  # Store balance by two's complement
		self.failed_attempts = 0		#count of the failed times
		self.is_locked = False			#status of the account

	def deposit(self, amount):		#add balance to account with 2's complement
		current_balance = self.from_twos_complement(self.balance, 32)
		new_balance = current_balance + int(amount * 100)
		self.balance = self.twos_complement(new_balance, 32)

	def withdraw(self, amount):		#remove balance from account with 2's complement
		current_balance = self.from_twos_complement(self.balance, 32)
		if current_balance - int(amount * 100) < -150000:
			raise ValueError("Insufficient funds. Overdraft limit reached.")
		new_balance = current_balance - int(amount * 100)
		self.balance = self.twos_complement(new_balance, 32)

	def transfer(self, target_account, amount):		#check the account and make a transfer to another account
		current_balance = self.from_twos_complement(self.balance, 32)
		if current_balance - int(amount * 100) < -150000:		#check account make sure not over draft before make transfer
			raise ValueError("Insufficient funds. Overdraft limit reached.")
		new_balance = current_balance - int(amount * 100)
		self.balance = self.twos_complement(new_balance, 32)
		target_account.deposit(amount)

	def check_balance(self):		#check account balance
		current_balance = self.from_twos_complement(self.balance, 32)
		print(f"Stored balance (two's complement): {bin(self.balance)}")
		return current_balance / 100

	def lock(self):		#check account status
		self.is_locked = True

	def reset_failed_attempts(self):		#count the failed times
		self.failed_attempts = 0

	def increment_failed_attempts(self):		#increase the failed times
		self.failed_attempts += 1
		if self.failed_attempts >= 3:
			self.lock()

	@staticmethod
	def twos_complement(value, bit_width):		#transe the balance by 2's complement
		if value < 0:
			value = (1 << bit_width) + value
		return value

	@staticmethod
	def from_twos_complement(value, bit_width):	#transe the balance back to float by 2's complement
		if value & (1 << (bit_width - 1)):
			value -= (1 << bit_width)
		return value


class Bank:		#class about account
	def __init__(self):
		self.accounts = {}

	def create_account(self, username, password):	#creat account by provided username and password
		if username in self.accounts:
			print("Username already exists.")
		else:
			self.accounts[username] = Account(username, password)
			print("Account created successfully.")

	def get_account(self, username, password):		#get account info and login management
		account = self.accounts.get(username)
		if account and account.password == password:
			if account.is_locked:
				print("Account is locked due to multiple failed login attempts.")
				return None
			account.reset_failed_attempts()
			return account
		elif account:
			account.increment_failed_attempts()
			print("Incorrect password.")
			return None
		else:
			print("Account not found.")
			return None


class CLI:		#class about command lines output and functions build
	def __init__(self, bank):
		self.bank = bank

	def start(self):
		while True:
			print("\nWelcome to the Banking Application")
			print("1. Open a new account")
			print("2. Open an existing account")
			print("3. Exit")
			choice = input("Enter your choice: ")

			if choice == "1":
				self.open_new_account()
			elif choice == "2":
				self.open_existing_account()
			elif choice == "3":
				print("Thank you for using the Banking Application.")
				break
			else:
				print("Invalid choice. Please try again.")

	def open_new_account(self):
		username = input("Enter a username: ")
		while True:
			password = input("Enter a password (8-16 characters): ")
			if 8 <= len(password) <= 16:
				break
			else:
				print("Password must be between 8 and 16 characters.")
		initial_deposit = float(input("Enter initial deposit amount: "))
		self.bank.create_account(username, password)
		self.bank.accounts[username].deposit(initial_deposit)
		print("Account created successfully! You can now log in with your credentials.")

	def open_existing_account(self):
		username = input("Enter your username: ")
		password = input("Enter your password: ")
		account = self.bank.get_account(username, password)
		if account:
			self.main_application(account)

	def main_application(self, account):
		while True:
			print("\nMain Menu")
			print("1. Check balance")
			print("2. Deposit money")
			print("3. Withdraw money")
			print("4. Transfer money")
			print("5. Exit")
			choice = input("Enter your choice: ")

			if choice == "1":
				print(f"Your balance is: £{account.check_balance()}")
			elif choice == "2":
				amount = float(input("Enter amount to deposit: "))
				account.deposit(amount)
				print("Deposit successful.")
			elif choice == "3":
				amount = float(input("Enter amount to withdraw: "))
				try:
					account.withdraw(amount)
					print("Withdrawal successful.")
				except ValueError as e:
					print(e)
			elif choice == "4":
				target_username = input("Enter the username of the target account: ")
				if target_username in self.bank.accounts:
					amount = float(input("Enter amount to transfer: "))
					try:
						account.transfer(self.bank.accounts[target_username], amount)
						print("Transfer successful.")
					except ValueError as e:
						print(e)
				else:
					print("Target account not found.")
			elif choice == "5":
				break
			else:
				print("Invalid choice. Please try again.")

if __name__ == "__main__":		#initallization the program for unittest
	CLI(Bank()).start()