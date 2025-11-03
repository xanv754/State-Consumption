import unittest
from unittest.mock import patch
from state_consumption.utils.configuration.env import Environment


class TestEnvironment(unittest.TestCase):
    """Tests for Environment configuration loader."""

    @patch("state_consumption.utils.configuration.env.path.exists", return_value=True)
    @patch("state_consumption.utils.configuration.env.dotenv_values")
    def test_loads_from_specified_env_files(self, mock_dotenv_values, mock_exists):
        """Should load variables from the specified env files when flags are set."""
        # Arrange
        mock_dotenv_values.side_effect = [
            {"KEY": "DEV"},
            {"KEY": "TEST"},
        ]

        # Act
        dev_env = Environment(dev=True)
        test_env = Environment(test=True)

        # Assert
        self.assertEqual(dev_env._get_env_var("KEY"), "DEV")
        self.assertEqual(test_env._get_env_var("KEY"), "TEST")
        self.assertEqual(mock_dotenv_values.call_count, 2)

    @patch("state_consumption.utils.configuration.env.path.exists", return_value=False)
    def test_raises_when_env_file_missing(self, mock_exists):
        """Should terminate when required env file is missing."""
        with self.assertRaises(SystemExit):
            Environment(prod=True)
        with self.assertRaises(SystemExit):
            Environment(dev=True)
        with self.assertRaises(SystemExit):
            Environment(test=True)

    def test_raises_when_no_flag_provided(self):
        """Should terminate when no environment flag provided."""
        with self.assertRaises(SystemExit):
            Environment()

    @patch("state_consumption.utils.configuration.env.path.exists", return_value=True)
    @patch("state_consumption.utils.configuration.env.dotenv_values", return_value={"MONGO_HOST": "localhost", "MONGO_PORT": "27017", "MONGO_DB": "db"})
    def test_parses_mongo_related_vars(self, mock_dotenv_values, mock_exists):
        """Should parse and expose mongo related env vars via _get_env_var."""
        env = Environment(test=True)
        self.assertEqual(env._get_env_var("MONGO_HOST"), "localhost")
        self.assertEqual(env._get_env_var("MONGO_PORT"), "27017")
        self.assertEqual(env._get_env_var("MONGO_DB"), "db")

    @patch("state_consumption.utils.configuration.env.path.exists", return_value=True)
    @patch("state_consumption.utils.configuration.env.dotenv_values", return_value={"TESTING": "true", "DB_NAME": "state_consumption_test"})
    def test_testing_flag_allows_test_specific_values(self, mock_dotenv_values, mock_exists):
        """Should allow reading testing-specific keys when test flag is set."""
        env = Environment(test=True)
        self.assertEqual(env._get_env_var("TESTING"), "true")
        self.assertEqual(env._get_env_var("DB_NAME"), "state_consumption_test")

    @patch("state_consumption.utils.configuration.env.path.exists", return_value=True)
    @patch("state_consumption.utils.configuration.env.dotenv_values", return_value={"ONLY_KEY": "value"})
    def test_missing_required_key_raises(self, mock_dotenv_values, mock_exists):
        """Should raise an explicit exception when accessing a missing key."""
        env = Environment(test=True)
        with self.assertRaises(Exception) as ctx:
            env._get_env_var("MISSING")
        self.assertIn("Variable 'MISSING' no declarada", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
