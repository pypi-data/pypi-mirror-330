import unittest
from tenzro_store import TenzroStore
import os
import shutil
import json
from threading import Thread
import time

class TestTenzroStore(unittest.TestCase):
    def setUp(self):
        self.store_dir = "test_store"
        self.follower_dir = "test_store_follower"
        self.store = TenzroStore(base_dir=self.store_dir, node_id="test")
        self.store.clear()  # Ensure a clean slate

    def tearDown(self):
        for directory in [self.store_dir, self.follower_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def test_put_and_get(self):
        """Test basic put and get operations."""
        data = {"transaction_id": "tx_123", "metadata": {"project": "test"}, "payload": {}}
        key = self.store.put("tx_123", data)
        self.assertEqual(key, "tx_123")
        retrieved = self.store.get("tx_123")
        self.assertEqual(retrieved, data)
        # Verify file exists
        self.assertTrue(os.path.exists(os.path.join(self.store_dir, "tx_123.tzds")))

    def test_get_nonexistent_key(self):
        """Test retrieving a key that doesn't exist."""
        self.assertIsNone(self.store.get("nonexistent"))

    def test_replicate(self):
        """Test data replication to a follower store."""
        data = {"transaction_id": "tx_456", "metadata": {"project": "replica"}}
        self.store.put("tx_456", data)
        self.store.replicate_to(self.follower_dir)
        follower = TenzroStore(base_dir=self.follower_dir, node_id="follower")
        replicated = follower.get("tx_456")
        self.assertEqual(replicated, data)
        # Verify replicated file exists
        self.assertTrue(os.path.exists(os.path.join(self.follower_dir, "tx_456.tzds")))

    def test_thread_safety(self):
        """Test concurrent put operations."""
        def store_data(store, key, data):
            time.sleep(0.1)  # Simulate concurrent access
            store.put(key, data)

        data1 = {"transaction_id": "tx_1", "value": 1}
        data2 = {"transaction_id": "tx_2", "value": 2}
        t1 = Thread(target=store_data, args=(self.store, "tx_1", data1))
        t2 = Thread(target=store_data, args=(self.store, "tx_2", data2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(self.store.get("tx_1"), data1)
        self.assertEqual(self.store.get("tx_2"), data2)

    def test_clear(self):
        """Test clearing the store."""
        data = {"transaction_id": "tx_789", "metadata": {"test": "clear"}}
        self.store.put("tx_789", data)
        self.store.clear()
        self.assertIsNone(self.store.get("tx_789"))
        self.assertFalse(os.path.exists(os.path.join(self.store_dir, "tx_789.tzds")))

    def test_load_existing(self):
        """Test loading existing .tzds files on initialization."""
        # Manually create a .tzds file
        filepath = os.path.join(self.store_dir, "tx_load.tzds")
        data = {"transaction_id": "tx_load", "test": "load"}
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        # Reinitialize store to load existing data
        new_store = TenzroStore(base_dir=self.store_dir, node_id="test")
        self.assertEqual(new_store.get("tx_load"), data)

if __name__ == "__main__":
    unittest.main()