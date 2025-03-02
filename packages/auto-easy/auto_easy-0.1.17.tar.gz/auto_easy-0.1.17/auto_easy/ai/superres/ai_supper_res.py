import os

import cv2
import numpy as np

from auto_easy.ai.model_mgr_v2 import AIModelBase
from auto_easy.constant import get_test_pic
from auto_easy.image.cvt import img_2_ndarray_rgb, img_2_list, list_2_ndarray


class SuperRes(AIModelBase):
    def __init__(self, *args, **kwargs):
        self.arg = args
        self.kwargs = kwargs
        dir = os.path.dirname(__file__)
        # 受限于PIP大小，这里只上传一个pb
        self.scale_conf = {
            # 2: os.path.join(dir, 'EDSR_x2.pb'),
            3: os.path.join(dir, 'EDSR_x3.pb'),
            # 4: os.path.join(dir, 'EDSR_x4.pb'),
        }
        self.scale_model_map = {}
        super().__init__(name='SuperRes')

    def init_model(self):
        for scale_factor, model_path in self.scale_conf.items():
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            # 读取预训练的模型
            sr.readModel(model_path)
            # 设置放大倍数
            sr.setModel("edsr", scale_factor)
            self.scale_model_map[scale_factor] = sr

    def predict(self, img, scale_factor=3):
        if self.use_rpc():
            return self.rpc_call(img, scale_factor)

        self.wait_model_init()
        if scale_factor not in self.scale_model_map.keys():
            raise Exception('scale factor {} not supported. only support 2/3/4'.format(scale_factor))
        sr = self.scale_model_map[scale_factor]
        img = img_2_ndarray_rgb(img)
        # 对图像进行超分辨率放大
        result = sr.upsample(img)
        return result

    def rpc_req_encode(self, *args, **kwargs):
        if len(args) < 1:
            raise Exception('args length error')
        args_list = list(args)
        args_list[0] = img_2_list(args_list[0])
        args = tuple(args_list)
        return args, kwargs

    def rpc_req_decode(self, *args, **kwargs):
        args_list = list(args)
        args_list[0] = list_2_ndarray(args_list[0])
        args = tuple(args_list)
        return args, kwargs

    def rpc_resp_encode(self, origin_resp):
        return origin_resp.tolist()

    def rpc_resp_decode(self, str_resp):
        img = list_2_ndarray(str_resp)
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
        return img


# ocr = AIOCR()
if __name__ == '__main__':
    supper_res = SuperRes()
    ans = supper_res.mock_rpc_call(get_test_pic('skill_name.bmp'), scale_factor=4)
    print(type(ans))
    ans = ans.astype(np.uint8)
    cv2.imshow('result', ans)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(get_test_pic('skill_name_scaled.bmp'), ans)
    print(ans.shape)
