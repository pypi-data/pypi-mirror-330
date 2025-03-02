from typing import List

from auto_easy.utils import is_actual_subclass, logger
from auto_easy.models import Ctx
from auto_easy.dag.executor import Executor, ExecutorDebug
from auto_easy.dag.layer import DAGLayerDef, LayerConf, DAGLayerSimple, cvt_dag_2_executor


class DAG:
    def __init__(self, name, retry_mode=None):
        self.name = name
        self.layers: List[DAGLayerDef] = []
        self.retry_mode = retry_mode  # None-不重试, 1-回退重试
        self._constructed = False

    def add_layer(self, layer, conf: LayerConf = None):
        # layer支持: executor/layer/sub_dag(待实现)
        if is_actual_subclass(layer, DAG):
            layer = cvt_dag_2_executor(layer)

        if is_actual_subclass(layer, Executor):
            layer = DAGLayerSimple(executor=layer, conf=conf)

        if not is_actual_subclass(layer, DAGLayerDef):
            raise Exception("Dag add layer failed")
        self.layers.append(layer)

    def add_layers(self, layers):
        for layer in layers:
            self.add_layer(layer)

    def insert_dag_layers(self, other):
        for layer in other.layers:
            self.layers.append(layer)

    def construct_layers(self, ctx):
        pass

    def hit(self, ctx: Ctx) -> bool:
        if not self._constructed:
            self.construct_layers(ctx)
            self._constructed = True
        return self.layers[0].hit(ctx=ctx)

    def run(self, ctx: Ctx):
        if not self._constructed:
            self.construct_layers(ctx)
            self._constructed = True
        if len(self.layers) == 0:
            raise Exception("Dag empty, no layers added")
        logger.info(f'开始执行DAG: {self.name}')
        idx = 0
        retry = 0
        while idx < len(self.layers):
            layer = self.layers[idx]
            succ = False
            if layer.hit(ctx=ctx):
                if layer.run(ctx=ctx):
                    succ = True
            if succ or layer.conf.skip_err:
                idx += 1
                continue

            if self.retry_mode and self.retry_mode == 1 and retry < 1:
                if idx > 0:
                    logger.warning("Retrying layer, failed layer: {}, goback: {}".format(self.layers[idx].name,
                                                                                         self.layers[idx - 1].name))
                    idx = idx - 1
                    retry += 1
                    continue

            logger.error(f'DAG({self.name}) 执行失败, layer: {layer.name}')
            return False
        return True

    @staticmethod
    def simple_new(name, executors: List[Executor]):
        dag = DAG(name)
        dag.add_layers(executors)
        return dag


class SubDAG2Executor(Executor):
    def __init__(self, dag: DAG):
        super().__init__(dag.name)
        self.dag = dag

    def hit_start(self, ctx: Ctx) -> bool:
        return self.dag.hit(ctx=ctx)

    def exec(self, ctx: Ctx) -> bool:
        return self.dag.run(ctx=ctx)

    @staticmethod
    def cvt(dag: DAG):
        return SubDAG2Executor(dag=dag)


if __name__ == "__main__":
    dag = DAG('测试重试功能', retry_mode=1)
    dag.add_layer(
        ExecutorDebug('layer1')
    )
    dag.add_layer(
        ExecutorDebug('layer2', exec_wait=1)
    )
    dag.add_layer(
        ExecutorDebug('layer3', hit_ret=True)
    )
    ok = dag.run(ctx=Ctx())
    print(ok)
    pass
