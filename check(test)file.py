import random

def new_deck():
    cards = []
    suits = ["Club", "Diamonds", "Spades", "Hearts"]
    Values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for Suit in suits:
        for Value in Values:
            Quicklist = [Value, Suit]
            cards.append(Quicklist)
    random.shuffle(cards)
    return cards

def split_player_plays(hand, deck):
    while True:
        print(hand)
        user = input("Hit or Stand: ")
        if user == "Hit":
            hand.append(deck.pop(0))
            print(hand)
            v = value_check(hand)
            if v >= 21:
                return v
        if user == "Stand":
            v = value_check(hand)
            return v


def split_check(hand):
    print(len(hand))
    if len(hand) != 2:
        return "Can't"
    print(hand[0][0])
    print(hand[1][0])
    if hand[0][0] != hand[1][0]:
        return "Can't"
    else:
        return "Good"


def split(hand, deck):
    if len(hand) != 2:
        return "Can't"
    if hand[0][0] != hand[1][0]:
        return "Can't"
    else:
        handone = [hand.pop(0)]
        handtwo = [hand.pop(0)]
        one = split_player_plays(handone, deck)
        two = split_player_plays(handtwo, deck)
        if one >= two:
            return one
        else:
            return two


def changevalue(value):
    if value == "A":
        return 11
    if value == "2":
        return 2
    if value == "3":
        return 3
    if value == "4":
        return 4
    if value == "5":
        return 5
    if value == "6":
        return 6
    if value == "7":
        return 7
    if value == "8":
        return 8
    if value == "9":
        return 9
    if value == "10":
        return 10
    if value == "J" or value == "Q" or value == "K":
        return 10


def value_check(checklist):
    value = 0
    Ace_count = 0
    Ace_check = False
    for i in checklist:
        if i[0] == "A":
            Ace_check = True
    for x in checklist:
        v = changevalue(x[0])
        value += v
        if Ace_check == True:
            while value > 21 or Ace_count > 0:
                value -= 10
    return value

if __name__ == '__main__':
    dealer = [["A", "S"], ["2", "S"], ["A", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["2", "S"], ["3", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["2", "S"], ["A", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["2", "S"], ["A", "S"], ["A", "S"]]
    print(value_check(dealer))
    dealer = [["2", "S"], ["2", "S"], ["3", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["2", "S"], ["A", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["K", "S"]]
    print(value_check(dealer))
    dealer = [["A", "S"], ["9", "S"], ["K", "S"]]
    print(value_check(dealer))
    print("")
    dealer = [["A", "S"], ["A", "S"]]
    print(split_check(dealer))
    dealer = [["A", "S"]]
    print(split_check(dealer))
    dealer = [["A", "S"], ["2", "S"]]
    print(split_check(dealer))
    dealer = [["10", "S"], ["K", "S"]]
    print(split_check(dealer))
