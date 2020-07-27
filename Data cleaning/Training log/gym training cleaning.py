import pandas as pd
import numpy as np
import re
import datetime
import math
import os
from pandas import ExcelWriter

def replace_kg(n):
    if pd.isna(n):
        return n
    
    elif "bw" in n.lower():
        bw_indx = w.index[w["Weight"] == n].to_list()[0]
        date = w["Date"].iloc[bw_indx]
        wc_indx = wc.index[wc["Date"]==date]
        new_w = wc["Weight"].iloc[wc_indx]
        return new_w.item()
    
    else:
        return str(n).replace("kg","")
        
def extract_dates(n):
    n = n[6:len(n)-1]
    return datetime.datetime.strptime(n, "%d/%m/%y").strftime("%Y-%m-%d")
                
def fill_rir(n):
    if pd.isna(n):
        Nan_loc = w.index[pd.isna(w["RIR"])].tolist()[0]
        return rir_dict[str(w["Week"].iloc[Nan_loc])]
    elif type(n)== datetime.datetime:
        n = int(n.strftime("%d"))
        return n
    else:
        return n
    
def round_nearest(x, a):
    return round(x / a) * a

def one_r_m(n):
    rep = str(n[4]).split(",")[0]
    orm = float(n[3]) * (1 +(float(rep)+(n[5]))/30)
    n[6] = round_nearest(orm,0.25)
    return n[6]

def save_xls(dict_df, path): # FUNCTION TO SAVE EACH A FILE AS AN .XLSX FILE
    
    writer = ExcelWriter(path)
    for key in dict_df:
        dict_df[key].to_excel(writer, key,index=False)
    writer.save()
        
folder_dir = "D:/Laptop Data/Louis Box 2664/Documents/gym data project/gym training log/training log files"
weight_change_fp = "D:/Laptop Data/Louis Box 2664/Documents/gym data project/cleaned weight log/clean weight log.csv"
wc = pd.read_csv(weight_change_fp)


def full_cleaning():
    for file in os.scandir(folder_dir):

        t = pd.ExcelFile(file)

        tl = {"1": pd.read_excel(t,0),
                "2": pd.read_excel(t,1), 
                "3": pd.read_excel(t,2),
                "4": pd.read_excel(t,3),
                "5": pd.read_excel(t,4)}

        for s in tl:

            w = tl[s]
            rir_dict={"1":2,"2":2,"3":1,"4":0,"5":3}

            w.columns =["Date","Exercise","Weight","Reps","RIR","Notes","Video"]
            w["1RM"]=None

            indx_vol_table = w.index[w['Date'] == "Volume Tally"].to_list()[0]
            drop_list = list(range(indx_vol_table,len(w.index)))
            w.drop(drop_list,inplace=True)
            w.drop(columns = ["Notes","Video"],inplace=True)
            w.dropna(how="all",inplace=True)

            w.insert(1,"Week",int(s))
            w.reset_index(drop=True,inplace=True)

            w["Date"].fillna(method="ffill",inplace=True)        
            w["Date"] = w["Date"].apply(extract_dates)
            w["Weight"]=w["Weight"].apply(replace_kg)
            w["RIR"]=w["RIR"].apply(fill_rir)
            w["Weight"] = w["Weight"].apply(pd.to_numeric)
            w["1RM"] = w.apply(one_r_m, axis=1)

            file_template = tl["1"]["Date"].iloc[0] + " clean TL.xlsx"

        save_xls(tl,"D:/Laptop Data/Louis Box 2664/Documents/gym data project/cleaned training logs/"+file_template)
    
if __name__ == "__main__":
    full_cleaning()