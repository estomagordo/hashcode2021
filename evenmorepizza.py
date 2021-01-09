from sys import argv


def find_delivery(remaining, bigfirst, n):
    value = 0
    delivery = []
    ingredients = set()

    for x, pizza in bigfirst:
        if x in remaining:
            delivery.append(x)
            ingredients |= set(pizza)
            
            if len(delivery) == n:
                return delivery, len(ingredients)**2


def solve(m, t2, t3, t4, pizzas):
    deliveries = []
    bigfirst = sorted([(x, pizzas[x]) for x in range(m)], key=lambda pair: -len(pair[1]))
    remaining = {x for x in range(m)}
    score = 0

    while t4:
        if len(remaining) < 4:
            break

        delivery, value = find_delivery(remaining, bigfirst, 4)
        score += value
        remaining -= set(delivery)
        deliveries.append([4] + delivery)
        t4 -= 1

    while t3:
        if len(remaining) < 3:
            break

        delivery, value = find_delivery(remaining, bigfirst, 3)
        score += value
        remaining -= set(delivery)
        deliveries.append([3] + delivery)
        t3 -= 1

    while t2:
        if len(remaining) < 2:
            break

        delivery, value = find_delivery(remaining, bigfirst, 2)
        score += value
        remaining -= set(delivery)
        deliveries.append([2] + delivery)
        t2 -= 1

    return deliveries, score


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
                pizzas.append(pizza[1:])

            deliveries, score = solve(m, t2, t3, t4, pizzas)

            print(f'Finished {file} with score {score}')

            with open(outputfile, 'w') as g:
                g.write(str(len(deliveries)) + '\n')
                
                for delivery in deliveries:
                    g.write(' '.join(str(i) for i in delivery))

if __name__ == '__main__':
    main()