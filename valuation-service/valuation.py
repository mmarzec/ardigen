import csv


def read_products_data(csvfile):
    data = []
    data_csv = csv.DictReader(csvfile)
    for row in data_csv:
        row['id'] = int(row['id'])
        row['price'] = float(row['price'])
        row['quantity'] = int(row['quantity'])
        row['matching_id'] = int(row['matching_id'])
        data.append(row)
    return data

def read_currencies(csvfile):
    currencies = {}
    currencies_csv = csv.DictReader(csvfile)
    for item in currencies_csv:
        currencies[item['currency']] = float(item['ratio'])
    return currencies

def read_top_priced_count(csvfile):
    matchings_id_top_priced_count = {}
    top_priced_count_csv = csv.DictReader(csvfile)
    for item in top_priced_count_csv:
        matchings_id_top_priced_count[int(item['matching_id'])] = int(item['top_priced_count'])
    return matchings_id_top_priced_count

def get_top_products(products, currencies, matchings_id_top_priced_count):

    # count_total_pln_price
    for item in products:
        item['total_pln_price'] = item['price'] * currencies[item['currency']] * item['quantity']

    # group data by matching_id
    data_grouped_by_matching_id = {}
    for item in products:
        if not item['matching_id'] in data_grouped_by_matching_id:
            data_grouped_by_matching_id[item['matching_id']] = []
        data_grouped_by_matching_id[item['matching_id']].append(item)

    # sort by total_pln_price
    for matching_id in data_grouped_by_matching_id:
        data_grouped_by_matching_id[matching_id].sort(key=lambda k: k['total_pln_price'], reverse=True)

    # prepare top_products
    top_products = []
    for matching_id in data_grouped_by_matching_id:
        top_product = {}
        top_product['matching_id'] = matching_id

        # limit data set by top_priced_count
        limited_data_set = data_grouped_by_matching_id[matching_id][0:matchings_id_top_priced_count[matching_id]]

        # count ignored_products
        ignored_products = len(data_grouped_by_matching_id[matching_id]) - matchings_id_top_priced_count[matching_id]
        if ignored_products < 0:
            ignored_products = 0
        top_product['ignored_products_count'] = ignored_products

        # count total price and avg_price
        total_price = 0
        avg_price_quantity_count = 0
        for item in limited_data_set:
            total_price += item['total_pln_price']
            avg_price_quantity_count += item['quantity']
        top_product['total_price'] = total_price
        if avg_price_quantity_count > 0:
            top_product['avg_price'] = total_price / avg_price_quantity_count
        else:
            top_product['avg_price'] = 0

        # currency is normalized to PLN
        top_product['currency'] = 'PLN'

        top_products.append(top_product)

    return top_products


if __name__ == '__main__':


    # read input files

    # read products data
    with open('data.csv', 'rb') as csvfile:
        products = read_products_data(csvfile)

    # read currencies
    currencies = {}
    with open('currencies.csv', 'rb') as csvfile:
        currencies = read_currencies(csvfile)

    # read matchings top_priced_count
    with open('matchings.csv', 'rb') as csvfile:
        matchings_id_top_priced_count = read_top_priced_count(csvfile)


    # calculate output data
    top_products = get_top_products(products, currencies, matchings_id_top_priced_count)


    # save final result
    with open('top_products.csv', 'w') as csvfile:
        fieldnames = ['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in top_products:
            writer.writerow(item)
