import unittest
import naukri


class Test(unittest.TestCase):
    def test_naukri(self):
        (status, driver) = naukri.naukriLogin(headless=True)
        naukri.tearDown(driver)
        self.assertFalse(status)


if __name__ == "__main__":
    unittest.main()
