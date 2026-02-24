# yt-dlp GUI 视频下载工具

基于开源项目 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 的图形界面视频下载工具，支持全网视频下载。

## ✨ 功能特点

- 🚀 支持 YouTube、Bilibili 等主流视频网站
- 📦 内置 yt-dlp、FFmpeg、Node.js 引擎
- 🖱️ 拖拽支持，可拖入链接文件
- 📊 实时进度显示
- 🔧 环境自检与自动升级
- 🍪 Cookie 支持（解决登录限制）

## 📁 项目结构

```
yt-dlp/
├── gui_ytdlp.py          # 主程序源码
├── 双击启动工具.bat       # 启动脚本
├── 使用说明.txt          # 使用说明
├── bin/                  # 二进制工具 (需自行下载)
│   ├── yt-dlp.exe
│   ├── ffmpeg.exe
│   ├── node.exe
│   └── ...
└── python/               # Python 运行时 (需自行下载)
```

## 🚀 使用方法

1. **下载并解压**：确保路径中无中文
2. **环境自检**：双击 `双击启动工具.bat`，点击"环境自检与升级"
3. **关联 Cookie**（可选）：导出 YouTube Cookie 文件到根目录
4. **开始下载**：粘贴视频链接，点击"开始任务"

## 📥 依赖下载

由于文件大小限制，以下依赖需要单独下载：

| 组件 | 下载地址 |
|------|----------|
| yt-dlp | https://github.com/yt-dlp/yt-dlp/releases |
| FFmpeg | https://ffmpeg.org/download.html |
| Node.js | https://nodejs.org/ |

将下载的文件放入 `bin/` 目录即可。

## 🙏 致敬开源

本工具核心基于以下开源项目：
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org)
- [Node.js](https://nodejs.org)

## 📄 许可证

本项目遵循开源协议，仅供学习交流使用。
