import random

from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Bank:
    def __init__(self):
        db_card = create_engine('sqlite:///card.s3db?check_same_thread=False')
        Base = declarative_base()

        class CardTable(Base):
            __tablename__ = 'card'
            id = Column(Integer, primary_key=True)
            number = Column(Text)
            pin = Column(Text, default='0000')
            balance = Column(Integer, default=0)

            def __repr__(self):
                return f"{self.number}, {self.pin}, {self.balance}"

            def __str__(self):
                return [self.number, self.pin, self.balance]

        Base.metadata.create_all(db_card)
        self.session = sessionmaker(bind=db_card)()
        self.CardTable = CardTable
        self.work()

    def work(self):
        while True:
            print('1. Create an account\n2. Log into account\n0. Exit')
            user_input = self.enter_choice(('0', '1', '2'))
            if user_input == '1':
                self.create_account()
            elif user_input == '2':
                user_input = self.work_with_account()
            if user_input == '0':
                break
        self.session.commit()
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
        random_number = random.randint(0, 999999999)
        card_number = f'400000{random_number:09d}'
        last_number = self.luhn_algorithm(card_number)
        card_number += str(last_number)
        card_pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9))
        new_row = self.CardTable(number=card_number, pin=card_pin)
        self.session.add(new_row)
        self.session.commit()
        # rows = self.session.query(self.CardTable).all()
        # print(rows)
        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{card_pin}\n')
        return

    def luhn_algorithm(self, card_number):
        card_number_list = list(card_number)
        for x in range(0, 16, 2):
            y = int(card_number_list[x]) * 2
            card_number_list[x] = str(y - 9 if y > 9 else y)
        sum = 0
        for x in card_number_list:
            sum += int(x)
        return (10 - sum % 10) % 10

    def work_with_account(self):
        card_info = self.login_account()
        result = ''
        if card_info:
            while True:
                print('1. Balance\n2. Log out\n0. Exit')
                user_input = self.enter_choice(('0', '1', '2'))
                if user_input == '1':
                    balance = card_info[0].balance
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
        card_number = str(input().strip())
        print('Enter your PIN:')
        card_pin = str(input().strip())
        # rows = self.session.query(self.CardTable).all()
        # print(rows)
        rows = self.session.query(self.CardTable).filter(self.CardTable.number == card_number).all()
        # print(rows)
        if rows == [] or (rows[0].pin != card_pin):
            print('\nWrong card number or PIN!\n')
            return False
        else:
            print('\nYou have successfully logged in!\n')
            return rows


if __name__ == '__main__':
    my_bank = Bank()
