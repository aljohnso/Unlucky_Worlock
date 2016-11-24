import os
import PyCharmPOAProject
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, PyCharmPOAProject.app.config['DATABASE'] = tempfile.mkstemp()
        PyCharmPOAProject.app.config['TESTING'] = True
        self.app = PyCharmPOAProject.app.test_client()
        with PyCharmPOAProject.app.app_context():
            PyCharmPOAProject.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(PyCharmPOAProject.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()