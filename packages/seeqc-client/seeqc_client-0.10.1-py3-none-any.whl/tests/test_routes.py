import unittest
from unittest.mock import patch

from seeqc_client import Client, Experiment
from .mocked_routes import VALID_PASSWORD, VALID_USERNAME, VALID_ACCESS, VALID_REFRESH, MockedAuthenticate, \
    MockedRefresh, MockedVersion, MockedEmulator, MockedQueue, MockedPendingStatus
from seeqc_client.tests.test_vars import QueueTestVars, EXPERIMENT_ID


class BaseCase(unittest.TestCase):
    """
    CLI Tests
    """
    def setUp(self):
        """Setup tests"""
        self.credentials = {'email': VALID_USERNAME, 'password': VALID_PASSWORD}
        self.client = Client()

    def tearDown(self) -> None:
        self.client.auth.access_token = None
        self.client.auth.refresh_token = None

    def test_post_good_emulator_request(self):
        """Test that a successful request can be made to an emulator backend"""
        with patch('requests.sessions.Session.post', MockedEmulator):
            response = self.client._run_emulator_request('seeqc_client/tests/test.qasm', '', 10)
        self.assertEqual(response.status_code, 200)

    def test_post_bad_emulator_request(self):
        """Test that a successful request can be made to an emulator backend"""
        with patch('requests.sessions.Session.post', MockedEmulator):
            response = self.client._run_emulator_request('seeqc_client/tests/bad_extension.qasm2', '', 10)
            self.assertEqual(response.status_code, 400)

    def test_get_experiments(self):
        """Check experiment queue get"""
        with patch('requests.sessions.Session.get', MockedQueue):
            data = self.client.get_experiments()
        self.assertEqual(data[0]['experiment_id'], QueueTestVars.experiment_id0)
        self.assertEqual(len(data), 5)

    def test_get_experiments_private(self):
        """Check experiment queue get private method"""
        with patch('requests.sessions.Session.get', MockedQueue):
            response = self.client._run_queue_request(start_index=0, end_index=20)
        self.assertEqual(response.status_code, 200)
        data = response.queue
        self.assertEqual(data[0]['experiment_id'], QueueTestVars.experiment_id0)
        self.assertEqual(len(data.keys()), 5)

    def test_get_experiments_short(self):
        """Check experiment queue with shortened queue"""
        with patch('requests.sessions.Session.get', MockedQueue):
            response = self.client._run_queue_request(start_index=1, end_index=3)
        self.assertEqual(response.status_code, 200)
        data = response.queue
        self.assertEqual(data[1]['experiment_id'], QueueTestVars.experiment_id1)
        self.assertFalse(QueueTestVars.experiment_id4 in data.keys())
        self.assertFalse(QueueTestVars.experiment_id0 in data.keys())
        self.assertEqual(len(data.keys()), 3)

    def test_get_experiments_too_long(self):
        """Test experiment queue fails when too many experiments requested"""
        with self.assertRaises(AssertionError):
            self.client.get_experiments(start_index=0, end_index=Client().max_queue_length+1)

    def test_get_experiments_bad_range(self):
        """Test experiment queue fails when indices are given in wrong order"""
        with self.assertRaises(AssertionError):
            self.client.get_experiments(start_index=10, end_index=0)

    def test_pending_get_status(self):
        """Test that when an experiment is found to be pending that the results are not fetched"""
        experiment = Experiment(uid=EXPERIMENT_ID, get_results=False)
        with patch('requests.sessions.Session.get', MockedPendingStatus), \
             patch('seeqc_client.Experiment._get_status') as mock_results:
            status = experiment._get_status()
            mock_results.assert_called_once()
            self.assertIsNotNone(status)

    def test_get_results(self):
        """Test that a results request is made as expected"""
        experiment = Experiment(uid=EXPERIMENT_ID, get_results=False)
        with patch('seeqc_client.Experiment._get_results_request') as mocked:
            experiment._get_results()
            mocked.assert_called_once()

    def test_cancel(self):
        experiment = Experiment(uid=EXPERIMENT_ID, get_results=False)
        with patch('seeqc_client.Experiment._post_cancel_request') as mock_cancel:
            experiment.cancel()
            mock_cancel.assert_called_once()

    def test_format_result(self):
        """Get experiment status response"""
        result = { "measurement_outcomes": { "0": 2, "1": 0 } }
        formatted = self.client._format_emulator_result(result)
        self.assertEqual(formatted, result)
