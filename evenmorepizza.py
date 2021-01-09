from sys import argv


def find_delivery(remaining, bigfirst, n):
    delivery = []

    for x, _ in bigfirst:
        if x in remaining:
            delivery.append(x)
            
            if len(delivery) == n:
                return delivery


def solve(m, t2, t3, t4, pizzas):
    deliveries = []
    bigfirst = sorted([(x, pizzas[x]) for x in range(m)], key=lambda pair: -len(pair[1]))
    remaining = {x for x in range(m)}

    while t4:
        if len(remaining) < 4:
            break

        delivery = find_delivery(remaining, bigfirst, 4)
        remaining -= set(delivery)
        deliveries.append(delivery)

    while t3:
        if len(remaining) < 3:
            break

        delivery = find_delivery(remaining, bigfirst, 3)
        remaining -= set(delivery)
        deliveries.append(delivery)

    while t2:
        if len(remaining) < 2:
            break

        delivery = find_delivery(remaining, bigfirst, 2)
        remaining -= set(delivery)
        deliveries.append(delivery)

    return deliveries


def main():
    inputfiles = {
        'a': 'a_example',
        'b': 'b_little_bit_of_everything.in',
        'c': 'c_many_ingredients.in',
        'd': 'd_many_pizzas.in',
        'e': 'e_many_teams.in'
    }

    to_run = []

    if len(argv) > 2:
        print('This script only takes one optional parameter. Run either parameterless, or with one parameter, containing the letter codes for the input files you wish to process!')
        return

    if len(argv) == 2:
        if any(c not in 'abcde' for c in argv[1]):
            print('Illegal option', argv[1])
            return

        for c in set(argv[1]):
            to_run.append(inputfiles[c])

    else:
        to_run += list(inputfiles.values())

    to_run.sort()

    print('Going to run:')
    print('\n'.join(to_run))

    for file in to_run:
        outputfile = (file[:file.find('.')] if '.' in file else file) + '.out'
        
        with open(file) as f:
            m, t2, t3, t4 = map(int, f.readline().split())
            pizzas = []

            for _ in range(m):
                pizza = f.readline().split()
                pizzas.append((int(pizza[0]), pizza[1:]))

            deliveries = solve(m, t2, t3, t4, pizzas)

            with open(outputfile, 'w') as g:
                g.write(int(len(deliveries)))
                
                for delivery in deliveries:
                    g.write(' '.join(str(i) for i in delivery))

if __name__ == '__main__':
    main()