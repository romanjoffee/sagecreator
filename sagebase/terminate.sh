#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${ROOT_DIR}/util.sh

export ANSIBLE_CONFIG=$ROOT_DIR/ansible.cfg
export ANSIBLE_INVENTORY=$ROOT_DIR/inventory/stage/ec2.py
export EC2_INI_PATH=$ROOT_DIR/inventory/stage/ec2.ini
export ANSIBLE_ROLES_PATH=$ROOT_DIR/roles

function parse_args() {
  while [[ $# -gt 0 ]]; do
    local var="$1"
    case "$var" in
      --service=*)
        service="${var##*=}"
        if [[ "$service" == "" ]]; then
          echo "service parameter value missing" $var
        fi
      ;;
    esac

    shift 1
  done
}

function run() {
    local service
    parse_args "$@"

    echo "...Terminating cluster..."
    ansible-playbook -i ${ROOT_DIR}/inventory/stage ${ROOT_DIR}/playbooks/provision/terminate.yml -e service=${service} -vvv
    return 0
}

run "$@"
