
from whois import query


def create_list1(file):
    with open(file) as f:
        cast_list = [line.replace('\n', '.com') for line in f]
    return cast_list


def create_list2(file):
    with open(file) as f:
        domains = []
        for line in f:
            d1 = line.replace('\n', 'exchange.com')
            d2 = line.replace('\n', 'finance.com')
            d3 = line.replace('\n', 'financial.com')
            d4 = line.replace('\n', 'fx.com')
            d5 = line.replace('\n', 'coin.com')
            d6 = 'bit' + line.replace('\n', '.com')
            domains += [d1, d2, d3, d4, d5, d6]
    return domains




dotcom3000 = create_list1('english3000.txt')
fxdotcom = create_list2('english3000.txt')


print(dotcom3000)
print(fxdotcom)


def check_domain(name):
    try:
        domain = query(name)

        if domain is None:
            result = name + ' is AVAILABLE\n'
            print(result)
            f = open('domain-available.txt', 'a')
            f.write(name + '\n')
            f.close()
        else:
            print(name + ' is TAKEN')
            # f = open('domain-available.txt', 'a')
            # f.write(name + '\n')
            # f.close()
    except Exception as e2:
        print(name, 'error: ', e2)



#for name in fxdotcom:
#    check_domain(name)

##34