from server import handle_presence_message
import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestServer(unittest.TestCase):

    err_dict = {
        'response': 400,
        'error': 'Bad Request'
    }
    ok_dict = {'response': 200, 'time': 1.1, 'alert': 'Guest is online'}

    def test_no_action(self):
        self.assertEqual(handle_presence_message(
            {'time': 1.1, 'user': {'account_name': 'Guest', 'status': 'online'}}), self.ok_dict)

    def test_wrong_action(self):
        self.assertEqual(handle_presence_message(
            {'action': 'Wrong', 'time': 1.1, 'user': {'account_name': 'Guest', 'status': 'online'}}), self.ok_dict)

    def test_no_time(self):
        self.assertEqual(handle_presence_message(
            {'action': 'presence', 'user': {'account_name': 'Guest', 'status': 'online'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(handle_presence_message(
            {'action': 'presence', 'time': 1.1}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(handle_presence_message(
            {'action': 'presence', 'time': 1.1, 'user': {'account_name': 'Guest', 'status': 'online'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
