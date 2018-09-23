#!/usr/bin/python3
import pandas as pd
import numpy as np

def format_to_excel(rows, output, sheetname='noname'):
    """Just wrapper for pd.ExcelWriter
    
    Arguments:
        rows {object} -- pd.DataFrame with some data
        output {str} -- file for write excel table
    
    Keyword Arguments:
        sheetname {str} -- excel sheet (default: {'noname'})
    
    Returns:
        object -- pd.ExcelWriter with formated data
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    rows.to_excel(writer, sheet_name=sheetname, index=False)
    
    # set column width as max len of cells
    worksheet = writer.sheets[sheetname]
    for idx, col in enumerate(rows):
        maxlen = np.max([len(str(el)) for el in rows[col]]) + 1
        worksheet.set_column(idx, idx, maxlen)
    return writer
