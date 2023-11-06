from celery import shared_task


@shared_task
def order_created():
    message = 'Это задание Celery для отслеживания очереди!'
    return message