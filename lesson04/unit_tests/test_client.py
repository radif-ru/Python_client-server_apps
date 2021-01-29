"""Unittest клиента"""
import time
import unittest
from client import create_new_presence, process_answer
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    this_time = time.time()

    out = create_new_presence()
    out[TIME] = this_time

    test_out = {
        ACTION: PRESENCE,
        TIME: this_time,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    def test_create_new_presence(self):
        self.assertEqual(self.out, self.test_out)

    def test_process_answer_res_200(self):
        self.assertEqual(process_answer({RESPONSE: 200}), '200 : OK')

    def test_process_answer_res_400(self):
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: 'Bad Request'}), f'400 : Bad Request')

    def test_process_answer_res_not(self):
        self.assertRaises(ValueError, process_answer, {})


if __name__ == '__main__':
    unittest.main()
