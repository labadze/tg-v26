import csv
import datetime
import os
import sys
import time

from telethon.sync import errors, TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

TARGET_GROUP_LINK = ''
client = TelegramClient(api_id=00000, api_hash='GGGGGGG', session='SESSION_FILE')


def get_group_members():
    try:
        client.connect()
    except Exception as e:
        print(e)
    if client.get_me() is not None:
        try:
            group_entity = client.get_entity(TARGET_GROUP_LINK)
        except errors.rpcerrorlist.UsernameNotOccupiedError as e:
            print(e)
            time.sleep(1)
            try:
                client.disconnect()
            except errors.rpc_errors_re as e:
                print(e)
                time.sleep(1)

        print(group_entity)
        time.sleep(2)
        try:
            JoinChannelRequest(group_entity)
        except errors.rpc_errors_re as e:
            print(RED + 'We are getting some error...')
            print(e)
        time.sleep(1)
        try:
            members = client.get_participants(group_entity)
        except Exception as e:
            print(RED + 'We are getting some error...')
            print(e)
            time.sleep(1)
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        try:
            LeaveChannelRequest(group_entity)
            print(GREEN + 'Success...')
        except errors.rpc_errors_re as e:
            print(RED + 'We are getting some error...')
            print(e)
            time.sleep(1)
        try:
            client.disconnect()
        except errors.rpcerrorlist.PeerFloodError as e:
            print(RED + 'We cannot do this action right now because: ')
            print(e)
            time.sleep(1)
        file_name = TARGET_GROUP_LINK.replace('https://t.me/', '') + '-' + str(
            datetime.datetime.now().isoformat()) + '-members.csv'
        with open(file_name, 'w', newline='') as csv_file:
            fieldnames = ['got_at', 'group_name_url', 'id', 'is_self', 'contact',
                          'mutual_contact', 'deleted', 'bot', 'restricted',
                          'access_hash', 'first_name', 'last_name', 'username', 'status', 'was_online']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for member in members:
                print(YELLOW + 'Writing new member with id : ')
                print(str(member.id))
                if member.status is not None and hasattr(member.status, "was_online"):
                    writer.writerow({'got_at': str(datetime.datetime.now().isoformat()),
                                     'group_name_url': TARGET_GROUP_LINK,
                                     'id': member.id,
                                     'is_self': member.is_self,
                                     'contact': member.contact,
                                     'mutual_contact': member.mutual_contact,
                                     'deleted': member.deleted,
                                     'bot': member.bot,
                                     'restricted': member.restricted,
                                     'access_hash': member.access_hash,
                                     'first_name': member.first_name,
                                     'last_name': member.last_name,
                                     'username': member.username,
                                     'status': member.status,
                                     'was_online': str(member.status.was_online.replace(
                                         tzinfo=datetime.timezone.utc).isoformat())
                                     # str(member.status.was_online.replace(tzinfo=None))
                                     })
                else:
                    writer.writerow({'got_at': str(datetime.datetime.now().isoformat()),
                                     'group_name_url': TARGET_GROUP_LINK,
                                     'id': member.id,
                                     'is_self': member.is_self,
                                     'contact': member.contact,
                                     'mutual_contact': member.mutual_contact,
                                     'deleted': member.deleted,
                                     'bot': member.bot,
                                     'restricted': member.restricted,
                                     'access_hash': member.access_hash,
                                     'first_name': member.first_name,
                                     'last_name': member.last_name,
                                     'username': member.username,
                                     'status': member.status,
                                     'was_online': None
                                     })
        print(RESET)
        print(UNDERLINE + 'Returning')
        print(RESET)
    else:
        print('Session is dead')


if __name__ == '__main__':
    get_group_members()
