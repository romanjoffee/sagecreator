#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${ROOT_DIR}/util.sh
NO_ERROR=0

export ANSIBLE_CONFIG=${ROOT_DIR}/ansible.cfg
export ANSIBLE_INVENTORY=${ROOT_DIR}/inventory/stage/ec2.py
export EC2_INI_PATH=${ROOT_DIR}/inventory/stage/ec2.ini
export ANSIBLE_ROLES_PATH=${ROOT_DIR}/roles

function parse_args() {
  while [[ $# -gt 0 ]]; do
    local var="$1"
    case "$var" in
      --private_key_file=*)
        private_key_file="${var##*=}"
        if [[ "$private_key_file" == "" ]]; then
          echo "private_key_file parameter value missing" $var
        fi
      ;;

      --service=*)
        service="${var##*=}"
        if [[ "$service" == "" ]]; then
          echo "service parameter value missing" $var
        fi
      ;;

      --instance_type=*)
        instance_type="${var##*=}"
        if [[ "$instance_type" == "" ]]; then
          echo "instance_type parameter value missing" $var
        fi
      ;;

      --spot_price=*)
        spot_price="${var##*=}"
        if [[ "$spot_price" == "" ]]; then
          echo "spot_price parameter value missing" $var
        fi
      ;;

      --cluster_size=*)
        cluster_size="${var##*=}"
        if [[ "$cluster_size" == "" ]]; then
          echo "cluster_size parameter value missing" $var
        fi
      ;;
    esac

    shift 1
  done
}

function provision() {
    local private_key_file
    local service
    local instance_type
    local spot_price
    local cluster_size
    parse_args "$@"

    echo "...Provisioning cluster..."
    ansible-playbook --key-file ${private_key_file} -i ${ROOT_DIR}/inventory/stage ${ROOT_DIR}/playbooks/sage/aws_provision.yml -e service=${service} -e instance_type=${instance_type} -e spot_price=${spot_price} -e cluster_size=${cluster_size} #-vvv
    return $NO_ERROR
}

function install() {
    local private_key_file
    local service
    local "${@}"

    echo "...Installing software..."
    ansible-playbook --key-file ${private_key_file} -i ${ROOT_DIR}/inventory/stage ${ROOT_DIR}/playbooks/sage/install.yml -e service=${service} #-vvv
    return $NO_ERROR
}

function refresh_inventory() {
    echo "...Refreshing inventory..."
    local inventory_data=$(python $ROOT_DIR/inventory/stage/ec2.py --refresh-cache)
}

function run() {
    local private_key_file
    local service
    parse_args "$@"

    provision "$@"
    refresh_inventory
    install private_key_file=${private_key_file} service=${service}

    return $NO_ERROR
}

run "$@"
