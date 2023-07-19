import datetime
import json
import logging
import os
import re

logging.basicConfig(filename='../FileDirOperate.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('FileDirOperate')
log.setLevel(logging.INFO)
handle = logging.StreamHandler()
handle.setFormatter(formatter)
log.addHandler(handle)


class BasicOperator:
    def __init__(self):
        self.cur_date = datetime.date.today().strftime("%Y-%m-%d")
        self.recode_dir = f'/home/ptking/src/submit-recoded/{self.cur_date}/'
        pass

    format_date = datetime.date.today().strftime('%m%d')

    def compare_two_dir(self, dir1, ext1: str, dir2, ext2: str):
        if not (os.path.exists(dir1) or os.path.exists(dir2)):
            log.error("目录不存在")
            return
        fileset1 = set(os.path.splitext(file)[0] for file in os.listdir(dir1))
        fileset2 = set(os.path.splitext(file)[0] for file in os.listdir(dir2))
        self.__delwith(fileset1, fileset2, dir1, ext1)
        self.__delwith(fileset2, fileset1, dir2, ext2)

    def __delwith(self, filesetbig, filesetsmall, dir, ext):
        res = filesetbig.difference(filesetsmall)
        for basename in res:
            file = os.path.join(dir, basename) + ext
            print(file, "将被删除")
            filesetbig.remove(basename)
            os.remove(file)

    # 递归获取所有目录
    def _get_dirs(self, dir, dirlist: list):
        if not os.path.isdir(dir):
            return
        dirlist.append(dir)
        for subdir in os.listdir(dir):
            s = os.path.join(dir, subdir)
            self._get_dirs(s, dirlist)

    # 复制目录树
    def _copy_path_tree_frame(self, src, dst):
        file_list = []
        self._get_dirs(src, file_list)
        for file in file_list:
            dst_path = os.path.join(dst, os.path.relpath(file, src))
            log.info(f'{file} --》{dst_path}')
            os.system(f'mkdir -p {dst_path}')

            log.info(f'mkdir -p {dst_path}')

    def copy_path_tree(self, src, dst, suffix=''):
        self._copy_path_tree_frame(src, dst + suffix)

    def delete_empty_files(self, dir1):
        if not os.path.exists(dir1):
            log.error("目录不存在")
            return
        file_list = self.get_all_file(dir1)
        for file in file_list:
            if os.path.getsize(file) == 0:
                print(file, "will be deleete ")
                os.remove(file)

    ##

    def _get_files(self, dir, filelist: list):
        if os.path.isdir(dir):
            for f in os.listdir(dir):
                self._get_files(os.path.join(dir, f), filelist)
        else:
            filelist.append(dir)

    def _moveFiles(self, src, dst):
        file_list = []
        self._get_files(src, file_list)
        self._move_files_in_list(file_list, src, dst)

    def _move_files_in_list(self, file_list, src, dst):
        for file in file_list:
            log.info(f'{file}, {os.path.join(dst, os.path.relpath(file, src))}')
            os.system(f'mv {file} {os.path.join(dst, os.path.relpath(file, src))}')

    def get_all_file(self, dir):
        file_list = []
        if not os.path.exists(dir):
            log.error("目录不存在")
            return []
        self._get_files(dir, file_list)
        return file_list

    def get_sub_dir(self, dir):
        lang_list = []
        for lang_dir in os.listdir(dir):
            lang_list.append(os.path.join(dir, lang_dir))
        return lang_list

    def get_all_dir(self, dir):
        dir_list = []
        if not os.path.exists(dir):
            log.error("目录不存在")
            return []
        self._get_dirs(dir, dir_list)
        return dir_list

    def copy_path_tree_frame(self, src, dst):
        if not os.path.exists(src):
            log.error("目录不存在")
            return
        self._copy_path_tree_frame(src, dst)

    def move_path_tree(self, src, dst):
        self.copy_path_tree_frame(src, dst)
        self._moveFiles(src, dst)

    def _get_sub_dir_name(self, dir):
        dir_list = []
        for sub_dir in os.listdir(dir):
            if not os.path.isdir(os.path.join(dir, sub_dir)):
                continue
            dir_list.append(sub_dir)
        return dir_list

    def bakup(self, src, dst):
        file_list = self.get_all_file(src)
        with open(dst, mode='w') as f:
            for file in file_list:
                print(file)
                f.write(file + '\n')

    def find_files_less_than(self, dir, size):
        file_list = self.get_all_file(dir)
        res = []
        for file in file_list:
            if os.path.getsize(file) / 1024 / 1024 < size:
                res.append(file)
        return res

    def _get_files_by_keyword(self, file_list, keyword):
        excepts = set()
        excepts.add('.m4a')
        excepts.add('.webm')
        res_list = []
        file_list = set(file_list)
        for file in file_list:
            if os.path.splitext(file)[-1] in excepts:
                continue
            LANG_PATTERN = re.compile('\.(.*)\.vtt')
            res = LANG_PATTERN.findall(file)[0]
            if keyword in res:
                if f"{file.split('.')[0]}.m4a" in file_list:
                    res_list.append(file)
                    res_list.append(f"{file.split('.')[0]}.m4a")
                elif f"{file.split('.')[0]}.webm" in file_list:
                    res_list.append(file)
                    res_list.append(f"{file.split('.')[0]}.webm")
        return res_list


from langdetect import detect

if __name__ == '__main__':
    bc = BasicOperator()
    file = '/media/ptking/Elements/en.json'
    with open(file, mode='r') as f:
        for line in f:
            try:
                if detect(json.loads(line)['content']) == 'en':
                    file_name = json.loads(line)['domain']
                    with open(f"eng/{file_name}.txt", mode='a') as f:
                        f.write(line)
                    print(line)
                else:
                    pass
            except Exception as e:
                pass
