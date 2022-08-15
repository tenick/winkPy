import re
from enum import IntEnum
from collections import deque
import traceback
from typing import Callable
import time
import logging

import ring as Ring
from ring import Bet

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class RingState(IntEnum):
    CAN_BET = 1
    CANT_BET = 2


class RingDriver:
    def GetCurrentRingState(self) -> RingState:
        wheel = self.driver.find_element(By.XPATH, Ring.WHEEL_CURRENT_STATE_XPATH)

        try:
            if len(wheel.text) > 0 and wheel.text[0].isdigit():
                return RingState.CAN_BET
            else:
                return RingState.CANT_BET
        except Exception as e:
            logging.error(traceback.format_exc())
            return RingState.CANT_BET

    @staticmethod
    def WaitForState(state: RingState) -> Callable[[uc.Chrome], bool]:
        def _predicate(driver: uc.Chrome):
            wheel = driver.find_element(By.XPATH, Ring.WHEEL_CURRENT_STATE_XPATH)
            
            try:
                if len(wheel.text) > 0 and wheel.text[0].isdigit():
                    return state == RingState.CAN_BET
                else:
                    return state == RingState.CANT_BET
            except Exception as e:
                logging.error(traceback.format_exc())
                return state == RingState.CANT_BET

        return _predicate
    
    def start(self) -> None:
        self.profile = r'C:\Users\usare\AppData\Local\Google\Chrome\User Data\Default'
        self.options = uc.ChromeOptions()
        self.options.add_argument(f"user-data-dir={self.profile}")
        self.driver = uc.Chrome(driver_executable_path='./chromedriver.exe', options=self.options, use_subprocess=True)
        
        # open Wink Ring in google chrome
        self.driver.get(Ring.LINK)

    def init_ring(self) -> None:
        # switch to wink ring's game iFrame
        WebDriverWait(self.driver, 100).until(EC.frame_to_be_available_and_switch_to_it(0))
        print("successfully switched to frame")

        # initialize betting elements
        self.bet2x = self.driver.find_element(By.XPATH, Ring.BET2X_XPATH)
        self.bet3x = self.driver.find_element(By.XPATH, Ring.BET3X_XPATH)
        self.bet5x = self.driver.find_element(By.XPATH, Ring.BET5X_XPATH)
        self.bet50x = self.driver.find_element(By.XPATH, Ring.BET50X_XPATH)

        self.trx_bet_amount_input = self.driver.find_element(By.XPATH, Ring.TRX_BET_AMOUNT_INPUT_XPATH)

    def do_bet(self, trx_size: int, bet_multiplier: Bet):
        # set the bet amount input first (if necessary)
        self.trx_bet_amount_input.click()
        wink_trx_bet_size = self.trx_bet_amount_input.get_attribute('value')
        time.sleep(0.04)
        if int(wink_trx_bet_size) != trx_size:
            # selecting textbox contents to be overrided
            self.trx_bet_amount_input.send_keys(Keys.CONTROL + "a")
            time.sleep(0.08) # 80 ms

            # entering digit by digit
            for digit in str(trx_size):
                self.trx_bet_amount_input.send_keys(digit)
                time.sleep(0.08) # 80 ms
        
        time.sleep(0.1)

        # then proceed bet
        match bet_multiplier:
            case Bet.X2:
                self.bet2x.click()
            case Bet.X3:
                self.bet3x.click()
            case Bet.X5:
                self.bet5x.click()
            case Bet.X50:
                self.bet50x.click()
        
        print('betting', trx_size, 'trx at', bet_multiplier)
    
    def wait_for_ring_state(self, state: RingState) -> None:
        WebDriverWait(self.driver, 100).until(self.WaitForState(state))

    def get_history(self) -> deque[Ring.Bet]:
        bet_history = deque([Ring.Bet])

        # get history
        history = self.driver.find_element(By.XPATH, Ring.HISTORY_XPATH)
        history_bets = history.find_elements(By.XPATH, Ring.HISTORY_BETS_XPATH)
        for bet_li in history_bets:
            bet_class = bet_li.get_attribute('class')
            match = re.search('2x|3x|5x|50x', bet_class)
            s, e = match.span()
            bet = bet_class[s:e]
            bet_history.append(Ring.TextToBet(bet))
        return bet_history

    def stop(self) -> None:
        self.driver.quit()
        self.driver = None

