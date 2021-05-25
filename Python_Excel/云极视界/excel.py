from numpy import False_
import pandas as pd
import os

judge_list = []
staff_list = []
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

class Execl():
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data_frame = None
        self.sheet_len = len(pd.ExcelFile(file_path).sheet_names)

    def get_staff(self):
        str = self.data_frame.iloc[1,0].split('：' or ':')

        staff_list.append(str[3])

    def get_judge(self):
        for col in range(5,8):
            for row in range(4, self.rows-4):
                if self.data_frame.iloc[row,col] == "" :
                    continue

                if self.data_frame.iloc[row,col] in judge_list:
                    continue

                judge_list.append(self.data_frame.iloc[row,col])

    def get_score(self):
        score_dict = {}

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

        for row in range(4, self.rows-15):
            for col in range(5,8):
                if self.data_frame.iloc[row,col] == "" :
                    

                score_dict["编号"] = 
                score_dict["部门"] = department
                score_dict["岗位"] = post
                score_dict["姓名"] = name
                score_dict["项目"] = self.data_frame.fillna(method='ffill').iloc[row,1]
                score_dict["内容"] = self.data_frame.fillna(method='ffill').iloc[row,2]
                score_dict["指标获得满分的标准"] = self.data_frame.fillna(method='ffill').iloc[row,3]
                score_dict["权重"] = self.data_frame.fillna(method='ffill').iloc[row,4]
                score_dict["占比"] = ""
                score_dict["分数"] = ""
        
        score_list.append(score_dict)

    def handle_execl(self):
        for i in range(0, self.sheet_len):
            self.data_frame = pd.read_excel(self.file_path, sheet_name=i, index_col=None, header=None, keep_default_na=False)
            self.rows = self.data_frame.shape[0]
            self.cols = self.data_frame.columns.size
            self.get_staff()
            self.get_judge()
            self.get_score()

if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\assessment'
    # folder_path = os.path.dirname(os.path.realpath(__file__)) + '\\assessment'

    for file_path in get_file_path(folder_path):
        if not check_file_type(file_path):
            print('File:%s is not Excel!' % file_path)
            continue

        execl = Execl(file_path)
        execl.handle_execl()

    print(staff_list)
    print(score_list)
    print(judge_list)


    