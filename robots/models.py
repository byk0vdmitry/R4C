import re
from django.core.exceptions import ValidationError
from django.db import models


def validate_serial_length(value):
    """
    Validate the length of the serial number.
    """
    if len(value) != 5:
        raise ValidationError('Serial number must be exactly 5 characters long.')


def validate_serial_regex(value):
    """
    Validates a serial number format using a regular expression pattern.

    Args:
        value (str): The serial number to be validated.

    Raises:
        ValidationError: If the serial number format is invalid.
    """
    pattern = r'^..-..$'  # Define the regular expression pattern
    match = re.match(pattern, value)  # Check if the serial number matches the pattern
    if not match:
        raise ValidationError(
            'Invalid serial number format.'
            )  # Raise an exception if the format is invalid


def validate_model_length(value):
    """
    Validate the length of the model.
    """
    if len(value) != 2:
        raise ValidationError('Model must be exactly 2 characters long.')


def validate_version_length(value):
    """
    Validate the length of the version.
    """
    if len(value) != 2:
        raise ValidationError('Version must be exactly 2 characters long.')


class Robot(models.Model):
    """
    Represents a Robot model.
    """
    serial = models.CharField(max_length=5, validators=[validate_serial_length,
                                                        validate_serial_regex])
    model = models.CharField(max_length=2, validators=[validate_model_length])
    version = models.CharField(max_length=2, validators=[validate_version_length])
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Save the Robot object after validating fields.
        """
        self.full_clean()
        super().save(*args, **kwargs)
