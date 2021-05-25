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

        for col in range(1,8):
            for row in range(4, self.rows-15):
                


        str = self.data_frame.iloc[1,0].split('：' or ':')
        for s in str[1].split(' '):
            if(s != ''):
                score_dict["部门"] = s
                break

        for s in str[2].split(' '):
            if(s != ''):
                score_dict["岗位"] = s
                break
        
        score_dict["姓名"] = str[3]

        
        
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


    