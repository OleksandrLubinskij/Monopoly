import random


class Player:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn
        self.town_list = []
        self.balance = 500

    def move(self, field):
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
        if town is not None and town.isBought is False and town not in self.town_list:
            buy_it = input(f'Ви бажаєте купити місто {town.name} за {town.cost}\n1 - Так\t\t2 - Ні\n')
            if buy_it == '1':
                self.balance -= town.cost
                town.isBought = True
                self.town_list.append(town)

        else:
            pass

    def pay(self, field):
        player2 = (p2, p1)[self.turn]
        town = self.find_city(field, self.turn)
        if town is not None and town.isMortgaged is False and town.isBought and town not in self.town_list:
            self.balance -= town.rent
            player2.balance += town.rent
            print(f'Гравець {self.name} став на локацію {town.name}. Тому повинен заплатити гравцеві {player2.name} - '
                  f'{town.rent} грн')

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
    print(f'{p1.name} має на рахунку - {p1.balance}\n{p2.name} має на рахунку - {p2.balance}')
    choose = input(f"\nНатисніть Enter, щоб зробити хід\n")
    if choose == '':
        if turn == 0:
            p1.move(field)
            p1.buy(field)
            p1.pay(field)
            turn += 1
        else:
            p2.move(field)
            p2.buy(field)
            p2.pay(field)
            turn -= 1
