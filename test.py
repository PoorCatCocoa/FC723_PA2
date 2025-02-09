import unittest
from FC723_PA2.main import *

class TestBankingApp(unittest.TestCase):

	def setUp(self):					#setup for the unit test
		self.bank = Bank()
		self.bank.create_account('user1', 'password123')
		self.bank.create_account('user2', 'password456')


	def test_create_account(self):		#check if account create
		self.assertIn('user1', self.bank.accounts)
		self.assertIn('user2', self.bank.accounts)
		self.assertEqual(self.bank.accounts['user1'].username, 'user1')
		self.assertEqual(self.bank.accounts['user2'].username, 'user2')

	def test_deposit(self):				#check if the account deposit 100 pounds
		account = self.bank.get_account('user1', 'password123')
		account.deposit(100)
		self.assertEqual(account.check_balance(), 100)

	def test_withdraw(self):			#check if the account does deposit and withdraw
		account = self.bank.get_account('user1', 'password123')
		account.deposit(200)
		account.withdraw(100)
		self.assertEqual(account.check_balance(), 100)
		with self.assertRaises(ValueError):
			account.withdraw(1601)  	#should raise the error when overdraft limit

	def test_transfer(self):			#check if the account does transfer to another account
		account1 = self.bank.get_account('user1', 'password123')
		account2 = self.bank.get_account('user2', 'password456')
		account1.deposit(500)
		account1.transfer(account2, 200)
		self.assertEqual(account1.check_balance(), 300)
		self.assertEqual(account2.check_balance(), 200)

	def test_check_balance(self):		#check if the account correct save the money
		account = self.bank.get_account('user1', 'password123')
		account.deposit(100)
		self.assertEqual(account.check_balance(), 100)

	def test_lock_account(self):		#check if the account freeze correctly when enter wrong password three times
		account = self.bank.get_account('user1', 'password123')
		account.increment_failed_attempts()
		account.increment_failed_attempts()
		account.increment_failed_attempts()
		self.assertTrue(account.is_locked)

	def test_twos_complement(self):		#check if 2's complement work properly
		account = self.bank.get_account('user1', 'password123')
		self.assertEqual(Account.twos_complement(5, 8), 5)		 # the 8 bit 2's complement of 5 is same of 5 in binary
		self.assertEqual(Account.twos_complement(-5, 8), 251) 		 # 256-5 = 251, the 8-bit two's complement of -5
		self.assertEqual(Account.from_twos_complement(251, 8), -5) 	 # trans back using 2's complement


if __name__ == '__main__':				#initlliaztion the test
	unittest.main()