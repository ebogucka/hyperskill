from enum import Enum


def show_menu():
    print('\nWrite action (buy, fill, take, remaining, exit): ')


class CoffeeMachine:
    class State(Enum):
        CHOOSING_ACTION = 1
        CHOOSING_COFFEE_TYPE = 2
        FILLING_WATER = 3
        FILLING_MILK = 4
        FILLING_COFFEE = 5
        FILLING_CUPS = 6

    def __init__(self, money, water, milk, coffee, cups):
        self.money = money
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cups = cups
        self.state = self.State.CHOOSING_ACTION

    def __str__(self):
        return ('\nThe coffee machine has:\n'
                '{} of water\n'
                '{} of milk\n'
                '{} of coffee beans\n'
                '{} of disposable cups\n'
                '${} of money'.format(self.water, self.milk, self.coffee,
                                      self.cups, self.money))

    def buy(self, order):
        if self.water < order.water:
            print('Sorry, not enough water!')
            return
        if self.milk < order.milk:
            print('Sorry, not enough milk!')
            return
        if self.coffee < order.coffee:
            print('Sorry, not enough coffee beans!')
            return
        if self.cups < 1:
            print('Sorry, not enough disposable cups!')
            return

        print('I have enough resources, making you a coffee!')
        self.water -= order.water
        self.milk -= order.milk
        self.coffee -= order.coffee
        self.cups -= 1
        self.money += order.price

    def fill(self, water = 0, milk = 0, coffee = 0, cups = 0):
        self.water += water
        self.milk += milk
        self.coffee += coffee
        self.cups += cups

    def take(self):
        earnings = self.money
        print('I gave you ${}'.format(earnings))
        self.money = 0
        return earnings

    def handle(self, command):
        if self.state == self.State.CHOOSING_ACTION:
            if command == 'buy':
                print('What do you want to buy? 1 - espresso, 2 - latte,'
                      ' 3 - cappuccino, back - to main menu: ')
                self.state = self.State.CHOOSING_COFFEE_TYPE
            elif command == 'fill':
                print('Write how many ml of water do you want to add: ')
                self.state = self.state.FILLING_WATER
            elif command == 'take':
                self.take()
                self.state = self.state.CHOOSING_ACTION
                show_menu()
            elif command == 'remaining':
                print(self)
                self.state = self.state.CHOOSING_ACTION
                show_menu()
        elif self.state == self.State.CHOOSING_COFFEE_TYPE:
            if command in '123':
                if command == '1':
                    order = Coffee('espresso')
                elif command == '2':
                    order = Coffee('latte')
                elif command == '3':
                    order = Coffee('cappuccino')
                self.buy(order)
                self.state = self.state.CHOOSING_ACTION
                show_menu()
            elif command == 'back':
                show_menu()
                self.state = self.State.CHOOSING_ACTION
        elif self.state == self.State.FILLING_WATER:
            try:
                amount = int(command)
                self.fill(water=amount)
                print('Write how many ml of milk do you want to add: ')
                self.state = self.state.FILLING_MILK
            except ValueError:
                return
        elif self.state == self.State.FILLING_MILK:
            try:
                amount = int(command)
                self.fill(milk=amount)
                print('Write how many grams of coffee beans do you want to add: ')
                self.state = self.state.FILLING_COFFEE
            except ValueError:
                return
        elif self.state == self.State.FILLING_COFFEE:
            try:
                amount = int(command)
                self.fill(coffee=amount)
                print('Write how many disposable cups do you want to add: ')
                self.state = self.state.FILLING_CUPS
            except ValueError:
                return
        elif self.state == self.State.FILLING_CUPS:
            try:
                amount = int(command)
                self.fill(cups=amount)
                show_menu()
                self.state = self.state.CHOOSING_ACTION
            except ValueError:
                return


class Coffee:
    def __init__(self, variety):
        if variety == 'espresso':
            self.water = 250
            self.milk = 0
            self.coffee = 16
            self.price = 4
        elif variety == 'latte':
            self.water = 350
            self.milk = 75
            self.coffee = 20
            self.price = 7
        elif variety == 'cappuccino':
            self.water = 200
            self.milk = 100
            self.coffee = 12
            self.price = 6


coffee_machine = CoffeeMachine(550, 400, 540, 120, 9)
show_menu()
while True:
    action = input()
    if action == 'exit':
        break
    coffee_machine.handle(action)
