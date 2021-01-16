from django.core.management import call_command

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

# Run task every hour
@periodic_task(run_every=(crontab(minute='*/60')), name='crawl_products')
def crawl_products():
    call_command('crawl')
    logger.info("Products scraped")

# obj = locals()['crawl_products']
# obj.run()