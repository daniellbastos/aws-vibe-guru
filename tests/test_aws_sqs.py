import os
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError, NoCredentialsError

from aws_toolbelt.aws_sqs import create_sqs_connection, list_sqs_queues, read_aws_credentials


def test_read_credentials_from_environment_variables(env_vars):

    with patch.dict(os.environ, env_vars):
        credentials = read_aws_credentials()

        assert credentials["access_key"] == "test_access_key"
        assert credentials["secret_key"] == "test_secret_key"
        assert credentials["region"] == "us-east-1"


def test_read_credentials_from_environment_empty_environment():
    with patch.dict(os.environ, {}, clear=True):
        credentials = read_aws_credentials()

        assert credentials["access_key"] == ""
        assert credentials["secret_key"] == ""
        assert credentials["region"] == "us-east-1"


def test_create_connection_with_environment_variables(mocked_boto_client, mocked_read_credentials, env_vars):
    # Converter env_vars para o formato esperado pela função
    credentials = {
        "access_key": env_vars["AWS_ACCESS_KEY_ID"],
        "secret_key": env_vars["AWS_SECRET_ACCESS_KEY"],
        "region": env_vars["AWS_DEFAULT_REGION"]
    }
    mocked_read_credentials.return_value = credentials
    mock_client = Mock()
    mocked_boto_client.return_value = mock_client

    client = create_sqs_connection()

    assert client == mock_client
    mocked_boto_client.assert_called_once_with(
        "sqs",
        aws_access_key_id="test_access_key",
        aws_secret_access_key="test_secret_key",
        region_name="us-east-1"
    )


def test_create_connection_with_profile(mocked_boto_client, mocked_read_credentials, env_vars):
    mocked_read_credentials.return_value = env_vars
    mock_client = Mock()
    mocked_boto_client.return_value = mock_client

    client = create_sqs_connection(
        access_key="custom_access_key",
        secret_key="custom_secret_key",
        region="us-west-2"
    )

    assert client == mock_client
    mocked_boto_client.assert_called_once_with(
        "sqs",
        aws_access_key_id="custom_access_key",
        aws_secret_access_key="custom_secret_key",
        region_name="us-west-2"
    )



def test_list_queues_success(mocked_sqs_client_with_queues):
    sqs_client = mocked_sqs_client_with_queues
    queues = list_sqs_queues(sqs_client)

    assert len(queues) == 2
    assert queues[0]["name"] == "queue1"
    assert queues[0]["url"] == "https://sqs.us-east-1.amazonaws.com/123456789012/queue1"
    assert queues[0]["region"] == "us-east-1"
    assert queues[1]["name"] == "queue2"
    assert queues[1]["url"] == "https://sqs.us-east-1.amazonaws.com/123456789012/queue2"
    assert queues[1]["region"] == "us-east-1"

    mocked_sqs_client_with_queues.list_queues.assert_called_once_with(MaxResults=1000)

def test_list_queues_with_prefix(mocker):
    mock_client = mocker.Mock()
    mock_client.list_queues.return_value = {
        "QueueUrls": [
            "https://sqs.us-west-2.amazonaws.com/123456789012/prod-queue"
        ]
    }

    queues = list_sqs_queues(mock_client, queue_name_prefix="prod-")

    assert len(queues) == 1
    assert queues[0]["name"] == "prod-queue"
    assert queues[0]["region"] == "us-west-2"

    mock_client.list_queues.assert_called_once_with(
        MaxResults=1000,
        QueueNamePrefix="prod-"
    )
