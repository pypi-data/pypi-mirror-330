import time
from abc import abstractmethod
from typing import List

from auto_core import set_obj_by_dict, Ctx, Timeout, is_actual_subclass, logger, concurrent_exec_multi_func_one_arg
from auto_core.dag.executor import Executor, ExecutorDebug


class LayerConf:
    def __init__(self, skip_err=False):
        # 通用配置: 控制DAG图的运行逻辑
        self.name = ''
        self.skip_err = skip_err  # 忽略该层错误,继续往下执行,达到类似节点跳过的效果

        # 定制化配置
        self.type = DAGLayerSimple

    @staticmethod
    def new_by_json(js):
        conf = LayerConf()
        set_obj_by_dict(conf, js)
        return conf


class DAGLayerDef:
    def __init__(self, name='', conf: LayerConf = None):
        self.conf = conf if conf is not None else LayerConf()
        self.name = name
        pass

    @abstractmethod
    def hit(self, ctx: Ctx) -> bool:
        pass

    @abstractmethod
    def run(self, ctx: Ctx):
        pass


class DAGLayerSimple(DAGLayerDef):
    def __init__(self, executor: Executor, conf: LayerConf = None):
        super().__init__(executor.name, conf)
        self.executor = cvt_dag_2_executor(executor)

    def hit(self, ctx: Ctx) -> bool:
        return self.executor.hit_start(ctx)

    def run(self, ctx: Ctx):
        return self.executor.run(ctx)


class LayerLoopConf(LayerConf):
    def __init__(self):
        super().__init__()
        self.loop_times = 1  # 最大循环次数
        self.loop_suc_times = 0  # 至少成功的次数


class DAGLayerLoop(DAGLayerSimple):
    def __init__(self, executor: Executor, conf: LayerLoopConf = None):
        conf = conf if conf is not None else LayerLoopConf()
        super().__init__(executor, conf)
        self.conf = conf

    def run(self, ctx: Ctx):
        success_cnt = 0
        for i in range(1, self.conf.loop_times):
            success = self.executor.run(ctx)
            if success:
                success_cnt += 1

            if not success:
                return success_cnt >= self.conf.loop_suc_times
        return True


class DAGLayerSwitch(DAGLayerDef):
    def __init__(self, executors: List[Executor], switch_to=1):
        super().__init__('多分支互斥路由')
        self.executors = [cvt_dag_2_executor(e) for e in executors]
        self.switch_to = switch_to
        self.target_exec = None

    def hit(self, ctx: Ctx) -> bool:
        # 实现switch效果,选择命中的exec
        to = Timeout(self.switch_to)
        self.target_exec = None
        while to.not_timeout():
            for executor in self.executors:
                if executor.hit_start(ctx):
                    self.target_exec = executor
                    break
            if self.target_exec:
                break
            time.sleep(self.switch_to / 10)
        if self.target_exec:
            return True
        return False

    def run(self, ctx: Ctx):
        return self.target_exec.run(ctx)


class SwitchBranch:
    def __init__(self, executor: Executor, is_finish=False):
        self.executor: Executor = executor
        self.is_finish = is_finish


class DAGLayerLoopSwitch(DAGLayerDef):
    def __init__(self, loop_to=1, min_loop_time=0, loop_sleep=0.1, bf_sleep=0):
        super().__init__('循环多分支路由')
        self.branches: list[SwitchBranch] = []
        self.loop_to = loop_to
        self.loop_sleep = loop_sleep
        self.min_loop_time = min_loop_time
        self.bf_sleep = bf_sleep

    def hit(self, ctx: Ctx) -> bool:
        return True

    def add_branch(self, executor, is_finish=False):
        executor = cvt_dag_2_executor(executor)
        self.branches.append(SwitchBranch(executor, is_finish))

    def run(self, ctx: Ctx):
        time.sleep(self.bf_sleep)
        to = Timeout(self.loop_to)
        while to.not_timeout():
            target_branch = None
            funcs = [branch.executor.hit_start for branch in self.branches]
            hits = concurrent_exec_multi_func_one_arg(funcs, ctx)
            for i, is_hit in enumerate(hits):
                if is_hit:
                    target_branch = self.branches[i]
                    break
            if not target_branch:
                time.sleep(self.loop_sleep)
                continue
            ok = target_branch.executor.run(ctx)
            if not ok:
                logger.debug('Layer(循环多分支路由) 执行失败, Executor: {}'.format(target_branch.executor.name))
                return False

            if target_branch.is_finish:
                return True
            time.sleep(self.loop_sleep)
        logger.error('Layer(循环多分支路由) 执行失败, 超时: {}'.format(self.loop_to))
        return False


class DAGLayerSwitchOneV2(DAGLayerDef):
    def __init__(self, loop_to=1, loop_sleep=0.1, bf_sleep=0):
        super().__init__('多分支选一执行')
        self.branches: list[SwitchBranch] = []
        self.loop_to = loop_to
        self.loop_sleep = loop_sleep
        self.bf_sleep = bf_sleep

    def hit(self, ctx: Ctx) -> bool:
        return True

    def add_branch(self, executor, is_finish=False):
        executor = cvt_dag_2_executor(executor)
        self.branches.append(SwitchBranch(executor, is_finish))

    def run(self, ctx: Ctx):
        time.sleep(self.bf_sleep)
        to = Timeout(self.loop_to)
        target_branch = None
        while to.not_timeout():
            funcs = [branch.executor.hit_start for branch in self.branches]
            hits = concurrent_exec_multi_func_one_arg(funcs, ctx)
            for i, is_hit in enumerate(hits):
                if is_hit:
                    target_branch = self.branches[i]
                    break
            if target_branch:
                break
            time.sleep(self.loop_sleep)

        if not target_branch:
            logger.error('Layer(多分支选一执行) 规定时间内未选中任意分支, 超时: {}, 分支名: {}'
                         .format(self.loop_to, [branch.executor.name for branch in self.branches]))
            return False

        ok = target_branch.executor.run(ctx)
        if not ok:
            logger.error('Layer(多分支选一执行) 执行分支({})失败'.format(target_branch.executor.name))
            return False
        return True


def cvt_dag_2_executor(obj) -> Executor:
    if is_actual_subclass(obj, Executor):
        return obj

    from auto_core.dag.dag import DAG, SubDAG2Executor
    if is_actual_subclass(obj, DAG):
        return SubDAG2Executor.cvt(obj)
    raise Exception('layer only support DAG/Executor')


if __name__ == '__main__':
    layer = DAGLayerSwitchOneV2(loop_to=1.1)
    layer.add_branch(ExecutorDebug('1', hit_ret=False, hit_wait=0.2))
    layer.add_branch(ExecutorDebug('2', hit_ret=False, hit_wait=0.2))
    layer.add_branch(ExecutorDebug('3', hit_ret=True, hit_wait=0.1, exec_ret=False))
    ok = layer.run(Ctx())
    print(ok)
