import pandas as pd
from pathlib2 import Path
from basicframe.midwares.mongodbclient import MongoDBClient
#
class ExcelOperator:
    def __init__(self, path: Path):
        self.file_path = path
        self.xlsx = pd.ExcelFile(path)
        self.mongo_client = MongoDBClient().connect()

    def get_sheet(self, sheet_name):
        df = self.xlsx.parse(sheet_name)
        sheet_data = df.to_dict(orient='records')
        return sheet_data


    def save_sheet_to_mongo(self, sheet_name, db, cell):
        raw_data = self.get_sheet(sheet_name)
        sheet_data = []
        for row in raw_data:
            stripped_dict = {key.strip(): str(value) for key, value in row.items()}
            sheet_data.append(stripped_dict)
        self.mongo_client[db][cell].insert_many(sheet_data)



    def save_all_sheets_to_mongo(self, db, cell):
        for sheet_name in self.xlsx.sheet_names:
            self.save_sheet_to_mongo(sheet_name, db, cell)

if __name__ == '__main__':

    sheet_name = ['各语种持续刷新大型信源', '韩语', '日语', '阿拉伯语', '俄语', '法语', '葡语', '西班牙语', '德语', '泰语', '意大利语', '印地语', '越南语', '土耳其语', '马来语', '印尼语']
    el = ExcelOperator(Path('~/多语种-文本-20230615.xlsx'))
    for sheet in sheet_name:
        el.save_sheet_to_mongo(sheet, 'test', 'siteinfo')
