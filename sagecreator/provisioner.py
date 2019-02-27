# !/usr/bin/python

import os
import subprocess
import base64


class Provisioner:

    def __init__(self, configurator):
        self._configurator = configurator

    def provision(self):
        props = self._configurator.get_properties()
        private_key_file = self._get_private_key_file(props)
        current_env = self._get_env(props)
        self._call_bootstrap_script(private_key_file, current_env)

    def _call_bootstrap_script(self, private_key_file, current_env):
        rc = subprocess.call(["{}/bootstrap.sh".format(self._configurator.get_root_path()), private_key_file], env=current_env)
        return rc

    def terminate(self):
        current_env = self._get_env(self._configurator.get_properties())
        rc = subprocess.call(["{}/terminate.sh".format(self._configurator.get_root_path())], env=current_env)
        return rc

    def _get_env(self, props):
        current_env = os.environ.copy()
        current_env["AWS_ACCESS_KEY_ID"] = self.validate_and_get("aws_access_key", props)
        current_env["AWS_SECRET_ACCESS_KEY"] = base64.b64decode(self.validate_and_get("aws_secret_key", props)).decode("utf-8")
        return current_env

    def _get_private_key_file(self, props):
        if "private_key_file" in props:
            return props.get("private_key_file")
        return "{}/.ssh/{}".format(self._configurator.get_root_path(), self.validate_and_get("default_private_key_file", props))

    @staticmethod
    def validate_and_get(prop_name, props):
        if prop_name not in props:
            raise ValueError("Property {} is undefined".format(prop_name))
        return props.get(prop_name)
