import unittest
from final import *
from nato import *

class TestDatabase(unittest.TestCase):

    def test_dog_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Dogs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Wookie',), result_list)
        self.assertEqual(len(result_list), 4166)


if __name__ == '__main__':
    unittest.main()
