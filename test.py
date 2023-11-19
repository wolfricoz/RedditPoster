import unittest
from unittest.mock import patch, mock_open
from classes.config import Config
import os

class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.config = Config('test/config.json')

    def test_config_creation(self):
        self.config.create_config()
        self.assertTrue(os.path.exists('test/config.json'))

    def test_key_retrieval(self):
        self.config.config = {"key": "value"}
        self.assertEqual(self.config.get_key("key"), "value")

    def test_subreddit_addition(self):
        self.config.add_subreddit("test")
        self.assertIn("test", self.config.config["subreddits"])

    def test_subreddit_removal(self):
        self.config.add_subreddit("test")
        self.config.remove_subreddit("test")
        self.assertNotIn("test", self.config.config["subreddits"])

    def test_subreddit_update(self):
        self.config.add_subreddit("test")
        self.config.update_subreddit("test", "flair_name", "flair_id")
        self.assertEqual(self.config.config["subreddits"]["test"]["flair_name"], "flair_name")
        self.assertEqual(self.config.config["subreddits"]["test"]["flair_id"], "flair_id")

    def test_subreddit_renaming(self):
        self.config.add_subreddit("test")
        self.config.rename_subreddit("test", "new_test")
        self.assertNotIn("test", self.config.config["subreddits"])
        self.assertIn("new_test", self.config.config["subreddits"])

    def test_string_saving(self):
        self.config.save_string("key", "value")
        self.assertEqual(self.config.config["key"], "value")

    def test_integer_setting(self):
        self.config.set_int("key", 1)
        self.assertEqual(self.config.config["key"], 1)

if __name__ == '__main__':
    unittest.main()