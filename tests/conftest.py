import pytest


@pytest.fixture()
def env_vars():
    return {
        "AWS_BEARER_TOKEN_BEDROCK_ACCESS_KEY": "test_access_key",
        "AWS_BEARER_TOKEN_BEDROCK_SECRET_KEY": "test_secret_key",
        "AWS_DEFAULT_REGION": "us-east-1",
    }


@pytest.fixture()
def mocked_boto_client(mocker):
    return mocker.patch("aws_toolbelt.aws_sqs.boto3.client")


@pytest.fixture()
def mocked_read_credentials(mocker):
    return mocker.patch("aws_toolbelt.aws_sqs.read_aws_credentials")


@pytest.fixture()
def mocked_sqs_client(mocker):
    return mocker.patch("aws_toolbelt.aws_sqs.create_sqs_connection")


@pytest.fixture()
def mocked_sqs_client_with_queues(mocker):
    mock_client = mocker.Mock()
    mock_client.list_queues.return_value = {
        "QueueUrls": [
            "https://sqs.us-east-1.amazonaws.com/123456789012/queue1",
            "https://sqs.us-east-1.amazonaws.com/123456789012/queue2",
        ]
    }
    return mock_client
