#!/usr/bin/env python3
# hub bin python3
import dbm
from getpass import getpass

import bcrypt

install_prefix = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')

if __name__ == '__main__':
    print('create user or update password:')
    username = input('Username: ').encode()
    password = getpass()
    with dbm.open(install_prefix+'/state/passwords.dbm', 'c', 0o600) as db:
        db[username] = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print('password for user `{username}` created or updated'.format(username=username))

