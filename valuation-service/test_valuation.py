from io import BytesIO

import pytest

import valuation



def test_read_products_data_ok():
    input_csv = """id,price,currency,quantity,matching_id
1,1000,GBP,2,3
2,1050,EU,1,1
3,2000,PLN,1,1
4,1750,EU,2,2
5,1400,EU,4,3
6,7000,PLN,3,2
7,630,GBP,5,3
8,4000,EU,1,3
9,1400,GBP,3,1
"""
    file_obj = BytesIO(input_csv)

    result = valuation.read_products_data(file_obj)
    expected = [
        {'id': 1, 'price': 1000.0, 'currency': 'GBP', 'quantity': 2, 'matching_id': 3},
        {'id': 2, 'price': 1050.0, 'currency': 'EU',  'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 4, 'price': 1750.0, 'currency': 'EU',  'quantity': 2, 'matching_id': 2},
        {'id': 5, 'price': 1400.0, 'currency': 'EU',  'quantity': 4, 'matching_id': 3},
        {'id': 6, 'price': 7000.0, 'currency': 'PLN', 'quantity': 3, 'matching_id': 2},
        {'id': 7, 'price': 630.0,  'currency': 'GBP', 'quantity': 5, 'matching_id': 3},
        {'id': 8, 'price': 4000.0, 'currency': 'EU',  'quantity': 1, 'matching_id': 3},
        {'id': 9, 'price': 1400.0, 'currency': 'GBP', 'quantity': 3, 'matching_id': 1}
    ]

    assert result == expected


def test_read_products_data_bad_data():

    input_csv = """id,price,currency,quantity,matching_id
1,asd,GBP,2,3
"""
    file_obj = BytesIO(input_csv)

    with pytest.raises(Exception):
        result = valuation.read_products_data(file_obj)


def test_read_currencies_ok():
    input_csv = """currency,ratio
GBP,2.4
EU,2.1
PLN,1
"""
    file_obj = BytesIO(input_csv)

    result = valuation.read_currencies(file_obj)
    expected = {
        'GBP': 2.4,
        'EU': 2.1,
        'PLN': 1.0
    }

    assert result == expected

def test_read_currencies_bad_data():

    input_csv = """currency,ratio
GBP,2.4
EU,2.1
PLN,asd
"""
    file_obj = BytesIO(input_csv)

    with pytest.raises(Exception):
        result = valuation.read_currencies(file_obj)


def test_read_top_priced_count_ok():
    input_csv = """matching_id,top_priced_count
1,2
2,2
3,3
"""
    file_obj = BytesIO(input_csv)

    result = valuation.read_top_priced_count(file_obj)
    expected = {
        1: 2,
        2: 2,
        3: 3
    }

    assert result == expected


def test_read_top_priced_count_bad_data():

    input_csv = """matching_id,top_priced_count
1,2
2,2
3,asd
"""
    file_obj = BytesIO(input_csv)

    with pytest.raises(Exception):
        result = valuation.read_top_priced_count(file_obj)



def test_get_top_products_1():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 5000.0, 'avg_price': 2500.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected


def test_get_top_products_2():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 30000.0, 'avg_price': 1500.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected

def test_get_top_products_3():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 1},
        {'id': 2, 'price': 1000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 2},
        {'id': 3, 'price': 2000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 2},
        {'id': 4, 'price': 2000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 1},
        {'id': 5, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 6, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 2}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2,
        2: 2
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 30000.0, 'avg_price': 1500.0, 'currency': 'PLN', 'ignored_products_count': 1},
        {'matching_id': 2, 'total_price': 30000.0, 'avg_price': 1500.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected

def test_get_top_products_4():

    input_products = [
        {'id': 1, 'price': 2000.0, 'currency': 'GBP', 'quantity': 10, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 10, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0,
        'GBP': 0.5
    }

    input_matchings_id_top_priced_count = {
        1: 2
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 30000.0, 'avg_price': 1500.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected


def test_get_top_products_5():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 0
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 0.0, 'avg_price': 0.0, 'currency': 'PLN', 'ignored_products_count': 3}
    ]

    assert result == expected

def test_get_top_products_6():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 0, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 3000.0, 'avg_price': 1500.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected

def test_get_top_products_7():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'GBP', 'quantity': 2, 'matching_id': 3},
        {'id': 2, 'price': 1050.0, 'currency': 'EU',  'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 4, 'price': 1750.0, 'currency': 'EU',  'quantity': 2, 'matching_id': 2},
        {'id': 5, 'price': 1400.0, 'currency': 'EU',  'quantity': 4, 'matching_id': 3},
        {'id': 6, 'price': 7000.0, 'currency': 'PLN', 'quantity': 3, 'matching_id': 2},
        {'id': 7, 'price': 630.0,  'currency': 'GBP', 'quantity': 5, 'matching_id': 3},
        {'id': 8, 'price': 4000.0, 'currency': 'EU',  'quantity': 1, 'matching_id': 3},
        {'id': 9, 'price': 1400.0, 'currency': 'GBP', 'quantity': 3, 'matching_id': 1}
    ]

    input_currencies = {
        'GBP': 2.4,
        'EU': 2.1,
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2,
        2: 2,
        3: 3
    }

    result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)

    expected = [
        {'matching_id': 1, 'total_price': 12285.0, 'avg_price': 3071.25, 'currency': 'PLN', 'ignored_products_count': 1},
        {'matching_id': 2, 'total_price': 28350.0, 'avg_price': 5670.0, 'currency': 'PLN', 'ignored_products_count': 0},
        {'matching_id': 3, 'total_price': 27720.0, 'avg_price': 2772.0, 'currency': 'PLN', 'ignored_products_count': 1}
    ]

    assert result == expected

def test_get_top_products_missing_currency():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'GBP', 'quantity': 1, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        1: 2
    }

    with pytest.raises(KeyError):
        result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)


def test_get_top_products_missing_matchings_id():

    input_products = [
        {'id': 1, 'price': 1000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 2, 'price': 2000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1},
        {'id': 3, 'price': 3000.0, 'currency': 'PLN', 'quantity': 1, 'matching_id': 1}
    ]

    input_currencies = {
        'PLN': 1.0
    }

    input_matchings_id_top_priced_count = {
        2: 2
    }

    with pytest.raises(KeyError):
        result = valuation.get_top_products(input_products, input_currencies, input_matchings_id_top_priced_count)
