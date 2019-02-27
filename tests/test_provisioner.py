from unittest import TestCase, main
from unittest.mock import Mock

from sagecreator import Configurator
from sagecreator import Provisioner


class ProvisionerTestCase(TestCase):
    _configurator = None

    def setUp(self):
        self._configurator = Configurator()

    def test_provision_should_fail_if_aws_secret_undefined(self):
        self._configurator.get_properties = Mock(return_value={"aws_access_key": "abc"})
        provisioner = Provisioner(self._configurator)

        with self.assertRaises(ValueError) as context:
            provisioner.provision()
            self.assertTrue("Property aws_secret_key is undefined" in str(context))

    def test_provision_should_call_script(self):
        self._configurator.get_properties = Mock(
            return_value={"aws_access_key": "valid", "aws_secret_key": b'dGhlX2F3c19zZWNyZXRfa2V5', "default_private_key_file": "valid"})

        provisioner = Provisioner(self._configurator)
        provisioner._call_bootstrap_script = Mock(return_value=None)
        provisioner.provision()
        provisioner._call_bootstrap_script.assert_called_once()


if __name__ == '__main__':
    main()
