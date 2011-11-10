import unittest
import sqlite3 

import pygrametl
from pygrametl.tables import FactTable
#from pygrametl.datasources import SQLSource

def createTargetFact():
    return FactTable(name='target', keyrefs=['id'], measures=['value'])

class FactTableEnsureTest(unittest.TestCase):
    def setUp(self):
        con=sqlite3.connect(":memory:")
        cur=con.cursor()
        cur.execute('CREATE TABLE target\
                        ( id INT PRIMARY KEY\
                         ,value VARCHAR(200)\
                        )')

        self.records = [(1,'First Value'), 
                   (2,'Second Value')]
        pygcon = pygrametl.ConnectionWrapper(con)
        pygcon.setasdefault()
        self.connection = con
        self.fact = createTargetFact()
        
    def tearDown(self):
        self.connection.close()
    
    def testLookup(self):
        fact = self.fact
        res = fact.lookup({'id': -2, 'value': 'doesnt exist'})
        self.assertTrue(res is None, 'lookup should return None if match is not found')
    
    def testEnsure(self):
        """ checks that FactTable.ensure and lookup methods function properly """
        fact = self.fact
        for record in self.records:
            row = {'id': record[0], 'value': record[1]}
            fact.ensure(row)
            
            lookupRec=fact.lookup(row)        
            self.assertEqual(row['id'], lookupRec['id'], "Lookup didn't return correct record")
        

if __name__ == "__main__":
    unittest.main()