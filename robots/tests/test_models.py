import datetime
from django.forms import ValidationError

from django.test import TestCase

from robots.models import Robot


class RobotTestCase(TestCase):
    """Test case for the Robot model"""

    def setUp(self):
        """Set up the test case by creating a Robot object"""
        Robot.objects.create(serial='R2-D2', model='R2', version='D2', created='2020-01-01')

    def test_serial(self):
        """Test the serial attribute of the Robot object"""
        robot = Robot.objects.get(id=1)
        self.assertEqual(robot.serial, 'R2-D2')

    def test_serial_max_length(self):
        """Test the max_length attribute of the serial field"""
        robot = Robot.objects.get(id=1)
        max_length = robot._meta.get_field('serial').max_length
        self.assertEqual(max_length, 5)

    def test_serial_validation(self):
        """Test the validation of the serial field"""
        with self.assertRaises(ValidationError):
            Robot.objects.create(serial='', model='R2', version='D2', created='2020-01-01')

        with self.assertRaises(ValidationError):
            Robot.objects.create(serial='1', model='R2', version='D2', created='2020-01-01')

        with self.assertRaises(ValidationError):
            Robot.objects.create(serial='12345', model='R2', version='D2', created='2020-01-01')

        with self.assertRaises(ValidationError):
            Robot.objects.create(serial='123456', model='R2', version='D2', created='2020-01-01')

    def test_serial_validatiors(self):
        """Test the validators of the serial field"""
        robot = Robot.objects.get(id=1)
        validators = robot._meta.get_field('serial').validators
        validator_list = ['validate_serial_length', 'validate_serial_regex']
        for validator in validator_list:
            self.assertIn(validator, str(validators))

    def test_model(self):
        """Test the model attribute of the Robot object"""
        robot = Robot.objects.get(id=1)
        self.assertEqual(robot.model, 'R2')

    def test_model_max_length(self):
        """Test the max_length attribute of the model field"""
        robot = Robot.objects.get(id=1)
        max_length = robot._meta.get_field('model').max_length
        self.assertEqual(max_length, 2)

    def test_model_validation(self):
        """Test the validation of the model field"""
        robot = Robot.objects.get(id=1)
        validators = robot._meta.get_field('model').validators
        validator_list = ['validate_model_length']
        for validator in validator_list:
            self.assertIn(validator, str(validators))

    def test_version(self):
        """Test the version attribute of the Robot object"""
        robot = Robot.objects.get(id=1)
        self.assertEqual(robot.version, 'D2')

    def test_version_max_length(self):
        """Test the max_length attribute of the version field"""
        robot = Robot.objects.get(id=1)
        max_length = robot._meta.get_field('version').max_length
        self.assertEqual(max_length, 2)

    def test_version_validation(self):
        """Test the validation of the version field"""
        robot = Robot.objects.get(id=1)
        validators = robot._meta.get_field('version').validators
        validator_list = ['validate_version_length']
        for validator in validator_list:
            self.assertIn(validator, str(validators))

    def test_created(self):
        """Test the created attribute of the Robot object"""
        robot = Robot.objects.get(id=1)
        print(robot.created)
        self.assertEqual(robot.created, datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
