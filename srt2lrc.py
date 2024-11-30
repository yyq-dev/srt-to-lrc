import os
import re

def srt_to_lrc(srt_content):
    """
    将 SRT 格式转换为 LRC 格式
    """
    lrc_lines = []
    for line in srt_content.splitlines():
        # 匹配时间戳
        match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})", line)
        if match:
            start_min = int(match.group(2))
            start_sec = int(match.group(3))
            start_ms = int(match.group(4))
            # 转换为 LRC 的时间格式：[mm:ss.xx]
            lrc_time = f"[{start_min:02}:{start_sec:02}.{int(start_ms/10):02}]"
            lrc_lines.append(lrc_time)
        elif line.strip() and not line.isdigit():  # 忽略空行和序号行
            lrc_lines[-1] += line.strip()  # 将歌词内容追加到时间戳后
    return "\n".join(lrc_lines)

def convert_srt_to_lrc(input_directory, output_directory):
    """
    将输入目录中的所有 .srt 文件转换为 .lrc 文件，并保存到指定输出目录
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # 如果输出目录不存在，则创建

    for filename in os.listdir(input_directory):
        if filename.endswith(".srt"):
            srt_path = os.path.join(input_directory, filename)
            lrc_path = os.path.join(output_directory, filename.replace(".srt", ".lrc"))

            with open(srt_path, "r", encoding="utf-8") as srt_file:
                srt_content = srt_file.read()
                lrc_content = srt_to_lrc(srt_content)

            with open(lrc_path, "w", encoding="utf-8") as lrc_file:
                lrc_file.write(lrc_content)
            print(f"转换完成: {filename} -> {lrc_path}")

if __name__ == "__main__":
    input_directory = input("请输入SRT文件所在目录路径：").strip()
    output_directory = input("请输入LRC文件保存目录路径：").strip()

    if os.path.isdir(input_directory):
        convert_srt_to_lrc(input_directory, output_directory)
    else:
        print("输入的SRT文件目录无效，请检查路径并重试。")
