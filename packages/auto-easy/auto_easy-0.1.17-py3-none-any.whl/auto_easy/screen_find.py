import PIL
import aircv as ac
import cv2
import numpy as np
from PIL import Image

from auto_easy.utils import logger
from auto_easy.constant import get_test_pic
from auto_easy.image.cvt import img_2_ndarray_rgb
from auto_easy.models import Box


def find_pic(im_source: PIL.Image, im_search: PIL.Image, scale=1, match_box: Box = None, multi_match=False, rgb=True,
             sim=0.9):
    origin_source = im_source
    # logger.debug(f'find_pic args: {type(im_source)},{im_search}  {scale}, {match_box}, {multi_match}, {rgb}, {sim}')
    if isinstance(im_source, str):
        im_source = Image.open(im_source)
    if isinstance(im_search, str):
        im_search = Image.open(im_search)

    if match_box is not None:
        im_source = im_source.crop(match_box.tuple())

    im_source = img_2_ndarray_rgb(im_source)
    im_search = img_2_ndarray_rgb(im_search)
    if scale != 1:
        im_search = cv2.resize(im_search, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    maxcnt = 0 if multi_match else 1
    try:
        match_results = ac.find_all_template(im_source, im_search, threshold=sim, rgb=rgb, bgremove=False,
                                             maxcnt=maxcnt)
    except Exception as e:
        logger.debug(
            f'find_pic fail: {e},{type(origin_source)},{origin_source.size},{match_box}, {len(cv2.split(im_source))}, {len(cv2.split(im_search))} ')
        raise e
    boxes = []
    for match_result in match_results:
        box = Box(match_result['rectangle'][0][0], match_result['rectangle'][0][1], match_result['rectangle'][3][0],
                  match_result['rectangle'][3][1])
        if match_box is not None:
            box.move(match_box.x1, match_box.y1)
        boxes.append(box)
        # logger.debug(f'{match_result["confidence"]}; {box}')
    return boxes


def proc_test(img):
    img = cv2.imread(img)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # 边缘检测
    img = cv2.Canny(img, 100, 200)
    return img


if __name__ == '__main__':
    # set_env('window_prefix', 'Phone-VB')
    steps = [1]
    steps = np.arange(0.91, 0.92, 0.01)
    for i in steps:
        # pic1 = get_test_pic('zjm.jpg')
        pic1 = get_test_pic('debug/fsdsyc1.bmp')
        pic2 = get_test_pic('debug/40_破坏者碉堡轰炸$$$level=40&type=主动技能.bmp')
        # pic1 = get_test_pic('source_pic_2.bmp')
        # pic1 = get_test_pic('zjm.bmp')
        # pic2 = get_test_pic('search_pic_2.bmp')
        # pic2 = get_test_pic('pl0_1.png')
        # pic1 = image_color_keep(pic1,'976536-393734')
        # show_image(pic1)
        # pic2 = image_color_keep(pic2,'976536-393734')
        # show_image(pic2)

        # A31913-3B1A14
        # pic1 = proc_test(pic1)
        # pic2 = proc_test(pic2)
        # show_image(pic1)
        # show_image(pic2)

        print(i)
        box = find_pic(pic1, pic2, rgb=False, multi_match=False, sim=0.9, scale=i)
        if len(box) > 0:
            print([str(x) for x in box])
            box = box[0]
            # img = Image.open(pic1)
            # crop_img = img.crop(box.tuple())
            # crop_img.show()
            # crop_img.save(gen_test_pic('crop.bmp'))
            # ok = find_color_in_image(crop_img,'A01E1E-3E1E1E')
            # print(f'ok:{ok}')
