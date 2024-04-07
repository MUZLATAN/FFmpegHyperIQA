import ffmpeg

import subprocess
import os
import re
from pathlib import Path



def get_video_duration(video_path):
    # 使用subprocess.run来执行命令
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # 获取标准输出并转换成浮点数
    duration = float(result.stdout.decode('utf-8').strip())
    return duration


def extract_frames(input_file: str, output_dir: str):
    """
    使用FFmpeg每隔一秒从视频中提取关键帧并以时间命名保存。

    参数：
    input_file: 输入视频文件路径。
    output_dir: 输出关键帧的目录。
    """

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 构建FFmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'fps=1',
        '-vsync', '0',
        f'{output_dir}/frame-%03d.jpg'
    ]
    subprocess.run(ffmpeg_cmd)

def cut_video(input_file, output_file, start_time, duration):
    """
    使用FFmpeg截取视频。

    参数：
    input_file: 输入视频文件路径。
    output_file: 输出视频文件路径。
    start_time: 截取开始时间，格式为 HH:MM:SS 或者 秒数。
    duration: 截取的时长，格式为 HH:MM:SS 或者 秒数。
    """
    # 构建FFmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-ss', start_time,
        '-i', input_file,
        '-t', duration,
        '-c', 'copy',
        output_file
    ]

    # 执行FFmpeg命令
    subprocess.run(ffmpeg_cmd)