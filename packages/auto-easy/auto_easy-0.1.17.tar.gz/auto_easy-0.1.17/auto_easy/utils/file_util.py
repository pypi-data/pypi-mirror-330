import os

from PIL import Image


def is_image(file_path):
    try:
        img = Image.open(file_path)  # 尝试打开图像文件  
        img.verify()  # 验证文件是否损坏  
        return True
    except (IOError, SyntaxError):  # PIL无法识别的文件类型会抛出IOError  
        return False


def get_files(dir_path, file_prefix='', file_ext=''):
    res = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file_prefix != '' and not file.startswith(file_prefix):
                continue
            if file_ext != '' and not file.endswith(file_ext):
                continue
            abs_path = os.path.join(root, file)
            res.append(abs_path)
    return res
