import random


class Player:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn
        self.town_list = []
        self.balance = 500


class Field:
    def __init__(self):
        self.field = ['STR', 'POL', 'LUC', '*?*', 'KYV', 'VIN', '*#*', 'RIV', 'TER', '*$*']
        self.a_player = ['*A*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.b_player = ['*B*', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''', '''   ''',
                         '''   ''']
        self.building = [f'''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''', '(0)', '(0)', '''   ''']
