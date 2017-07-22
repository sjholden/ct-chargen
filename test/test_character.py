import os
os.environ['BUCKET_NAME'] = 'a non-existant bucket' # an ugly hack to not call app_identity_service and fail when testing.

import unittest
import character

class Test(unittest.TestCase):
    def testSimpleCreation(self):
        char = character.Character(fixRolls=[1,1,6,6,3,4,5,4,2,3,4,4])
        self.assertEqual(char.stats, [2, 12, 7, 9, 5, 8])
        self.assertEqual(char.age, 18)
        self.assertEqual(char.career, None)
        self.assertEqual(char.terms, 0)
        self.assertEqual(char.skills, {})
        self.assertEqual(char.possessions, {})
        self.assertEqual(char.credits, 0)
        self.assertEqual(char.rank, 0)
