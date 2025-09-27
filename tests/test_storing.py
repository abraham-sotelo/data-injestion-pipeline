import unittest
from unittest.mock import patch, MagicMock
import json
from src.lambda_storing import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch("src.lambda_storing.table")
    def test_valid_message(self, mock_table):
        event = {
            "Records": [
                {
                    "body": json.dumps({"ts": "2025-09-25T12:00:00Z", "County": "Albany"}),
                    "messageId": "123",
                }
            ]
        }

        mock_table.put_item.return_value = {}

        result = lambda_handler(event, None)

        mock_table.put_item.assert_called_once()
        args, kwargs = mock_table.put_item.call_args
        item = kwargs["Item"]

        self.assertEqual(item["ts"], "2025-09-25T12:00:00Z")
        self.assertEqual(item["County"], "Albany")
        self.assertEqual(item["pk"], "EVT")
        self.assertIn("expires_at", item)
        self.assertIsInstance(item["expires_at"], int)
        self.assertEqual(result["statusCode"], 200)

    @patch("src.lambda_storing.table")
    def test_missing_ts(self, mock_table):
        event = {
            "Records": [
                {
                    "body": json.dumps({"County": "Albany"}),
                    "messageId": "124",
                }
            ]
        }

        with self.assertRaises(KeyError):  # ts is required
            lambda_handler(event, None)

    @patch("src.lambda_storing.table")
    def test_corrupt_json(self, mock_table):
        event = {
            "Records": [
                {"body": "{not-json}", "messageId": "125"}
            ]
        }

        # Should raise JSONDecodeError
        with self.assertRaises(json.JSONDecodeError):
            lambda_handler(event, None)

    @patch("src.lambda_storing.table")
    def test_dynamodb_failure(self, mock_table):
        event = {
            "Records": [
                {
                    "body": json.dumps({"ts": "2025-09-25T12:00:00Z", "County": "Albany"}),
                    "messageId": "126",
                }
            ]
        }

        mock_table.put_item.side_effect = Exception("Dynamo down")

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        # Still returns 200, but logs error

if __name__ == "__main__":
    unittest.main()
