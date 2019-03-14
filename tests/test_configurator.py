from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock

import yaml

import base64

from sagecreator import Configurator


class ConfiguratorTestCase(TestCase):
    _tests_dir = "tests/resources/"

    def test_should_persist_config(self):
        configurator = Configurator()

        persist_path = Path("{}/config_persisted_mock.yml".format(self._tests_dir))

        configurator.get_config_path = Mock(return_value=str(persist_path))
        configurator.get_root_path = Mock(return_value=self._tests_dir)
        try:
            configurator.persist("the_aws_access_key", "the_aws_secret_key", "the_company", "owner", key_pair_name="my key pair",
                                 private_key_file="/path/to/pkey")
            with open(str(persist_path), "r") as stream:
                config = yaml.safe_load(stream)
            self.assertEqual("the_aws_access_key", config.get("aws_access_key"))
            self.assertEqual("the_aws_secret_key", base64.b64decode(config.get("aws_secret_key")).decode("utf-8"))
            self.assertEqual("the_company", config.get("company"))
            self.assertEqual("my key pair", config.get("key_pair_name"))
            self.assertEqual("/path/to/pkey", config.get("private_key_file"))
        finally:
            persist_path.unlink()

    def test_should_load_persisted_properties(self):
        configurator = Configurator()

        persist_path = Path("{}/config_persisted_mock.yml".format(self._tests_dir))

        configurator.get_config_path = Mock(return_value=str(persist_path))
        configurator.get_root_path = Mock(return_value=self._tests_dir)
        try:
            configurator.persist("the_aws_access_key", "the_aws_secret_key", "the_company", "owner", key_pair_name="my key pair",
                                 private_key_file="/path/to/pkey")
            props = configurator.get_properties()
            self.assertEqual("the_aws_access_key", props.get("aws_access_key"))
            self.assertEqual("the_aws_secret_key", base64.b64decode(props.get("aws_secret_key")).decode("utf-8"))
            self.assertEqual("the_company", props.get("company"))
            self.assertEqual("/path/to/pkey", props.get("private_key_file"))
        finally:
            persist_path.unlink()

    def test_should_return_expected_config_path(self):
        configurator = Configurator()
        configurator.get_root_path = Mock(return_value=self._tests_dir)
        self.assertEqual("{}/inventory/stage/group_vars/all/{}".format(self._tests_dir, "config.yml"), configurator.get_config_path())

    def test_read_template_raises_error_if_file_doesnt_exist(self):
        configurator = Configurator()
        with self.assertRaises(ValueError) as test_context:
            configurator.get_root_path = Mock(return_value="bogus_dir")
            configurator.persist("the_aws_access_key", "the_aws_secret_key", "the_company", "owner", key_pair_name="my key pair",
                                 private_key_file="/path/to/pkey")
            self.assertEquals("Template file with default configuration settings could not be read", str(test_context.exception))
