#!/bin/bash

# A lifecycle configuration script for SageMaker Studio JupyterLab apps.
# See SageMaker_SSH_IDE.ipynb for manual configuration and for explanation of commands.
# See https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lifecycle-configurations.html .

# Replace with your JetBrains License Server host name
# OR keep it as is and put the value into ~/.sm-jb-license-server inside SageMaker Studio to override
JB_LICENSE_SERVER_HOST="jetbrains-license-server.example.com"

# Replace with your password
# OR keep it as is and populate ~/.vnc/passwd inside SageMaker Studio to override (see https://linux.die.net/man/1/vncpasswd ).
VNC_PASSWORD="123456"

# Replace with a local UserId that is returned by `aws sts get-caller-identity` command
# OR keep it as is and put the value into ~/.sm-ssh-owner inside SageMaker Studio to override
LOCAL_USER_ID="AIDACKCEVSQ6C2EXAMPLE:terry@SSO"

set -e
set -o pipefail

# If not root, execute as root via sudo
if [ "$EUID" -ne 0 ]; then
  SUDO="sudo"
  $SUDO true
  echo 'jupyterlab-lc-config.sh: INFO - Executing as root via sudo'
  exec $SUDO -E HOME=/root "$0" "$@"
  exit 0
fi

PYTHON_BIN=$(which python3 || which python)

if [ -f /opt/sagemaker-ssh-helper/.ssh-ide-configured ]; then
    echo 'jupyterlab-lc-config.sh: INFO - SageMaker SSH Helper is already installed, remove /opt/sagemaker-ssh-helper/.ssh-ide-configured to reinstall'
else
  $PYTHON_BIN -m pip uninstall -y -q awscli
  $PYTHON_BIN -m pip install -q sagemaker-ssh-helper

  # Uncomment lines below to update SageMaker SSH Helper to the latest dev version from the main branch
  # git clone https://github.com/aws-samples/sagemaker-ssh-helper.git /tmp/sm-ssh-src/ || echo 'Already cloned'
  # cd /tmp/sm-ssh-src/ && git pull --no-rebase && git clean -f && $PYTHON_BIN -m pip install .
fi

cd /root

# We assume that the kernels are is installed into the sys prefix, e.g. with ipykernel install --sys-prefix command
SYSTEM_PYTHON_PREFIX=$($PYTHON_BIN -c "from __future__ import print_function;import sys; print(sys.prefix)")
export JUPYTER_PATH="$SYSTEM_PYTHON_PREFIX/share/jupyter/"

export PATH="$PATH:$SYSTEM_PYTHON_PREFIX/bin"

sm-ssh-ide get-metadata
sm-ssh-ide env-diagnostics

# If already configured in the container, it will not take any effect:
sm-ssh-ide configure
#sm-ssh-ide configure --ssh-only

# NOTE: If NOT configuring with --ssh-only flag, make sure the instance has at least 8 GB of RAM for the desktop apps

# Useful only in combination with VNC (keep it default, if configuring with --ssh-only flag):
sm-ssh-ide set-jb-license-server "$JB_LICENSE_SERVER_HOST"

# If configured with --ssh-only flag, will not take any effect (safe to keep the default):
sm-ssh-ide set-vnc-password "$VNC_PASSWORD"

# (Optional) Uncomment to reset the local user ID and to override the value configured by the user:
# rm ~/.sm-ssh-owner 2>/dev/null || echo "OK. Local user not configured"

# Set the local user ID. Will not override the existing value, if already configured:
sm-ssh-ide set-local-user-id "$LOCAL_USER_ID"

sm-ssh-ide init-ssm

nohup sm-ssh-ide start &

nohup sm-ssh-ide ssm-agent &
