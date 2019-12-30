import celery
from celery.task import task


class BaseTask(celery.Task):
    pass


@task(name='tasks.reload_foreign_key', base=BaseTask)
def reload_foreign_key(model, pk):
    # CASCADE orders in respect to the related models
    pass
