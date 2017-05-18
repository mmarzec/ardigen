import argparse
import sys


def fizzbuzz(n, m):
    numbers = xrange(n, m + 1)
    for number in numbers:
        if number % 15 == 0:  # multiples of both three and five
            yield 'FizzBuzz'
        elif number % 3 == 0:
            yield 'Fizz'
        elif number % 5 == 0:
            yield 'Buzz'
        else:
            yield str(number)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='from n')
    parser.add_argument('m', type=int, help='to m')
    args = parser.parse_args()


    # verify input
    if not 0 < args.n <= 10000:
        print 'input n={} out of range 0 < n <= 10000'.format(args.n)
        sys.exit(1)
    if not 0 < args.m <= 10000:
        print 'input m={} out of range 0 < m <= 10000'.format(args.m)
        sys.exit(1)
    if args.n >= args.m:
        print 'n={} >= m={} (should be n<m)'.format(args.n, args.m)
        sys.exit(1)


    # print input
    print 'input:'
    print args.n
    print args.m
    print


    # print output
    print 'output:'
    for item in fizzbuzz(args.n, args.m):
        print item
