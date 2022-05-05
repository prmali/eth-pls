import time
import certifi
import ssl
import aiohttp
import asyncio
import requests
import json

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


async def count(session, name, retry_limit):
    v2 = None
    for attempt in range(retry_limit):
        try:
            q1 = """
            query($name: String!) {
                domains(where: { name: $name }) {
                    labelhash
                }
            }
            """

            q2 = """
            query($id: ID!) {
                registration(id: $id) {
                    id
                    domain {
                        name
                        __typename
                    }
                    registrant {
                        id
                        __typename
                    }
                    __typename
                }
            }
            """

            v1 = {
                'name': name
            }

            if not v2:
                async with session.post('https://api.thegraph.com/subgraphs/name/ensdomains/ens', json={'query': q1, 'variables': v1}, ssl=SSL_CONTEXT) as res1:
                    r1 = await res1.json()
                    #print(name, json.dumps(r1, indent=2))

                    if len(r1['data']['domains']) == 0:
                        print(
                            f'{bcolors.HEADER}{name}{bcolors.ENDC} {bcolors.WARNING}T E S T{bcolors.ENDC}')
                        tests.append(name)
                        return

                    v2 = {
                        'id': r1['data']['domains'][0]['labelhash']
                    }

            async with session.post('https://api.thegraph.com/subgraphs/name/ensdomains/ens', json={'query': q2, 'variables': v2}, ssl=SSL_CONTEXT) as res2:
                r2 = await res2.json()
                #print(name, json.dumps(r2, indent=2))

                if not r2['data']['registration']:
                    valids.append(name)
                    print(
                        f'{bcolors.HEADER}{name}{bcolors.ENDC} {bcolors.OKGREEN}V A L I D{bcolors.ENDC}')
                else:
                    print(
                        f'{bcolors.HEADER}{name}{bcolors.ENDC} {bcolors.FAIL}B R U H{bcolors.ENDC}')

                return
        except Exception as e:
            pass

    print(f'❌ {name}')


async def main(retry_limit=500):
    start_time = time.time()
    async with aiohttp.ClientSession(trust_env=True) as session:
        print("--- 3 FILL COUNT ---")
        await asyncio.gather(*[count(session, f'{str(num).zfill(3)}.eth', retry_limit) for num in range(1, 999)])
        print("--- 4 FILL COUNT ---")
        await asyncio.gather(*[count(session, f'{str(num).zfill(4)}.eth', retry_limit) for num in range(1, 9999)])

    finalized_time = time.time() - start_time
    print("--- DONE ---")
    print("--- %s seconds ---" % (finalized_time))

    print('tests:', tests)
    print('valids:', valids)


asyncio.run(main())
