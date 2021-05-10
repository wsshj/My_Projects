import pandas as pd

fileName = '34.开关柜全过程技术监督精益化管理实施细则'

inputFile = 'G:/zhenzdl/技术监督精益化管理实施细则终稿/%s.xls' % fileName
# outputFile = './Excel/1.xlsx'
SsxzFile = './Excel/content/%s.xlsx' % fileName
SsxzxmxxFile = './Excel/code/%s.xlsx' % fileName
XzDlId = 25

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

outSsxz = []
outSsxzxmxx = []

for num in range(10):
    dataFrame = pd.read_excel(inputFile,
                              sheet_name=num,
                              usecols='B:I',
                              header=2)

    for row in dataFrame.itertuples():
        print(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        if type(row[5]) is float:
            continue

        dictSsxzxmxx = {}
        dictSsxzxmxx['SsxzDlId'] = XzDlId
        dictSsxzxmxx['SsxzJdId'] = num + 1
        dictSsxzxmxx['SsxzZyId'] = str2int.get(row[1], 0)
        dictSsxzxmxx['SsxzXmMc'] = row[3]

        outSsxzxmxx.append(dictSsxzxmxx)

        i = 1
        for rl in row[5].split('\n'):
            if rl == '':
                continue
            dictSsxz = {}
            dictSsxz['XzDlId'] = XzDlId
            dictSsxz['JsJdJdId'] = num + 1
            dictSsxz['JsJdZyId'] = str2int.get(row[1], 0)
            dictSsxz['JdXmId'] = row[2]
            dictSsxz['GjxQz'] = row[4]
            dictSsxz['JdYdXH'] = i
            dictSsxz['JdYdNr'] = rl
            dictSsxz['JdYj'] = row[6]
            dictSsxz['JdYq'] = row[7]
            dictSsxz['JdJg'] = row[8]

            outSsxz.append(dictSsxz)
            i += 1

outDataFrame = pd.DataFrame(outSsxzxmxx)
outDataFrame.to_excel(SsxzxmxxFile,
                      sheet_name='Sheet1',
                      startcol=0,
                      index=False)

outDataFrame = pd.DataFrame(outSsxz)
outDataFrame.to_excel(SsxzFile, sheet_name='Sheet1', startcol=0, index=False)
print('finish')
