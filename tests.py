import unittest

from hamcrest import assert_that, not_none, is_
import mock
from eurosms import EuroSms, sign_sms


class SmsApiTest(unittest.TestCase):
    def test_send(self):
        requests = mock.MagicMock()
        requests.get.return_value.content = 'ok|30405278\n'

        obj = EuroSms(id='1-TB672G', key='5^Af-8Ss', requests=requests)
        message_id = obj.send('John_Smith', '421988171819', 'Test message')
        assert_that(message_id, is_('30405278'))

        payload = {'action': 'send1SMSHTTP',
                   'i': '1-TB672G',
                   's': 'ffc3cd373ad',
                   'sender': 'John_Smith',
                   'number': '421988171819',
                   'msg': 'Test message'}
        target_url = 'http://as.eurosms.com/sms/Sender'
        requests.get.assert_called_once_with(target_url, params=payload)

    def test_validate(self):
        requests = mock.MagicMock()
        requests.get.return_value.content = 'ok|1'

        obj = EuroSms(id='1-TB672G', key='5^Af-8Ss', requests=requests)

        obj.validate(1)

        target_url = 'http://as.eurosms.com/sms/Sender'
        params = {'action': 'status1SMSHTTP', 'id': '1'}
        requests.get.assert_called_once_with(target_url, params=params)

    def test_sign(self):
        sign = sign_sms('5^Af-8Ss', '421988171819')
        assert_that(sign, is_('ffc3cd373ad'))
