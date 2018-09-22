#!/usr/bin/python3

import pandas as pd
import numpy as np

import api

def replace_dash(folio):
    return int(folio.replace('-', ''))

def get_property_rows_from_json(json):
    rows = []
    for p in json['SalesInfos']:
        bookpage = '%s-%s' % (p['OfficialRecordBook'], 
                              p['OfficialRecordPage'])

        rows.append(pd.Series({
            'Folio': folio, 'Date': p['DateOfSale'],
            'Price': p['SalePrice'], 'OR Book-Page': bookpage,
            'Qualification Description': p['QualificationDescription'],
            'Seller': p['GrantorName1'], 'Seller 2': p['GrantorName2'],
            'Buyer': p['GranteeName1'], 'Buyer 2': p['GranteeName2'],
        }))
    return rows
    

if __name__ == '__main__':
    folio_list = pd.read_csv('Miami - Dade Folio ID.csv', squeeze=True)

    rows = []
    for folio in folio_list:
        json = api.get_properties_by_folio(replace_dash(folio))
        rows.extend(get_property_rows_from_json(json))
    rows = pd.DataFrame(rows)


    # save to exel
    output = 'contracts.xlsx'
    sheetname = 'Sales Information'

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    rows.to_excel(writer, sheet_name=sheetname, index=False)
    worksheet = writer.sheets[sheetname]
    for idx, col in enumerate(rows):
        maxlen = np.max([len(str(el)) for el in rows[col]])+1
        worksheet.set_column(idx, idx, maxlen)
    writer.save()

