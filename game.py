import random
import sys
import time
CARD_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8']
NAMES = ['Frosty McWhopperCrank', 'Miss Stankbutt', 'Joedoe Rowboat', 
        'Radical Wildperson', 'Samey Seafarer', 'Luke Groundwalker', 
        'Frantic Questioneer', 'Doubly Whammical', 'Unlimiting Limiter',
        'Deacon Answer', 'Extender of Sympathies', 'Mister DisplayError',
        'Sir Whodunit', 'XxXProGam311rzXxX', 'The Popweasel', 'Underwhelming Grandmaster',
        'Adam Noether', 'Euclideulerman', 'Anakin Skysprinter']
ID = 0 # Ensures that every player has a unique id

class Statement:
    '''
    Keeps track of the current statement associated with a card being passed in this round 
    versus its true value.
    '''
    def __init__(self, card, bluff):
        self.card = card
        self.bluff = bluff
        self.value = True if card == bluff else False

class PlayerInterface():
    '''
    Provides an interface for a human player to interact with the game.
    '''

    def __init__(self, player, mode='terminal'):
        self.player = player
        self.mode = mode
        self.game = '' 
        self.greeting()

    def greeting(self):
        if self.mode == 'terminal':
            print("Welcome to the RoachPoker terminal interface. Waiting for game to start...")

    def choice(self, lst):
        '''
        Generating a choice menu from strings in input list.
        '''
        menuStr = '<q>: Quit\n<p>: Show player info\n<f>: Show entire field\n'
        for i in range(len(lst)):
            menuStr += '<%d>: %s\n' % (i+1, lst[i])
        while True: 
            try:
                userInput = input(menuStr)
                if userInput == 'q':
                    sys.exit()
                elif userInput == 'p':
                    print(str(self.player))
                elif userInput == 'f' and self.game != '':
                    print(self.game.get_field())
                elif int(userInput) <= (len(lst)):
                    return int(userInput) - 1
                else:
                    print("Invalid input. Please input one of the displayed options.")
            except ValueError:
                print("Invalid input. Please input one of the displayed options.")
       

    def game_start(self, game):
        self.game = game
        if self.mode == 'terminal':
            print("Game is starting. Your name is %s and your id is %s." % (self.player.name, self.player.id))
            print("Your current game state:")
            print(str(self.player))

    def call_card(self, statement):
        if self.mode == 'terminal':
            print("Do you believe the claim that this card is a %s?" % str(statement.bluff))
            lst = ["Yes", "No"]
            userInput = self.choice(lst)
            if userInput == 0:
                return True
            elif userInput == 1:
                return False

    def call_or_pass_card(self, statement):
        if self.mode == 'terminal':
            print("Would you like to call or pass this card?")
            userInput = self.choice(["Call", "Pass"])
            if userInput == 0:
                return 'call'
            elif userInput == 1:
                return 'pass'

    def pass_card(self, card):
        global CARD_LABELS
        if self.mode == 'terminal':
            print("The card is a [%s]." % card)
            print("Who would you like to pass this card to?")
            lst = []
            for player in self.game.validPlayers:
                lst.append(player.name)
            playerChosen = self.choice(lst)
            playerToPassTo = self.game.validPlayers[playerChosen]
            print("You are passing to %s. What are you claiming this %s to be?" % (lst[playerChosen], card))
            bluff = CARD_LABELS[self.choice(CARD_LABELS)]
            return (playerToPassTo, Statement(card, bluff))

    def pass_card_from_hand(self):
        global CARD_LABELS
        if self.mode == 'terminal':
            print("Please select a card to pass from your hand.")
            lst = sorted(list(set(self.player.hand)))
            card = lst[self.choice(lst)]
            print("Who would you like to pass this card to?")
            lst = []
            for player in self.game.validPlayers:
                lst.append(player.name)
            playerChosen = self.choice(lst)
            playerToPassTo = self.game.validPlayers[playerChosen]
            print("You are passing to %s. What are you claiming this %s to be?" % (lst[playerChosen], card))
            bluff = CARD_LABELS[self.choice(CARD_LABELS)]
            return (playerToPassTo, Statement(card, bluff))

    def win(self):
        if self.mode == 'terminal':
            print("You have won!")

    def loss(self):
        if self.mode == 'terminal':
            print("You have lost!")

class CPUInterface():
    '''
    Provides the logic for a CPU player to interact with the game.
    '''
    def __init__(self, player, mode=0, log=False, sleepDuration=1):
        self.player = player
        self.mode = mode # Difficulty setting, 0 for random
        self.log = log
        # Amount of time to hesitate on decisions in seconds
        self.sleepDuration = sleepDuration 
        self.game = ''

    def game_start(self, game):
        self.game = game

    def call_card(self, statement):
        time.sleep(self.sleepDuration)
        if self.mode == 0:
            return random.choice([True, False])

    def call_or_pass_card(self, statement):
        time.sleep(self.sleepDuration)
        if self.mode == 0:
            return random.choice(['call', 'pass'])

    def pass_card(self, card):
        time.sleep(self.sleepDuration)
        global CARD_LABELS
        if self.mode == 0:
            playerToPassTo = random.choice(self.game.validPlayers)
            validCards = CARD_LABELS.copy()
            validCards.remove(card)
            if random.randint(0,1) == 0:
                bluff = card
            else:
                bluff = random.choice(validCards)
            return (playerToPassTo, Statement(card, bluff))

    def pass_card_from_hand(self):
        time.sleep(self.sleepDuration)
        global CARD_LABELS
        if self.mode == 0:
            card = random.choice(self.player.hand)
            playerToPassTo = random.choice(self.game.validPlayers)
            validCards = CARD_LABELS.copy()
            validCards.remove(card)
            if random.randint(0,1) == 0:
                bluff = card
            else:
                bluff = random.choice(validCards)
            return (playerToPassTo, Statement(card, bluff))

    def win(self):
        pass

    def loss(self):
        pass

class Player:
    '''
    Keeps track of cards in a players hand and field and provides them with actions
    '''
    def __init__(self, isCPU = True, sleepDuration=1, CPUmode=0, log=False):
        global ID
        self.id = ID
        ID += 1
        self.hand = []
        self.field = []
        self.name = 'Unnamed Player'
        if isCPU:
            self.interface = CPUInterface(self, sleepDuration=sleepDuration, mode=CPUmode, log=log)
        else:
            self.interface = PlayerInterface(self)

    def __eq__(self, player):
        if self.id == player.id:
            return True
        return False

    def __str__(self):
        strHand = ''
        strField = ''
        self.hand.sort()
        self.field.sort()
        for card in self.hand:
            strHand += '[%s] ' % card
        for card in self.field:
            strField += '[%s] ' % card
        if strHand == '':
            strHand = '[Empty]'
        if strField == '':
            strField = '[Empty]'
        result = '-'*15 + self.name + '-'*15 + '\n'
        result += 'Hand:\n' + strHand + '\n'
        result += 'Field:\n' + strField + '\n'
        return result

    def get_field(self):
        strField = ''
        self.field.sort()
        for card in self.field:
            strField += '[%s] ' % card
        if strField == '':
            strField = '[Empty]'
        result = '-'*15 + self.name + '-'*15 + '\n'
        result += 'Field:\n' + strField + '\n'
        return result

    def place_on_field(self, card):
        self.field.append(card)
        if self.field.count(card) == 4 or len(self.hand) == 0:
            return 'lose'
        return ''

    def call_card(self, statement):
        '''
        Mechanism for calling a card that has been passed to a player. Game object
        handles management of the field of the losing player.
        '''
        call = self.interface.call_card(statement)
        if call == statement.value:
            return 'correct'
        return 'incorrect' 

    def pass_card(self, card):
        player_to_pass_to, statement = self.interface.pass_card(card)
        return (player_to_pass_to, statement)

    def call_or_pass_card(self, statement):
        decision = self.interface.call_or_pass_card(self)
        if decision == 'call':
            return ('call', self.call_card(statement))
        elif decision == 'pass':
            return ('pass', self.pass_card(statement.card))

    def pass_card_from_hand(self):
        '''
        This is the passing of a card that occurs after a player loses a round. If they
        are forced to pass with no cards in their hand, then they lose.

        Returns (player, card, statement) 
        '''
        player, statement = self.interface.pass_card_from_hand()
        self.hand.remove(statement.card)
        return (player, statement)

    def game_start(self, game):
        self.interface.game_start(game)

    def loss(self):
        self.interface.loss()

    def win(self):
        self.interface.win()
        
class Game:
    '''
    Keeps track of the current game state.
    '''
    def __init__(self, players, display=True, sleepDuration = 0.5):
        global CARD_LABELS
        self.sleepDuration = 0.5 # Time to wait in-between updates
        self.players = players # should be a list of initialized players
        self.validPlayers = self.players.copy() # list of players who haven't seen current card
        self.deck = CARD_LABELS*8
        random.shuffle(self.deck)
        self.display = display # Controls if game events will be displayed

    def __str__(self):
        result = ''
        for player in self.players:
            result += str(player)
        return result

    def get_field(self):
        result = ''
        for player in self.players:
            result += player.get_field()
        return result

    def get_state(self):
        '''
        Returns the current game state as a dictionary.
        '''
        state = {}
        pass

    def run(self):
        global CARD_LABELS
        global NAMES
        # Dealing hands
        random.shuffle(self.deck)
        numCardsPerP = int(float(len(self.deck))/float(len(self.players)))
        random.shuffle(NAMES)
        playerNames = '' 
        for i, p in enumerate(self.players):
            p.hand = self.deck[i*numCardsPerP: (i+1)*numCardsPerP]
            p.name = NAMES[i]
            playerNames += p.name + ', '
            p.game_start(self)
        playerNames = playerNames[:-2]
        losingPlayer = random.choice(self.players) # Losing player goes first
        if self.display:
            print("Players in game: %s" % playerNames)
            print("%s is starting the game." % losingPlayer.name)
            time.sleep(self.sleepDuration)
        lost = False
        while not lost:
            self.validPlayers = self.players.copy() # list of players who haven't seen current card
            self.validPlayers.remove(losingPlayer) # so player can't pass to himself
            passingPlayer = losingPlayer
            currentPlayer, statement = passingPlayer.pass_card_from_hand()
            if self.display:
                print("%s passed to %s, claiming it was a [%s]." % (passingPlayer.name, 
                    currentPlayer.name, statement.bluff))
            turn_over = False
            # Gameplay loop where last player hasn't been reached
            while len(self.validPlayers) > 1:
                # print("Current Player: %s" % currentPlayer.name)
                self.validPlayers.remove(currentPlayer)
                result = currentPlayer.call_or_pass_card(statement)
                # print(result)
                if result[0] == 'call':
                    if result[1] == 'correct':
                        losingPlayer = passingPlayer
                    elif result[1] == 'incorrect':
                        losingPlayer = currentPlayer
                    if losingPlayer.place_on_field(statement.card) == 'lose':
                        lost = True
                    if self.display:
                        print("%s called the card %sly. The card was a [%s]. %s lost this round."  % (currentPlayer.name, result[1], statement.card, losingPlayer.name))
                        time.sleep(self.sleepDuration)
                        print("The current game state is: ")
                        print(self.get_field())
                        time.sleep(self.sleepDuration)
                    turn_over = True
                    break
                elif result[0] == 'pass':
                    passingPlayer = currentPlayer
                    currentPlayer = result[1][0]
                    statement = result[1][1]
                    if self.display:
                        print("%s passed to %s, claiming it was a [%s]." % (passingPlayer.name, 
                            currentPlayer.name, statement.bluff))
            if not turn_over:
                # Current player is the last player and must call card
                result = currentPlayer.call_card(statement)
                if result == 'correct':
                    losingPlayer = passingPlayer
                elif result == 'incorrect':
                    losingPlayer = currentPlayer
                if losingPlayer.place_on_field(statement.card) == 'lose':
                    lost = True
                if self.display:
                        print("%s called the card %sly. The card was a [%s]. %s lost this round."  % (currentPlayer.name, result, statement.card, losingPlayer.name))
                        time.sleep(self.sleepDuration)
                        print("The current game state is: ")
                        time.sleep(self.sleepDuration)
                        print(self.get_field())
        # Notifying players of victory or loss
        for player in self.players:
            if player == losingPlayer:
                losingPlayer.loss()
            player.win()
        print("The game has concluded with %s's loss." % losingPlayer.name)


                        


                 
            
            
            
            



            
            




        
