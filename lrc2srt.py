import os
import re

def lrc_to_srt(lrc_content):
    """
    将 LRC 格式转换为 SRT 格式
    """
    srt_lines = []
    index = 1
    timestamps = []  # 用于存储时间戳和对应的文本

    # 解析 LRC 内容，提取时间戳和歌词
    for line in lrc_content.splitlines():
        match = re.match(r"\[(\d{2}):(\d{2})\.(\d{2})\](.*)", line)
        if match:
            minute = int(match.group(1))
            second = int(match.group(2))
            millisecond = int(match.group(3)) * 10
            text = match.group(4).strip()

            timestamps.append({
                "time": (minute * 60 + second) * 1000 + millisecond,  # 转为毫秒
                "text": text
            })

    # 生成 SRT 内容
    for i in range(len(timestamps)):
        start_time_ms = timestamps[i]["time"]
        end_time_ms = timestamps[i + 1]["time"] if i + 1 < len(timestamps) else start_time_ms + 5000

        # 格式化时间戳
        start_time = f"{start_time_ms // 3600000:02}:{(start_time_ms % 3600000) // 60000:02}:{(start_time_ms % 60000) // 1000:02},{start_time_ms % 1000:03}"
        end_time = f"{end_time_ms // 3600000:02}:{(end_time_ms % 3600000) // 60000:02}:{(end_time_ms % 60000) // 1000:02},{end_time_ms % 1000:03}"

        # 写入 SRT 格式
        srt_lines.append(f"{index}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(timestamps[i]["text"])
        srt_lines.append("")  # 空行分隔

        index += 1

    return "\n".join(srt_lines)

def convert_lrc_to_srt(input_directory, output_directory):
    """
    将输入目录中的所有 .lrc 文件转换为 .srt 文件，并保存到指定输出目录
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # 如果输出目录不存在，则创建

    for filename in os.listdir(input_directory):
        if filename.endswith(".lrc"):
            lrc_path = os.path.join(input_directory, filename)
            srt_path = os.path.join(output_directory, filename.replace(".lrc", ".srt"))

            with open(lrc_path, "r", encoding="utf-8") as lrc_file:
                lrc_content = lrc_file.read()
                srt_content = lrc_to_srt(lrc_content)

            with open(srt_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(srt_content)
            print(f"转换完成: {filename} -> {srt_path}")

if __name__ == "__main__":
    input_directory = input("请输入LRC文件所在目录路径：").strip()
    output_directory = input("请输入SRT文件保存目录路径：").strip()

    if os.path.isdir(input_directory):
        convert_lrc_to_srt(input_directory, output_directory)
    else:
        print("输入的LRC文件目录无效，请检查路径并重试。")
