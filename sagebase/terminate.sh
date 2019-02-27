#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#source $SCRIPT_DIR/utils.sh

export ANSIBLE_CONFIG=$ROOT_DIR/ansible.cfg
export ANSIBLE_INVENTORY=$ROOT_DIR/inventory/stage/ec2.py
export EC2_INI_PATH=$ROOT_DIR/inventory/stage/ec2.ini
export ANSIBLE_ROLES_PATH=$ROOT_DIR/roles

function run() {
    echo "==> Terminating cluster"
    ansible-playbook -i $ROOT_DIR/inventory/stage $ROOT_DIR/playbooks/provision/terminate.yml -vvv
    return 0
}

run "$@"
