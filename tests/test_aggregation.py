import unittest
import os
from unittest.mock import patch, MagicMock
from collections import Counter
from src.lambda_aggregation import lambda_handler


class TestAggregationLambda(unittest.TestCase):
    @patch.dict(os.environ, {"RAW_TABLE": "raw_test", "AGGREGATE_TABLE": "agg_test"})
    @patch("src.lambda_aggregation.dynamodb")
    def test_counts_and_writes_correctly(self, mock_dynamodb):
        # Fake DynamoDB query response
        mock_dynamodb.query.side_effect = [
            {
                "Items": [
                    {"county": {"S": "Albany"}},
                    {"county": {"S": "Albany"}},
                    {"county": {"S": "Saratoga"}},
                ],
                "LastEvaluatedKey": None,
            }
        ]
        mock_dynamodb.put_item.return_value = {}

        result = lambda_handler({}, None)

        # Verify DynamoDB.put_item was called
        mock_dynamodb.put_item.assert_called_once()
        put_item_args, put_item_kwargs = mock_dynamodb.put_item.call_args

        item = put_item_kwargs["Item"]

        # Check aggregate item content
        self.assertIn("updated", item)
        self.assertEqual(item["total_events"]["N"], "3")
        self.assertEqual(item["Albany"]["N"], "2")
        self.assertEqual(item["Saratoga"]["N"], "1")

        # Check lambda response
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"]["total_events"], 3)
        self.assertEqual(result["body"]["county_counts"], {"Albany": 2, "Saratoga": 1})


    @patch.dict(os.environ, {"RAW_TABLE": "raw_test", "AGGREGATE_TABLE": "agg_test"})
    @patch("src.lambda_aggregation.dynamodb")
    def test_no_items(self, mock_dynamodb):
        mock_dynamodb.query.return_value = {"Items": [], "LastEvaluatedKey": None}
        mock_dynamodb.put_item.return_value = {}

        result = lambda_handler({}, None)

        put_item_args, put_item_kwargs = mock_dynamodb.put_item.call_args
        item = put_item_kwargs["Item"]

        self.assertEqual(item["total_events"]["N"], "0")
        self.assertEqual(result["body"]["total_events"], 0)
        self.assertEqual(result["body"]["county_counts"], {})


    @patch.dict(os.environ, {"RAW_TABLE": "raw_test", "AGGREGATE_TABLE": "agg_test"})
    @patch("src.lambda_aggregation.dynamodb")
    def test_missing_county(self, mock_dynamodb):
        mock_dynamodb.query.return_value = {
            "Items": [
                {},  # no county attribute
                {"county": {"S": "Albany"}},
            ],
            "LastEvaluatedKey": None,
        }
        mock_dynamodb.put_item.return_value = {}

        result = lambda_handler({}, None)

        put_item_args, put_item_kwargs = mock_dynamodb.put_item.call_args
        item = put_item_kwargs["Item"]

        # Only Albany should be counted
        self.assertEqual(item["total_events"]["N"], "2")
        self.assertEqual(item["Albany"]["N"], "1")
        self.assertNotIn("UNKNOWN", item)  # you didn't default to UNKNOWN

        self.assertEqual(result["body"]["county_counts"], {"Albany": 1})


if __name__ == "__main__":
    unittest.main()
