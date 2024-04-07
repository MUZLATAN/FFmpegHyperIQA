import os
from pathlib import Path
import Utils
import glob
import HIQA
import shutil

if __name__ == "__main__":
    path = Path.cwd()
    input_file = path.absolute().joinpath('zelda.mp4') # 输入视频文件路径
    output_dir = "keyframes"  # 输出关键帧的目录



    Utils.extract_frames(input_file, output_dir)

    hyper_IQA = HIQA.HIQA()
    files = glob.glob(os.path.join(output_dir, '*.jpg'))
    duration = len(files)
    timeline = [False for i in range(int(duration))]
    for file in files:
        # 读取关键帧
        resource = hyper_IQA.inference(file)

        file = file[0: len(file) - 4]
        idx = str.find(file,'frame-')
        file = file[idx + 6:len(file)]
        print(" ----- "+str(resource)+" ----- "+file)
        if (resource > 35):
            timeline[int(file)-1] = True

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
                Utils.cut_video(input_file, "output_video/"+str(start_time)+"-"+str(end_time)+".mp4", str(start_time), str(end_time - start_time))
            is_continuous = False

    #shutil.rmtree("keframes")
    #shutil.rmtree("output_video")
