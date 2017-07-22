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

    def testDraft(self):
        """Test the draft rolls are correct."""
        for d, c in ((1, character.NAVY), (2,character.MARINES), (3, character.ARMY),
                  (4, character.SCOUTS), (5, character.MERCHANTS), (6, character.OTHER)):
            char = character.Character(fixRolls=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,d,6,6])
            char.selectCareer(character.NAVY)
            self.assertEqual(char.career, c)
