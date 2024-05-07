import configparser
import csv
import os
import time
from pathlib import Path
import numpy as np

import MAN
import Utils
import glob
import HIQA
import MOS
import shutil
import torch.nn as nn

def preprocess_video(input_file:str, key_frame_output_dir:str,class_name:str, threshold:float):
    Utils.extract_frames(input_file, key_frame_output_dir)
    if not os.path.exists(key_frame_output_dir):
        os.mkdir(key_frame_output_dir)

    ret_dict = dict()
    IQAClass = nn.Module()
    if class_name == "HyperIQA":
        IQAClass = HIQA.HIQA()
    elif class_name == "MOS":
        IQAClass = MOS.MOSNet()
        threshold = threshold / 100
    elif class_name == "MAN":
        IQAClass = MAN.MANNet()
        threshold = threshold / 100

    files = glob.glob(os.path.join(key_frame_output_dir, '*.jpg'))
    duration = len(files)
    timeline = [False for i in range(int(duration))]
    resource_arr = [0 for i in range(int(duration))]
    for file in files:
        # 读取关键帧
        resource = IQAClass.forward(file)

        file = file[0: len(file) - 4]
        idx = str.find(file, 'frame-')
        file = file[idx + 6:len(file)]
        print(" ----- " + str(resource) + " ----- " + file)
        resource_arr[int(file) - 1] = resource
        if (resource > threshold):
            timeline[int(file) - 1] = True

    if not os.path.exists("output_video"):
        os.mkdir("output_video")

    front = 0
    behind = 0
    for front in range(len(timeline)):
        if timeline[front]:
            continue
        else:
            if (front -1  - behind > 1):
                output_name = "output_video/" +str(time.time())+"-"+ str(behind) + "-" + str(front-1) + ".mp4"
                Utils.cut_video(input_file, output_name,   str(behind), str(front -1 - behind))
                ret_dict[output_name] = np.mean(resource_arr[behind:front-1])
            behind = front

    if (front - 1 - behind > 1):
        output_name = "output_video/" + str(time.time()) + "-" + str(behind) + "-" + str(front - 1) + ".mp4"
        Utils.cut_video(input_file, output_name, str(behind), str(front - 1 - behind))
        ret_dict[output_name] = np.mean(resource_arr[behind:front - 1])


    if os.path.exists(key_frame_output_dir):
        shutil.rmtree(key_frame_output_dir)

    return ret_dict

def find_mp4_files(directory):
    mp4_files = []
    for file_path in glob.glob(os.path.join(directory, '*.mp4')):
        mp4_files.append(file_path)
    return mp4_files

if __name__ == "__main__":
    path = Path.cwd()
    data_path = path.absolute().joinpath('data')  # 输入视频文件路径
    output_dir = "keyframes"  # 输出关键帧的目录

    if  os.path.exists(output_dir):
        shutil.rmtree("keyframes")

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 获取配置文件中指定的类名
    class_name = config['General']['class_name']
    threshold = float( config['General']['threshold'])

    csv_file_path = 'data.csv'
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    # 写入CSV文件
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        for file in find_mp4_files(data_path):
            print(file)
            data_dict = preprocess_video(file, output_dir, class_name, threshold)
            writer.writerows(data_dict.items())




