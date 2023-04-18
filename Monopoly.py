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


class Field:
    def __init__(self):
        self.field = ['STR', 'POL', 'LUC', '*?*', 'KYV', 'VIN', '*#*', 'RIV', 'TER', '*$*']
        self.a_player = ['*A*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.b_player = ['*B*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.building = [f'''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''']


p1 = Player('Sasha', 0)
p2 = Player('Oleg', 1)
turn = random.randint(0, 1)
field = Field()
while True:
    print(f'{p1.name} має на рахунку - {p1.balance}\n{p2.name} має на рахунку - {p2.balance}')
    choose = input(f"\nНатисніть Enter, щоб зробити хід\n")
    if choose == '':
        if turn == 0:
            p1.move(field)
            turn += 1
        else:
            p2.move(field)
            turn -= 1
