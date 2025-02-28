import sys
import os
import time
import json
import threading
from urllib.parse import urlparse
from pathlib import Path
import requests
import zipfile
from urllib.parse import *
import shutil
import hashlib

class TemplateService:
    def __init__(self):
        self.checking = False
        self.result = False, "Unknow"
        self.checkUUID = ""
        self.checkCount = 0
    
    def _post(self, func, domain="api.dalipen.com"): 
        res = requests.post(f"https://{domain}/{func}", headers={
            'Connection':'close',
            'Country':'all',
            'User-Agent': "temlate_res"
        }, data={}, verify=False, timeout=10)
        if res.status_code == 200:
            result_data = json.loads(res.content)
            if result_data["code"] == 0:
                if "data" in result_data:
                    return result_data["data"]
                return None
            else:
                raise Exception(result_data["msg"])
        raise Exception("fail")
    
    def getInfoWithTid(self, tid):
        try:
            try:
                datas = self._post(f"template/get?tid={tid}", "api.dalipen.com")
            except:
                datas = self._post(f"template/get?tid={tid}", "aigc.zjtemplate.com")
            if len(datas) > 0:
                return datas[0]
        except:
            pass
        return None, None, None

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
def _download_template_dir():
    def get_cache_size():
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(CACHE_DIR):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size / (1024 * 1024)  # 转换为 MB
    def get_oldest_folder():
        folders = [os.path.join(CACHE_DIR, folder) for folder in os.listdir(CACHE_DIR) if os.path.isdir(os.path.join(CACHE_DIR, folder))]
        if not folders:
            return None
        oldest_folder = min(folders, key=lambda x: os.path.getctime(x))
        return oldest_folder
    def delete_folder(folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    current_size = get_cache_size()
    while current_size > 1000:
        oldest_folder = get_oldest_folder()
        if oldest_folder:
            delete_folder(oldest_folder)
            current_size = get_cache_size()  # 重新计算大小
        else:
            break
    return CACHE_DIR

def calculate_hash(s):
    hash_object = hashlib.sha256()
    hash_object.update(s.encode('utf-8'))
    hash_value = hash_object.hexdigest()
    return hash_value

# def getTemplateInfoWithLocal(tid_dir):
#     name, cover_url, pkg_url, dic = "", "", "", {}
#     config_file = os.path.join(tid_dir, "post_info.conf")
#     if os.path.exists(config_file):
#         with open(config_file, "r") as f:
#             c = json.load(f)
#         name = c["name"]
#         cover_url = c["cover_url"]
#         pkg_url = c["pkg_url"]
#         dic = c["dic"]
#     return name, cover_url, pkg_url, dic

# def saveTemplateInfoWithLocal(tid_dir, name, cover_url, pkg_url, dic):
#     config_file = os.path.join(tid_dir, "post_info.conf")
#     with open(config_file, "w") as f:
#         json.dump(f)

def getTemplateWithTid(tid):
    info = TemplateService().getInfoWithTid(tid)
    name = info["name"]
    pkg_url = info["pkg"]
    if pkg_url:
        tid_dir = os.path.join(_download_template_dir(), f"{tid}_{calculate_hash(pkg_url)}")
        if os.path.exists(tid_dir):
            return name, tid_dir

        #clear old zip or dir
        for root,dirs,files in os.walk(_download_template_dir()):
            for dir in dirs:
                if dir.find("_") <= 0:
                    continue
                name = dir[0:dir.rindex("_")]
                if name == tid:
                    shutil.rmtree(os.path.join(_download_template_dir(), dir))
            if root != files:
                break

        zipSavePath = os.path.join(_download_template_dir(), f"{tid}.zip")
        if os.path.exists(zipSavePath):
            os.remove(zipSavePath)
        s = requests.session()
        s.keep_alive = False
        file = s.get(pkg_url, verify=False)
        with open(zipSavePath, "wb") as c:
            c.write(file.content)
        s.close()
        if os.path.exists(zipSavePath):
            try:
                with zipfile.ZipFile(zipSavePath, "r") as zipf:
                    zipf.extractall(tid_dir)
                os.remove(zipSavePath)
                #input_param & video_input is in inputList.conf file
                with open(os.path.join(tid_dir, "inputList.conf"), "w") as f:
                    f.write(info["input_param"])
                with open(os.path.join(tid_dir, "videoInput.bizconf"), "w") as f:
                    f.write(info["video_input"])
                return name, tid_dir
            except:
                if os.path.exists(tid_dir):
                    shutil.rmtree(tid_dir)
    return None, None
