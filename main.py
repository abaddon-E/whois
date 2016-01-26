#! env/bin/python
# coding: utf-8
import itertools
import json
import requests
import sqlite3

CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
TLDS = ('ir', )
REPEAT = 3

def main():
    chains = itertools.product(CHARACTERS, repeat=REPEAT)
    for tld in TLDS:
        for chain in chains:
            domain = creat_domain(chain, tld)
            if check_domain_cache(domain):
                continue
            if not validate(domain):
                continue
            print 'An available domain has been found : ** %s ** ' % domain
            export(domain)


def validate(domain):
    if domain.split('.')[1] == 'ir':
        return validate_ir(domain)
    return

def validate_ir(domain):
    url = 'http://whois.nic.ir/WHOIS?name=%s' % domain
    try:
        res = requests.get(url).text
    except Exception:
        print 'Request Exception has been raised'
        return
    check_string = 'ERROR:101:'
    if check_string not in res:
        return
    return True

def creat_domain(chain, tld):
    response = ''
    for character in chain:
        response += character
    response += '.%s' % tld
    return response

def check_domain_cache(domain):
    check = False
    with open("domains.txt", "r") as f:
        if domain in f.read():
            check = True
        f.close()
    return check

def export(domain):
    with open("domains.txt", "a") as f:
        f.write(domain + '\n')
        f.close()


if __name__ == '__main__':
    main()
