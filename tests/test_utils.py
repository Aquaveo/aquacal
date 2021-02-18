import datetime
import unittest
from unittest import mock

from requests import Response
from requests.exceptions import Timeout

from aquacal.utils import is_weekend, get_holidays


def mock_request_get(url):
    """Fake request.get function."""
    # Log a fake request for test output purposes
    print(f'Making a request to {url}.')
    print('Request received!')

    # Create a new Mock to imitate a Response
    mock_response = mock.MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        '12/25': 'Christmas',
        '7/4': 'Independence Day',
    }
    return mock_response


class TestUtils(unittest.TestCase):

    @mock.patch('aquacal.utils.datetime')
    def test_is_weekend__on_weekend(self, mock_datetime):
        """Test is_weekend on a weekend day."""
        # You can control the return value of a mocked function
        a_saturday = datetime.datetime(2021, 2, 13)
        mock_datetime.today.return_value = a_saturday

        ret = is_weekend()

        assert ret is True

    @mock.patch('aquacal.utils.datetime')
    def test_is_weekend__on_weekday(self, mock_datetime):
        """Test is_weekend on a weekday."""
        # You can control the return value of a mocked function
        a_monday = datetime.datetime(2021, 2, 15)
        mock_datetime.today.return_value = a_monday

        ret = is_weekend()

        assert ret is False

    @mock.patch('aquacal.utils.requests')
    def test_get_holidays__timeout(self, mock_request):
        """Test the get_holidays when the underlying request times out."""
        # When side_effect is set to an Exception, that exception
        # will be raised when the mock is called
        mock_request.get.side_effect = Timeout

        with self.assertRaises(Timeout):
            get_holidays()

    @mock.patch('aquacal.utils.requests')
    def test_get_holidays__successful(self, mock_request):
        """Test a successful request."""
        mock_request.get.side_effect = mock_request_get

        ret = get_holidays()

        assert ret['12/25'] == 'Christmas'

    @mock.patch('aquacal.utils.requests')
    def test_get_holidays__retry(self, mock_request):
        """Test a successful request after failed request with Timeout."""
        mock_response = mock.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            '12/25': 'Christmas',
            '7/4': 'Independence Day',
        }

        # The side_effect can be an iterable,
        # one side effect/return value for each expected call
        mock_request.get.side_effect = [Timeout, mock_response]

        # The first call should raise Timeout
        with self.assertRaises(Timeout):
            get_holidays()

        # The second call should return successfully
        ret = get_holidays()
        assert ret['7/4'] == 'Independence Day'

        # Verify get_holidays called twice
        assert mock_request.get.call_count == 2


