import os
import subprocess
from tkinter import Tk, filedialog, messagebox, Label, Frame, Toplevel, Entry, StringVar
from tkinter.ttk import Style, Button as ttkButton
import webbrowser

class ToolBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-GORB Tool Box v1.0")
        self.root.geometry("450x450")  # 增加窗口宽度到450px
        self.root.resizable(False, False)  # 禁止调整窗口大小
        
        # 设置样式
        style = Style()
        style.configure('TButton', font=('Arial', 10), padding=5)
        
        try:
            self.root.iconbitmap('logo.ico')  # 设置应用程序图标
        except Exception as e:
            print(f"加载图标失败: {e}")
        
        # 标题标签
        self.title_label = Label(root, text="X-GORB Tool Box v1.0", font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=10)
        
        # 功能按钮容器
        button_frame = Frame(root)
        button_frame.pack(expand=True)
        
        self.btn_separate = ttkButton(button_frame, text="视频音频分离", command=self.video_audio_separate_dialog, style='TButton')
        self.btn_convert = ttkButton(button_frame, text="转换图片格式", command=self.convert_image_format_dialog, style='TButton')
        self.btn_merge = ttkButton(button_frame, text="合并音频视频", command=self.merge_audio_video_dialog, style='TButton')
        self.btn_about = ttkButton(button_frame, text="关于", command=self.show_about, style='TButton')
        self.btn_update = ttkButton(button_frame, text="检查更新", command=self.check_for_updates, style='TButton')

        self.btn_separate.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        self.btn_convert.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.btn_merge.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        self.btn_about.grid(row=3, column=0, padx=10, pady=5, sticky='ew')
        self.btn_update.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

        # 设置按钮列宽一致
        button_frame.grid_columnconfigure(0, weight=1)

        # 版权信息和核心人员信息
        self.copyright_label = Label(root, text="© 2024 X-GORB Studio. 保留所有权利。", font=('Arial', 8))
        self.core_personnel_label = Label(root, text="软件核心人员：吴延梓", font=('Arial', 8))
        self.copyright_label.pack(pady=(10, 0))
        self.core_personnel_label.pack(pady=(0, 10))

    def select_file(self, filetypes=None):
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        return file_path

    def select_directory(self):
        directory = filedialog.askdirectory()
        return directory

    def get_ffmpeg_path(self):
        if os.name == 'nt':  # Windows
            return os.path.join(os.path.dirname(__file__), '..', 'bin', 'ffmpeg', 'bin', 'ffmpeg.exe')
        else:  # macOS/Linux
            return os.path.join(os.path.dirname(__file__), '..', 'bin', 'ffmpeg', 'bin', 'ffmpeg')

    def get_magick_path(self):
        if os.name == 'nt':  # Windows
            return os.path.join(os.path.dirname(__file__), '..', 'bin', 'imagemagick', 'magick.exe')
        else:  # macOS/Linux
            return os.path.join(os.path.dirname(__file__), '..', 'bin', 'imagemagick', 'magick')

    def video_audio_separate_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("视频音频分离对话框")
        dialog.geometry("450x250")  # 调整对话框大小以适应内容
        dialog.resizable(False, False)

        Label(dialog, text="输入视频文件路径").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        browse_button_video = ttkButton(dialog, text="浏览", command=lambda: self.browse_input_video(), style='TButton')
        browse_button_video.grid(row=0, column=1, padx=10, pady=5)
        self.input_video_entry = Entry(dialog, width=50)
        self.input_video_entry.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

        Label(dialog, text="输出音频文件路径").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        browse_button_audio = ttkButton(dialog, text="浏览", command=lambda: self.browse_output_audio(), style='TButton')
        browse_button_audio.grid(row=1, column=1, padx=10, pady=5)
        self.output_audio_entry = Entry(dialog, width=50)
        self.output_audio_entry.grid(row=1, column=2, padx=10, pady=5, sticky='ew')

        Label(dialog, text="输出视频文件路径").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        browse_button_video_out = ttkButton(dialog, text="浏览", command=lambda: self.browse_output_video(), style='TButton')
        browse_button_video_out.grid(row=2, column=1, padx=10, pady=5)
        self.output_video_entry = Entry(dialog, width=50)
        self.output_video_entry.grid(row=2, column=2, padx=10, pady=5, sticky='ew')

        ttkButton(dialog, text="确定", command=lambda: self.video_audio_separate_action(dialog), style='TButton').grid(row=3, column=1, pady=10)

    def browse_input_video(self):
        file_path = self.select_file([("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.input_video_entry.delete(0, 'end')
            self.input_video_entry.insert(0, file_path)

    def browse_output_audio(self):
        directory = self.select_directory()
        if directory:
            output_audio_path = os.path.join(directory, "output_audio.mp3")
            self.output_audio_entry.delete(0, 'end')
            self.output_audio_entry.insert(0, output_audio_path)

    def browse_output_video(self):
        directory = self.select_directory()
        if directory:
            output_video_path = os.path.join(directory, "output_video.mp4")
            self.output_video_entry.delete(0, 'end')
            self.output_video_entry.insert(0, output_video_path)

    def video_audio_separate_action(self, dialog):
        input_video = self.input_video_entry.get()
        output_audio = self.output_audio_entry.get()
        output_video = self.output_video_entry.get()

        if not input_video or not output_audio or not output_video:
            messagebox.showerror("错误", "请填写所有字段。")
            return

        ffmpeg_path = self.get_ffmpeg_path()
        result_audio = subprocess.run([ffmpeg_path, "-i", input_video, "-q:a", "0", "-map", "a", output_audio], capture_output=True, text=True)
        if result_audio.returncode != 0:
            messagebox.showerror("错误", f"提取音频时出错:\n{result_audio.stderr}")
            return

        result_video = subprocess.run([ffmpeg_path, "-i", input_video, "-c:v", "copy", "-an", output_video], capture_output=True, text=True)
        if result_video.returncode != 0:
            messagebox.showerror("错误", f"提取视频时出错:\n{result_video.stderr}")
            return

        messagebox.showinfo("成功", "视频和音频已成功分离。")
        dialog.destroy()

    def convert_image_format_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("转换图片格式对话框")
        dialog.geometry("450x200")  # 调整对话框大小以适应内容
        dialog.resizable(False, False)

        Label(dialog, text="输入图片文件路径").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        browse_button_image = ttkButton(dialog, text="浏览", command=lambda: self.browse_input_image(), style='TButton')
        browse_button_image.grid(row=0, column=1, padx=10, pady=5)
        self.input_image_entry = Entry(dialog, width=50)
        self.input_image_entry.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

        Label(dialog, text="输出图片格式").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.output_format_var = StringVar(value='png')
        formats = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
        format_combobox = ttkButton(dialog, textvariable=self.output_format_var, command=self.toggle_format_list, style='TButton')
        format_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.format_options = []
        for fmt in formats:
            option = ttkButton(dialog, text=f".{fmt}", command=lambda fmt=fmt: self.set_output_format(fmt), style='TButton')
            option.grid(row=1, column=1, padx=10, pady=5, sticky='w')
            option.grid_remove()
            self.format_options.append(option)

        Label(dialog, text="输出图片文件路径").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        browse_button_image_out = ttkButton(dialog, text="浏览", command=lambda: self.browse_output_image(), style='TButton')
        browse_button_image_out.grid(row=2, column=1, padx=10, pady=5)
        self.output_image_entry = Entry(dialog, width=50)
        self.output_image_entry.grid(row=2, column=2, padx=10, pady=5, sticky='ew')

        ttkButton(dialog, text="确定", command=lambda: self.convert_image_format_action(dialog), style='TButton').grid(row=3, column=1, pady=10)

    def toggle_format_list(self):
        for option in self.format_options:
            if option.winfo_viewable():
                option.grid_remove()
            else:
                option.grid()

    def set_output_format(self, fmt):
        self.output_format_var.set(fmt)
        for option in self.format_options:
            option.grid_remove()

    def browse_input_image(self):
        file_path = self.select_file([("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            self.input_image_entry.delete(0, 'end')
            self.input_image_entry.insert(0, file_path)

    def browse_output_image(self):
        directory = self.select_directory()
        if directory:
            input_image = self.input_image_entry.get()
            if input_image:
                _, ext = os.path.splitext(input_image)
                output_image_name = f"{os.path.basename(input_image).replace(ext, '')}.{self.output_format_var.get()}"
                output_image_path = os.path.join(directory, output_image_name)
                self.output_image_entry.delete(0, 'end')
                self.output_image_entry.insert(0, output_image_path)

    def convert_image_format_action(self, dialog):
        input_image = self.input_image_entry.get()
        output_image = self.output_image_entry.get()

        if not input_image or not output_image:
            messagebox.showerror("错误", "请填写所有字段。")
            return

        magick_path = self.get_magick_path()
        result = subprocess.run([magick_path, input_image, output_image], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("错误", f"转换图片格式时出错:\n{result.stderr}")
            return

        messagebox.showinfo("成功", "图片格式已成功转换。")
        dialog.destroy()

    def merge_audio_video_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("合并音频视频对话框")
        dialog.geometry("450x250")  # 调整对话框大小以适应内容
        dialog.resizable(False, False)

        Label(dialog, text="输入视频文件路径").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        browse_button_video_in = ttkButton(dialog, text="浏览", command=lambda: self.browse_input_video_merge(), style='TButton')
        browse_button_video_in.grid(row=0, column=1, padx=10, pady=5)
        self.input_video_entry = Entry(dialog, width=50)
        self.input_video_entry.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

        Label(dialog, text="输入音频文件路径").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        browse_button_audio_in = ttkButton(dialog, text="浏览", command=lambda: self.browse_input_audio(), style='TButton')
        browse_button_audio_in.grid(row=1, column=1, padx=10, pady=5)
        self.input_audio_entry = Entry(dialog, width=50)
        self.input_audio_entry.grid(row=1, column=2, padx=10, pady=5, sticky='ew')

        Label(dialog, text="输出视频文件路径").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        browse_button_video_out = ttkButton(dialog, text="浏览", command=lambda: self.browse_output_video_merge(), style='TButton')
        browse_button_video_out.grid(row=2, column=1, padx=10, pady=5)
        self.output_video_merge_entry = Entry(dialog, width=50)
        self.output_video_merge_entry.grid(row=2, column=2, padx=10, pady=5, sticky='ew')

        ttkButton(dialog, text="确定", command=lambda: self.merge_audio_video_action(dialog), style='TButton').grid(row=3, column=1, pady=10)

    def browse_input_video_merge(self):
        file_path = self.select_file([("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.input_video_entry.delete(0, 'end')
            self.input_video_entry.insert(0, file_path)

    def browse_input_audio(self):
        file_path = self.select_file([("Audio files", "*.mp3 *.wav *.aac")])
        if file_path:
            self.input_audio_entry.delete(0, 'end')
            self.input_audio_entry.insert(0, file_path)

    def browse_output_video_merge(self):
        directory = self.select_directory()
        if directory:
            output_video_path = os.path.join(directory, "output_video.mp4")
            self.output_video_merge_entry.delete(0, 'end')
            self.output_video_merge_entry.insert(0, output_video_path)

    def merge_audio_video_action(self, dialog):
        input_video = self.input_video_entry.get()
        input_audio = self.input_audio_entry.get()
        output_video = self.output_video_merge_entry.get()

        if not input_video or not input_audio or not output_video:
            messagebox.showerror("错误", "请填写所有字段。")
            return

        ffmpeg_path = self.get_ffmpeg_path()
        result = subprocess.run([ffmpeg_path, "-i", input_video, "-i", input_audio, "-c:v", "copy", "-c:a", "aac", output_video], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("错误", f"合并音频和视频时出错:\n{result.stderr}")
            return

        messagebox.showinfo("成功", "音频和视频已成功合并。")
        dialog.destroy()

    def show_about(self):
        about_text = (
            "X-GORB 工具箱 v1.0\n"
            "版权所有 © 2024 X-GORB Studio.\n"
            "软件核心人员：吴延梓"
        )
        dialog = Toplevel(self.root)
        dialog.title("关于")
        dialog.geometry("450x250")  # 调整对话框大小以适应内容
        dialog.resizable(False, False)

        Label(dialog, text=about_text, justify='left').pack(padx=10, pady=10)

        frame_links = Frame(dialog)
        frame_links.pack(pady=10)

        ttkButton(frame_links, text="Bilibili", command=lambda: self.open_url("https://space.bilibili.com/3493287799294517?spm_id_from=333.1007.0.0"), style='TButton').grid(row=0, column=0, padx=10, pady=5)
        ttkButton(frame_links, text="抖音", command=lambda: self.open_url("https://www.douyin.com/user/MS4wLjABAAAAITP9gSC4XLaDCkT2-4rOMGiQlcpLk_jJwbWqO_tzj2T0_-LG4ILdBa3cdESiIfLz?from_tab_name=main"), style='TButton').grid(row=0, column=1, padx=10, pady=5)
        ttkButton(frame_links, text="小红书", command=lambda: self.open_url("https://www.xiaohongshu.com/user/profile/65292b28000000002b0004be"), style='TButton').grid(row=0, column=2, padx=10, pady=5)
        ttkButton(frame_links, text="官方网站", command=lambda: self.open_url("http://xgorb.cn"), style='TButton').grid(row=1, column=0, padx=10, pady=5)
        ttkButton(frame_links, text="软件发布页", command=lambda: self.open_url("http://xgorb.cn/tools"), style='TButton').grid(row=1, column=1, padx=10, pady=5)

    def open_url(self, url):
        webbrowser.open(url)

    def check_for_updates(self):
        latest_version = self.fetch_latest_version()
        current_version = "1.0"

        if latest_version and latest_version > current_version:
            messagebox.showinfo("更新可用", f"发现新版本 {latest_version}。\n请访问我们的网站下载最新版本。")
        else:
            messagebox.showinfo("已是最新版本", "您当前使用的已经是最新版本。")

    def fetch_latest_version(self):
        try:
            response = requests.get("https://example.com/latest-version.txt")
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"获取最新版本信息时出错: {e}")
            return None

if __name__ == "__main__":
    root = Tk()
    app = ToolBoxApp(root)
    root.mainloop()



