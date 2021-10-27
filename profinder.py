#!/usr/bin/env python3
import os
import config
import argparse
import time
import json

from telethon import TelegramClient, events
from dotenv import load_dotenv
from processing import Profinder
from colorama import init
init(autoreset=True)
from colorama import Fore, Back


# load api id and api hash from .env
load_dotenv()
try:
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
except:
    print('API_ID or API_HASH envar isn\'t set!')
    exit(0)

parser = argparse.ArgumentParser(description="Profinder")
parser.add_argument('-n', '--names', default=None, help='File with names')
parser.add_argument('-g', '--groups', default=None, help='File with groups')
parser.add_argument('-M', '--more', action='store_true', help='More combinations (may produce a lot of useless results) [for files]')
parser.add_argument('-s', '--sleep', type=int, default=None, help='Sleep for n seconds between each name resolution')
parser.add_argument('-o', '--outfile', default=None, help='File to save results')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
args = parser.parse_args()

# parse files if passed
if args.names:
    names = {}
    with open(args.names, 'r') as f:
        for n in f:
            ns = n.strip().split(' ')
            if len(ns) > 2:
                ns = ns[:2]
            name = ' '.join(ns)
            if not args.more:
                ns = [' '.join(ns)]
            else:
                ns = [' '.join(ns), ns[0]]
            names[name] = ns
    config.names = names
if args.groups:
    groups = []
    with open(args.groups, 'r') as f:
        for g in f:
            groups.append(g.strip())
    config.groups = groups

client = TelegramClient('Profinder', api_id, api_hash)
client.start()

p = Profinder(client, config.groups)
matches = {}
for test in config.names.keys():
    m = p.findUser(config.names[test])
    if args.verbose:
        print(Fore.BLUE + f'Name {test}:')
        print(Fore.BLUE + str(m))

    matches[test] = m
    if args.sleep:
        time.sleep(args.sleep)

data = json.dumps(matches, ensure_ascii=False).encode('utf8')
data = data.decode()
print(Fore.GREEN + data)

if args.outfile:
    with open(args.outfile, 'w') as f:
        f.write(data)

client.disconnect()
