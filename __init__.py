import sys
import os
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt
from aqt.utils import showInfo
from aqt import mw
import wave
import tempfile
import shutil

# 获取当前插件目录的路径
current_dir = os.path.dirname(os.path.realpath(__file__))
# 将当前插件目录添加到sys.path的开头，确保从这个目录导入模块
sys.path.insert(0, current_dir)

# 设置ffmpeg和ffprobe的路径
ffmpeg_path = os.path.join(current_dir, "ffmpeg")
os.environ["PATH"] += os.pathsep + ffmpeg_path

# 现在尝试导入pydub
from pydub import AudioSegment

# 移除插件目录从sys.path，如果你之后还需要导入其他模块但不希望它们也从这个目录加载
sys.path.remove(current_dir)

def convert_wave_mp3_to_real_mp3(directory, progress_dialog):
    converted_count = 0
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                file_count += 1
                progress_dialog.setValue(file_count)
                if progress_dialog.wasCanceled():
                    return converted_count
                file_path = os.path.join(root, file)
                try:
                    # 使用临时文件进行转换
                    with wave.open(file_path, 'rb') as wave_file:
                        temp_dir = tempfile.mkdtemp(dir=directory)  # 创建临时目录
                        temp_file_path = os.path.join(temp_dir, file)
                        sound = AudioSegment.from_wav(file_path)
                        sound.export(temp_file_path, format='mp3', codec="libmp3lame")
                        
                        # 替换原文件
                        os.remove(file_path)  # 删除原文件
                        shutil.move(temp_file_path, file_path)  # 将临时文件移动到原位置
                        
                        converted_count += 1
                except (wave.Error, EOFError, FileNotFoundError):
                    continue
    progress_dialog.setValue(file_count)
    return converted_count

def convert_wave_files():
    media_dir = mw.col.media.dir()
    # 计算总文件数以设置进度对话框的范围
    total_files = sum([len(files) for r, d, files in os.walk(media_dir) if any(file.endswith('.mp3') for file in files)])
    progress_dialog = QProgressDialog("正在转换文件...", "取消", 0, total_files, mw)
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.show()
    converted_count = convert_wave_mp3_to_real_mp3(media_dir, progress_dialog)
    # 确保进度条完全填满
    progress_dialog.setValue(total_files)
    progress_dialog.close()  # 关闭进度条对话框
    showInfo(f"已转换 {converted_count} 个MP3扩展名的Wave格式文件为真正的MP3格式。")


action = QAction("在媒体文件夹中将Wave转为MP3", mw)
action.triggered.connect(convert_wave_files)  # 使用connect方法连接信号和槽
mw.form.menuTools.addAction(action)