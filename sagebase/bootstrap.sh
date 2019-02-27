#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#source $SCRIPT_DIR/utils.sh
NO_ERROR=0

export ANSIBLE_CONFIG=$ROOT_DIR/ansible.cfg
export ANSIBLE_INVENTORY=$ROOT_DIR/inventory/stage/ec2.py
export EC2_INI_PATH=$ROOT_DIR/inventory/stage/ec2.ini
export ANSIBLE_ROLES_PATH=$ROOT_DIR/roles

function provision() {
    local private_key_file=$1

    echo "...Provisioning cluster..."
    ansible-playbook --key-file $private_key_file -i $ROOT_DIR/inventory/stage $ROOT_DIR/playbooks/sage/aws_provision.yml #-vvv
    return $NO_ERROR
}

function install() {
    local private_key_file=$1

    echo "...Installing software..."
    ansible-playbook --key-file $private_key_file -i $ROOT_DIR/inventory/stage $ROOT_DIR/playbooks/sage/install.yml #-vvv
    return $NO_ERROR
}

function refresh_inventory() {
    echo "...Refreshing inventory..."
    local inventory_data=$(python $ROOT_DIR/inventory/stage/ec2.py --refresh-cache)
}

function run() {
    local private_key_file=$1

    provision $private_key_file
    refresh_inventory
    install $private_key_file

    return $NO_ERROR
}

run "$@"
