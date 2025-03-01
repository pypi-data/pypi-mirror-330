import logging
import os
from datetime import timedelta
from pathlib import Path

import boto3
import pytest
import sagemaker
from sagemaker import Predictor
from sagemaker.djl_inference import DJLPredictor
from sagemaker.pytorch import PyTorch, PyTorchProcessor
from sagemaker.utils import name_from_base

from sagemaker_ssh_helper.log import SSHLog
from sagemaker_ssh_helper.wrapper import SSHEstimatorWrapper, SSHProcessorWrapper, SSHModelWrapper

import json


# noinspection DuplicatedCode
@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_train_placeholder_manual():
    bucket = sagemaker.Session().default_bucket()
    checkpoints_prefix = f"s3://{bucket}/checkpoints/"

    estimator = PyTorch(
        entry_point=os.path.basename('source_dir/training_placeholder/train_placeholder.py'),
        source_dir='source_dir/training_placeholder/',
        dependencies=[SSHEstimatorWrapper.dependency_dir()],  # <--NEW
        # (alternatively, add sagemaker_ssh_helper into requirements.txt
        # inside source dir) --
        base_job_name='ssh-training-manual',
        framework_version='1.9.1',
        py_version='py38',
        instance_count=1,
        instance_type='ml.g4dn.xlarge',
        max_run=60 * 60 * 3,
        keep_alive_period_in_seconds=1800,
        container_log_level=logging.INFO,
        checkpoint_s3_uri=checkpoints_prefix
    )

    ssh_wrapper = SSHEstimatorWrapper.create(estimator, connection_wait_time_seconds=0)  # <--NEW--

    estimator.fit(wait=False)

    ssh_wrapper.print_ssh_info()

    ssh_wrapper.wait_training_job()


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_processing_framework_manual():
    torch_processor = PyTorchProcessor(
        base_job_name='ssh-pytorch-processing-manual',
        framework_version='1.9.1',
        py_version='py38',
        instance_count=1,
        instance_type="ml.m5.xlarge",
        max_runtime_in_seconds=60 * 60 * 3,
    )

    wait_time = 3600

    ssh_wrapper = SSHProcessorWrapper.create(torch_processor, connection_wait_time_seconds=wait_time)

    torch_processor.run(
        source_dir="source_dir/processing/",
        dependencies=[SSHProcessorWrapper.dependency_dir()],
        code="process_framework.py",
        logs=True,
        wait=False
    )

    ssh_wrapper.print_ssh_info()

    ssh_wrapper.wait_processing_job()


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_inference_manual():
    estimator = PyTorch.attach("pytorch-training-2023-02-21-23-58-16-252")

    model = estimator.create_model(entry_point='inference_ssh.py',
                                   source_dir='source_dir/inference/',
                                   dependencies=[SSHModelWrapper.dependency_dir()])

    ssh_wrapper = SSHModelWrapper.create(model, connection_wait_time_seconds=0)

    endpoint_name = name_from_base('ssh-inference-manual')

    _: Predictor = model.deploy(initial_instance_count=1,
                                instance_type='ml.m5.xlarge',
                                endpoint_name=endpoint_name,
                                wait=True)

    ssh_wrapper.print_ssh_info()

    ssh_wrapper.wait_for_endpoint()


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_djl_inference():
    predictor = DJLPredictor("djl-inference-ssh-2023-05-15-16-26-57-895")
    data = {
        "inputs": [
            "Hello world!",
        ],
        "parameters": {
            "max_length": 200,
            "temperature": 0.1,
        },
    }
    result = predictor.predict(data)
    assert result == "42"


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_subprocess():
    import subprocess
    subprocess.check_call("uname -a".split(' '))
    logging.info("OK")


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_sns_publish(request):
    sns_notification_topic_arn = request.config.getini('sns_notification_topic_arn')
    logging.info(f"Send notification email and/or SMS through Amazon SNS topic {sns_notification_topic_arn}")
    sns_resource = boto3.resource('sns')
    sns_notification_topic = sns_resource.Topic(sns_notification_topic_arn)
    response = sns_notification_topic.publish(
        Subject='Manual test subject',
        Message='Manual test message'
    )
    logging.info(f"SNS response: {response}")


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_low_gpu_lambda():
    from sagemaker_ssh_helper.cdk.low_gpu.low_gpu_lambda import handler
    with open(str(Path('data/lambda/lambda_processing_event.json')), 'r') as f:
        event = f.read()
        event = json.loads(event)
    handler(event, None)


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_cloudwatch_metrics_sns(request):
    sns_notification_topic_arn = request.config.getini('sns_notification_topic_arn')
    topic_name = sns_notification_topic_arn.split(':')[-1]

    log = SSHLog()
    metrics_count = log.count_sns_notifications(topic_name, timedelta(minutes=15))
    logging.info(metrics_count)

    assert metrics_count > 0


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_can_attach_to_endpoint():
    boto3_session = boto3.session.Session(region_name="us-east-2")
    session = sagemaker.session.Session(boto_session=boto3_session)
    wrapper = SSHModelWrapper.attach('sd-inf2-ml-inf2-2023-11-07-13-33-05-254', session)
    assert 'sd-inf2-ml-inf2-2023-11-07-13-33-05-254' in wrapper.get_cloudwatch_url()
    assert wrapper.get_instance_id(timeout_in_sec=0) is not None


@pytest.mark.skipif(os.getenv('PYTEST_IGNORE_SKIPS', "false") == "false",
                    reason="Manual test")
def test_get_ssh_instance_timestamp():
    from sagemaker_ssh_helper.manager import SSMManager
    print(SSMManager().get_ssh_instance_timestamp('mi-0c5a1be17a45c83bf'))
