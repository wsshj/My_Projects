import pandas as pd

fileName = '26.干式电抗器全过程技术监督精益化管理实施细则'

inputFile = 'G:/zhenzdl/技术监督精益化管理实施细则终稿/%s.xls' % fileName
outputFile = './Excel/%s.xlsx' % fileName
XzDlId = 20

str2int = {
    '电气设备性能': 1,
    '化学': 2,
    '环境保护': 3,
    '土建': 4,
    '金属': 5,
    '电气性能': 6,
    '自动化': 7,
    '保护与控制': 8,
    '电测': 9,
    '反事故措施': 10,
    '电能质量': 11,
    '信息通信': 12,
    '节能': 13,
    '热工': 14,
}

outList = []
for num in range(10):
    dataFrame = pd.read_excel(inputFile,
                              sheet_name=num,
                              usecols='B,D',
                              header=2)

    for row in dataFrame.itertuples():
        print(row[0], row[1], row[2])

        dictLine = {}
        dictLine['SsxzDlId'] = XzDlId
        dictLine['SsxzJdId'] = num + 1
        dictLine['SsxzZyId'] = str2int.get(row[1], 0)
        dictLine['SsxzXmMc'] = row[2]

        outList.append(dictLine)

outDataFrame = pd.DataFrame(outList)

# 在excel表格的第1列写入, 不写入index
outDataFrame.to_excel(outputFile, sheet_name='Sheet1', startcol=0, index=False)
print('finish')
