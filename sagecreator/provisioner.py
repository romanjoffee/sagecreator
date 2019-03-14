# !/usr/bin/python

import os
import subprocess
import base64


class Provisioner:

    def __init__(self, configurator):
        self._configurator = configurator

    def provision(self, service, instance_type, spot_price, cluster_size):
        props = self._configurator.get_properties()
        props.update({'service': service,
                      'instance_type': instance_type,
                      'spot_price': spot_price,
                      'cluster_size': cluster_size})
        private_key_file = self._get_private_key_file(props)
        current_env = self._get_env(props)
        self._call_bootstrap_script(props, private_key_file, current_env)

    def _call_bootstrap_script(self, props, private_key_file, current_env):
        rc = subprocess.call(
            ["{}/bootstrap.sh".format(self._configurator.get_root_path()),
             "--{}={}".format('private_key_file', private_key_file),
             "--{}={}".format('service', props.get('service')),
             "--{}={}".format('instance_type', props.get('instance_type')),
             "--{}={}".format('spot_price', props.get('spot_price')),
             "--{}={}".format('cluster_size', int(props.get('cluster_size')))], env=current_env)
        return rc

    def terminate(self, service):
        current_env = self._get_env(self._configurator.get_properties())
        rc = subprocess.call(["{}/terminate.sh".format(self._configurator.get_root_path()),
                              "--{}={}".format('service', service)], env=current_env)
        return rc

    def _get_env(self, props):
        current_env = os.environ.copy()
        current_env["AWS_ACCESS_KEY_ID"] = self.validate_and_get("aws_access_key", props)
        current_env["AWS_SECRET_ACCESS_KEY"] = base64.b64decode(self.validate_and_get("aws_secret_key", props)).decode("utf-8")
        return current_env

    def _get_private_key_file(self, props):
        if "private_key_file" in props:
            return props.get("private_key_file")
        return "{}/.ssh/{}".format(self._configurator.get_root_path(), self.validate_and_get("default_private_key_file_name", props))

    @staticmethod
    def validate_and_get(prop_name, props):
        if prop_name not in props:
            raise ValueError("Property {} is undefined".format(prop_name))
        return props.get(prop_name)
