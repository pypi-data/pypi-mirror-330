import unittest
from unittest.mock import MagicMock
from typing import Dict, Any
from masterpiece import Composite
from masterpiece_plugin.hello_world import HelloWorld




class TestHelloWorldPlugin(unittest.TestCase):

    def setUp(self) -> None:
        """Set up the test environment."""
        self.app_mock = MagicMock(spec=Composite)  # Mock the Composite app
        self.app_mock.name = "TestApp"  # Mock the 'name' attribute of the app
        self.plugin = HelloWorld(name="TestPlugin", description="Test Hello World")

    def test_install_hello_world(self) -> None:
        """Test the install method when install_hello_world is True."""
        self.plugin.install_hello_world = True
        self.plugin.install(self.app_mock)

        # Assert that app.add() was called to add the HelloWorld object
        self.app_mock.add.assert_called_once()

    def test_install_hello_world_disabled(self) -> None:
        """Test the install method when install_hello_world is False."""
        self.plugin.install_hello_world = False
        self.plugin.install(self.app_mock)

        # Assert that app.add() was NOT called
        self.app_mock.add.assert_not_called()

    def test_to_dict(self) -> None:
        """Test the to_dict method."""
        expected_dict = {
            "_class": self.plugin.get_class_id(),  # Assuming get_class_id is properly defined
            "_version:": 0,
            self.plugin._HELLO_WORLD_KEY: {
                "description": "Test Hello World",
            },
        }
        result = self.plugin.to_dict()

        # Assert the returned dictionary matches the expected result
        self.assertEqual(result, expected_dict)

    def test_from_dict(self) -> None:
        """Test the from_dict method."""
        data: Dict[str, Any] = {
            self.plugin._HELLO_WORLD_KEY: {
                "description": "Updated Hello World",
            }
        }

        self.plugin.from_dict(data)

        # Assert that the description was updated correctly
        self.assertEqual(self.plugin.description, "Updated Hello World")

    def test_initialization(self) -> None:
        """Test the initialization of the HelloWorld plugin."""
        self.assertEqual(self.plugin.name, "TestPlugin")
        self.assertEqual(self.plugin.description, "Test Hello World")


if __name__ == "__main__":
    unittest.main()
