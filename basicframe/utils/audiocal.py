import json
import math
import os
import re

import pandas as pd

from basicoperator import BasicOperator


class AudioCal(BasicOperator):
    subtitle_type = ['.vtt', '.txt', '.vtf', '.ttf', '.srt', '.ssa', '.ass', '.srt', '.sub', '.json', '.pdf']
    duration_pattern = re.compile('_(\d+?\.?\d*?)_')  # 匹配 bilibili_34.43_xxx...  ytd_3424_xd等格式，提取时长

    def __init__(self):
        super().__init__()

    @staticmethod
    def is_text_type(file):
        return os.path.splitext(file)[-1] in AudioCal.subtitle_type

    def _get_audio_time(self, path):
        duration_not_in_title_list = []
        duration_in_title_acc = 0
        for index, file in enumerate(self.get_all_file(path)):
            if self.is_text_type(file):
                print("text type:", index, file)
                continue
            try:
                duration = float(AudioCal.duration_pattern.findall(file)[0])
                print("duration: ", duration, file)
                duration_in_title_acc += duration
            except IndexError as e:
                # print("按照大小计算时长")
                duration_not_in_title_list.append(file)
        duration_not_in_title_acc = self._get_audio_file_size_in_list(duration_not_in_title_list)
        return math.ceil(duration_in_title_acc / 60 / 60 + duration_not_in_title_acc / 1024 / 1024 / 100)

    def _get_audio_time_tmp(self, path):
        duration_not_in_title_list = []
        duration_in_title_acc = 0
        for index, file in enumerate(self.get_all_file(path)):
            if self.is_text_type(file):
                print("text type:", index, file)
                continue
            try:
                duration = os.path.splitext(file)[0].split('_')[-1]
                if duration == "None":
                    raise IndexError
                if duration == "0.0":
                    raise IndexError
                duration = float(duration)
                if duration < 7:
                    duration = duration * 3600
                print("duration: ", duration, file)
                duration_in_title_acc += duration
            except IndexError as e:
                # print("按照大小计算时长")
                duration_not_in_title_list.append(file)
        duration_not_in_title_acc = self._get_audio_file_size_in_list(duration_not_in_title_list)
        return math.ceil(duration_in_title_acc / 60 / 60 + duration_not_in_title_acc / 1024 / 1024 / 450)

    def _get_audio_file_size_in_dir(self, dir):
        file_list = self.get_all_file(dir)
        acc = self._get_audio_file_size_in_list(file_list)
        return acc

    def _get_audio_file_size_in_list(self, file_list):
        acc = 0
        for file in file_list:
            acc += os.path.getsize(file)
        return acc

        ## 有字幕和音频的移走

    def _moveParied(self, src, dst):
        paried = self.__get_paried(src)
        file_list = []
        for key in paried:
            for i in range(0, len(paried[key])):
                file_list.append(paried[key][i])
        self._move_files_in_list(file_list, src, dst)
        print("共计%d, 有字幕和音频的" % len(paried))

    def __get_paried(self, src):
        file_list = self.get_all_file(src)
        all = {}
        for file in file_list:
            key = os.path.splitext(file)[0]
            value = file
            all.setdefault(key, []).append(value)

        paried = {}
        for key in all:
            if len(all[key]) == 2:
                paried[key] = all[key]
        return paried

    def get_domain_autio_time(self, domain_dir):
        category_acc = self._get_audio_time(domain_dir)
        return category_acc

    def get_domain_sub_or_no_sub(self, domain_dir, domae_name, has_sub: bool):
        audio_time = self.get_domain_autio_time(domain_dir)
        if has_sub:
            return [f"{domae_name}_sub", audio_time]
        return f"{domae_name}", audio_time

    def get_all_domain(self, lang_dir):
        domains_list = os.listdir(lang_dir)
        has_sub = lang_dir.find('sub') != -1
        domains_dict = {}
        for domain in domains_list:
            domain_info = self.get_domain_sub_or_no_sub(os.path.join(lang_dir, domain), domain, has_sub)
            domains_dict[domain_info[0]] = domain_info[1]
        return domains_dict

    def get_lang_info(self, lang_dir):
        domains_no_sub_dir = self.get_all_domain(lang_dir)
        domains_has_sub_dir = self.get_all_domain(f"{lang_dir}-sub")
        domains_has_sub_dir.update(domains_no_sub_dir)
        lang_info_dict = domains_has_sub_dir
        return lang_info_dict

    def cal_lang(self, lang_info_dict):
        domain_list = lang_info_dict.keys()
        keys_has_sub = set()
        keys_no_sub = set()
        for domain in domain_list:
            if domain.find('sub') == -1:
                keys_no_sub.add(domain)
            else:
                keys_has_sub.add(domain)
        # print(keys_has_sub)
        all_keys = set(x.split('_')[0] for x in keys_has_sub) | keys_no_sub
        lang_info = {}
        domains = {}
        domains_has_sub_acc = 0
        domains_no_sub_acc = 0
        for key in all_keys:
            domain = {}
            summary = {
                'has_sub': lang_info_dict.get(f'{key}_sub') if lang_info_dict.get(f'{key}_sub') is not None else 0,
                'no_sub': lang_info_dict.get(f'{key}') if lang_info_dict.get(f'{key}') is not None else 0}
            domain['total'] = summary['has_sub'] + summary['no_sub']
            domain['summary'] = summary
            domains[key] = domain
            domains_has_sub_acc += summary['has_sub']
            domains_no_sub_acc += summary['no_sub']
        lang_info['total'] = domains_no_sub_acc + domains_has_sub_acc
        lang_info['summary'] = {
            'has_sub': domains_has_sub_acc,
            'no_sub': domains_no_sub_acc
        }
        lang_info['domains'] = domains
        return lang_info

    def cal_all_lang(self, langs_dir):
        res = {}
        langs = {}
        langs_has_sub_acc = 0
        langs_no_sub_acc = 0
        for lang in os.listdir(langs_dir):
            if lang.find('sub') != -1:  # 目录名称存在sub就跳过
                continue
            if not os.path.isdir(os.path.join(langs_dir, lang)):  ## 跳过文件
                continue
            lang_info_dict = self.get_lang_info(os.path.join(langs_dir, lang))
            lang_info_dict = self.cal_lang(lang_info_dict)
            langs[lang] = lang_info_dict
            langs_has_sub_acc += lang_info_dict['summary']['has_sub']
            langs_no_sub_acc += lang_info_dict['summary']['no_sub']
        res['total'] = langs_has_sub_acc + langs_no_sub_acc
        res['summary'] = {
            'has_sub': langs_has_sub_acc,
            'no_sub': langs_no_sub_acc
        }
        res['langs'] = langs
        return res

    def json_to_csv(self, json_str):
        data = json_str
        lang_name_list = data['langs'].keys()
        # 每个语种一个 DataFrame
        lang_frames = []
        for lang_name in lang_name_list:
            domain_summary = data['langs'][lang_name]['domains']
            domain_list = [(domain, int(summary['summary']['has_sub']), int(summary['summary']['no_sub']),
                            int(summary['summary']['has_sub'] + summary['summary']['no_sub']))
                           for domain, summary in domain_summary.items()]
            lang_frame = pd.DataFrame(domain_list, columns=["领域", "有字幕", "无字幕", "合计"])
            lang_frames.append(lang_frame)

        # 将所有语种合并成一个 DataFrame
        total_list = [(lang_name, int(lang_summary['summary']['has_sub']), int(lang_summary['summary']['no_sub']),
                       int(lang_summary['summary']['has_sub'] + lang_summary['summary']['no_sub']))
                      for lang_name, lang_summary in data['langs'].items()]
        total_frame = pd.DataFrame(total_list, columns=["语种", "有字幕", "无字幕", "合计"])

        # 写入 Excel 文件
        with pd.ExcelWriter(f"summary_{self.format_date}.xlsx") as writer:
            for lang_frame, lang_name in zip(lang_frames, lang_name_list):
                lang_frame.to_excel(writer, sheet_name=lang_name, index=False)
            total_frame.to_excel(writer, sheet_name="所有语种", index=False)

    def get_dir_frame(self, dir):
        dir_info = []
        sub_dir_list = self._get_sub_dir_name(dir)
        acc = 0
        for sub_dir in sub_dir_list:
            sub_dir_info = []
            sub_dir_info.append(sub_dir)
            print(sub_dir)
            duration = self._get_audio_time_tmp(os.path.join(dir, sub_dir))
            sub_dir_info.append(duration)
            dir_info.append(sub_dir_info)
            acc += duration
        frame = pd.DataFrame(dir_info, columns=["文件夹", "时长H"])
        return frame, acc

    def dir_to_csv(self, dir):
        frame, acc = self.get_dir_frame(dir)
        print(frame)
        with pd.ExcelWriter(f"summary_{self.format_date}.xlsx") as writer:
            frame.to_excel(writer, sheet_name="summary", index=False)

    def mov_video(self, dir):
        video_type = ['.mp4']
        file_list = self.get_all_file(dir)
        for file in file_list:
            if os.path.splitext(file)[-1] in video_type:
                print(file)

    def delete_empty_files(self, dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            # 判断是否为文件
            if os.path.isfile(file_path):
                # 判断文件大小是否为0
                if os.path.getsize(file_path) == 0:
                    # 删除文件
                    os.remove(file_path)
                    # 删除同名的txt文件
                    txt_file = os.path.splitext(file_path)[0] + '.txt'
                    if os.path.exists(txt_file):
                        os.remove(txt_file)

    def save_json_to_file(self, json_str):
        with open(f"summary_{self.format_date}.json", mode='w') as f:
            f.write(json.dumps(json_str, ensure_ascii=False))

    def get_duration_by_size(self, dir):
        file_list = self.get_all_file(dir)
        size = self._get_audio_file_size_in_list(file_list)
        return size / 1024 / 1024 / 300

    def ruoyuzhong_csv(self, dir):
        lang_frames = []
        lang_list = self.get_sub_dir(dir)
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
            total_frame.to_excel(writer, sheet_name="所有类型", index=False)


if __name__ == '__main__':
    au = AudioCal()
