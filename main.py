import itertools
import whois
import json

CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
TLDS = ('ir', 'com')
REPEAT = 3
AVAILABLE = list()

def main():
    chains = itertools.product(CHARACTERS, repeat=REPEAT)
    for tld in TLDS:
        for chain in chains:
            check_domain = creat_domain(chain, tld)
            print check_domain
            res = whois.whois(check_domain)
            if not res['emails']:
                AVAILABLE.append(check_domain)

def creat_domain(chain, tld):
    response = ''
    for character in chain:
        response += character
    response += '.%s' % tld
    return response

def get_json():
    main()
    with open("domains.json", "a") as f:
        f.write(json.dumps(AVAILABLE))
        f.close()

if __name__ == '__main__':
    get_json()
