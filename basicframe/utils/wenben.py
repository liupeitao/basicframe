# -*- coding: utf-8 -*-
import os.path
import pprint
import re

import pandas as pd
from basicoperator import BasicOperator


class Wenben(BasicOperator):
    ITEM_PATTER = re.compile('{("_?title"|"_?id"|\'_?id\'|\'_?title\')')

    def get_dir_item(self, dir):
        file_list = self.get_all_file(dir)
        acc = 0
        for file in file_list:
            print("正在计算：", file, end='')
            acc += self.get_count_per_file(file)
        return acc

    def get_count_per_file(self, file):
        count = 0
        with open(file, mode='r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                count += 1
        return count

    def get_file_by_type(self, dir, type_set: set()):
        file_list = self.get_all_file(dir)
        tmp = [file for file in file_list if os.path.splitext(file)[-1] in type_set]
        file_list = tmp
        return file_list

    def get_file_by_exclude_type(self, dir, type_set: set()):
        file_list = self.get_all_file(dir)
        tmp = [file for file in file_list if os.path.splitext(file)[-1] not in type_set]
        file_list = tmp
        return file_list

    def langs_to_csv(self, dir):
        lang_list = self.get_all_lang(dir)
        langs_info = []
        for lang in lang_list:
            lang_info = []
            lang_info.append(os.path.relpath(lang, dir).split('-')[0])
            item_count = self.get_dir_item(lang)
            print(lang, item_count)
            lang_info.append(item_count)
            langs_info.append(lang_info)
        frame = pd.DataFrame(langs_info, columns=["语种", "文本数量/条"])
        with pd.ExcelWriter("summary.xlsx") as writer:
            frame.to_excel(writer, sheet_name="summary", index=False)

    def to_csv(self, dir):
        lang_frames = []
        lang_list = self.get_all_lang(dir)
        lang_total = []
        for lang in lang_list:
            frame, acc = self.get_dir_frame(lang)
            lang_frames.append(frame)
            lang_total.append(acc)
        total_list = [(lang_name, acc) for lang_name, acc in zip(os.listdir(dir), lang_total)]
        total_frame = pd.DataFrame(total_list, columns=["语种", "数量"])
        with pd.ExcelWriter(f"summary_{self.format_date}.xlsx") as writer:
            for lang_frame, lang_name in zip(lang_frames, os.listdir(dir)):
                lang_frame.to_excel(writer, sheet_name=lang_name, index=False)
            total_frame.to_excel(writer, sheet_name="所有语种", index=False)

    def dir_to_csv(self, dir):
        sub_dir_list = self._get_sub_dir_name(dir)
        dir_info = []
        for sub_dir in sub_dir_list:
            sub_dir_info = []
            sub_dir_info.append(sub_dir)
            print(sub_dir)
            duration = self.get_dir_item(os.path.join(dir, sub_dir), type='.txt')
            sub_dir_info.append(duration)
            dir_info.append(sub_dir_info)
        frame = pd.DataFrame(dir_info, columns=["领域", "数量"])
        pprint.pprint(frame)
        with pd.ExcelWriter(f"summary_{self.format_date}.xlsx") as writer:
            frame.to_excel(writer, sheet_name="summary", index=False)

    def get_dir_frame(self, dir):
        sub_dir_list = self._get_sub_dir_name(dir)
        dir_info = []
        acc = 0
        for sub_dir in sub_dir_list:
            sub_dir_info = []
            sub_dir_info.append(sub_dir)
            print(sub_dir)
            duration = self.get_dir_item(os.path.join(dir, sub_dir))
            acc += duration
            sub_dir_info.append(duration)
            dir_info.append(sub_dir_info)
        frame = pd.DataFrame(dir_info, columns=["领域", "数量"])
        return frame, acc

    def get_all_lang(self, dir):
        lang_list = []
        for lang_dir in os.listdir(dir):
            lang_list.append(os.path.join(dir, lang_dir))
        return lang_list

    def scatter_domains(self, line, save_dir, domain):
        with open(os.path.join(save_dir, domain), mode='a') as f:
            f.write(line + '\n')

    # fenlingyu daima

    def mkdir_acrroding_to_file(self, dir):
        file_list = self.get_all_file(dir)
        for file in file_list:
            base_name = os.path.basename(file)
            new_path = os.path.join(dir, 'domains', base_name)
            os.mkdir(new_path)
            os.system(f'cp {file} {new_path}/{base_name}.txt')


if __name__ == '__main__':
    pass
