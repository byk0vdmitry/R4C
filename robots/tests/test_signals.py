from django.core import mail
from django.test import TestCase
from customers.models import Customer

from robots.models import Robot
from orders.models import Order
from robots.signals import send_mail_to_customer, check_in_prod_robot

class RobotTest(TestCase):
    def setUp(self):
        # Create customers and orders for testing
        customer = Customer.objects.create(email='user1@example.com')
        customer2 = Customer.objects.create(email='user2@example.com')
        Order.objects.create(customer=customer, robot_serial='SE-23')
        Order.objects.create(customer=customer2, robot_serial='SE-26')
        Robot.objects.create(serial='SE-56', model='SE', version='56', created='2020-01-01')

    def test_create_mail_to_order(self):
        """
        Test case for sending mail to customer after creating an order.
        """
        robot = Robot(serial='SE-23', model='SE', version='23', created='2020-01-01')
        customer = Customer.objects.get(id=1)
        message = (
            f'Добрый день!\nНедавно вы интересовались нашим роботом модели {robot.model}, '
            f'версии {robot.version}.\nЭтот робот теперь в наличии. Если вам подходит '
            f'этот вариант - пожалуйста, свяжитесь с нами'
        )

        send_mail_to_customer(robot.serial, robot.model, robot.version, customer.email)

        # Assert that the mail was sent with the correct subject, body, and recipient
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Заказ на робота SE-23')
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].to, [customer.email])
        mail.outbox = []

    def test_check_in_prod_robot(self):
        """
        Test case for checking if a robot is in production and sending a mail to the customer if it is not.
        """
        prod_robot = Robot(serial='SE-56', model='SE', version='56', created='2020-01-01')
        customer = Customer.objects.get(id=2)

        check_in_prod_robot(sender=Robot, instance=prod_robot)

        # Assert that no mail was sent for a robot in production
        self.assertEqual(len(mail.outbox), 0)

        non_prod_robot = Robot(serial='SE-26', model='SE', version='26', created='2023-01-01')
        message = (
            f'Добрый день!\nНедавно вы интересовались нашим роботом модели {non_prod_robot.model}, '
            f'версии {non_prod_robot.version}.\nЭтот робот теперь в наличии. Если вам подходит '
            f'этот вариант - пожалуйста, свяжитесь с нами'
        )

        check_in_prod_robot(sender=Robot, instance=non_prod_robot)
        # Assert that a mail was sent for a non-production robot
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Заказ на робота SE-26')
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].to, [customer.email])
