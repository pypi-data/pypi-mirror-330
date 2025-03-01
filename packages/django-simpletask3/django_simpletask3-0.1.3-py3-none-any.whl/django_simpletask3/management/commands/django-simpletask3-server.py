import logging
import djclick as click
from django_simpletask3.services import get_simpletask_models
from django_simpletask3.server import SimpleTaskServer

_logger = logging.getLogger(__name__)


@click.command()
def server():
    _logger.info("django-simpletask3 server start...")
    models = get_simpletask_models()
    server = SimpleTaskServer(models)
    server.signal_setup()
    server.serve_forever()
