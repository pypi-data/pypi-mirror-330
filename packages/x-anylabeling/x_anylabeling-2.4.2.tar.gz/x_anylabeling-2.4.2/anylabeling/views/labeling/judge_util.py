import base64
import json
import logging
import os
import sys
from io import BytesIO
from PIL import Image, ImageDraw
from PIL import ImageFont
# from PyQt5 import Qt
from PyQt5.QtCore import Qt
# from PIL.ImageFont import ImageFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QSplitter, \
    QSizePolicy, QHBoxLayout,QDialog,QMessageBox
from onnxruntime.transformers.shape_infer_helper import file_path

from anylabeling.views.labeling.singleton import Config
import requests
from anylabeling.views.labeling.base64_to_file import base64_to_file
from anylabeling.views.labeling.utils.url import URLProvider

# from PyQt5.QtGui import QPixmap

# 指定文件夹路径

class JudgeDialog(QDialog):
    def __init__(self, parent=None):
        super(JudgeDialog, self).__init__(parent)
        self.current_index=0

        self.folder_path = 'D://JudgeData'
        # 获取文件夹中的所有文件名
        self.files=os.listdir(self.folder_path)

        if len(self.files) < 1:
            return  # 停止初始化，不显示对话框
        # 过滤出JSON文件
        self.json_files = [f for f in self.files if f.endswith('.json')]

        self.json_data1 = self.read_json_file(self.json_files[0],"jsonData")
        self.json_data2 = self.read_json_file(self.json_files[1],"jsonData")

        self.image1=None
        self.image2=None

        try:


            self.image1 = self.draw_shapes_on_image(self.json_files[0])
            self.image2 = self.draw_shapes_on_image(self.json_files[1])

            if self.image1 and self.image2:
                buffer1 = BytesIO()
                self.image1.save(buffer1, format='PNG')
                buffer1.seek(0)  # 确保缓冲区位置正确
                q_image1 = QPixmap()
                if not q_image1.loadFromData(buffer1.getvalue()):
                    raise ValueError("Could not load image 1")

                buffer2 = BytesIO()
                self.image2.save(buffer2, format='PNG')
                buffer2.seek(0)  # 确保缓冲区位置正确
                q_image2 = QPixmap()
                if not q_image2.loadFromData(buffer2.getvalue()):
                    raise ValueError("Could not load image 2")

                layout = QVBoxLayout()

                self.setWindowTitle('Judge')
                # 获取屏幕尺寸
                screen = QApplication.primaryScreen()
                screen_geometry = screen.geometry()
                screen_width = screen_geometry.width()
                screen_height = screen_geometry.height()
                # 设置对话框大小为屏幕的 80%
                dialog_width = int(screen_width * 0.8)
                dialog_height = int(screen_height * 0.8)
                self.setFixedSize(dialog_width, dialog_height)
                # layout = QVBoxLayout()
                #
                # self.setWindowTitle('Judge')
                # self.setFixedSize(1000, 500)

                self.label1 = QLabel()
                self.label1.setPixmap(q_image1)
                self.label1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
                self.label1.setScaledContents(True)

                self.label2 = QLabel()
                self.label2.setPixmap(q_image2)
                self.label2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
                self.label2.setScaledContents(True)


                self.button1 = QPushButton('选择左边图片')
                self.button1.clicked.connect(self.select1)
                self.button1.clicked.connect(self.next_group)

                self.button2 = QPushButton('选择右边图片')
                self.button2.clicked.connect(self.select2)
                self.button2.clicked.connect(self.next_group)

                self.button3 = QPushButton('选择并重新标注左边图片')
                self.button3.clicked.connect(self.relabel1)
                self.button3.clicked.connect(self.next_group)

                self.button4 = QPushButton('选择并重新标注右边图片')
                self.button4.clicked.connect(self.relabel2)
                self.button4.clicked.connect(self.next_group)


                self.container1=QWidget()
                self.container2=QWidget()

                container1_layout = QVBoxLayout()
                container1_layout.addWidget(self.label1)
                container1_layout.addWidget(self.button1)
                container1_layout.addWidget(self.button3)
                self.container1.setLayout(container1_layout)

                container2_layout = QVBoxLayout()
                container2_layout.addWidget(self.label2)
                container2_layout.addWidget(self.button2)
                container2_layout.addWidget(self.button4)
                self.container2.setLayout(container2_layout)

                self.container3 = QWidget()
                container3_layout = QHBoxLayout()
                container3_layout.addWidget(self.container1)
                container3_layout.addWidget(self.container2)
                self.container3.setLayout(container3_layout)

                # 直接将控件添加到水平布局中
                layout.addWidget(self.container3)


                self.setLayout(layout)


        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON data: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def next_group(self):
      try:
          # 计算上一组文件的位置
        prev_index1 = self.current_index
        prev_index2 = self.current_index + 1

        if prev_index2 < len(self.json_files):
            for file_path in [self.json_files[prev_index1], self.json_files[prev_index2]]:
                file_path='D://JudgeData'+'/'+file_path
                if os.path.exists(file_path):
                    os.remove(file_path)
                    #print(f"删除了文件: {file_path}")
                else:
                    print(f"文件 {file_path} 不存在，无法删除")

        # 计算下一个文件的位置
        next_index1 = self.current_index + 2
        next_index2 = self.current_index + 3

        # 检查是否还有文件可读
        if next_index2 < len(self.json_files):
            self.json_data1 = self.read_json_file(self.json_files[next_index1], "jsonData")
            self.json_data2 = self.read_json_file(self.json_files[next_index2], "jsonData")

            self.image1 = self.draw_shapes_on_image(self.json_files[next_index1])
            self.image2 = self.draw_shapes_on_image(self.json_files[next_index2])

            buffer1 = BytesIO()
            self.image1.save(buffer1, format='PNG')
            buffer1.seek(0)  # 确保缓冲区位置正确
            q_image1 = QPixmap()
            if not q_image1.loadFromData(buffer1.getvalue()):
                raise ValueError("Could not load image 1")

            buffer2 = BytesIO()
            self.image2.save(buffer2, format='PNG')
            buffer2.seek(0)  # 确保缓冲区位置正确
            q_image2 = QPixmap()
            if not q_image2.loadFromData(buffer2.getvalue()):
                raise ValueError("Could not load image 2")

            self.label1.setPixmap(q_image1)
            self.label2.setPixmap(q_image2)

            self.current_index += 2
            print("读取了新的文件组")
        else:
            QMessageBox.information(None,'提示', '没有更多的文件了')
      except Exception as e:
        print(f"An error occurred while reading the next group: {e}")

    def select1(self):
       try:
           index=self.current_index
           file_path = "D://JudgeData/json01.json"
           # 打开文件并写入 JSON 数据
           file_name="D://JudgeData/"+self.json_files[index]
           if not os.path.exists(file_name):
               #print(f"json文件 {file_name} 不存在")
               return

           data1=self.read_json_file(self.json_files[index], "jsonData")
           dict1=json.loads(data1)
           with open(file_path, 'w', encoding='utf-8') as file:
               json.dump(dict1, file, ensure_ascii=False, indent=4)

           send_file(file_path)

           if os.path.exists(file_path):
              # print("删除文件 D://JudgeData/json01.json")
               os.remove(file_path)

       except Exception as e:
        print(f"An error occurred while select1: {e}")

    def select2(self):
        try:
            index = self.current_index+1
            file_path = "D://JudgeData/json02.json"

            # 打开文件并写入 JSON 数据
            file_name = "D://JudgeData/" + self.json_files[index]
            if not os.path.exists(file_name):
                #print(f"文件 {file_name} 不存在")
                return

            data2 = self.read_json_file(self.json_files[index], "jsonData")
            dict2 = json.loads(data2)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(dict2, file, ensure_ascii=False, indent=4)

            send_file(file_path)

            if os.path.exists(file_path):
                #print("删除文件 D://JudgeData/json02.json")
                os.remove(file_path)

        except Exception as e:
            print(f"An error occurred while select2: {e}")

    def relabel1(self):
        try:
            output_folder = "D://JudgeImageData/"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            index = self.current_index
            file_name1 = "D://JudgeData/" + self.json_files[index]
            if not os.path.exists(file_name1):
                print(f"json文件 {file_name1} 不存在")
                return

            data = self.read_json_file(self.json_files[index], "jsonData")
            dict = json.loads(data)

            image_name=dict.get("imagePath",{})
            file_name=image_name[:-4]+".json"
            image_path=os.path.join(output_folder, image_name)
            file_path=os.path.join(output_folder, file_name)

            with open(file_name1, 'r', encoding='utf-8') as file:
                dict1 = json.load(file)
                img_str = get_image_data_str(dict1.get("imageId", {}))
            imageData = img_str.split("data:image/.jpg;base64,")[1]

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(dict, file, ensure_ascii=False, indent=4)

            if imageData:
                # 解码 base64 编码的图像数据
                image_data_bytes = base64.b64decode(imageData)

                # 将解码后的图像数据写入文件
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data_bytes)
            else:
                print("imageData 为空或不存在")

        except Exception as e:
            print(f"An error occurred while relabel1: {e}")

    def relabel2(self):
        try:
            output_folder = "D://JudgeImageData/"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            index = self.current_index+1
            file_name1 = "D://JudgeData/" + self.json_files[index]
            if not os.path.exists(file_name1):
                print(f"json文件 {file_name1} 不存在")
                return
            data = self.read_json_file(self.json_files[index], "jsonData")
            dict = json.loads(data)

            image_name = dict.get("imagePath", {})
            file_name = image_name[:-4] + ".json"
            image_path = os.path.join(output_folder, image_name)
            file_path = os.path.join(output_folder, file_name)

            with open(file_name1, 'r', encoding='utf-8') as file:
                dict1 = json.load(file)
                img_str = get_image_data_str(dict1.get("imageId", {}))
            imageData = img_str.split("data:image/.jpg;base64,")[1]

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(dict, file, ensure_ascii=False, indent=4)

            if imageData:
                image_data_bytes = base64.b64decode(imageData)

                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data_bytes)

        except Exception as e:
            print(f"An error occurred while relabel1: {e}")



    def read_json_file(self, file_name,keyStr):
        with open(os.path.join(self.folder_path, file_name), 'r', encoding='utf-8') as file:
            json_dict = json.load(file)
            json_str1=json_dict.get(keyStr,{})


            json_dict1 = json.loads(json_str1)
            return json.dumps(json_dict1, ensure_ascii=False, indent=4)

    def draw_shapes_on_image(self,file_name):
        try:

            data = json.loads(self.read_json_file(file_name, "jsonData"))
            print(data)

            with open(os.path.join(self.folder_path, file_name), 'r', encoding='utf-8') as file:
                dict = json.load(file)
                img_str=get_image_data_str(dict.get("imageId", {}))

            imageData=img_str.split("data:image/.jpg;base64,")[1]
            print(imageData)

            image_data = base64.b64decode(imageData)


            image = Image.open(BytesIO(image_data))
            draw = ImageDraw.Draw(image)

            for shape in data['shapes']:
                if 'total' in shape and shape['total']==True :  # 检查 shape 中是否含有 total 字段
                    label = shape['label']
                    points = shape['points']
                    int_points = [(int(round(p[0])), int(round(p[1]))) for p in points]
                    draw.polygon(int_points, outline='green')
                    label_position = (int_points[0][0], int_points[3][1])
                    draw.text(label_position, label, fill='green', font=ImageFont.truetype("arial.ttf", 12))
                else :
                    label = shape['label']
                    points = shape['points']
                    int_points = [(int(round(p[0])), int(round(p[1]))) for p in points]
                    draw.polygon(int_points, outline='red')
                    label_position = (int_points[0][0], int_points[3][1])
                    draw.text(label_position, label, fill='blue', font=ImageFont.truetype("arial.ttf", 12))

            return image
        except Exception as e:
            print(f"An error occurred while drawing shapes: {e}")
            return None




def resize_pixmap_to_label(pixmap, label):
        # 获取图片的宽度和高度
        img_width = pixmap.width()
        img_height = pixmap.height()

        # 获取标签的宽度和高度
        label_width = label.width()
        label_height = label.height()

        # 计算宽高比
        img_ratio = img_width / img_height
        label_ratio = label_width / label_height

        # 根据宽高比缩放图片
        if img_ratio > label_ratio:
            # 图片更宽，缩放宽度
            new_width = label_width
            new_height = int(new_width / img_ratio)
        else:
            # 图片更高或相等，缩放高度
            new_height = label_height
            new_width = int(new_height * img_ratio)

        # 返回缩放后的pixmap
        return pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

def downloadJudgeFiles():
    api_url = URLProvider.get_url()+'/images/getImageToJudge'
    # token=Config.get_token()
    #print(Config().get_token())
    # print(token)
    output_folder = "D://JudgeData/"
    try:
        success, data = get_jsons_from_backend(api_url)
    except Exception as e:
        print(f"An error occurred: {e}")
    if success:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        data1=(
            data.get('data',{}))
        # 遍历数据集中的每个元素
        for item in data1:
            id = item.get("id")
            imageId=item.get("imageId")
            if id and imageId:
                file_path = os.path.join(output_folder, f"{imageId}_{id}.json")
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(item, json_file, ensure_ascii=False, indent=4)
        QMessageBox.information(None,'提示', '获取文件成功')
    else:
        QMessageBox.information(None,'提示', '获取文件失败')


def get_jsons_from_backend(api_url):
    try:
        # 构建查询参数

        # 构建请求头，包括Authorization参数
        headers = {
            'Authorization': Config().get_token()
        }
        # 发送GET请求
        response = requests.post(api_url,  headers=headers)
        response.raise_for_status()  # 确保请求成功
        # 解析响应内容
        result = response.json()
        return True, result
    except requests.RequestException as e:
        return False, f"An error occurred: {e}"



def get_image_data_str(id):
    api_url = URLProvider.get_url()+f'/images/getImage/{id}'
    try:
        # 构建查询参数

        # 构建请求头，包括Authorization参数
        headers = {
            'Authorization': Config().get_token()
        }
        # 发送GET请求
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        # 解析响应内容
        result = response.json().get('data',{})
        print(result)

        return result

    except requests.RequestException as e:
        return False, f"An error occurred: {e}"

def send_file(file_path):
    api_url = URLProvider.get_url()+'/images/judgeImage'
    try:
        # 构建请求头，包括Authorization参数
        headers = {
            'Authorization': Config().get_token()
        }
        # 打开文件并构建文件参数
        with open(file_path, 'rb') as files:
            files = {
                'files': (file_path.split('/')[-1], files, 'application/json')  # 假设文件是 JSON 格式
            }
            #print(files)
            # 发送POST请求
            response = requests.post(api_url, headers=headers, files=files)
            response.raise_for_status()  # 确保请求成功

            logging.error("发送成功")
            # 解析响应内容
            result = response.json()
            return True, result
    except requests.RequestException as e:
        return False, f"An error occurred: {e}"