import time
import certifi
import ssl
import aiohttp
import asyncio
import secrets
from decouple import config
from web3 import Web3
from ens import ENS

from data import names, mythologicalCreatures

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

tests = []
valids = []


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


async def get(ns, session, name, retry_limit):
    v2 = None
    for attempt in range(retry_limit):
        try:
            owner = ns.owner(name)

            if (owner == "0x0000000000000000000000000000000000000000"):
                valids.append(name)
                print(
                    f'{bcolors.HEADER}{name}{bcolors.ENDC} {bcolors.OKGREEN}VALID{bcolors.ENDC}')
            else:
                print(
                    f'{bcolors.HEADER}{name}{bcolors.ENDC} {bcolors.FAIL}BRUH{bcolors.ENDC}')

            return
        except Exception as e:
            pass

    print(f'❌ {name}')


async def main(retry_limit=500):
    start_time = time.time()
    ALCHEMY_KEY = config('ALCHEMY_KEY')
    w3 = Web3(Web3.HTTPProvider(
        f'https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_KEY}'))
    ns = ENS.fromWeb3(w3)

    async with aiohttp.ClientSession(trust_env=True) as session:
        # await asyncio.gather(*[get(ns, session, f'{d}.eth', retry_limit) for d in set(mythologicalCreatures)])
        # await asyncio.gather(*[get(ns, session, f'{name}.eth', retry_limit) for name in names])
        # await asyncio.gather(*[get(ns, session, f'{str(num).zfill(3)}.eth', retry_limit) for num in range(644, 999)])
        # await asyncio.gather(*[get(ns, session, f'{str(num).zfill(4)}.eth', retry_limit) for num in range(1, 9999)])
        # await asyncio.gather(*[get(ns, session, f'{str(num).zfill(5)}.eth', retry_limit) for num in range(1, 99999)])

    finalized_time = time.time() - start_time
    print("--- DONE ---")
    print("--- %s seconds ---" % (finalized_time))

    print('valids:', valids)


asyncio.run(main())
