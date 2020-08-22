from whois import query
from english import english10k
from itertools import product


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
           'p','q','r','s','t','u','v','w','x','y','z']

five = [a + b + c + d + e for a in letters for b in letters for c in letters for d in letters for e in letters ]
app3 = [a + b + c + '.app' for a in letters for b in letters for c in letters]

com10k = [word + '.com' for word in english10k]




def check_domain(name: str):
    domain_name = name
    domain = query(domain_name)
    if domain is None:
        print(f'{domain_name} is available')
        with open('available_com.txt', 'a') as f:
            f.write(domain_name + '\n')
    else:
        print(f'{domain.name} ')
        #print(domain.expiration_date)
        #print(domain.__dict__)


with open('english10k.txt', 'r') as f:
    words1 = f.read().replace('\n', '\n').splitlines()
    words2 = sorted([x.strip() for x in words1])


def check_words():
    for w in com10k:
        try:
            check_domain(w)
        except Exception as e:
            print('err', e)


def action1():
    with open('english.py', 'a') as f:
        f.write(str(words2))


if __name__ == "__main__":
    check_words()
    print('done')
