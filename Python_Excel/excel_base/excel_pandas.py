import pandas as pd
import os

def getFile(folderPath):
    fileList = []

    for root, dirs, files in os.walk(folderPath):
        for name in files:
            fileList.append(os.path.join(root, name))

    return fileList

def checkFile(filePath):
    if '~$' in filePath:
        return False

    extensions = ['.xlsx', 'xls']

    return any(filePath.endswith(extension) for extension in extensions)

def readData(filePath):
    dataFrame = pd.read_excel(filePath, sheet_name=0, header=None)
    rowNum = dataFrame.shape[0]
    colNum = dataFrame.columns.size
    filenName = filePath.split('\\')[-1].split('.')[0]

    datas = [filenName]

    for col in range(0, colNum):
        data = {}
        data['编号'] = col + 1
        data['字段'] = dataFrame.iloc[0,col]
        data['名称'] = dataFrame.iloc[2,col]
        data['类型'] = dataFrame.iloc[1,col]
        data['备注'] = ''

        datas.append(data)

    return datas

def writeData(datas, writer):
    sheetName = datas[0]
    datas.pop(0)

    pd.DataFrame(datas).to_excel(writer, sheet_name = sheetName, index=False)

if __name__ == "__main__":
    folderPath = os.path.dirname(os.path.realpath(__file__)) + '\\AllData'
    outFile = os.path.dirname(os.path.realpath(__file__)) + '\\outFile.xlsx'

    fileList = getFile(folderPath)

    print('等待...')
    with pd.ExcelWriter(outFile) as writer:
        for filePath in fileList:
            if not checkFile(filePath):
                print('File:%s is not Excel!' % filePath)
                continue

            datas = readData(filePath)

            writeData(datas, writer)

    print('完成')