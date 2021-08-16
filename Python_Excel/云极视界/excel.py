import numpy as np
import pandas as pd
import os
import json


judge_list = ["未指定"]
staff_list = []
score_list = []
judge_dict = {}
staff_dict = {}

staff_id = 0

def get_file_path(folderName):
    file_path_list = []
    
    for root, dirs, files in os.walk(folderName):
        for name in files:
            file_path_list.append(os.path.join(root, name))
    
    return file_path_list

def check_file_type(file_name):
    extensions = ['.xlsx', '.xls']

    return any(file_name.endswith(extension) for extension in extensions)

class Execl():
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data_frame = None
        self.sheet_len = len(pd.ExcelFile(file_path).sheet_names)

    def get_staff(self):
        str = self.data_frame.iloc[1,0].split('：' or ':')
        print(str)
        staff_list.append(str[3])

    def get_judge(self):
        for col in range(5,8):
            for row in range(4, self.rows-4):
                if self.data_frame.iloc[row,col] is np.nan :
                    continue

                if self.data_frame.iloc[row,col] in judge_list:
                    continue

                judge_list.append(self.data_frame.iloc[row,col])

    def get_score(self, staff_id):
        str = self.data_frame.iloc[1,0].split('：' or ':')
        for s in str[1].split(' '):
            if(s != ''):
                department = s
                break

        for s in str[2].split(' '):
            if(s != ''):
                post = s
                break
        
        name = str[3]

        for row in range(4, self.rows-4):
            judge_num = 3
            ratio = 0
            if self.data_frame.iloc[row, 8] is np.nan :
                judge_num -= 1

            if self.data_frame.iloc[row, 7] is np.nan :
                judge_num -= 1

            for col in range(1, judge_num+1):
                score_dict = {}

                if judge_num == 3:
                    if col == 1:
                        ratio = 0.5
                    elif col == 2:
                        ratio = 0.3
                    else:
                        ratio = 0.2
                
                if judge_num == 2:
                    if col == 1:
                        ratio = 0.5
                    else:
                        ratio = 0.5
                
                if judge_num == 1:
                    ratio = 1

                # score_dict["编号"] = staff_id

                score_dict["部门"] = department
                score_dict["岗位"] = post
                score_dict["姓名"] = name

                score_dict["项目"] = self.data_frame.fillna(method='ffill').iloc[row,1]
                score_dict["内容"] = self.data_frame.iloc[row,2] if not self.data_frame.iloc[row,2] is np.nan else ""
                score_dict["指标获得满分的标准"] = self.data_frame.iloc[row,3] if not self.data_frame.iloc[row,3] is np.nan else ""
                score_dict["权重"] = "%s%%" % round(float(self.data_frame.iloc[row,4]) * 100) if not self.data_frame.iloc[row,4] is np.nan else ""
                score_dict["工作总结（工作成果及后续情况）"] = self.data_frame.iloc[row,5] if not self.data_frame.iloc[row,5] is np.nan else ""
                score_dict["考核人"] = self.data_frame.iloc[row,5+col]

                score_dict["占比"] = ratio
                score_dict["分数"] = ""
        
                score_list.append(score_dict)

    def handle_execl(self, staff_id):
        for i in range(0, self.sheet_len):
            self.data_frame = pd.read_excel(self.file_path, sheet_name=i, index_col=None, header=None)#, keep_default_na=False)
            staff_id += 1
            
            self.rows = self.data_frame.shape[0]
            self.cols = self.data_frame.columns.size
            self.get_staff()
            self.get_judge()
            self.get_score(staff_id)

    def screen_score(self): 
        for judge in judge_list:
            jl = []
            for score in score_list:
                if score.get("考核人") == judge:
                    jl.append(score)
                    # score_list.remove(score)

            judge_dict[judge] = jl

        wzd = []
        for score in score_list:
            if score.get("考核人") is np.nan:
                wzd.append(score)
                # score_list.remove(score)

        judge_dict["未指定"] = wzd

def print_execl(folder_path):
    for key,value in judge_dict.items():
        file_name = '\\%s.xlsx' % key
        outDataFrame = pd.DataFrame(value)
        outDataFrame.to_excel(folder_path + file_name,
                            sheet_name='Sheet1',
                            startcol=0,
                            index=False)

if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\assessment'
    print_folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\print'
    config_folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\config'

    for file_path in get_file_path(folder_path):
        print(file_path)
        if not check_file_type(file_path):
            print('File:%s is not Excel!' % file_path)
            continue

        execl = Execl(file_path)
        execl.handle_execl(staff_id)
        execl.screen_score()

    print_execl(print_folder_path)

    staff_dict["staff"] = staff_list
    with open(config_folder_path + "\\staff.json", "w" , encoding='utf8') as f:
        json.dump(staff_dict,f)

        # print(judge_dict)
        # print(score_list)
        # print(judge_list)
        

    