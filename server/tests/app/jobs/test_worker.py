import sys
import unittest
from unittest.mock import patch
from server.db.models import Task, Result
sys.path.append('.')

from app.jobs import worker

class TestWorker(unittest.TestCase):
    def test_extract_numbers_positive_case(self):
        result = worker._extract_numbers(["+491234567890", "+491234567890", "+291234567891", "00491234567891"])
        self.assertEqual(result, ["+491234567890", "00491234567891"])
    
    def test_extract_numbers_empty_case(self):
        result = worker._extract_numbers([])
        self.assertEqual(result, [])
    
    def test_save_processed_numbers_positive_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.first.return_value = Task()
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = Result()
                        worker._save_processed_numbers("123", ["+491234567890", "00491234567891"])
                        mock_query.return_value.filter.return_value.first.return_value.save.assert_called_once()

    def test_save_processed_numbers_empty_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.first.return_value = Task()
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = None
                        worker._save_processed_numbers("123", ["+491234567890", "00491234567891"])
                        mock_query.return_value.filter.return_value.first.return_value.save.assert_not_called()

    def test_tasks_to_process_positive_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.limit.return_value = [Task()]
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = Result()
                        result = worker._tasks_to_process()
                        self.assertEqual(len(result), 1)

    def test_tasks_to_process_empty_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.limit.return_value = []
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = None
                        result = worker._tasks_to_process()
                        self.assertEqual(len(result), 0)

    def test_process_task_positive_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.first.return_value = Task()
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = Result()
                        # mock worker
                        with patch('app.jobs.worker._extract_numbers') as mock_extract_numbers:
                            mock_extract_numbers.return_value = ["+491234567890", "00491234567891"]
                            with patch('app.jobs.worker._save_processed_numbers') as mock_save_processed_numbers:
                                worker._process_task(Task())
                                mock_save_processed_numbers.assert_called_once()

    def test_process_task_empty_case(self):
        # mock db
        with patch('app.jobs.worker.db') as mock_db:
            # mock session
            with patch('app.jobs.worker.db.session') as mock_session:
                # mock task
                with patch('app.jobs.worker.db.session.query') as mock_query:
                    mock_query.return_value.filter.return_value.first.return_value = None
                    # mock result
                    with patch('app.jobs.worker.db.session.query') as mock_query:
                        mock_query.return_value.filter.return_value.first.return_value = None
                        # mock worker
                        with patch('app.jobs.worker._extract_numbers') as mock_extract_numbers:
                            mock_extract_numbers.return_value = ["+491234567890", "00491234567891"]
                            with patch('app.jobs.worker._save_processed_numbers') as mock_save_processed_numbers:
                                worker._process_task(Task())
                                mock_save_processed_numbers.assert_not_called()

if __name__ == '__main__':
    unittest.main()