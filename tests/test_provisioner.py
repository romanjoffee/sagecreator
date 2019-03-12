from unittest import TestCase, main
from unittest.mock import Mock

from sagecreator import Configurator
from sagecreator import Provisioner

import os


class ProvisionerTestCase(TestCase):
    _configurator = None

    def setUp(self):
        self._configurator = Configurator()

    def test_provision_should_fail_if_aws_secret_undefined(self):
        self._configurator.get_properties = Mock(return_value={"aws_access_key": "abc"})
        prov = Provisioner(self._configurator)

        with self.assertRaises(ValueError) as context:
            prov.provision("service", "t3.small", 0.2, 1)
            self.assertTrue("Property aws_secret_key is undefined" in str(context))

    def test_provision_should_call_script(self):
        mock_props = {"aws_access_key": "valid",
                      "aws_secret_key": b'dGhlX2F3c19zZWNyZXRfa2V5',
                      "default_private_key_file_name": "default.pem"}
        self._configurator.get_properties = Mock(return_value=mock_props)
        current_env = os.environ.copy()
        current_env["AWS_ACCESS_KEY_ID"] = "valid"
        current_env["AWS_SECRET_ACCESS_KEY"] = "the_aws_secret_key"

        prov = Provisioner(self._configurator)
        prov._call_bootstrap_script = Mock(return_value=None)
        prov.provision("service", "t3.small", 0.2, 1)
        mock_props.update({"service": "service", "instance_type": "t3.small", "spot_price": 0.2, "cluster_size": 1})
        prov._call_bootstrap_script.assert_called_once_with(mock_props, "{}/.ssh/{}".format(self._configurator.get_root_path(), "default.pem"),
                                                            current_env)


if __name__ == '__main__':
    main()
