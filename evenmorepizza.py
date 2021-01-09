from functools import reduce
from itertools import combinations
from sys import argv
from time import time


def find_delivery(remaining, bigfirst, strat):
    MAXTRIES = 10**3

    bestdeliveries = []
    bestscore = 0
    
    for i, c in enumerate(combinations([bf for bf in bigfirst if bf[0] in remaining], sum(strat))):
        if i == MAXTRIES:
            break

        deliveries = []
        score = 0

        for s in strat:
            delivery = c[sum([len(d) for d in deliveries]):sum([len(d) for d in deliveries])+s]
            deliveries.append([d[0] for d in delivery])
            score += len(reduce(lambda a,b: set(a)|set(b), [entry[1] for entry in delivery]))**2

        if score > bestscore:
            bestscore = score
            bestdeliveries = deliveries

    return bestdeliveries, bestscore


def solve(m, t2, t3, t4, pizzas):
    deliveries = []
    bigfirst = sorted([(x, pizzas[x]) for x in range(m)], key=lambda pair: -len(pair[1]))
    remaining = {x for x in range(m)}
    score = 0

    while True:
        strat = [4] * min(2, t4) + [3] * min(2, t3) + [2] * min(2, t2)

        if len(strat) < 2:
            if len(strat) == 1:
                if sum(strat) <= len(remaining):
                    delivery, value = find_delivery(remaining, bigfirst, strat)
                    score += value

            return deliveries, score

        bestdeliveries = None
        bestscore = 0
        seen = set()

        for pair in combinations(strat, 2):
            if pair in seen:
                continue

            if sum(pair) <= len(remaining):
                delivery, value = find_delivery(remaining, bigfirst, pair)

                if value > bestscore:
                    bestdeliveries = delivery
                    bestscore = value

                seen.add(pair)

        if not bestscore:
            return deliveries, score
        
        score += bestscore

        for delivery in bestdeliveries:
            remaining -= set(delivery)
            deliveries.append([len(delivery)] + delivery)

            if len(delivery) == 4:
                t4 -= 1
            elif len(delivery) == 3:
                t3 -= 1
            else:
                t2 -= 1


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
        t = time()
        outputfile = (file[:file.find('.')] if '.' in file else file) + '.out'
        
        with open(file) as f:
            m, t2, t3, t4 = map(int, f.readline().split())
            pizzas = []

            for _ in range(m):
                pizza = f.readline().split()
                pizzas.append(pizza[1:])

            deliveries, score = solve(m, t2, t3, t4, pizzas)

            print(f'Finished {file} with score {score} in {time()-t} seconds.')

            with open(outputfile, 'w') as g:
                g.write(str(len(deliveries)) + '\n')
                
                for delivery in deliveries:
                    g.write(' '.join(str(i) for i in delivery) + '\n')

if __name__ == '__main__':
    main()