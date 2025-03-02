import os

from auto_easy.ai.ai_yolo.ai_yolo_v5 import ModelConf, AIYoloV5, AIYolo
from auto_easy.ai.model_mgr_v2 import ModelMgrV2, AIModelBase
from auto_easy.models import MYoloItem, YoloItem
from auto_easy.utils import find_classes_inheriting
from auto_easy.window.windows import Window


class WinYolo(Window, ModelMgrV2):
    def __init__(self, window_id, models: list[AIModelBase], rpc_server_port=8765, item_model_dir=''):
        Window.__init__(self, window_id=window_id)
        ModelMgrV2.__init__(self, models=models, rpc_server_port=rpc_server_port)
        self._cur_yolo_name = ''
        if item_model_dir != '' and not os.path.isdir(item_model_dir):
            raise Exception('item_model_dir must be a valid path: {}'.format(item_model_dir))
        self._item_model_dir = item_model_dir

    @property
    def cur_yolo_name(self):
        return self._cur_yolo_name

    @cur_yolo_name.setter
    def cur_yolo_name(self, name):
        yolo_models = self.get_models_by_cls(AIYolo)
        models_name = [model.name for model in yolo_models]
        if name not in models_name:
            raise Exception(f'invalid yolo model({name}), registed names: {models_name}')
        self._cur_yolo_name = name

    def yolo_predict(self, name=None) -> MYoloItem:
        yolo_models = self.get_models_by_cls(AIYolo)
        if len(yolo_models) == 0:
            raise Exception('No yolo models found')
        # 优先使用用户指定的模型,其次使用cur_yolo_name, 最后默认选择第一个
        model_name = self.cur_yolo_name if self.cur_yolo_name != '' else yolo_models[0].name
        if name is not None:
            model_name = name

        model: AIYolo = None
        for m in yolo_models:
            if m.name == model_name:
                model = m
                break
        if model is None:
            raise Exception(f'no yolo model named "{model_name}" found')

        img = self.capture()
        mdet: MYoloItem = model.predict(img)
        for i, item in enumerate(mdet.items):
            mdet.items[i] = self._auto_cvt_item(item)  # 类型转化
        return mdet

    def _auto_cvt_item(self, item: YoloItem) -> YoloItem:
        # 自动读取_item_model_dir目录下的AIItemBase类，然后调用其静态方法can_new_obj判断是否生成对象
        # 注：这里优先遍历派生类
        if self._item_model_dir == '':
            return item
        item_cls_list = find_classes_inheriting(self._item_model_dir, YoloItem)
        for cls in item_cls_list:
            if cls.can_new_obj(item.name):
                return cls(*item.params_list)
        return item


if __name__ == '__main__':
    conf = ModelConf('yolo_1', '../ai/ai_yolo/yolov5s_best.pt')
    yolo_1 = AIYoloV5(conf)
    conf = ModelConf('yolo_2', '../ai/ai_yolo/yolov5s_best.pt')
    yolo_2 = AIYoloV5(conf)
    # ai_yolo_v5.init_model()
    win = WinYolo('Phone-9a', [yolo_1, yolo_2], item_model_dir=r'E:\repo\dnf_tool\biz\models')
    win.cur_yolo_name = 'yolo_2'
    ans = win.yolo_predict()
    print(ans)
