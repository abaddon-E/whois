#! env/bin/python
# coding: utf-8
import itertools
import whois
import json
import sqlite3

CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
TLDS = ('ir', 'com')
REPEAT = 3

def main(try_tld=None, try_domain_index=None):
    if not try_tld or not try_domain_index:
        create_table()
    chains = itertools.product(CHARACTERS, repeat=REPEAT)
    for tld in TLDS:
        if try_tld and try_tld != tld:
            continue
        for counter, chain in enumerate(chains):
            if try_domain_index and try_domain_index < counter:
                continue
            domain = creat_domain(chain, tld)
            res = whois.whois(domain)
            if not res['emails']:
                print 'available domain:  %s' % domain
                insert_to_db(domain, counter)

def creat_domain(chain, tld):
    response = ''
    for character in chain:
        response += character
    response += '.%s' % tld
    return response


def create_table():
    connection = db().cursor()
    # Create table
    connection.execute('''CREATE TABLE domains (domain, counter)''')
    db().close()

def insert_to_db(domain, index):
    connection = db().cursor()
    connection.execute("INSERT INTO domains VALUES ('%s', '%s')" % (domain, index))
    db().commit()
    db().close()

def select_all():
    connection = db().cursor()
    row = connection.execute("SELECT * FROM domains")
    db().close()
    return row

def db():
    connection = sqlite3.connect('domain.db')
    return connection

def export():
    available = list()
    for row in select_all():
        available.append(row[0])

    with open("domains.json", "a") as f:
        f.write(json.dumps(available))
        f.close()



if __name__ == '__main__':
    main()
    export()
