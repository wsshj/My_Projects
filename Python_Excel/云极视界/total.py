import numpy as np
import pandas as pd
import os
import json

staff_list = []
info_list = []
score_list = []

def get_file_path(folderName):
    file_path_list = []
    
    for root, dirs, files in os.walk(folderName):
        for name in files:
            file_path_list.append(os.path.join(root, name))
    
    return file_path_list

def check_file_type(file_name):
    extensions = ['.xlsx', '.xls']

    return any(file_name.endswith(extension) for extension in extensions)

def open_json(file_name):
    with open(file_name,'r') as load_f:
        return  json.load(load_f).get("staff")

def count():
    for staff in staff_list:
        score = 0
        bm = ''
        gw = ''
        for info in info_list:
            if staff == info["xm"]:
                score += info["df"]
                bm = info["bm"]
                gw = info["gw"]

        d = {}
        d["部门"] = bm
        d["岗位"] = gw
        d["姓名"] = staff
        d["得分"] = score

        score_list.append(d)

def print_execl(file_name):
    outDataFrame = pd.DataFrame(score_list)
    outDataFrame.to_excel(file_name + "\\总分.xlsx",
                        sheet_name='Sheet1',
                        startcol=0,
                        index=False)  

class Execl():
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data_frame = pd.read_excel(self.file_path, sheet_name=0, index_col=None, header=None)
        self.rows = self.data_frame.shape[0]
        self.cols = self.data_frame.columns.size

    def get_data(self):
        for row in range(1, self.rows):
            d = {}
            d["bm"] = self.data_frame.iloc[row,0]
            d["gw"] = self.data_frame.iloc[row,1]
            d["xm"] = self.data_frame.iloc[row,2]

            d["qz"] = self.data_frame.iloc[row,6] if not self.data_frame.iloc[row,6] is np.nan else 0
            d["zb"] = self.data_frame.iloc[row,8] if not self.data_frame.iloc[row,8] is np.nan else 0
            d["fs"] = self.data_frame.iloc[row,9] if not self.data_frame.iloc[row,9] is np.nan else 0

            d["df"] = d["fs"] * d["zb"]# * d["qz"]

            info_list.append(d)  

if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\print'
    print_folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\total'

    staff_list = open_json(os.path.dirname(os.path.realpath(__file__)) + "\\config\\staff.json")

    for file_path in get_file_path(folder_path):
        if not check_file_type(file_path):
            print('File:%s is not Excel!' % file_path)
            continue

        execl = Execl(file_path)
        execl.get_data()

    count()
    print_execl(print_folder_path)

    # print(info_list)
    print(score_list)
    