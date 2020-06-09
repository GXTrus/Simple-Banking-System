import random

bank_accounts = {}


class Bank:
    def __init__(self):
        self.work()

    def work(self):
        while True:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            user_input = self.enter_choice(('0', '1', '2'))
            if user_input == '1':
                self.create_account()
            elif user_input == '2':
                user_input = self.work_with_account()
            if user_input == '0':
                break
        print('\nBye!')

    def enter_choice(self, variants):
        while True:
            a = input()
            if a in variants:
                break
            else:
                print('\nerror\n')
        return a

    def create_account(self):
        card_number = '400000' + str(random.randint(100000000, 999999999)) + str(random.randint(0, 9))
        card_pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9))
        bank_accounts[card_number] = {'pin': card_pin}
        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{card_pin}\n')
        return

    def work_with_account(self):
        card_number = self.login_account()
        result = ''
        if card_number:
            while True:
                print('1. Balance')
                print('2. Log out')
                print('0. Exit')
                user_input = self.enter_choice(('0', '1', '2'))
                if user_input == '1':
                    balance = bank_accounts[card_number].get('balance', 0)
                    print(f'\nBalance: {balance}\n')
                elif user_input == '2':
                    print('\nYou have successfully logged out!\n')
                    break
                else:
                    result = '0'
                    break
        return result

    def login_account(self):
        print('\nEnter your card number:')
        card_number = input()
        print('Enter your PIN:')
        card_pin = input()
        if bank_accounts.get(card_number) is None or bank_accounts[card_number]['pin'] != card_pin:
            print('\nWrong card number or PIN!\n')
            return False
        else:
            print('\nYou have successfully logged in!\n')
            return card_number


if __name__ == '__main__':
    my_bank = Bank()
