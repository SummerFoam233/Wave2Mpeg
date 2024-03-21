# Wave2Mpeg
## 主要功能
针对ios端anki mobile限制wave格式音频播放的问题，该插件提供一个工具栏以将当前用户媒体目录下所有的后缀为mp3但实际为wave格式的音频转换为mpeg格式，防止同步后在ios端出现报错。个人用于解决爬取有道发音文件后不能正常在ios播放的问题。
## 使用方法
1. 下载ffmpeg, ffplay, ffprobe放于ffmpeg目录中。
2. 下载pydub源文件，放于pydub目录中（https://github.com/jiaaro/pydub）。
3. 在anki工具栏中选择“在媒体文件夹中将Wave转换为MP3”。
## To do
1. 添加更多不受ios支持的音频转换格式（.ogg等）。
2. 尝试更新其他转换方法，避免手动下载ffmpeg和pydub。
