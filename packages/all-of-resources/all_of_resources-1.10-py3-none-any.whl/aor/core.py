import os
import json
import zipfile
import time
from threading import Thread
import shutil as sh

assets_assetIndex_json = {}
step2=""
assets_length = 0
assets_count = 0

def check(minecraftdir:str, version:str, extractdir:str):
    """返回值：(版本列表, 是否可以开始, 如果可以开始的话这里是提示，否则为None)"""
    verlist=[]
    if os.path.exists(minecraftdir) and minecraftdir.endswith(".minecraft"):
        verlist=os.listdir(os.path.join(minecraftdir,"versions"))
        if os.path.exists(extractdir) and version and os.listdir(extractdir)==[]:
            return (verlist, True, "等待任务开始...")
        else:
            return (verlist, False, None)
    else:
        return (None, False, None)

def task(minecraftdir, version, output, callback, page=None):
    """callback函数需要的参数: (进度 最大2000, 提示)
    返回值：(提示类型 I:信息 E:错误, 任务结果提示)
    
    如果你使用的是flet的话，请传入page"""
    global assets_assetIndex_json, step2, assets_length, assets_count
    callback(0, "Step 0: 确保版本完整...")
    jarPath=os.path.join(minecraftdir, "versions", version, version + ".jar")
    jsonPath=os.path.join(minecraftdir, "versions", version, version + ".json")
    with open(os.path.join(minecraftdir, "versions", version, version + ".json"),"r",encoding="utf-8") as f:
        version_json = json.load(f)
        f.close()
    assetIndexPath=os.path.join(minecraftdir, "assets/indexes", version_json["assetIndex"]["id"] + ".json")
    

    if os.path.exists(jarPath) and os.path.exists(jsonPath) and os.path.exists(assetIndexPath):
        step1="Step 1: 解压{}.jar\n".format(version)
        callback(0, step1)
        with zipfile.ZipFile(os.path.join(minecraftdir, "versions", version, version + ".jar")) as jar:
            files = [f for f in jar.namelist() if f.startswith("assets/") or f.startswith("data/")]
            progress = 0
            files_len = len(files)
            callback(0, step1+"0% ({}/{})".format(progress, files_len))
            for file in files:
                jar.extract(file, output)
                progress+=1
                callback((progress/files_len)*1000, step1+"{}% ({}/{})".format(round((progress/files_len)*100), progress, files_len))


        time.sleep(0.5)
        step2="Step 2: 根据 {} 复制文件\n".format(version_json["assetIndex"]["id"] + ".json")
        cpu_count = os.cpu_count()
        callback(1000, step2+"获取文件列表...")
        with open(assetIndexPath,"r",encoding="utf-8") as f:
            assets_assetIndex_json = json.load(f)
            f.close()
        assets = assets_assetIndex_json["objects"].keys()
        assets_threads = []
        assets_length = len(assets)
        assets_count = 0

        # 计算每个线程应该处理的元素数量
        elements_per_thread = assets_length // cpu_count
        # 计算剩余的元素数量
        remaining_elements = assets_length % cpu_count

        for i in range(cpu_count):
            # 计算当前线程应该处理的元素范围
            start_index = i * elements_per_thread
            end_index = start_index + elements_per_thread + (1 if i == cpu_count - 1 else 0) * remaining_elements
            # 获取当前线程应该处理的子列表
            sublist = list(assets)[start_index:end_index]
            # 创建并启动线程
            thread = Thread(target=copy_assets, args=(minecraftdir, callback, sublist, output))
            thread.start()
            assets_threads.append(thread)

        while any(thread.is_alive() for thread in assets_threads):
            time.sleep(0.1)
        time.sleep(0.5)
        callback(2000, "Step 3: 移动特殊文件/文件夹")
        try:
            sh.move(os.path.join(output, "assets", "pack.mcmeta"), os.path.join(output, "pack.mcmeta"))
            sh.move(os.path.join(output, "assets", "icons"), os.path.join(output, "icons"))
            sh.move(os.path.join(output, "assets", "minecraft", "resourcepacks"), os.path.join(output, "resourcepacks"))
        except:
            pass
        callback(2000, "All Of Resources By SystemFileB\n给个Star awa")
        return ("I", "任务完成！")
    else:
        callback(0, "Step 0: 确保版本完整...\n\n错误：版本文件缺失\n请你补全版本文件或启动一次游戏")
        return ("E", "版本文件缺失！\n请你补全版本文件或启动一次游戏")

def advcopy(source_file, destination_file):
    # 获取目标文件的目录路径
    destination_directory = os.path.dirname(destination_file)
    # 检查目标目录是否存在，如果不存在则创建它
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # 复制文件
    sh.copy(source_file, destination_file)

def copy_assets(minecraftdir, callback, keys, path):
    global assets_assetIndex_json, step2, assets_length, assets_count
    for asset in keys:
        fileHash = assets_assetIndex_json["objects"][asset]["hash"]
        filePath = os.path.join(minecraftdir, "assets", "objects", fileHash[0:2], fileHash)
        advcopy(filePath, os.path.join(path, "assets", asset))
        assets_count+=1
        callback(1000+(assets_count/assets_length)*1000, "{}{}% ({}/{})".format(step2, round((assets_count/assets_length)*100), assets_count, assets_length))
