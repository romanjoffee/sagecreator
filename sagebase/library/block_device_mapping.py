#!/usr/bin/env python

EPHEMERAL_STORAGE_DEVICES = {
    'c1.medium': 1,
    'c1.xlarge': 4,
    'c3.large': 2,
    'c3.xlarge': 2,
    'c3.2xlarge': 2,
    'c3.4xlarge': 2,
    'c3.8xlarge': 2,
    'cc2.8xlarge': 4,
    'cg1.4xlarge': 2,
    'cr1.8xlarge': 2,
    'd2.xlarge': 3,
    'd2.2xlarge': 6,
    'd2.4xlarge': 12,
    'd2.8xlarge': 24,
    'g2.2xlarge': 1,
    'g2.8xlarge': 2,
    'hi1.4xlarge': 2,
    'hs1.8xlarge': 24,
    'i2.xlarge': 1,
    'i2.2xlarge': 2,
    'i2.4xlarge': 4,
    'i2.8xlarge': 8,
    'm1.small': 1,
    'm1.medium': 2,
    'm1.large': 2,
    'm1.xlarge': 4,
    'm2.xlarge': 1,
    'm2.2xlarge': 1,
    'm2.4xlarge': 2,
    'm3.medium': 1,
    'm3.large': 1,
    'm3.xlarge': 2,
    'm3.2xlarge': 2,
    'r3.large': 1,
    'r3.xlarge': 1,
    'r3.2xlarge': 1,
    'r3.4xlarge': 1,
    'r3.8xlarge': 2
}

DEVICE_SEQUENCE = 'bcdefghijklmnopqrstuvwxy'


class Application(object):
    def __init__(self, **kwargs):
        # Set all given parameters
        for key, val in kwargs.items():
            setattr(self, key, val)

    def get_ephemeral_block_mapping(self):
        bdm = {}
        device_map = {k: v for k, v in EPHEMERAL_STORAGE_DEVICES.items() if v > 1}

        if self.instance_type in device_map:
            for i in range(0, device_map[self.instance_type]):
                device = {'ephemeral_name': "ephemeral{0}".format(i)}
                bdm['/dev/sd{0}'.format(DEVICE_SEQUENCE[i])] = device
        return bdm

    def get_block_mapping_ansible(self):
        bdm = list()
        root_device = {
            'volume_type': self.root_volume_type,
            'volume_size': self.root_volume_size,
            'delete_on_termination': self.ebs_delete_on_termination
        }

        if self.os_type == 'debian':
            root_device['device_name'] = '/dev/xvda'
        elif self.os_type == 'ubuntu' or self.os_type == 'bionic':
            root_device['device_name'] = '/dev/sda1'

        bdm.append(root_device)
        for (k, v) in self.get_ephemeral_block_mapping().items():
            d = dict(device_name=k, ephemeral=v['ephemeral_name'])
            bdm.append(d)

        if self.ebs_create_volumes:
            device_count = len(bdm) - 1  # For zero-based index
            for vol_count in range(0, self.ebs_volume_count):
                d = dict(device_name=self.device_name(DEVICE_SEQUENCE[device_count]))
                d['volume_type'] = self.ebs_volume_type
                if self.ebs_volume_iops:
                    d['iops'] = self.ebs_volume_iops

                if self.ebs_volume_size:
                    d['volume_size'] = self.ebs_volume_size

                d['delete_on_termination'] = self.ebs_delete_on_termination
                device_count = device_count + 1
                bdm.append(d)

        return bdm

    def device_name(self, sequence_combination):
        if self.os_type == 'debian':
            return '/dev/xvd{}'.format(sequence_combination)
        elif self.os_type == 'ubuntu' or self.os_type == 'bionic':
            return '/dev/sd{}'.format(sequence_combination)

        raise Exception("Unknown OS type")


def run(argument_spec, argv):
    print(argv)
    from argparse import ArgumentParser

    ap = ArgumentParser(prog="block_device_mapping")

    for k, v in argument_spec.items():
        ap.add_argument("--{}".format(k), required=v['required'])

    args = ap.parse_args(argv)
    app = Application(instance_type=args.instance_type)
    print(json.dumps(app.get_ephemeral_block_mapping(), sort_keys=True, indent=4))
    print(json.dumps(app.get_block_mapping_ansible(), sort_keys=True, indent=4))


def ansible_run(argument_spec):
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    try:
        app = Application(
            module=module,
            **module.params
        )
        module.exit_json(changed=False, result=app.get_block_mapping_ansible())

    except Exception as e:
        module.fail_json(msg=str(e))


from ansible.module_utils.basic import *


def main():
    argument_spec = dict(
        instance_type=dict(required=True, type='str'),
        os_type=dict(required=True, type='str', choices=['debian', 'ubuntu', 'bionic']),
        root_volume_size=dict(required=False, type='str'),
        root_volume_type=dict(required=False, type='str', choices=['gp2', 'io1', 'standard'], default='standard'),
        ebs_create_volumes=dict(required=False, type='bool'),
        ebs_volume_count=dict(required=False, type='int'),
        ebs_volume_type=dict(required=False, type='str', choices=['gp2', 'io1', 'standard'], default='standard'),
        ebs_volume_size=dict(required=False, type='int'),
        ebs_volume_iops=dict(required=False, type='int'),
        ebs_delete_on_termination=dict(required=False, type='bool', default=True),
    )
    ansible_run(argument_spec)


if __name__ == '__main__':
    main()
