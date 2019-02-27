from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock

import yaml

import base64

from sagecreator import Configurator


class ConfiguratorTestCase(TestCase):
    _tests_dir = "tests/resources/"

    def test_persist_should_persist_config(self):
        configurator = Configurator()

        persist_path = Path("{}/config_persisted_mock.yml".format(self._tests_dir))

        configurator.get_config_path = Mock(return_value=str(persist_path))
        configurator.get_root_path = Mock(return_value=self._tests_dir)

        try:
            configurator.persist("the_aws_access_key", "the_aws_secret_key", "the_company", "owner", "service", "t3.micro", 0.5, 1, "")
            with open(str(persist_path), "r") as stream:
                config = yaml.load(stream)
            self.assertEqual("the_aws_access_key", config.get("aws_access_key"))
            self.assertEqual("the_aws_secret_key", base64.b64decode(config.get("aws_secret_key")).decode("utf-8"))
            self.assertEqual("the_company", config.get("company"))
            self.assertEqual(0.5, config.get("spot_price"))
            self.assertEqual(1, config.get("cluster_size"))
            self.assertEqual("t3.micro", config.get("instance_type"))
        finally:
            persist_path.unlink()
