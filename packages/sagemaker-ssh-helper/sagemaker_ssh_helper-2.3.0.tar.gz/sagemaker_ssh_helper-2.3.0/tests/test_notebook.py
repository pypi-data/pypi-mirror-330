from sagemaker_ssh_helper.manager import SSMManager
from sagemaker_ssh_helper.proxy import SSMProxy


def test_notebook_instance(request):
    notebook_instance = request.config.getini('sagemaker_notebook_instance')
    notebook_ids = SSMManager().get_notebook_instance_ids(notebook_instance, timeout_in_sec=300)
    if not notebook_ids:
        raise ValueError(f"No notebook instance found with name {notebook_instance}")
    studio_id = notebook_ids[0]

    with SSMProxy(17022) as ssm_proxy:
        ssm_proxy.connect_to_ssm_instance(studio_id)

        _ = ssm_proxy.run_command("apt-get install -q -y net-tools")

        services_running = ssm_proxy.run_command_with_output("netstat -nptl")  # noqa
        services_running = services_running.decode('latin1')

        python_version = ssm_proxy.run_command_with_output("/opt/conda/bin/python --version")
        python_version = python_version.decode('latin1')

    assert "0.0.0.0:22" in services_running

    assert "Python 3.8" in python_version
