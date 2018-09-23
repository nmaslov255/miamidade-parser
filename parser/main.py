#!/usr/bin/python3
import pandas as pd

import api
import output
import cli

def replace_dash(folio):
    return int(folio.replace('-', ''))

def get_contracts_from_raw_data(json_dict, with_second_owner=False):
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

        contract = {
            'Folio': folio, 'Date': p['DateOfSale'],
            'Price': p['SalePrice'], 'OR Book-Page': bookpage,
            'Qualification Description': p['QualificationDescription'],
            'Seller': p['GrantorName1'], 'Buyer': p['GranteeName1'],
        }
        if with_second_owner:
            contract.update({'Seller 2': p['GrantorName2'], 
                             'Buyer 2': p['GranteeName2']})
        contracts.append(pd.Series(contract))
    return contracts
    

if __name__ == '__main__':
    folios_list = pd.read_csv(cli.args.csv, squeeze=True)

    contracts_table = []
    for folio in folios_list:
        json = api.get_contracts_info_by_folio(replace_dash(folio))
        contracts_table.extend(
            get_contracts_from_raw_data(json, cli.args.wso))
    contracts_table = pd.DataFrame(contracts_table)

    # save to excel
    sheetname = 'Sales Information'
    writer = output.format_to_excel(contracts_table, cli.args.out, sheetname)
    writer.save()

