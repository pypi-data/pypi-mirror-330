import json
import mimetypes
import os
import shutil
from tkinter import messagebox, Tk, filedialog, ttk
from PyQt5.QtWidgets import QMessageBox

from anylabeling.views.labeling import dir_config
from anylabeling.views.labeling.utils.url import URLProvider
from anylabeling.views.labeling.base64_to_file import base64_to_file
import requests
import tkinter as tk

from anylabeling.views.labeling.singleton import Config
# 后端服务器的上传接口URL
UPLOAD_URL = URLProvider.get_url()+'/uploadImages'

# 准备文件列表
files_to_upload = []
root = Tk()
root.withdraw()

#上传图片文件
def uploadImages():
    # 使用filedialog让用户选择文件夹
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_selected = filedialog.askdirectory(title="Select Folder")
    if not folder_selected:
        messagebox.showinfo("提示", "没有选择任何文件夹")
    else:
        FILES_DIR=folder_selected;

        try:
            # 读取文件目录中的文件
            for filename in os.listdir(FILES_DIR):
                if filename.endswith(".jpg") | filename.endswith('.png'):
                    file_path = os.path.join(FILES_DIR, filename)
                    # 获取文件的MIME类型
                    mime_type, _ = mimetypes.guess_type(filename)
                    # 如果mimetypes模块无法识别文件类型，默认为'application/octet-stream'
                    mime_type = mime_type if mime_type else 'application/octet-stream'
                    files_to_upload.append(('files', (filename, open(file_path,'rb'),mime_type)))
                    print(filename)
            print(files_to_upload)
            params = {
                "files": files_to_upload
            }
            # 准备上传的参数
            headers = {
                'Authorization': Config().get_token()
            }
            print(params)
            # 发送上传请求
            try:
                response = requests.post(UPLOAD_URL, files=files_to_upload, headers=headers)
                if response.status_code == 200:
                    messagebox.showinfo("上传成功", "所有文件已成功上传！")
                else:
                    messagebox.showerror("上传失败", f"上传失败，状态码：{response.status_code}\n{response.text}")

            except Exception as e:
                messagebox.showerror("上传失败", f"上传过程中发生错误：{e}")

        except Exception as e:
            messagebox.showerror("上传失败", f"上传过程中发生错误：{e}")

jsons = []


def uploadJsons():
    UPLOAD_JSON_URL=URLProvider.get_url()+'/uploadJsons'
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_selected = filedialog.askdirectory(title="Select Folder")
    json_file_count = 0  # 初始化JSON文件计数器
    jpg_file_count=0
    if not folder_selected:
        messagebox.showinfo("提示", "没有选择任何文件夹")
    else:
        FILES_DIR = folder_selected;

        # 读取文件目录中的文件
        for filename in os.listdir(FILES_DIR):
            if filename.endswith('.json'):
                json_file_count += 1
            elif filename.endswith('.jpg'):
                jpg_file_count += 1
        # 比较JSON文件和JPG文件的数量
        if json_file_count != jpg_file_count:
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showinfo("提示", "未完成标注")
            root.destroy()  # 销毁窗口
        else :
            # 读取文件目录中的文件
            for filename in os.listdir(FILES_DIR):
                if(filename.endswith('.json')):
                    json_file_count += 1  # 发现JSON文件，计数器加1
                    file_path = os.path.join(FILES_DIR, filename)
                    # 获取文件的MIME类型
                    mime_type, _ = mimetypes.guess_type(filename)
                    # 如果mimetypes模块无法识别文件类型，默认为'application/octet-stream'
                    mime_type = mime_type if mime_type else 'application/octet-stream'
                    files_to_upload.append(('files', (filename, open(file_path,'rb'),mime_type)))
                    print(filename)
            # 准备上传的参数
            headers = {
                'Authorization': Config().get_token()
            }
            # 创建一个顶级窗口，用于显示上传进度
            root1 = tk.Tk()
            root1.withdraw()  # 隐藏顶级窗口
            try:
                # 显示正在上传文件的弹窗
                progress_message = tk.Toplevel(root1)
                progress_message.title("上传中")
                tk.Label(progress_message, text="正在上传文件，请稍候...").pack(pady=40,padx=60)
                progress_message.update_idletasks()

                response = requests.post(UPLOAD_JSON_URL, files=files_to_upload,headers=headers)
                if response.status_code == 200:
                    messagebox.showinfo("上传成功", "所有json文件已成功上传！")
                    try:
                        # 删除所有 files_to_upload 中的文件以及同名的jpg文件
                        for filetuple in files_to_upload:
                            json_file_path = filetuple[1][0]
                            # 构造jpg文件的路径
                            jpg_file_path = os.path.splitext(json_file_path)[0] + '.jpg'
                            # 如果json文件存在，则删除json文件和jpg文件
                            if os.path.exists(folder_selected+'/'+json_file_path):
                                filetuple[1][1].close()
                                os.remove(folder_selected+'/'+jpg_file_path)
                                os.remove(folder_selected+'/'+json_file_path)
                                # print("Deleting file:", os.path.join(FILES_DIR, os.path.basename(jpg_file_path)))
                                # print("Deleting file:", os.path.join(FILES_DIR, os.path.basename(json_file_path)))
                                # print("已删除")
                        # 删除存放文件的目录（如果目录为空）
                        if not os.listdir(FILES_DIR):
                            shutil.rmtree(FILES_DIR)
                    except Exception as e:
                        print(e)
                    progress_message.destroy()  # 关闭上传进度弹窗
                else:
                    messagebox.showerror("上传失败", f"上传失败，状态码：{response.status_code}\n{response.text}")
                    progress_message.destroy()  # 关闭上传进度弹窗
            except Exception as e:
                progress_message.destroy()  # 关闭上传进度弹窗
                messagebox.showerror("上传失败", f"上传过程中发生错误：{e}")


def download_image():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    folder_selected = filedialog.askdirectory(title="Select Download Folder")
    if not folder_selected:
        messagebox.showinfo("提示", "没有选择任何文件夹")
        return

    folder_selected += "/"
    api_url = URLProvider.get_url() + '/images'
    size = 600  # 假设这是我们要获取的图片数量
    type = 2  # 假设我们要获取的是jpg类型的图片
    token = Config().get_token()

    success, data = get_images_from_backend(api_url, size, type,1)
    if not success:
        messagebox.showinfo('下载失败', '文件下载失败!')
        print("Failed to retrieve images:", data)
        return

    imageData = data.get("data", {})
    num_images = len(imageData)
    if num_images == 0:
        messagebox.showinfo('提示', '没有图片可以下载。')
        return

    # 创建进度条窗口
    progress_window = tk.Toplevel(root)
    progress_window.title("下载进度")
    progress_window.geometry("300x100")

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(progress_window, maximum=num_images, variable=progress_var,value=0, length=280)
    progress_bar.pack(pady=20)

    progress_label = tk.Label(progress_window, text="0/{0} 图片下载完成".format(num_images))
    progress_label.pack()

    def update_progress(index):

        progress_label.config(text="{0}/{1} 图片下载完成".format(index, num_images))
        progress_window.update_idletasks()
        progress_var.set(index)

    for index, image in enumerate(imageData, start=1):
        base64_to_file(image.get('imageData'), image.get('imageName'), folder_selected)
        update_progress(index)

    messagebox.showinfo('下载成功', '文件下载成功!')
    dir_config.dirconfig.set_dir(folder_selected)
    progress_window.destroy()
def get_images_from_backend(api_url, size,type,own):
    try:
        # 构建查询参数
        params = {
            'size': size,
            'type': type,
            'own':own
        }
        # 构建请求头，包括Authorization参数
        headers = {
            'Authorization': Config().get_token()
        }
        # 发送GET请求
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()  # 确保请求成功
        # 解析响应内容
        result = response.json()
        return True, result
    except requests.RequestException as e:
        return False, f"An error occurred: {e}"


def uploadJudgeImages():
    UPLOAD_JSON_URL=URLProvider.get_url()+'/images/judgeImage'
    FILES_DIR = "D://JudgeImageData/";
    # 读取文件目录中的文件
    for filename in os.listdir(FILES_DIR):
        if(filename.endswith('.json')):
            file_path = os.path.join(FILES_DIR, filename)
            # 获取文件的MIME类型
            mime_type, _ = mimetypes.guess_type(filename)
            # 如果mimetypes模块无法识别文件类型，默认为'application/octet-stream'
            mime_type = mime_type if mime_type else 'application/octet-stream'
            files_to_upload.append(('files', (filename, open(file_path,'rb'),mime_type)))
            print(filename)
    # 准备上传的参数
    headers = {
        'Authorization': Config().get_token()
    }
    try:
        response = requests.post(UPLOAD_JSON_URL, files=files_to_upload,headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("上传成功", "所有json文件已成功上传！")
            # 关闭所有文件
            for filetuple in files_to_upload:
                filetuple[1][1].close()
            shutil.rmtree(FILES_DIR)
        else:
            messagebox.showerror("上传失败", f"上传失败，状态码：{response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("上传失败", f"上传过程中发生错误：{e}")

def save_json_data(json_data):
    DOWNLOAD_JSON_URL=URLProvider.get_url()+'/images/getLabelResult'
    try:
        # 构建查询参数
        params = {

        }
        # 构建请求头，包括Authorization参数
        headers = {
            'Authorization': Config().get_token()
        }
        # 发送GET请求
        response = requests.get(DOWNLOAD_JSON_URL, params=params, headers=headers)
        response.raise_for_status()  # 确保请求成功
        # 解析响应内容
        result = response.json()
        return True, result
    except requests.RequestException as e:
        return False, f"An error occurred: {e}"



    try:
        # 创建一个 Tkinter 窗口
        root = tk.Tk()
        root.withdraw()
        # 让用户选择保存文件的文件夹
        save_folder = filedialog.askdirectory()
        if not save_folder:
            print("未选择保存文件夹，程序终止。")
            return
        # 解析 JSON 数据
        data = json.loads(json_data)
        # 遍历 data 列表中的每个元素
        for item in data['data']:
            image_name = item['imageName']
            json_data = item['jsonData']
            if json_data is not None:
                # 生成新的文件名，将 imageName 后缀修改为.json
                json_file_name = os.path.join(save_folder, image_name.split('.')[0] + '.json')
                # 以文本模式打开文件并写入 jsonData
                with open(json_file_name, 'w') as file:
                    file.write(json_data)
    except Exception as e:
        print(f"Error occurred: {e}")