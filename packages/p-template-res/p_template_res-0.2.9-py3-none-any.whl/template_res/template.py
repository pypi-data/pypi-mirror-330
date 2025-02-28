import zipfile
import platform
import subprocess
import json
import os
from pathlib import Path
import shutil
import stat
import requests
import hashlib
import mutagen
from template_res import server as template_search_service

def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
                file_data = fp.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        print(f"download {url} ")
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
        s.close()
        fname = name[0:name.index(".")]
        fext = name[name.index("."):]
        unzipDir = os.path.join(rootDir, fname)
        if os.path.exists(unzipDir):
            shutil.rmtree(unzipDir)
        print(f"unzip {url} -> {unzipDir}")

def musicDir(rootDir):
    rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
    dd = os.path.join(rootDir, "music")
    os.makedirs(dd, exist_ok=True)
    return dd

def savePut(src, dst, name):
    if name in src:
        dst[name] = src[name]

def saveGet(src, name):
    if name in src:
        return src[name]
    return ""

def saveGetI(src, name):
    if name in src:
        return src[name]
    return -1

def inputConfig(data):
    videoCount = 0
    imageCount = 0
    audioCount = 0
    textCount = 0
    list = []
    otherParam = []
    for it in data:
        try:
            if it["type"].lower() == "image":
                imageCount += 1
                list.append({
                    "type": "image",
                    "width": saveGetI(it, "width"),
                    "height": saveGetI(it, "height")
                })
            elif it["type"].lower() == "video":
                videoCount += 1
                list.append({
                    "type": "video",
                    "width": saveGetI(it, "width"),
                    "height": saveGetI(it, "height"),
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            elif it["type"].lower() == "audio" or it["type"].lower() == "music":
                audioCount += 1
                list.append({
                    "type": "audio",
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            elif it["type"].lower() == "text":
                textCount += 1
                list.append({
                    "type": "text",
                    "value": it["value"],
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                })
            else:
                dd = {
                    "type": it["type"],
                    "name": saveGet(it, "name"),
                    "group": saveGet(it, "group")
                    }
                savePut(it, dd, "minValue")
                savePut(it, dd, "maxValue")
                if "paramSettingInfo" in it:
                    filterIndex = it["paramSettingInfo"][0]["filterIndex"]
                    paramName = it["paramSettingInfo"][0]["paramName"]
                    objName = it["paramSettingInfo"][0]["paramName"]
                    valueType = it["paramSettingInfo"][0]["valueType"]
                    dd["paramKey"] = f"{filterIndex}:{paramName}"
                    dd["obj"] = objName
                    dd["valueType"] = valueType
                otherParam.append(dd)
        except Exception as e:
            list = []
    return {
        "videoCount":videoCount,
        "imageCount":imageCount,
        "audioCount":audioCount,
        "textCount":textCount,
        "list":list,
        "otherParams":list
    }

def findVideoInput(dir):
    input_list_path = os.path.join(dir, "videoInput.bizconf")
    if os.path.exists(input_list_path):
        with open(input_list_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    return None

def findInputList(dir):
    input_list_path = os.path.join(dir, "inputList.conf")
    if os.path.exists(input_list_path):
        with open(input_list_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    input_list_path1 = os.path.join(dir, "skyinput0.conf")
    if os.path.exists(input_list_path1):
        with open(input_list_path1, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    return None

def listTemplate(searchPath, tid):
    result = []
    tpDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        tpDir = template_search_service._download_template_dir()
    else:
        tpDir = searchPath
    if len(tpDir) <= 0 or os.path.exists(tpDir) == False:
        print("template resource not found")
        return result
    #3.0模板走这里
    for root,dirs,files in os.walk(tpDir):
        for dir in dirs:
            if len(tid) > 0 and dir != tid:
                continue
            projFile = os.path.join(root, dir, "template.proj")
            if os.path.exists(projFile) == False:
                for root,dirs,files in os.walk(os.path.join(root, dir)):
                    for file in files:
                        name, ext = os.path.splitext(file)
                        if ext == ".proj":
                            projFile = os.path.join(root, file)
            with open(projFile, 'r', encoding='utf-8') as f:
                projConfig = json.load(f)
            inputList = findInputList(os.path.join(root, dir), projConfig["inputList"])
            if inputList == None or "type" not in projConfig:
                continue
            data = {}
            data.update(inputConfig(inputList))
            data["name"] = dir
            data["path"] = os.path.join(root, dir)
            result.append(data)
        if root != files:
            break
    #其他服务端下载模板走这里，可能有2.0，可能有3.0
    if len(tid) > 0:
        name, tid_dir = template_search_service.getTemplateWithTid(tid)
        if tid_dir:
            tid_params = {}
            tid_params.update(inputConfig(findInputList(tid_dir)))
            tid_params["video_input"] = findVideoInput(tid_dir)
            tid_params["input_param"] = findInputList(tid_dir)
            tid_params["tid"] = tid
            tid_params["name"] = name
            tid_params["path"] = tid_dir
            result.append(tid_params)
    return result

def listMusic(searchPath):
    mDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        mDir = musicDir()
    else:
        mDir = searchPath
    if len(mDir) <= 0 or os.path.exists(mDir) == False:
        print("music resource not found")
        return
    result = []
    for root,dirs,files in os.walk(mDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")].lower()
            ext = file[file.rindex("."):].lower()
            if ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
                audioPath = os.path.join(root, file)
                f = mutagen.File(audioPath)
                result.append({
                    "name":file,
                    "path":audioPath,
                    "length":f.info.length,
                    "channels":f.info.channels
                })
        if root != files:
            break
    return result