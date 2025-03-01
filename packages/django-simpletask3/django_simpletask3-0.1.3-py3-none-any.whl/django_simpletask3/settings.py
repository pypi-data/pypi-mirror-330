import os
import django_environment_settings

DJANGO_SIMPLETASK3_EVENT_QUEUE_CHANNEL_TEMPLATE = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_EVENT_QUEUE_CHANNEL_TEMPLATE",
    "django-simpletask3:{app_label}.{model_name}",
)
DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE",
    "django-simpletask3:{app_label}.{model_name}:{id}",
)

DJANGO_SIMPLETASK3_SIMQ_REDIS_URL = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_REDIS_URL",
    os.environ.get("redis://localhost:6379/0"),
    aliases=[
        "DJANGO_SIMPLETASK3_SIMQ_REDIS",
        "SIMQ_REDIS_URL",
        "SIMQ_REDIS",
        "REDIS_URL",
        "REDIS",
    ],
)
DJANGO_SIMPLETASK3_SIMQ_PREFIX = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_PREFIX",
    "simq",
    aliases=["SIMQ_PREFIX"],
)
DJANGO_SIMPLETASK3_SIMQ_ACK_EVENT_EXPIRE = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_ACK_EVENT_EXPIRE",
    60 * 60 * 24,
    aliases=["SIMQ_ACK_EVENT_EXPIRE"],
)
DJANGO_SIMPLETASK3_SIMQ_DONE_ITEM_EXPIRE = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_DONE_ITEM_EXPIRE",
    60 * 60 * 24 * 7,
    aliases=["SIMQ_DONE_ITEM_EXPIRE"],
)
DJANGO_SIMPLETASK3_SIMQ_WORKER_STATUS_EXPIRE = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_WORKER_STATUS_EXPIRE",
    60 * 5,
    aliases=["SIMQ_WORKER_STATUS_EXPIRE"],
)
DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT",
    60 * 5,
    aliases=["SIMQ_RUNNING_TIMEOUT"],
)
DJANGO_SIMPLETASK3_SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION = (
    django_environment_settings.get(
        "DJANGO_SIMPLETASK3_SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION",
        "recover",
        aliases=["SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION"],
    )
)
DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES = (
    django_environment_settings.get(
        "DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES",
        None,
        aliases=["SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES"],
    )
)
DJANGO_SIMPLETASK3_SIMQ_POP_TIMEOUT = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_SIMQ_POP_TIMEOUT",
    5,
    aliases=["SIMQ_POP_TIMEOUT"],
)
DJANGO_SIMPLETASK3_DEFAULT_SIMQ_WORKER_NUMBER = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_DEFAULT_SIMQ_WORKER_NUMBER",
    5,
    aliases=["DEFAULT_SIMQ_WORKER_NUMBER"],
)
DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL = (
    django_environment_settings.get(
        "DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL",
        60 * 2,
        aliases=[
            "SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL",
        ],
    )
)
DJANGO_SIMPLETASK3_TASK_WORKER_MAX_MAIN_LOOP_COUNTER = django_environment_settings.get(
    "DJANGO_SIMPLETASK3_TASK_WORKER_MAX_MAIN_LOOP_COUNTER",
    1000,
)
