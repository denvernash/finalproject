import unittest
from build_database import *
from mapping import *
from nato import *

class TestDatabase(unittest.TestCase):

    def test_dog_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Dogs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Wookie',), result_list)
        self.assertEqual(('Harry',), result_list[100])
        self.assertEqual(len(result_list), 4166)


        sql = 'SELECT Name, Breed FROM Dogs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Delilah', 'Pug'), result_list)
        self.assertEqual(('Goku', 'Blue Lacy'), result_list[284])

    def test_breed_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT Breed FROM Breeds'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 234)
        self.assertEqual(('Borzoi',), result_list[39])
        self.assertEqual(('Whippet',), result_list[225])


        sql = 'SELECT Id, Breed_Group FROM Breeds'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual((101, 'Non-Sporting'), result_list[100])


        sql = 'SELECT Origin FROM Breeds'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(('Germany',), result_list[180])

    def test_shelter_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT Id, Name FROM Shelters'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(('MI138', 'WAG Animal Rescue'), result_list[100])
        self.assertEqual(len(result_list), 1790)

    def test_displays(self):
        self.assertEqual(len(DISPLAY_SHELTER_LIST), 1790)
        self.assertEqual(len(DISPLAY_DOG_LIST), 4166)
        self.assertEqual(len(DISPLAY_IMAGE_LIST), 234)
        self.assertEqual(len(DISPLAY_BREED_LIST), 234)
        self.assertEqual(DISPLAY_SHELTER_LIST[0].id, 'MI798')
        self.assertEqual(DISPLAY_DOG_LIST[0].id, 1949542)
        self.assertEqual(DISPLAY_IMAGE_LIST[0].id, 1)
        self.assertEqual(DISPLAY_BREED_LIST[0].breed, 'Affenpinscher')

if __name__ == '__main__':
    unittest.main()
