from enum import IntEnum

LINK = 'https://www.wink.org/games/dice/ring'

BET2X_XPATH = '//div[@class="bet-button-click-value" and contains(.,"2")]'
BET3X_XPATH = '//div[@class="bet-button-click-value" and contains(.,"3")]'
BET5X_XPATH = '//div[@class="bet-button-click-value" and contains(.,"5") and not(contains(.,"0"))]'
BET50X_XPATH = '//div[@class="bet-button-click-value" and contains(.,"5") and contains(.,"0")]'

HISTORY_XPATH = '//ul[@class="ring-history"]'
HISTORY_BETS_XPATH = '//ul[@class="ring-history"]/li'

WHEEL_CURRENT_STATE_XPATH = '//div[@class="ring-wheel-arrow-container"]/div/div[1]'

# https://stackoverflow.com/questions/28125055/enum-in-python-doesnt-work-as-expected
# problem with enum being imported in different files, comparison Enum.type1 (imported in file 1) == Enum.type1 (imported in file 2) returns False, fix is use IntEnum

class Bet(IntEnum):
    X2 = 1
    X3 = 2
    X5 = 3
    X50 = 4

def BetToColor(bet: Bet) -> str:
    match bet:
        case Bet.X2:
            return '#652fff'
        case Bet.X3:
            return '#ff613f'
        case Bet.X5:
            return '#0094ff'
        case Bet.X50:
            return '#fbb709'

def TextToBet(text: str) -> Bet:
    match text:
        case '2x':
            return Bet.X2
        case '3x':
            return Bet.X3
        case '5x':
            return Bet.X5
        case '50x':
            return Bet.X50