import os
import env
import secrets
import time
from decimal import Decimal, ROUND_DOWN
from web3 import Web3


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def gen_w3(http_provider):
    return Web3(Web3.HTTPProvider(http_provider))


def gen_pk():
    return secrets.token_hex(32)


def get_address(w3, pk):
    return w3.eth.account.from_key(pk).address


def get_balance(w3, address):
    return w3.eth.get_balance(address)


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())


def scan(w3):
    curr_time = get_time()
    pk = gen_pk()
    address = get_address(w3, pk)
    balance = Decimal(w3.fromWei(get_balance(w3, address), 'ether')
                      ).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    curr_time = get_time()

    print(f'[{curr_time}] {bcolors.HEADER}{pk}{bcolors.ENDC} {bcolors.OKCYAN}{address}{bcolors.ENDC} {bcolors.OKGREEN if balance > 0 else bcolors.FAIL}{str(balance)} ETH{bcolors.ENDC}')

    if (balance > 0):
        print(f'{bcolors.OKGREEN}JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT JACKPOT{bcolors.ENDC}')
        return True


def main():
    w3 = gen_w3(
        f'https://eth-mainnet.alchemyapi.io/v2/{os.getenv('ALCHEMY_SECRET')}')
    detect = False
    print('LETS BEGIN')
    start = time.time()
    while True:
        detect = scan(w3)
        if detect:
            time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
            print('TASK COMPLETE')
            return

    return f'{bcolors.FAIL}NO YIELD{bcolors.ENDC}'


main()
