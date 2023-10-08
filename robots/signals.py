from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order

from .models import Robot


def send_mail_to_customer(serial, model, version, order_email):
    """
    Creates and sends an email notification to the customer about the availability of a robot.
    """
    subject = f'Заказ на робота {serial}'
    message = (
        f'Добрый день!\nНедавно вы интересовались нашим роботом модели {model}, '
        f'версии {version}.\nЭтот робот теперь в наличии. Если вам подходит '
        f'этот вариант - пожалуйста, свяжитесь с нами'
    )
    # Send an email notification to the customer
    send_mail(subject, message, 'test@mail.com', [order_email], fail_silently=False)


@receiver(pre_save, sender=Robot)
def check_in_prod_robot(sender, instance, **kwargs):
    """
    Signal handler that checks if a robot instance is a production robot
    and sends an email notification if it is.
    """
    serial = instance.serial
    model = instance.model
    version = instance.version

    # Get all production robots
    prod_robots = Robot.objects.all()

    # Get all orders
    orders = Order.objects.all()

    # Check if the robot instance is not in the list of production robots
    # and there are orders with the same serial number
    if instance not in prod_robots and orders.filter(robot_serial=serial).exists():
        # Get the email address of the customer who ordered a robot with the same serial number
        to_email = orders.filter(robot_serial=serial).values_list('customer__email', flat=True).first()

        # Create and send an email notification to the customer
        send_mail_to_customer(serial, model, version, to_email)
