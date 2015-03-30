import argparse

import requests


def pushbulletable_devices():
    parser = argparse.ArgumentParser(description='Findout your PushBullet'
                                                 ' devices iden.')
    parser.add_argument('k', help='Your PushBullet Access Token. '
                                  'https://www.pushbullet.com/account')
    args = parser.parse_args()
    key = args.k
    url = 'https://api.pushbullet.com/v2/devices'
    headers = {'content-type': 'application/json',
               'Auth'
               'orization': 'Bearer ' + key}
    r = requests.get(url, headers=headers)
    for i in r.json()['devices']:
        if i['active']:
            print(i['nickname'] + '\t\tIDEN:\t' + i['iden'])


if __name__ == "__main__":
    print(pushbulletable_devices())