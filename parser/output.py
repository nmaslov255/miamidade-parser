#!/usr/bin/python3
import pandas as pd
import numpy as np

def format_to_exel(rows, output, sheetname='noname'):
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    rows.to_excel(writer, sheet_name=sheetname, index=False)
    
    # set column width as max len of cells
    worksheet = writer.sheets[sheetname]
    for idx, col in enumerate(rows):
        maxlen = np.max([len(str(el)) for el in rows[col]])+1
        worksheet.set_column(idx, idx, maxlen)
    return writer
