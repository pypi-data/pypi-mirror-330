import redis
from simqcore import SimQ
from .settings import DJANGO_SIMPLETASK3_SIMQ_REDIS_URL
from .settings import DJANGO_SIMPLETASK3_SIMQ_PREFIX
from .settings import DJANGO_SIMPLETASK3_SIMQ_ACK_EVENT_EXPIRE
from .settings import DJANGO_SIMPLETASK3_SIMQ_DONE_ITEM_EXPIRE
from .settings import DJANGO_SIMPLETASK3_SIMQ_WORKER_STATUS_EXPIRE
from .settings import DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT
from .settings import DJANGO_SIMPLETASK3_SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION
from .settings import DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES

_GLOBAL_SIMQ_CLIENT = {
    "simq_client": None,
    "redis_connection_pool": None,
    "redis_client": None,
}


def get_simq_client():
    if _GLOBAL_SIMQ_CLIENT["simq_client"]:
        return _GLOBAL_SIMQ_CLIENT["simq_client"]

    if not _GLOBAL_SIMQ_CLIENT["redis_connection_pool"]:
        _GLOBAL_SIMQ_CLIENT["redis_connection_pool"] = redis.ConnectionPool.from_url(
            DJANGO_SIMPLETASK3_SIMQ_REDIS_URL
        )

    if not _GLOBAL_SIMQ_CLIENT["redis_client"]:
        _GLOBAL_SIMQ_CLIENT["redis_client"] = redis.Redis(
            connection_pool=_GLOBAL_SIMQ_CLIENT["redis_connection_pool"]
        )

    if not _GLOBAL_SIMQ_CLIENT["simq_client"]:
        _GLOBAL_SIMQ_CLIENT["simq_client"] = SimQ(
            db=_GLOBAL_SIMQ_CLIENT["redis_client"],
            prefix=DJANGO_SIMPLETASK3_SIMQ_PREFIX,
            ack_event_expire=DJANGO_SIMPLETASK3_SIMQ_ACK_EVENT_EXPIRE,
            done_item_expire=DJANGO_SIMPLETASK3_SIMQ_DONE_ITEM_EXPIRE,
            worker_status_expire=DJANGO_SIMPLETASK3_SIMQ_WORKER_STATUS_EXPIRE,
            running_timeout=DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT,
            default_running_timeout_action=DJANGO_SIMPLETASK3_SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION,
            running_timeout_handler_policies=DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES,
        )

    return _GLOBAL_SIMQ_CLIENT["simq_client"]
