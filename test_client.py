from client import parse_server_response, create_presence_message
import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):

    def test_def_presense(self):
        account_name = 'Guest'
        test = create_presence_message(account_name=account_name)
        test['time'] = 1.1
        self.assertEqual(
            test, {'action': 'presence', 'time': 1.1, 'user': {'account_name': account_name, 'status': 'online'}})

    def test_200_ans(self):
        self.assertEqual(parse_server_response({'response': 200}), 200)

    def test_400_ans(self):
        self.assertEqual(parse_server_response(
            {'responce': 400, 'error': 'Bad Request'}), None)

    def test_no_response(self):
        self.assertEqual(parse_server_response({'response': None}), None)


if __name__ == '__main__':
    unittest.main()
