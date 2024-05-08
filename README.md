# Localstack Example:


- To run: `docker-compose up --build --exit-code-from test-runner`

## What it does:

- Localstack image should be pulled and sqs provisioned
- Test runner should run `unittest` command
- Test setup should use boto3 client to create a queue and add a message
- Main test should call the main function which reads, process and delete message
- It asserts these are competed correctly
- Containers should shut down.

## Docs Referenced:

- https://docs.localstack.cloud/user-guide/aws/sqs/
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
- https://hub.docker.com/r/localstack/localstack