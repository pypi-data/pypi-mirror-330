import base64
import os


def base64_to_file(base64_string, file_name, dir_path):
    """
    将Base64字符串转换为文件。

    :param base64_string: 输入的Base64字符串。
    :param file_path: 输出文件的路径。

    Args:
        dir_path:
    """
    # 移除前缀
    base64_data = base64_string.split(",")[1]

    # 确保base64字符串有正确的填充
    padding = '=' * (-len(base64_data) % 4)
    base64_data += padding

    # 解码base64字符串
    image_data = base64.b64decode(base64_data)

    # 将Base64字符串解码为原始数据
    data = base64.b64decode(base64_data)
    if(dir_path==None):
        dir_path="D://ImageData/"
    # 检查文件路径是否存在，如果不存在则创建目录
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将数据写入文件
    with open(dir_path+file_name, 'wb') as file:
        file.write(data)

    # 打印文件路径以供确认
    print(f'文件已写入: {dir_path+file_name}')


# 示例Base64字符串
# base64_string = '你的Base64字符串'

# 示例文件路径
# file_path = '/mnt/data/output_file.jpg'

# 调用函数转换Base64字符串到文件
# base64_to_file(base64_string, file_path)
