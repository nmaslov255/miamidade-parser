#!/usr/bin/python3
import pandas as pd

import api
import output

def replace_dash(folio):
    return int(folio.replace('-', ''))

def get_contracts_from_raw_data(json_dict):
    """
    Arguments:
        json_dict {dict} -- json dict with parsed info from website
    
    Returns:
        object -- pandas.Series like table rows from website
    """
    contracts = []
    for p in json_dict['SalesInfos']:
        bookpage = '%s-%s' % (p['OfficialRecordBook'], 
                              p['OfficialRecordPage'])

        contracts.append(pd.Series({
            'Folio': folio, 'Date': p['DateOfSale'],
            'Price': p['SalePrice'], 'OR Book-Page': bookpage,
            'Qualification Description': p['QualificationDescription'],
            'Seller': p['GrantorName1'], 'Seller 2': p['GrantorName2'],
            'Buyer': p['GranteeName1'], 'Buyer 2': p['GranteeName2'],
        }))
    return contracts
    

if __name__ == '__main__':
    folio_list = pd.read_csv('~/Desktop/Miami - Dade Folio ID.csv', squeeze=True)

    contracts_table = []
    for folio in folio_list:
        json = api.get_contracts_info_by_folio(replace_dash(folio))
        contracts_table.extend(get_contracts_from_raw_data(json))
    contracts_table = pd.DataFrame(contracts_table)

    # save to excel
    outfile = 'contracts.xlsx'
    sheetname = 'Sales Information'
    writer = output.format_to_excel(contracts_table, outfile, sheetname)
    writer.save()

