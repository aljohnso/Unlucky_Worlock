import os
import Pitzer_Outdoor_Adventure as Main
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Main.app.config['DATABASE'] = tempfile.mkstemp()
        Main.app.config['TESTING'] = True
        self.app = Main.app.test_client()
        with Main.app.app_context():
            Main.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Main.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()