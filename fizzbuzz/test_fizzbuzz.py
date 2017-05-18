import fizzbuzz

def test_1():

    # input
    n = 3
    m = 16

    # expected output
    expected_otput = [
        'Fizz',
        '4',
        'Buzz',
        'Fizz',
        '7',
        '8',
        'Fizz',
        'Buzz',
        '11',
        'Fizz',
        '13',
        '14',
        'FizzBuzz',
        '16'
    ]

    output = []
    for item in fizzbuzz.fizzbuzz(n, m):
        output.append(item)
    assert expected_otput == output

def test_2():

    # input
    n = 1
    m = 2

    # expected output
    expected_otput = [
        '1',
        '2'
    ]

    output = []
    for item in fizzbuzz.fizzbuzz(n, m):
        output.append(item)
    assert expected_otput == output

def test_3():

    # input
    n = 9999
    m = 10000

    # expected output
    expected_otput = [
        'Fizz',
        'Buzz'
    ]

    output = []
    for item in fizzbuzz.fizzbuzz(n, m):
        output.append(item)
    assert expected_otput == output
