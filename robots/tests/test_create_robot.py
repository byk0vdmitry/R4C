import json
from django.test import TestCase
from django.urls import reverse


class CreateRobotTestCase(TestCase):
    def test_request_get_create_robot(self):
        """
        Test GET request to create_robot endpoint.
        """
        url = 'create_robot'
        response = self.client.get(reverse(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"error": "Invalid request method"}')

    def test_request_post_valid_data_create_robot(self):
        """
        Test POST request with valid data to create_robot endpoint.
        """
        url = 'http://127.0.0.1:8000/robots/create_robot'
        data = {"model": "DD", "version": "GG", "created": "2023-10-06 15:59:59"}
        content_type = 'application/json'
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type=content_type)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['success'], 'Robot created')

    def test_request_post_invalid_data_create_robot(self):
        """
        Test POST request with invalid data to create_robot endpoint.
        """
        url = 'http://127.0.0.1:8000/robots/create_robot'
        data_list = [{"model": "DD", "version": "GG"},
                     {"model": "DD", "created": "2023-10-06 15:59:59"},
                     {"version": "GG", "created": "2023-10-06 15:59:59"},
                     {"version": "GG", "created": "2023-10-06 15:59:59"},
                     {"serial": "DD-GG", "model": "DD", "version": "GG", "created": "2023-10-06 15:59:59"},
                     ]
        content_type = 'application/json'
        for data in data_list:
            json_data = json.dumps(data)
            response = self.client.post(url, data=json_data, content_type=content_type)
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.content)
            self.assertEqual(response_data['error'], 'Invalid request data')

    def test_validation_error_create_robot(self):
        """
        Test POST request with validation error to create_robot endpoint.
        """
        url = 'http://127.0.0.1:8000/robots/create_robot'
        data = {"model": "Dcc", "version": "GGGg", "created": "2023-10 15:59:59"}
        content_type = 'application/json'
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type=content_type)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        expected_error_message = "Validation error: {'serial': ['Serial number must be exactly 5 characters long.', 'Invalid serial number format.', 'Ensure this value has at most 5 characters (it has 8).'], 'model': ['Model must be exactly 2 characters long.', 'Ensure this value has at most 2 characters (it has 3).'], 'version': ['Version must be exactly 2 characters long.', 'Ensure this value has at most 2 characters (it has 4).'], 'created': ['“2023-10 15:59:59” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.']}"
        self.assertEqual(response_data['error'], expected_error_message)
