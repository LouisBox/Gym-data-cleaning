import pandas as pd
import numpy as np
import os
import datetime

def order_dates(folder_path):
    split_date = [ n.split(" ",1)[0] for n in os.listdir(folder_path)]

    date_order = [datetime.datetime.strptime(i, "%d-%m-%y") for i in split_date]
    date_order.sort()

    string_order = [datetime.datetime.strftime(i, "%d-%m-%y") for i in date_order]

    full_string = [str(n) for n in os.listdir(folder_path)]

    file_order = [i for n in string_order for i in full_string if n in i]
    return file_order

def fix_weight(n):
    if type(n) == str:
        fix = ""
        for v in n:
            if v.isdigit() or v==".":
                fix += v
        return fix
    else:
        return n

def BulkCutFill(file):
    if "bulk" in file.lower():
        wc["Goal"] = "Bulk"
    elif "mini" in file.lower():
        wc["Goal"] = "Mini-cut"
    elif "cut" in file.lower():
        wc["Goal"] = "Cut"
    elif "maintain" in file.lower():
        wc["Goal"] = "Maintain"
        
def convert_date_format(n):
    return datetime.datetime.strptime(n, "%d/%m/%Y").strftime("%Y-%m-%d")

folder_path = "D:/Laptop Data/Louis Box 2664/Documents/gym data project/weight change/"

col = ["Date","Weight","Goal"]

concat_df = pd.DataFrame(columns = col)

files = [folder_path + n for n in order_dates(folder_path)]

def full_cleaning():
    for f in files:

        wc = pd.read_csv(f)

        wc.drop(columns = wc.columns[2:], inplace =True)
        wc.dropna(how="all",inplace=True)
        wc.reset_index(drop=True,inplace=True)

        wc.drop(labels = wc.iloc[7::8, :].index.to_list(), inplace=True)
        wc.reset_index(drop=True,inplace=True)

        wc.columns = ["Date","Weight"]

        wc["Weight"] = wc["Weight"].apply(fix_weight)
        wc["Weight"] = wc["Weight"].apply(pd.to_numeric)    
        wc["Date"] = wc["Date"].apply(convert_date_format
                                     )
        BulkCutFill(f)

        concat_df = pd.concat([concat_df,wc],ignore_index=True)    
        concat_df["Weight"].fillna(method="ffill",inplace=True) 

        #np.savetxt("D:/Laptop Data/Louis Box 2664/Documents/gym data project/cleaned weight log/clean weight log.csv", 
         #       concat_df, fmt="%s", header="Date,Weight,Goal", comments="", delimiter=',')

if __name__ == "__main__":
    full_cleaning()