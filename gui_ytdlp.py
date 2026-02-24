import os
import sys
import threading
import subprocess
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import windnd

# --- 1. 核心路径配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(BASE_DIR, "bin")
YTDLP_EXE = os.path.join(BIN_DIR, "yt-dlp.exe")
FFMPEG_DIR = BIN_DIR

class YtdlpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("生活作弊码 | 全网万能视频下载神器yt-dlp")
        self.root.geometry("800x700")
        self.root.configure(bg="#f8f9fa")

        # 标题栏
        header = tk.Label(root, text="🚀 全网视频下载 (基于开源项目yt-dlp优化)", font=("微软雅黑", 16, "bold"), fg="#333", bg="#f8f9fa")
        header.pack(pady=15)

        # 1. 链接输入区
        tk.Label(root, text=" 1. 粘贴视频链接 (每行一个)", font=("微软雅黑", 10, "bold"), bg="#f8f9fa").pack(anchor="w", padx=20, pady=(5, 0))
        self.text_urls = tk.Text(root, font=("Consolas", 10), height=6, relief="flat", borderwidth=1)
        self.text_urls.pack(fill="x", padx=20, pady=5)
        
        # 2. 保存路径区
        tk.Label(root, text=" 2. 选择下载保存位置", font=("微软雅黑", 10, "bold"), bg="#f8f9fa").pack(anchor="w", padx=20, pady=(5, 0))
        path_frame = tk.Frame(root, bg="#f8f9fa")
        path_frame.pack(fill="x", padx=20, pady=5)
        self.entry_output = tk.Entry(path_frame, font=("Consolas", 10))
        self.entry_output.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=3)
        default_save = os.path.join(os.path.expanduser("~"), "Desktop", "Downloads_Video")
        self.entry_output.insert(0, os.path.normpath(default_save))
        tk.Button(path_frame, text=" 浏览目录 ", command=self.select_output).pack(side="right")

        # 3. 参数设置区
        settings_frame = tk.LabelFrame(root, text=" 3. 下载参数配置 ", padx=15, pady=10, bg="#f8f9fa")
        settings_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(settings_frame, text="代理地址:", bg="#f8f9fa").grid(row=0, column=0, sticky="w")
        self.entry_proxy = tk.Entry(settings_frame, width=20)
        self.entry_proxy.insert(0, "")
        self.entry_proxy.grid(row=0, column=1, padx=10, sticky="w")

        tk.Label(settings_frame, text="批量下载:", bg="#f8f9fa").grid(row=0, column=2, padx=(20, 0), sticky="w")
        self.playlist_var = tk.StringVar(value="no")
        ttk.Combobox(settings_frame, textvariable=self.playlist_var, values=["yes", "no"], width=5, state="readonly").grid(row=0, column=3, padx=10)

        tk.Label(settings_frame, text="Cookie文件:", bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=10)
        self.entry_cookie_file = tk.Entry(settings_frame, width=40)
        self.entry_cookie_file.grid(row=1, column=1, columnspan=2, padx=10, sticky="w")
        default_cookie = os.path.join(BASE_DIR, "www.youtube.com_cookies.txt")
        if os.path.exists(default_cookie):
            self.entry_cookie_file.insert(0, os.path.normpath(default_cookie))
        tk.Button(settings_frame, text="浏览文件", command=self.select_cookie_file).grid(row=1, column=3)

        # 4. 执行按钮区
        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=10)
        self.btn_run = tk.Button(btn_frame, text="🚀 开始任务", command=self.start_thread, 
                                 bg="#d9534f", fg="white", font=("微软雅黑", 12, "bold"), width=20, height=2)
        self.btn_run.pack(side="left", padx=10)
        
        # 将自检功能也放入线程，防止点击时卡死
        tk.Button(btn_frame, text="🔄 环境自检与升级", command=self.start_check_env, 
                  bg="#5bc0de", fg="white", width=16, height=2).pack(side="left")

        # 5. 进度与日志区
        self.progress_val = tk.DoubleVar()
        self.bar = ttk.Progressbar(root, variable=self.progress_val, maximum=100)
        self.bar.pack(fill="x", padx=20, pady=10)

        self.log_area = scrolledtext.ScrolledText(root, font=("Consolas", 9), height=12, bg="#1e1e1e", fg="#dee2e6")
        self.log_area.pack(fill="both", padx=20, pady=10, expand=True)

        windnd.hook_dropfiles(self.root, func=self.on_drop_files)

    def select_output(self):
        p = filedialog.askdirectory()
        if p: self.entry_output.delete(0, tk.END); self.entry_output.insert(0, os.path.normpath(p))

    def select_cookie_file(self):
        f = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if f: self.entry_cookie_file.delete(0, tk.END); self.entry_cookie_file.insert(0, os.path.normpath(f))

    def log(self, content):
        self.log_area.insert(tk.END, content + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def on_drop_files(self, files):
        try:
            path = files[0].decode('gbk')
            if path.endswith('.txt'):
                with open(path, 'r', encoding='utf-8') as f:
                    self.text_urls.insert(tk.END, f.read())
        except: pass

    def start_check_env(self):
        """线程化启动自检"""
        self.log_area.delete('1.0', tk.END)
        threading.Thread(target=self.check_env_logic, daemon=True).start()

    def check_env_logic(self):
        self.log(">>> 正在启动环境自检与核心升级程序...")
        abs_bin = os.path.abspath(BIN_DIR)
        proxy = self.entry_proxy.get().strip()
        
        # 1. 检查 Node
        node_exe = os.path.join(abs_bin, "node.exe")
        try:
            res = subprocess.run([node_exe, "-v"], capture_output=True, text=True, timeout=5)
            self.log(f"✅ Node 引擎: 正常 [{res.stdout.strip()}]")
        except: self.log("❌ Node 引擎: 异常，请确认 bin 目录下 node.exe 是否正常。")

        # 2. 检查 FFmpeg
        ffmpeg_exe = os.path.join(abs_bin, "ffmpeg.exe")
        self.log(f"✅ FFmpeg 合成器: {'已就绪' if os.path.exists(ffmpeg_exe) else '未找到'}")

        # 3. 核心升级逻辑
        self.log(">>> 正在检查 yt-dlp 核心升级 (可能需要 10-30 秒)...")
        upd_cmd = [YTDLP_EXE, "-U"]
        if proxy:
            if not proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                proxy = "http://" + proxy
            upd_cmd += ["--proxy", proxy]

        try:
            # 执行升级命令并实时获取输出
            p = subprocess.Popen(upd_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                 text=True, encoding='utf-8', errors='replace',
                                 creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            for line in p.stdout:
                self.log(line.strip())
            p.wait()
            self.log(">>> 升级检查结束。")
        except Exception as e:
            self.log(f"❌ 升级检查出错: {e}")

    def start_thread(self):
        self.log_area.delete('1.0', tk.END)
        threading.Thread(target=self.process_logic, daemon=True).start()

    def process_logic(self):
        urls = [u.strip() for u in self.text_urls.get("1.0", tk.END).split('\n') if u.strip()]
        out_dir = self.entry_output.get().strip()
        if not urls:
            messagebox.showwarning("提示", "请输入链接！")
            return
        
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        self.btn_run.config(state=tk.DISABLED, text="正在处理中...", bg="#6c757d")
        for url in urls:
            self.download_engine(url, out_dir)
        
        self.btn_run.config(state=tk.NORMAL, text="🚀 开始任务", bg="#d9534f")
        messagebox.showinfo("完成", f"所有下载任务已结束！")

    def download_engine(self, url: str, out_dir: str):
        proxy = self.entry_proxy.get().strip()
        cookies = self.entry_cookie_file.get().strip()
        abs_bin = os.path.abspath(BIN_DIR)

        # 注入环境变量，确保 node 和 ffmpeg 能被找到
        env = os.environ.copy()
        env["PATH"] = abs_bin + os.pathsep + env.get("PATH", "")

        cmd = [
            YTDLP_EXE, url,
            "-o", os.path.join(out_dir, "%(title)s [%(id)s].%(ext)s"),
            "--ffmpeg-location", abs_bin,
            "--no-check-certificate",
            "--force-ipv4",
            "--impersonate", "chrome",
            "--js-runtimes", "node",
            "--extractor-args", "youtube:player_client=android_vr,tv;player_skip=web,mweb,android,ios",
            "--format", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--verbose",
        ]

        if self.playlist_var.get() == "no": cmd += ["--no-playlist"]
        else: cmd += ["--yes-playlist"]

        if proxy:
            if not proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                proxy = "http://" + proxy
            cmd += ["--proxy", proxy]

        if cookies and os.path.isfile(cookies):
            cmd += ["--cookies", cookies]

        def read_output(p):
            try:
                for raw_line in iter(p.stdout.readline, b''):
                    line = ""
                    for enc in ['utf-8', 'gbk']:
                        try:
                            line = raw_line.decode(enc).rstrip('\r\n')
                            break
                        except: continue
                    if not line: line = raw_line.decode('utf-8', errors='replace').rstrip('\r\n')
                    self.log(line)
                    match = re.search(r'(\d+(?:\.\d+)?)%', line)
                    if match:
                        try: self.progress_val.set(float(match.group(1)))
                        except: pass
            except: pass
            finally:
                if p.stdout: p.stdout.close()

        try:
            self.log(f">>> 正在处理: {url}")
            p = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                universal_newlines=False, env=env, cwd=abs_bin,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            t = threading.Thread(target=read_output, args=(p,), daemon=True)
            t.start()
            p.wait()
            if p.returncode == 0: self.progress_val.set(100)
            t.join(timeout=2.0)
        except Exception as e:
            self.log(f"❌ 启动失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk(); app = YtdlpGUI(root); root.mainloop()