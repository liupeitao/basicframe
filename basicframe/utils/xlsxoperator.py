import pandas as pd
from pathlib2 import Path
from basicframe.midwares.mongodbclient1 import MongoDBClient


class ExcelOperator:
    def __init__(self, path: Path):
        self.file_path = path
        self.xlsx = pd.ExcelFile(path)
        self.mongo_client = MongoDBClient().connect()

    def get_sheet(self, sheet_name):
        df = self.xlsx.parse(sheet_name)
        sheet_data = df.to_dict(orient='records')
        return sheet_data

    def save_sheet_to_mongo(self, df):
        sheet_data = df.to_dict(orient='records')
        sheet_data = [{key.strip(): str(value) for key, value in row.items()} for row in sheet_data]
        self.mongo_client['test']['siteinfo'].insert_many(sheet_data)

    def save_all_sheets_to_mongo(self):
        df = pd.read_excel(self.file_path, sheet_name=None)
        for d in df.values():
            self.save_sheet_to_mongo(d)


if __name__ == '__main__':
    el = ExcelOperator(Path('~/多语种-文本-20230615.xlsx'))
    el.save_all_sheets_to_mongo()
