import csv
import datetime
import json
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


def send_single_message():
    client_index = 0
    account_index = 0
    dead_sessions = 0
    recipient_index = 0
    recipients = []
    campaign_results = []
    f = open("templates/message1.txt", "r")

    message = f.read()
    print(message)
    file = os.path.isfile(str('recipients.csv'))
    print(file)
    if file is True:
        print('Move file')
        # moved_file = "tmp/recipients-" + str(datetime.datetime.now().isoformat()) + '.csv'
        # shutil.move(str('campaigns/recipients.csv'), 'recipients.csv')
        if os.path.isfile('recipients.csv') is True:
            with open('recipients.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    # TODO: Fix sending with id
                    # all_recipients.append(row)
                    # print(row)
                    if len(row["username"]) > 2:
                        usr_obj = {
                            "id": row["id"],
                            "access_hash": row["access_hash"],
                            "first_name": row["first_name"],
                            "last_name": row["last_name"],
                            "username": row["username"]
                        }
                        print(usr_obj)
                        recipients.append(usr_obj)
                with open('static/clients.json') as json_file:
                    clients = json.load(json_file)
                    print(len(clients))
                    sessions = [x for x in os.listdir('sessions/.') if 'session' in x]
                    # sessions = sessions[980:]
                    available_sessions = len(sessions) - dead_sessions
                    # while account_index < available_sessions * 16:
                    while recipient_index < 800:
                        if account_index < len(recipients):
                            for session in sessions:
                                print(session)
                                client = TelegramClient(session='sessions/' + str(session).replace('.session', ''),
                                                        api_id=clients[client_index]["api_id"],
                                                        api_hash=clients[client_index]["api_hash"])

                                print('Connecting')
                                try:
                                    client.connect()
                                except Exception as e:
                                    print(e)
                                    continue
                                print('Getting me')
                                try:
                                    me = client.get_me()
                                except Exception as e:
                                    print(e)
                                    continue
                                if me is not None:
                                    print(me)
                                    try:
                                        receiver = client.get_entity(recipients[recipient_index]["username"])
                                        print(MAGENTA)
                                        print(receiver)
                                    except Exception as e:
                                        print(e)
                                        continue

                                    if receiver is not None:
                                        try:
                                            client.send_message(
                                                receiver,
                                                message=message,
                                                parse_mode='md',
                                                file="PATH_TO_IMAGE",
                                            )
                                            msg_obj = {
                                                "date_time": str(datetime.datetime.now().isoformat()),
                                                "recipient": recipients[recipient_index]["username"],
                                                "application": session,
                                                "success": True,
                                                "error": None
                                            }
                                            campaign_results.append(msg_obj)

                                            print(CYAN + 'Success, Sent...')
                                            # r += 1
                                            print(CYAN + str(recipient_index))
                                        except Exception as e:
                                            msg_obj = {
                                                "date_time": str(datetime.datetime.now().isoformat()),
                                                "recipient": recipients[recipient_index]["username"],
                                                "application": session,
                                                "success": False,
                                                "error": str(e)
                                            }
                                            campaign_results.append(msg_obj)

                                            print(e)
                                            print(RED + 'Cannot')
                                            print(recipient_index)
                                            continue
                                        try:
                                            client.disconnect()
                                            print(RESET)
                                            print('DISCONNECTING')
                                        except Exception as e:
                                            print(e)
                                            continue

                                client_index += 1
                                account_index += 1
                                recipient_index += 1
                                time.sleep(1)
                                if client_index == 60:
                                    client_index = 0
                    file_name = 'results/' + str(
                        datetime.datetime.now().isoformat()) + '-sent.csv'
                    with open(file_name, 'w', newline='') as out_csv_file:
                        fieldnames = ['date', 'recipient', 'success', 'app', 'error']
                        writer = csv.DictWriter(out_csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        for result in campaign_results:
                            writer.writerow({'date': str(datetime.datetime.now().isoformat()),
                                             'recipient': result["recipient"],
                                             'success': result["success"],
                                             'app': result["application"],
                                             'error': result["error"]
                                             })


if __name__ == '__main__':
    get_group_members()
