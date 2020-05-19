#!/usr/bin/python3
import os 

import pandas as pd
from progress.bar import Bar
from datetime import datetime

import api
import output
import cli

def replace_dash(folio):
    return int(folio.replace('-', ''))

def date_parse(str):
    date = [int(n) for n in str.split('/')]
    year, month, day = date[-1], date[-3], date[-2]
    return datetime(year, month, day)

def get_contracts_from_raw_data(json_dict, with_second_owner=False,
                                min_date=None):
    """
    Arguments:
        json_dict {dict} -- json dict with parsed info from website
    
    Returns:
        object -- pandas.Series like table rows from website
    """
    columns = ['Folio', 'Date', 'Price', 'OR Book-Page',
               'Qualification Description', 'Seller', 'Buyer']
    if with_second_owner:
        columns.extend(['Seller 2', 'Buyer 2'])

    contracts = []
    for p in json_dict['SalesInfos']:
        # date filter
        if min_date != None:
            if min_date > date_parse(p['DateOfSale']):
                continue

        bookpage = '%s-%s' % (p['OfficialRecordBook'], 
                              p['OfficialRecordPage'])

        contract = [folio, p['DateOfSale'], p['SalePrice'], 
                    bookpage, p['QualificationDescription'],
                    p['GrantorName1'],  p['GranteeName1']]
        if with_second_owner:
            contract.extend([p['GrantorName2'], p['GranteeName2']])

        contracts.append(pd.Series(contract, columns))
    return contracts
    

if __name__ == '__main__':
    folios_list = pd.read_csv(cli.args.csv, squeeze=True)
    Progressbar = Bar('Processing property information', max=len(folios_list))

    contracts_table = []
    for folio in folios_list:
        json = api.get_contracts_info_by_folio(replace_dash(folio))
        contracts_table.extend(get_contracts_from_raw_data(json, cli.args.wso, 
                                                           cli.args.min_year))
        Progressbar.next()
    contracts_table = pd.DataFrame(contracts_table)

    # save to excel
    sheetname = 'Sales Information'
    writer = output.format_to_excel(contracts_table, cli.args.out, sheetname)
    writer.save()

    Progressbar.finish()

    print('Owner data success saved in:')
    print(os.path.abspath(cli.args.out))

