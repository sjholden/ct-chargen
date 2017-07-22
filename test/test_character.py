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
            
    def testEnlistment(self):
        """Test the enlistment rolls."""
        def nonOtherTest(career, enlistment, dm1stat, dm1num, dm2stat, dm2num):
            for dm1roll in self._getAll2DSums():
                dm1sum = sum(dm1roll)
                for dm2roll in self._getAll2DSums():
                    dm2sum = sum(dm2roll)
                    for enlistroll in self._getAll2DSums():
                        enlistsum = sum(enlistroll)
                        if dm1sum >= dm1num:
                            enlistsum += 1
                        if dm2sum >= dm2num:
                            enlistsum += 2
                        statrolls = [1,1,1,1,1,1,1,1,1,1,1,1]
                        statrolls[dm1stat*2:dm1stat*2+2] = dm1roll
                        statrolls[dm2stat*2:dm2stat*2+2] = dm2roll
                        char = character.Character(fixRolls=statrolls + enlistroll + [6] )
                        char.selectCareer(career)
                        if enlistsum >= enlistment:
                            self.assertEqual(char.career, career)
                        else:
                            self.assertEqual(char.career, character.OTHER)
        nonOtherTest(character.NAVY, 8, character.INT, 8, character.EDU, 9)
        nonOtherTest(character.MARINES, 9, character.INT, 8, character.STR, 8)
        nonOtherTest(character.ARMY, 5, character.DEX, 6, character.END, 5)
        nonOtherTest(character.SCOUTS, 7, character.INT, 6, character.STR, 8)
        nonOtherTest(character.MERCHANTS, 7, character.STR, 7, character.INT, 6)
        for enlistroll in self._getAll2DSums():
            char = character.Character(fixRolls=[1,1,1,1,1,1,1,1,1,1,1,1]+enlistroll+[1])
            char.selectCareer(character.OTHER)
            if sum(enlistroll) >= 3:
                self.assertEqual(char.career, character.OTHER)
            else:
                self.assertEqual(char.career, character.NAVY)

    def testSurvivalRolls(self):
        """Test the survival rolls."""
        for career, survival, dmstat, dmnum, in ((character.NAVY, 5, character.INT, 7),
                                                 (character.MARINES, 6, character.END, 8),
                                                 (character.ARMY, 5, character.EDU, 6),
                                                 (character.SCOUTS, 7, character.END, 9),
                                                 (character.MERCHANTS, 5, character.INT, 7),
                                                 (character.OTHER, 5, character.INT, 9)):
            for statroll in self._getAll2DSums():
                for survivalroll in self._getAll2DSums():
                    statrolls = [1,1,1,1,1,1,1,1,1,1,1,1]
                    statrolls[dmstat*2:dmstat*2+2] = statroll
                    char = character.Character(fixRolls=statrolls + [6,6] + survivalroll)
                    char.selectCareer(career)
                    survivalsum = sum(survivalroll)
                    if sum(statroll) >= dmnum:
                        survivalsum += 2
                    if survivalsum >= survival:
                        self.assertFalse(char.dead)
                    else:
                        self.assertTrue(char.dead)
    
    def _getAll2DSums(self):
        return [[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6]]
