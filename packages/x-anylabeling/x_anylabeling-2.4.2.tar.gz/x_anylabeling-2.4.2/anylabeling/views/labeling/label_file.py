import os
import base64
import contextlib
import io
import json
import os.path as osp

import PIL.Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from ...app_info import __version__
from . import utils
from .shape import Shape
from .logger import logger
from .label_converter import LabelConverter

PIL.Image.MAX_IMAGE_PIXELS = None

@contextlib.contextmanager
def io_open(name, mode):
    assert mode in ["r", "w"]
    encoding = "utf-8"
    yield io.open(name, mode, encoding=encoding)


class LabelFileError(Exception):
    pass


class LabelFile:
    suffix = ".json"

    def __init__(self, filename=None, image_dir=None):
        self.shapes = []
        self.image_path = None
        self.image_data = None
        self.image_dir = image_dir
        if filename is not None:
            self.load(filename)
        self.filename = filename

    @staticmethod
    def load_image_file(filename, default=None):
        try:
            with open(filename, "rb") as f:
                return f.read()
        except:
            logger.error("Failed opening image file: %s", filename)
            return default

    def load(self, filename):
        keys = [
            "version",
            "imageData",
            "imagePath",
            "shapes",  # polygonal annotations
            "flags",  # image level flags
            "imageHeight",
            "imageWidth",
        ]
        try:
            with io_open(filename, "r") as f:
                data = json.load(f)
            version = data.get("version")
            if version is None:
                logger.warning(
                    "Loading JSON file (%s) of unknown version", filename
                )

            # Deprecated
            if data["shapes"]:
                for i in range(len(data["shapes"])):
                    shape_type = data["shapes"][i]["shape_type"]
                    shape_points = data["shapes"][i]["points"]
                    if shape_type == "rectangle" and len(shape_points) == 2:
                        logger.warning(
                            "UserWarning: Diagonal vertex mode is deprecated in X-AnyLabeling release v2.2.0 or later.\n"
                            "Please update your code to accommodate the new four-point mode."
                        )
                        data["shapes"][i][
                            "points"
                        ] = utils.rectangle_from_diagonal(shape_points)

            data["imagePath"] = osp.basename(data["imagePath"])
            if data["imageData"] is not None:
                image_data = base64.b64decode(data["imageData"])
            else:
                # relative path from label file to relative path from cwd
                if self.image_dir:
                    image_path = osp.join(self.image_dir, data["imagePath"])
                else:
                    image_path = osp.join(
                        osp.dirname(filename), data["imagePath"]
                    )
                image_data = self.load_image_file(image_path)
            flags = data.get("flags") or {}
            image_path = data["imagePath"]
            self._check_image_height_and_width(
                base64.b64encode(image_data).decode("utf-8"),
                data.get("imageHeight"),
                data.get("imageWidth"),
            )
            shapes = [Shape().load_from_dict(s) for s in data["shapes"]]
        except Exception as e:  # noqa
            raise LabelFileError(e) from e

        other_data = {}
        for key, value in data.items():
            if key not in keys:
                other_data[key] = value

        # Add new fields if not available
        other_data["description"] = other_data.get("description", "")

        # Only replace data after everything is loaded.
        self.flags = flags
        self.shapes = shapes
        self.image_path = image_path
        self.image_data = image_data
        self.filename = filename
        self.other_data = other_data

    @staticmethod
    def _check_image_height_and_width(image_data, image_height, image_width):
        img_arr = utils.img_b64_to_arr(image_data)
        if image_height is not None and img_arr.shape[0] != image_height:
            logger.error(
                "image_height does not match with image_data or image_path, "
                "so getting image_height from actual image."
            )
            image_height = img_arr.shape[0]
        if image_width is not None and img_arr.shape[1] != image_width:
            logger.error(
                "image_width does not match with image_data or image_path, "
                "so getting image_width from actual image."
            )
            image_width = img_arr.shape[1]
        return image_height, image_width

    def save(
        self,
        filename=None,
        shapes=None,
        image_path=None,
        image_height=None,
        image_width=None,
        image_data=None,
        other_data=None,
        flags=None,
    ):
        if image_data is not None:
            image_data = base64.b64encode(image_data).decode("utf-8")
            image_height, image_width = self._check_image_height_and_width(
                image_data, image_height, image_width
            )

        if other_data is None:
            other_data = {}
        if flags is None:
            flags = {}
        # 计算 points 的最值
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
        labelTotal = False
        #构建shapes
        for i, shape in enumerate(shapes):
            if "total" in shape and shape["total"] is True:
                labelTotal=True
            if shape["shape_type"] == "rectangle":
                sorted_box = LabelConverter.calculate_bounding_box(
                    shape["points"]
                )
                xmin, ymin, xmax, ymax = sorted_box
                shape["points"] = [
                    [xmin, ymin],
                    [xmax, ymin],
                    [xmax, ymax],
                    [xmin, ymax],
                ]
                min_x=min(min_x,xmin)
                min_y=min(min_y,ymin)
                max_x=max(max_x,xmax)
                max_y=max(max_y,ymax)
                shapes[i] = shape

        # 将shapes数组按照坐标排序
        shapes = sorted(shapes, key=lambda shape: shape['points'][0][0])
        if labelTotal==False:
            #对label进行收集整合
            label_str = ""
            for shape in shapes:
                # 检查形状中是否存在 label 属性
                if "label" in shape:
                    try:
                        # 尝试将 label 转换为浮点数
                        label_num = float(shape["label"])
                        # 向下取整
                        label_num = int(label_num)
                        # 转换为字符串
                        label_str += str(label_num)
                    except ValueError:
                        # 如果 label 无法转换为浮点数，进行异常处理
                        print(f"Warning: The label '{shape['label']}' cannot be converted to a number.")

            # 创建新的 rectangle 对象
            new_rectangle = {
                "kie_linking": [],
                "label": label_str,
                "score": None,
                "points": [
                    [min_x, min_y],
                    [max_x, min_y],
                    [max_x, max_y],
                    [min_x, max_y]
                ],
                "group_id": None,
                "description": "",
                "difficult": False,
                "shape_type": "rectangle",
                "flags": {},
                "attributes": {},
                "total": True
            }
            # 将新对象添加到 shapes 列表
            shapes.append(new_rectangle)

        # 将整个水表的读数放在第一位
        longest_label_shape = max(shapes, key=lambda shape: len(shape['label']))

        shapes.remove(longest_label_shape)
        shapes.insert(0, longest_label_shape)
        data = {
            "version": __version__,
            "flags": flags,
            "shapes": shapes,
            "imagePath": image_path,
            "imageData": image_data,
            "imageHeight": image_height,
            "imageWidth": image_width,
        }

        for key, value in other_data.items():
            assert key not in data
            data[key] = value
        try:
            with io_open(filename, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.filename = filename
        except Exception as e:  # noqa
            raise LabelFileError(e) from e

    @staticmethod
    def is_label_file(filename):
        return osp.splitext(filename)[1].lower() == LabelFile.suffix
