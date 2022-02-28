import threading
import time
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

import pytz
from schedule import Scheduler

from menu.models import Menu


def get_menus_created_or_updated_in_last_day() -> list[str]:
    """Get menus names created or updated in last day"""
    current_day = date.today()
    previous_day = current_day - timedelta(days=1)
    current_day_as_datetime = datetime(current_day.year, current_day.month, current_day.day,
                                       tzinfo=pytz.UTC)
    previous_day_as_datetime = datetime(previous_day.year, previous_day.month, previous_day.day,
                                        tzinfo=pytz.UTC)
    menus_created_in_last_day = Menu.objects.filter(created__gte=previous_day_as_datetime,
                                                    created__lt=current_day_as_datetime) \
                                            .values_list('name', flat=True)
    menus_updated_in_last_day = Menu.objects.filter(updated__gte=previous_day_as_datetime,
                                                    updated__lt=current_day_as_datetime) \
                                            .values_list('name', flat=True)
    return list(menus_created_in_last_day | menus_updated_in_last_day)


def get_user_emails() -> list[str]:
    """Get user emails"""
    return list(get_user_model().objects.all().values_list('email', flat=True))


def send_update_mails() -> None:
    """Method for sending users mail with updated menus"""
    menus_created_or_updated_in_last_day = get_menus_created_or_updated_in_last_day()
    user_emails = get_user_emails()
    message_content = f'Hi,\n\nThose menus was created or updated in previous day: ' \
                      f'{list(menus_created_or_updated_in_last_day)}'
    send_mail('New or updated emails from yesterday', message_content, 'from_email@example.com',
              user_emails, fail_silently=True)


def run_continuously(self, interval: int = 1) -> threading.Thread:
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        """Monkey patch class to enable scheduler run on different thread"""
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler():
    """Method that starts scheduler"""
    scheduler = Scheduler()
    scheduler.every().day.at("10:00").do(send_update_mails)
    scheduler.run_continuously()
