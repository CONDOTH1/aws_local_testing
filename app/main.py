import boto3
from botocore.config import Config


def main() -> str | None:
    config = Config(
        region_name="eu-west-1"
    )

    client = boto3.client(
        "sqs",
        aws_access_key_id="id",
        aws_secret_access_key="secret",
        config=config,
        endpoint_url="http://localstack:4566"
    )

    queue = client.get_queue_url(
        QueueName='test',
    )

    messages = client.receive_message(
        QueueUrl=queue.get("QueueUrl"),
        MessageAttributeNames=['Author'],
        WaitTimeSeconds=5,
    )

    # Process messages by printing out body and optional author name
    if messages.get("Messages", None):
        for message in messages['Messages']:
            # Get the custom author message attribute if it was set
            author_text = ''
            if message.get("MessageAttributes", None):
                author_name = message.get("MessageAttributes").get('Author').get('StringValue')
                if author_name:
                    author_text = ' ({0})'.format(author_name)

            return_msg = 'Hello, {0}!{1}'.format(message.get("Body"), author_text)

            # Let the queue know that the message is processed
            client.delete_message(
                QueueUrl=queue.get("QueueUrl"),
                ReceiptHandle=message.get("ReceiptHandle")
            )
            return return_msg
