import configparser
import os
import time
from pathlib import Path

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
    for file in files:
        # 读取关键帧
        resource = IQAClass.forward(file)

        file = file[0: len(file) - 4]
        idx = str.find(file, 'frame-')
        file = file[idx + 6:len(file)]
        print(" ----- " + str(resource) + " ----- " + file)
        if (resource > threshold):
            timeline[int(file) - 1] = True

    if not os.path.exists("output_video"):
        os.mkdir("output_video")

    is_continuous = False
    for i in range(len(timeline)):
        if timeline[i]:
            if not is_continuous:
                start_time = i
            is_continuous = True
        else:
            if is_continuous:
                end_time = i
                Utils.cut_video(input_file, "output_video/" +str(time.time())+"-"+ str(start_time) + "-" + str(end_time) + ".mp4",
                                str(start_time), str(end_time - start_time))
            is_continuous = False

    shutil.rmtree("keyframes")
    #shutil.rmtree("output_video")

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

    for file in find_mp4_files(data_path):
        print(file)
        preprocess_video(file, output_dir, class_name, threshold)




