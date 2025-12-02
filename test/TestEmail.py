import os
import sys
from O365 import Account



def get_mail_policy(ask):
    pending_policy = [ ]
    from pathlib import Path
    import datetime
    from O365 import Account, FileSystemTokenBackend
    dirname_root = os.path.dirname(os.path.realpath(__file__))
    token_backend = FileSystemTokenBackend(token_path=f'{dirname_root}/../../share.o365-token', token_filename='itsupport@amgwealth.com.txt')
    account = Account(credentials=(
        'c8057deb-a24e-484b-bf57-58bd5b196eb4',
        'Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN',
    ), token_backend=token_backend)
    inbox = account.mailbox().inbox_folder()
    folder = inbox.get_folder(folder_name='New Business')
    messages = folder.get_messages(limit=99)

    pass

    for message in messages:
        recv = str(message.received)
        bid = datetime.datetime.strptime(str(message.created), '%Y-%m-%d %H:%M:%S%z').timestamp()
        bid = int(bid)
        if bid > ask:
            import re
            policy_no = re.search(r'<policy no. (\d+)>', message.subject).group(1)
            pending_policy.append({
                'PolicyNo': policy_no,
                'DateCreated': message.created,
                'GroupPlacement': message.created.strftime('%Y%m%d'),
            })
    pending_policy = sorted(pending_policy, key=lambda d: d['DateCreated'])
    #
    return pending_policy

# get_mail_policy("dd")
a='c8057deb-a24e-484b-bf57-58bd5b196eb4'
b='Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN'
def testmail():
    credentials = (a, b)
    account = Account(credentials)
    inbox = account.mailbox().inbox_folder()
    folder = inbox.get_folder(folder_name='New Business')
    messages = folder.get_messages(limit=99)

testmail()
RuntimeError: No auth token found. Authentication Flow needed
