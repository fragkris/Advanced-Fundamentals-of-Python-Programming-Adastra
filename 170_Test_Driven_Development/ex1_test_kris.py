from unittest import TestCase
from ex1_kris import Account
from parameterized import parameterized


class Test_Account(TestCase):

    @parameterized.expand([
        (None, "25031994", 2.1, 1999.99),
        ("25031994", 2.1, 1999.99),
        ("BG033CECB352355", "254", 2.1, 1999.99),
        ("BG033CECB352355", None, 2.1, 1999.99),
        ("BG033CECB352355", 2.1, 1999.99),
        ("BG033CECB352355", "25031994", None, 1999.99),
        ("BG033CECB352355", "25031994", '2.1', 1999.99),
        ("BG033CECB352355", "25031994", 1999.99),
        ("BG033CECB352355", "25031994", 2.1, "1999.99"),
        ("BG033CECB352355", "25031994", 2.1, None),
        ("BG033CECB352355", "25031994", 2.1),
        ()
    ])
    def test_account_should_not_initialize_with_Null_or_empty_or_missing_value(self, acc_num, date_created, interest_rate, balance):
        self.assertFalse(Account(acc_num, date_created, interest_rate, balance))


    def test_account_initializes_correctly(self):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertEqual(self.account.accNumber, 'BG033CECB352355')
        self.assertEqual(self.account.dateOpen, '25031994')
        self.assertEqual(self.account.interestRate, '2.1')
        self.assertEqual(self.account.opening_balance, '1999.99')


    @parameterized.expand([
        (0, -1, -0.1)
    ])
    def deposit_should_fail_if_amount_is_negative_or_zero(self, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertFalse(self.account.deposit(amount))


    @parameterized.expand([
        (0.1, 1, 10)
    ])
    def deposit_should_pass_if_amount_is_greater_than_zero(self, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertTrue(self.account.deposit(amount))


    @parameterized.expand([
        (2000.00, 1999.995, 2001)
    ])
    def withdraw_should_fail_if_amount_is_greater_than_balance(self, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertTrue(self.account.deposit(amount))

    @parameterized.expand([
        (0, -1, -0.1)
    ])
    def withdraw_should_fail_if_amount_is_negative_or_zero(self, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertFalse(self.account.deposit(amount))

    @parameterized.expand([
        (0.1, 1, 10, 1999.99)
    ])
    def withdraw_should_pass_if_amount_is_greater_than_zero(self, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertTrue(self.account.deposit(amount))


    def transfer_should_fail_if_account_number_is_empty(self):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertFalse(self.account.transfer(1900))

    def transfer_should_fail_if_transferred_amount_is_greater_than_balance(self):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertFalse(self.account.transfer("BG033CECB777777", 2000))

    @parameterized.expand([
        ("BG033CECB777777",1999.99),
        ("BG033CECB777777",0.1),
        ("BG0CECB777777",50)
    ])
    def transfer_should_pass_if_corectly_called(self, acc_num, amount):
        self.account = Account("BG033CECB352355", "25031994", 2.1, 1999.99)
        self.assertTrue(self.account.transfer(acc_num, amount))

