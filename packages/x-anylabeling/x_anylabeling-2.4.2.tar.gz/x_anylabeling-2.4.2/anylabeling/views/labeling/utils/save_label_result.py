import json
import os
import sys
import tkinter
from datetime import datetime
from tkinter import filedialog

import requests
from PyQt5.QtCore import QDate, QDateTime, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QDateTimeEdit, QLabel, QApplication, QMessageBox
import tkinter as tk

from anylabeling.views.labeling.singleton import Config
from anylabeling.views.labeling.utils.url import URLProvider


# 假设下面两个模块存在且能正常工作
# from anylabeling.views.labeling.singleton import Config
# from anylabeling.views.labeling.utils.url import URLProvider


def download_json(start_time=None, end_time=None):
    # 这里假设 URLProvider.get_url() 能正常返回一个有效的 URL
    DOWNLOAD_JSON_URL = URLProvider.get_url() +'/images/getLabelResult'
    try:
        # 构建查询参数
        params = {}
        if start_time:
            # 将 start_time 转换为所需的格式
            params['startTimeStr'] = start_time
        if end_time:
            # 将 end_time 转换为所需的格式
            params['endTimeStr'] = end_time
        # 构建请求头，包括 Authorization 参数
        headers = {
            'Authorization': Config().get_token()
            # 'Authorization':
        }
        # 发送 GET 请求
        response = requests.get(DOWNLOAD_JSON_URL, params=params, headers=headers)
        response.raise_for_status()  # 确保请求成功
        # 解析响应内容
        result = response.json()
        return True, result
    except requests.RequestException as e:
        print(e)
        return False, f"An error occurred: {e}"


class DateTimeEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 开始时间选择器
        self.start_dateEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        # 结束时间选择器
        self.end_dateEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.btn = QPushButton("获取 JSON 数据")
        self.result_label = QLabel("")  # 用于显示结果的标签

        self.initUI()

    def initUI(self):
        self.setWindowTitle("选择时间范围并获取 JSON")
        self.resize(300, 200)

        layout = QVBoxLayout()
        # 设置开始时间选择器的显示格式和范围
        self.start_dateEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.start_dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.start_dateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.start_dateEdit.setCalendarPopup(True)

        # 设置结束时间选择器的显示格式和范围
        self.end_dateEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.end_dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.end_dateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.end_dateEdit.setCalendarPopup(True)

        self.btn.clicked.connect(self.onButtonClick)

        layout.addWidget(QLabel("开始时间:"))
        layout.addWidget(self.start_dateEdit)
        layout.addWidget(QLabel("结束时间:"))
        layout.addWidget(self.end_dateEdit)
        layout.addWidget(self.btn)
        layout.addWidget(self.result_label)  # 添加结果标签
        self.setLayout(layout)

    def onButtonClick(self):
        start_dateTime = self.start_dateEdit.dateTime()
        end_dateTime = self.end_dateEdit.dateTime()
        # 这里可以添加额外的时间范围验证逻辑，确保开始时间不晚于结束时间
        if start_dateTime > end_dateTime:
            QMessageBox.warning(self, "时间范围错误", "开始时间不能晚于结束时间")
            return
        # 将 QDateTime 对象转换为 ISO 8601 格式的字符串
        start_time = start_dateTime.toString(Qt.ISODate)
        end_time = end_dateTime.toString(Qt.ISODate)
        success, result = download_json(start_time, end_time)
        if success:
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
                data = result
                # 遍历 data 列表中的每个元素
                for item in data['data']:
                    image_name = item['imageName']
                    json_data = item['jsonData']
                    if json_data is not None:
                        # 生成新的文件名，将 imageName 后缀修改为.json
                        json_file_name = os.path.join(save_folder, image_name.split('.')[0] + '.json')
                        # 删除 json_data 中的 \r
                        json_data = json_data.replace('\r', '')
                        # 以文本模式打开文件并写入 jsonData
                        with open(json_file_name, 'w') as file:
                            file.write(json_data)
                # 显示成功提示框
                QMessageBox.information(self, "成功", "JSON 文件下载并保存成功！")
                # 下载和保存完成后自动关闭对话框
                self.accept()
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            tkinter.messagebox.showerror("Error", "下载失败，请检查网络或参数！")


def getjson():
    # app = QApplication(sys.argv)
    dialog = DateTimeEditDialog()
    dialog.exec_()


def save_json_data_from_json(json_data):
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


if __name__ == "__main__":
    getjson()