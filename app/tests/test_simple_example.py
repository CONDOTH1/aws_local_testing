import unittest
import boto3
from botocore.config import Config
from app.main import main


class SimpleExampleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = Config(
            region_name="eu-west-1"
        )

        cls.client = boto3.client(
            "sqs",
            aws_access_key_id="id",
            aws_secret_access_key="secret",
            config=config,
            endpoint_url="http://localstack:4566"
        )
        queue = cls.client.create_queue(QueueName='test', Attributes={
            'DelaySeconds': '1'
        })
        cls.queue_url = queue.get("QueueUrl")

    def setUp(self) -> None:
        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody='world',
            MessageAttributes={
                'Author': {
                    "StringValue": "Winston",
                    'BinaryValue': b'bytes',
                    'StringListValues': [
                        'test',
                    ],
                    'BinaryListValues': [
                        b'bytes',
                    ],
                    'DataType': 'String'
                }
            },
        )

    def test_message_is_read(self):
        """
        Simple test
        """
        res = main()
        self.assertEqual(res, "Hello, world! (Winston)")

        messages = self.client.receive_message(
            QueueUrl=self.queue_url,
            WaitTimeSeconds=1,
        )
        has_messages = "Messages" in messages
        self.assertFalse(has_messages)


if __name__ == '__main__':
    unittest.main()
