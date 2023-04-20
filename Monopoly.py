print('\t\t<<<КОРОТКИЙ ОПИС ГРИ>>>\t\t\n'
      'Ця гра дещо відрізняється від оригінальної гри Монополія\n'
      'Тут вам не потрібно збирати міста з однієї колекції, щоб почати будувати будинки\n'
      'Поле в рази зменшено, всього лиш 10 позицій\n'
      'Максимум 2 гравці\n'
      'Виграє той, хто доведе до банкрутства свого суперника\n\n')
import random


class Player:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn
        self.town_list = []
        self.balance = 200
        self.chanse_card = ['Ви знайшли на землі 30 грн', 'Заплатіть за візит до лікаря 50 грн',
                            "Ви виграли 100 грн на конкурсі "
                            "'Найкраща гра Монополія написана на Python'", 'Вас обікрали на 70 грн']
        self.is_prisoner = False
        self.time_in_prison = 0
        self.mortgage_town = []

    def move(self, field):
        if self.is_prisoner:
            self.time_in_prison += 1
            if self.time_in_prison == 2:
                print("Ви вийшли із в'язниці!")
                self.is_prisoner = False
                self.time_in_prison = 0
        else:
            player_board = field.a_player if self.turn == 0 else field.b_player
            opponent_board = field.b_player if self.turn == 0 else field.a_player
            icon = '*A*' if self.turn == 0 else '*B*'
            step = random.randint(1, 4)
            p_pos = player_board.index(icon)
            obj = player_board.pop(p_pos)
            actual_pos = p_pos + step
            if actual_pos >= 10:
                self.balance += 50
                actual_pos -= 10
            player_board.insert(actual_pos, obj)
            print(f'{self.name} пересунувся на {step} кроки')
            print(*player_board)
            print(*opponent_board)
            print(*field.field)
            print(*field.building)
            if actual_pos == 6:
                print(f'{self.name} потрапив в тюрму!')
                self.is_prisoner = True

    @staticmethod
    def find_city(field, turn):
        player_board = field.a_player if turn == 0 else field.b_player
        icon = '*A*' if turn == 0 else '*B*'
        p_pos = player_board.index(icon)
        title = field.field[p_pos]
        event_places = ['STR', '*?*', '*#*', '*$*']
        if title not in event_places:
            for town in towns:
                if town.title == title:
                    return town
        else:
            return None

    def buy(self, field):
        town = self.find_city(field, self.turn)
        if town is not None and town.isBought is False and town not in self.town_list and self.balance >= 100:
            buy_it = input(f'Ви бажаєте купити місто {town.name} за {town.cost}\n1 - Так\t\t2 - Ні\n')
            if buy_it == '1':
                self.balance -= town.cost
                town.isBought = True
                self.town_list.append(town)

    def pay(self, field):
        player2 = (p2, p1)[self.turn]
        town = self.find_city(field, self.turn)
        if town is not None and town.isMortgaged is False and town.isBought and town not in self.town_list:
            self.balance -= town.rent
            player2.balance += town.rent
            print(f'Гравець {self.name} став на локацію {town.name}. Тому повинен заплатити гравцеві {player2.name} - '
                  f'{town.rent} грн')

    def build(self, field):
        if self.town_list and self.is_prisoner is False:
            build = input('Ви хочете збудувати будинок на одній з своїх територій?\n1 - Так\t\t2 - Ні\n')
            if build == '1':
                for i, x in enumerate(self.town_list):
                    print(f'{i}.{x.name} - {x.build_cost}')
                town_index = int(input('Введіть номер міста у якому хочете збудувати будинок: '))
                if 0 <= town_index <= len(self.town_list):
                    town = self.town_list[town_index]
                    if self.balance >= town.build_cost and town.num_of_building <= 4 and town.isMortgaged is False:
                        self.balance -= town.build_cost
                        town.rent += 15
                        town.num_of_building += 1
                        town_field_index = field.field.index(town.title)
                        field.building[town_field_index] = f'({town.num_of_building})'
                    else:
                        print(f'\nВи не можете збудувати будинок у місті {town.name}!\nМожливі причини\n'
                              f'\t-Недостатньо коштів\n'
                              f'\t-Досягнуто ліміт кількості будинків\n'
                              f'\t-Територія закладена\n')

    def show_town_list(self):
        town_str = ''
        for town in self.town_list:
            town_str += f'\t{town.name}\n'
        return town_str

    def mortgage(self):
        if self.town_list:
            for i, x in enumerate(self.town_list):
                print(f'{i}.{x.name} - {x.cost - 30}')
            town_index = int(input('Введіть номер міста яке хочете закласти: '))
            if 0 <= town_index <= len(self.town_list):
                town = self.town_list[town_index]
                self.balance += town.cost - 30
                print(f'Ви заклали місто {town.name} і получили за це {town.cost - 30}')
                town_field_index = field.field.index(town.title)
                field.building[town_field_index] = f'(#)'
                self.town_list.remove(town)
                self.mortgage_town.append(town)
                town.isMortgaged = True
        else:
            print('У вас у володінні немає міст, вам немає що закладати')

    def unMortgage(self):
        if self.mortgage_town and self.balance >= 77:
            for i, x in enumerate(self.mortgage_town):
                print(f'{i}.{x.name} - {(x.cost - 30) + (x.cost - 30) * 0.1}')
            town_index = int(input('Введіть номер міста яке хочете вивести із застави: '))
            if 0 <= town_index <= len(self.mortgage_town):
                town = self.mortgage_town[town_index]
                cost = (town.cost - 30) + (town.cost - 30) * 0.1
                self.balance -= cost
                print(f'Ви вивели місто {town.name} із застави і витратили {cost} грн')
                town_field_index = field.field.index(town.title)
                field.building[town_field_index] = f'({town.num_of_building})'
                self.town_list.append(town)
                self.mortgage_town.remove(town)
                town.isMortgaged = False
        else:
            print('Недостатньо коштів або у вас немає закладених міст')

    def casino(self, field):
        player_board = field.a_player if turn == 0 else field.b_player
        icon = '*A*' if turn == 0 else '*B*'
        p_pos = player_board.index(icon)
        if p_pos == 9:
            choose = input('\nВи прийшли на локацію Казино!\nБажаєте зіграти?\n1 - Так\t\t2 - Ні\n')
            if choose == '1':
                print('''Виграшні комбінації\n'$'- 3:x10\t2:x9\n'%'- 3:x8\t2:x7\n'@'- 3:x6\t2:x5\n'*'- 3:x4\t2:x3''')
                print(f'Ваш баланс - {self.balance}')
                money = int(input('Введіть ставку:'))
                if money < self.balance:
                    symbols = ['*', '@', '%', '$']
                    win_combinations = {
                        '$': {3: 10, 2: 6},
                        '%': {3: 9, 2: 5},
                        '@': {3: 8, 2: 4},
                        '*': {3: 7, 2: 3}}
                    combination = [random.choice(symbols) for i in range(3)]
                    symbol_counts = {symbol: combination.count(symbol) for symbol in symbols}
                    print(f'Ваша комбінація - {symbol_counts}')
                    self.balance -= money
                    for symbol, counts in symbol_counts.items():
                        if counts in win_combinations[symbol]:
                            win = win_combinations[symbol][counts] * money
                            print(f'\nВи виграли - {win} грн!\n')
                            self.balance += win
                            return self.balance
                    else:
                        print('\nВи програли\n')
                else:
                    print('\nНедостатньо коштів\n')

    def chance(self, field):
        player_board = field.a_player if turn == 0 else field.b_player
        icon = '*A*' if turn == 0 else '*B*'
        p_pos = player_board.index(icon)

        if p_pos == 3:
            print("\nВи стали на позицію 'Шанс'")
            probability = [0.2, 0.4, 0.1, 0.3]
            result = random.choices(self.chanse_card, probability, k=1)
            print(f'{result[0]}\n')
            if self.chanse_card.index(result[0]) == 0:
                self.balance += 30
            elif self.chanse_card.index(result[0]) == 1:
                self.balance -= 50
            elif self.chanse_card.index(result[0]) == 2:
                self.balance += 100
            elif self.chanse_card.index(result[0]) == 3:
                self.balance -= 70

    def win(self):
        player2 = (p2, p1)[self.turn]
        if self.balance < 0 and not self.town_list:
            print(f'Гравець {player2.name} виграв!\nГравець {self.name} програв')
            return True
        else:
            return False


class RealEstate:
    def __init__(self, title, name, cost, rent, build_cost):
        self.title = title
        self.name = name
        self.cost = cost
        self.rent = rent
        self.build_cost = build_cost
        self.num_of_building = 0
        self.isBought = False
        self.isMortgaged = False


class Field:
    def __init__(self):
        self.field = ('STR', vinnyca.title, lutsk.title, '*?*', rivne.title, ternopil.title, '*#*', kyiv.title,
                      lviv.title,
                      '*$*')
        self.a_player = ['*A*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.b_player = ['*B*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.building = [f'''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''']


p1 = Player('Sasha', 0)
p2 = Player('Oleg', 1)

turn = random.randint(0, 1)
vinnyca = RealEstate('VIN', 'Вінниця', 100, 10, 50)
lutsk = RealEstate('LUC', 'Луцьк', 110, 15, 55)
rivne = RealEstate('RIV', 'Рівне', 120, 20, 60)
ternopil = RealEstate('TER', 'Тернопіль', 130, 25, 65)
kyiv = RealEstate('KYV', 'Київ', 140, 30, 70)
lviv = RealEstate('LVI', 'Львів', 150, 35, 75)

towns = (vinnyca, lutsk, rivne, ternopil, kyiv, lviv)

field = Field()
while True:
    print(f'{p1.name} має на рахунку - {p1.balance}\n'
          f'{p2.name} має на рахунку - {p2.balance}\n'
          f'\n<<<<<Зараз ходить гравець {p1.name if turn == 0 else p2.name}>>>>>')
    choose = input(f"Натисніть Enter, щоб зробити хід\nНатисніть 1, щоб переглянути об'єкти у власності\n"
                   f"Натисніть 2, щоб закласти місто\nНатисніть 3, щоб вивести із застави місто:\n")
    if p1.win() or p2.win():
        break
    if choose == '':
        if turn == 0:
            p1.build(field)
            p1.move(field)
            p1.chance(field)
            p1.casino(field)
            p1.buy(field)
            p1.pay(field)
            turn += 1
        elif turn == 1:
            p2.build(field)
            p2.move(field)
            p2.chance(field)
            p2.casino(field)
            p2.buy(field)
            p2.pay(field)
            turn -= 1
    elif choose == '1':
        if turn == 0:
            print(f'У гравця {p1.name} у власності такі будівлі:\n{p1.show_town_list()}')
        else:
            print(f'У гравця {p2.name} у власності такі будівлі:\n{p2.show_town_list()}')
    elif choose == '2':
        if turn == 0:
            p1.mortgage()
        else:
            p2.mortgage()
    elif choose == '3':
        if turn == 0:
            p1.unMortgage()
        else:
            p2.unMortgage()
