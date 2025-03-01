from typing import List
import os
import time
import logging
import signal
import platform
import threading
from django import db
from .models import SimpleTask
from .services import get_simpletask_models
from .simq import get_simq_client
from .settings import DJANGO_SIMPLETASK3_SIMQ_POP_TIMEOUT
from .settings import DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL
from .settings import DJANGO_SIMPLETASK3_TASK_WORKER_MAX_MAIN_LOOP_COUNTER

_logger = logging.getLogger(__name__)


class SimpleTaskServer(object):
    def __init__(self, models: List[SimpleTask]):
        self.models = models
        self.stop_flag = False
        self.sleep_seconds = 5
        self.workers = []

    def signal_setup(self):
        def _stop(*args, **kwargs):
            _logger.warning("django-simpletask3 got stop signal!")
            _logger.warning("django-simpletask3 wait for workers to stop...")
            self.sleep_seconds = 1
            self.stop_flag = True

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

    def serve_forever(self):
        # 启动超时任务回收工作线程
        worker = SimQTimeoutTaskRecoveryWorker(self)
        worker.start()
        self.workers.append(worker)
        # 启动丢失任务重新推送工作线程
        worker = SimQLostTaskRecoveryWorker(self)
        worker.start()
        self.workers.append(worker)
        # 启动异常任务工作线程
        for model in self.models:
            worker_number = model.get_worker_number()
            for index in range(worker_number):
                worker = SimpleTaskWorker(self, model, index)
                worker.start()
                self.workers.append(worker)
        _logger.info(
            "django-simpletask3 server main thread waiting for stop signals..."
        )
        while not self.stop_flag:
            try:
                time.sleep(self.sleep_seconds)
            except Exception:
                pass
        while True:
            print(".", end="", flush=True)
            wait_flag = False
            for worker in self.workers:
                if worker.is_alive():
                    wait_flag = True
                    break
            if wait_flag:
                time.sleep(1)
            else:
                break


class SimQTimeoutTaskRecoveryWorker(object):
    def __init__(self, server):
        self.server = server
        self.work_thread = None

    def start(self):
        _logger.info("django-simpletask3 start simq-timeout-task-recovery-worker...")
        self.work_thread = threading.Thread(target=self._main, daemon=True)
        self.work_thread.start()

    def join(self):
        if self.work_thread:
            self.work_thread.join()

    def is_alive(self):
        if self.work_thread:
            return self.work_thread.is_alive()
        else:
            return False

    def _main(self):
        while not self.server.stop_flag:
            try:
                self._main_loop()
            except Exception as error:
                _logger.exception(
                    "django-simpletask3 simq-timeout-task-recovery-worker main loop error: error=%s",
                    error,
                )
                time.sleep(1)

    def _main_loop(self):
        simq_client = get_simq_client()
        while not self.server.stop_flag:
            for i in range(
                int(DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL / 5)
            ):
                if self.server.stop_flag:
                    break
                time.sleep(5)
            if self.server.stop_flag:
                break
            _logger.info(
                "django-simpletask3 simq-timeout-task-recovery-worker start to do recovery."
            )
            simq_client.recovery()
            _logger.info(
                "django-simpletask3 simq-timeout-task-recovery-worker recovery done!"
            )


class SimpleTaskWorker(object):
    def __init__(self, server: SimpleTaskServer, model: SimpleTask, worker_index: int):
        self.server = server
        self.model = model
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name
        self.worker_index = worker_index
        self.channel = model.get_event_channel()
        self.work_thread = None
        self.error_counter = 0
        # 错误重试等待时间控制器
        self.error_wait_seconds_pointer = 0
        self.error_wait_seconds = list(range(1, 31)) + [30] * 30

    def start(self):
        _logger.info(
            "django-simpletask3 start task-worker: app_label=%s, model_name=%s, worker_index=%s",
            self.app_label,
            self.model_name,
            self.worker_index,
        )
        self.work_thread = threading.Thread(target=self._main, daemon=True)
        self.work_thread.start()

    def join(self):
        self.work_thread.join()

    def is_alive(self):
        return self.work_thread.is_alive()

    def get_worker_name(self):
        node = platform.node()
        process_id = os.getpid()
        thread_id = threading.current_thread().ident
        return f"django-simpletask3-server:{self.app_label}.{self.model_name}:{self.worker_index}:{node}:{process_id}:{thread_id}"

    def _main(self):
        # 开启主循环
        while not self.server.stop_flag:
            try:
                db.close_old_connections()
                self._main_loop()
            except Exception as error:
                self.error_counter += 1
                self.error_wait_seconds_pointer = (
                    self.error_wait_seconds_pointer + 1
                ) % len(self.error_wait_seconds)
                _logger.error(
                    "django-simpletask3-server-worker main loop error, wait for %s seconds and retry: app_label=%s, model_name=%s, worker_index=%s, error=%s",
                    self.error_wait_seconds[self.error_wait_seconds_pointer],
                    self.app_label,
                    self.model_name,
                    self.worker_index,
                    error,
                )
                try:
                    time.sleep(self.error_wait_seconds[self.error_wait_seconds_pointer])
                except Exception:
                    break

    def _main_loop(self):
        pop_empty_counter = 0
        simq_client = get_simq_client()
        _main_loop_counter = 0
        while not self.server.stop_flag:
            _main_loop_counter += 1
            if (
                _main_loop_counter
                > DJANGO_SIMPLETASK3_TASK_WORKER_MAX_MAIN_LOOP_COUNTER
            ):
                break
            msg = simq_client.pop(
                self.channel,
                worker=self.get_worker_name(),
                timeout=DJANGO_SIMPLETASK3_SIMQ_POP_TIMEOUT,
            )
            # 成功执行后，错误重试等待时间控制器复位
            if self.error_wait_seconds_pointer != 0:
                self.error_wait_seconds_pointer = 0
                _logger.error(
                    "django-simpletask3-server-worker main loop error recovered: app_label=%s, model_name=%s, worker_index=%s",
                    self.app_label,
                    self.model_name,
                    self.worker_index,
                )
            # 消息处理
            if not msg:
                # 没有取到消息，重新获取
                pop_empty_counter += 1
                if pop_empty_counter and pop_empty_counter % 60 == 0:
                    _logger.info(
                        "django-simpletask3 task-worker got NO task for a long time: app_label=%s, model_name=%s, worker_index=%s",
                        self.app_label,
                        self.model_name,
                        self.worker_index,
                    )
                continue
            pop_empty_counter = 0
            msgid = msg.get("id", None)
            if not msgid:
                # 获取格式非法的消息，记录错误日志，重新获取
                _logger.error(
                    "django-simpletask3 got a bad msg missing msg_id: app_label=%s, model_name=%s, worker_index=%s, msg=%s",
                    self.app_label,
                    self.model_name,
                    self.worker_index,
                    msg,
                )
                continue
            if self.server.stop_flag:
                # 如果已经要求停止服务，直接退回消息后直接退出
                simq_client.ret(msgid)
                continue
            task_id = msg.get("data", {}).get("id", None)
            if not task_id:
                # 获取格式非法的消息，记录错误日志，重新获取
                _logger.error(
                    "django-simpletask3 got a bad msg missing task_id: app_label=%s, model_name=%s, worker_index=%s, msg=%s",
                    self.app_label,
                    self.model_name,
                    self.worker_index,
                    msg,
                )
                continue
            try:
                obj: SimpleTask = self.model.objects.get(id=task_id)
            except Exception as error:
                # 获取到消息后，从数据库中获取任务实例失败
                # 再回退消息
                simq_client.ret(msgid)
                continue
            task_execute_result = obj.execute(
                worker=self,
                msg=msg,
                simq_client=simq_client,
            )
            simq_client.ack(msgid, result=task_execute_result)


class SimQLostTaskRecoveryWorker(object):
    def __init__(self, server: SimpleTaskServer):
        self.server = server
        self.work_thread = None

    def start(self):
        _logger.info("django-simpletask3 start simq-lost-task-recovery-worker...")
        self.work_thread = threading.Thread(target=self._main, daemon=True)
        self.work_thread.start()

    def join(self):
        self.work_thread.join()

    def is_alive(self):
        return self.work_thread.is_alive()

    def _main(self):
        while not self.server.stop_flag:
            try:
                db.close_old_connections()
                self._main_loop()
            except Exception as error:
                _logger.exception(
                    "django-simpletask3 simq-lost-task-recovery-worker main loop error: error=%s",
                    error,
                )
                time.sleep(1)

    def _main_loop(self):
        simq = get_simq_client()
        while not self.server.stop_flag:
            for i in range(
                int(DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL / 5)
            ):
                if self.server.stop_flag:
                    break
                time.sleep(5)
            if self.server.stop_flag:
                break
            _logger.info(
                "django-simpletask3 simq-lost-task-recovery-worker start to do recovery."
            )
            models = get_simpletask_models()
            for model in models:
                if self.server.stop_flag:
                    break
                tasks = model.get_maybe_lost_tasks()
                for task in tasks:
                    if self.server.stop_flag:
                        break
                    task_id = task.get_task_id()
                    # 查询不到任务信息，说明任务已经丢失
                    if not simq.query(task_id):
                        _logger.info(
                            "django-simpletask3 simq-lost-task-recovery-worker recovery a lost task: task_id=%s",
                            task_id,
                        )
                        task.push_to_event_queue()
            _logger.info(
                "django-simpletask3 simq-lost-task-recovery-worker recovery done!"
            )
