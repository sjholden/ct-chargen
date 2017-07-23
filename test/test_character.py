import os
os.environ['BUCKET_NAME'] = 'a non-existant bucket' # an ugly hack to not call app_identity_service and fail when testing.

import unittest
import character

class Test(unittest.TestCase):
    def testSimpleCreation(self):
        """Simple blank character test."""
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

    def testCommissionRolls(self):
        """Test the commission rolls."""
        for career, commission, dmstat, dmnum in ((character.NAVY, 10, character.SOC, 9),
                                                  (character.MARINES, 9, character.EDU, 7),
                                                  (character.ARMY, 5, character.END, 7),
                                                  (character.MERCHANTS, 4, character.INT, 6)):
            for statroll in self._getAll2DSums():
                for commissionroll in self._getAll2DSums():
                    statrolls = [1,1,1,1,1,1,1,1,1,1,1,1]
                    statrolls[dmstat*2:dmstat*2+2] = statroll
                    char = character.Character(fixRolls=statrolls + [6,6,6,6] + commissionroll + [1,1])
                    char.selectCareer(career)
                    commissionsum = sum(commissionroll)
                    if sum(statroll) >= dmnum:
                        commissionsum += 1
                    if commissionsum >= commission:
                        self.assertEqual(char.rank, 1)
                    else:
                        self.assertEqual(char.rank, 0)

    def testPromotionRolls(self):
        """Test the promotion rolls."""
        for career, promotion, dmstat, dmnum in ((character.NAVY, 8, character.EDU, 8),
                                                  (character.MARINES, 9, character.SOC, 8),
                                                  (character.ARMY, 6, character.EDU, 7),
                                                  (character.MERCHANTS, 10, character.INT, 9)):
            for statroll in self._getAll2DSums():
                for promotionroll in self._getAll2DSums():
                    statrolls = [1,1,1,1,1,1,1,1,1,1,1,1]
                    statrolls[dmstat*2:dmstat*2+2] = statroll
                    char = character.Character(fixRolls=statrolls + [6,6,6,6,6,6] + promotionroll)
                    char.selectCareer(career)
                    promotionsum = sum(promotionroll)
                    if sum(statroll) >= dmnum:
                        promotionsum += 1
                    if promotionsum >= promotion:
                        self.assertEqual(char.rank, 2)
                    else:
                        self.assertEqual(char.rank, 1)

    def testReenlist(self):
        """Test the reenlist rolls."""
        stats = [1,1,1,1,1,1,1,1,1,1,1,1]
        enlist = [6,6]
        survive = [6,6]
        commission= [1,1]
        twoskillrolls = [1,1]
        for career, reenlist in ((character.NAVY, 6), (character.MARINES, 6), (character.ARMY, 7),
                                 (character.SCOUTS, 3), (character.MERCHANTS, 4), (character.OTHER, 5)):
            for reenlistroll in self._getAll2DSums():
                rolls = stats + enlist + survive
                if career not in (character.SCOUTS, character.OTHER):
                    rolls = rolls + commission
                # try to reenlist
                char = character.Character(fixRolls=rolls+twoskillrolls+reenlistroll)
                char.selectCareer(career)
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('Yes')
                if sum(reenlistroll) >= reenlist:
                    self.assertEqual(char.terms, 2)
                else:
                    self.assertEqual(char.terms, 1)
                # try not to reenlist
                char = character.Character(fixRolls=rolls+twoskillrolls+reenlistroll)
                char.selectCareer(career)
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('No')
                if sum(reenlistroll) == 12:
                    self.assertEqual(char.terms, 2)
                else:
                    self.assertEqual(char.terms, 1)

    def testRanks(self):
        """Test rank progression."""
        stats = [1,1,1,1,1,1,1,1,1,1,1,1]
        enlist = [6,6]
        survive = [6,6]
        commission= [6,6]
        promotionno = [1,1]
        promotionyes = [6,6]
        skillroll = [1]
        aging = [6,6,6,6,6,6]
        rolls = (stats +
                 enlist + survive + commission + promotionno + skillroll*3 +
                 (enlist + survive + promotionyes + skillroll*2) * 2 +
                 (enlist + survive + promotionyes + skillroll*2 + aging) * 4)
        # do navy
        for career, ranks in ((character.NAVY, ('Ensign', 'Lieutenant', 'Lieutenant Commander', 'Commander', 'Captain', 'Admiral')),
                              (character.MARINES, ('Lieutenant', 'Captain', 'Force Commander', 'Lieutenant Colonel', 'Colonel', 'Brigadier')),
                              (character.ARMY, ('Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'General')),
                              (character.MERCHANTS, ('4th Officer', '3rd Officer', '2nd Officer', '1st Officer', 'Captain'))):            
            char = character.Character(fixRolls=rolls)
            char.selectCareer(career)
            # first term had an extra skill
            self.assertEqual(char.rank, 1)
            self.assertEqual(char.convertForClient()['rank'], ranks[0])
            char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
            char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
            char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
            # ither terms have skill for term plus promotion.
            for i in range(1, len(ranks)):
                char.selectReEnlist('Yes')
                self.assertEqual(char.rank, i+1)
                self.assertEqual(char.convertForClient()['rank'], ranks[i])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
            # make sure there's not an extra rank on the end.
            char.selectReEnlist('Yes')
            self.assertEqual(char.rank, len(ranks))
            self.assertEqual(char.convertForClient()['rank'], ranks[-1])

    def testMusteringOut(self):
        """Test the mustering out rolls."""
        stats = [1,1,1,1,1,1,1,1,1,1,1,1]
        enlist = [6,6]
        survive = [6,6]
        commission= [1,1]
        skillroll = [1]
        noenlist = [1,1]
        def checkBenefit(char, benefit):
            if benefit is None:
                self.assertEqual(char.stats, [5,2,2,2,2,2])
                self.assertEqual(len(char.possessions), 0)
            elif benefit == '+1 Intel':
                self.assertEqual(char.stats[character.INT], 3)
            elif benefit == '+2 Intel':
                self.assertEqual(char.stats[character.INT], 4)
            elif benefit == '+1 Educ':
                self.assertEqual(char.stats[character.EDU], 3)
            elif benefit == '+2 Educ':
                self.assertEqual(char.stats[character.EDU], 4)
            elif benefit == '+1 Social':
                self.assertEqual(char.stats[character.SOC], 3)
            elif benefit == '+2 Social':
                self.assertEqual(char.stats[character.SOC], 4)
            elif benefit == 'Blade':
                self.assertIn('Dagger', char.possessions)
            elif benefit == 'Gun':
                self.assertIn('Rifle', char.possessions)
            elif benefit == 'TAS':
                self.assertTrue(char.tasmember)
            elif benefit == 'Scout Ship':
                self.assertIn('Scout Ship (on loan)', char.possessions)
            elif benefit == 'Free Trader':
                self.assertIn('Free Trader (0 years paid off)', char.possessions)                
            else:
                self.assertIn(benefit, char.possessions)
        # generate two muster out rolls
        rolls = stats + enlist + survive + commission + skillroll*2 + enlist + survive + commission + skillroll + noenlist
        otherrolls = stats + enlist + survive + skillroll*2 + enlist + survive + skillroll + noenlist
        scoutrolls = stats + enlist + survive + skillroll*2 + enlist + survive + skillroll*2 + noenlist
        for career, benefits, cash in ((character.NAVY,
                                            ('Low Psg', '+1 Intel', '+2 Educ', 'Blade', 'TAS', 'High Psg', '+2 Social'),
                                            (1000, 5000, 5000, 10000, 20000, 50000, 50000)),
                                       (character.MARINES,
                                            ('Low Psg', '+2 Intel', '+1 Educ', 'Blade', 'TAS', 'High Psg', '+2 Social'),
                                            (2000, 5000, 5000, 10000, 20000, 30000, 40000)),
                                       (character.ARMY,
                                            ('Low Psg', '+1 Intel', '+2 Educ', 'Gun', 'High Psg', 'Mid Psg', '+1 Social'),
                                            (2000, 5000, 10000, 10000, 10000, 20000, 30000)),
                                       (character.SCOUTS,
                                            ('Low Psg', '+2 Intel', '+2 Educ', 'Blade', 'Gun', 'Scout Ship'),
                                            (20000, 20000, 30000, 30000, 50000, 50000, 50000)),
                                       (character.MERCHANTS,
                                            ('Low Psg', '+1 Intel', '+1 Educ', 'Gun', 'Blade', 'Low Psg', 'Free Trader'),
                                            (1000, 5000, 10000, 20000, 20000, 40000, 40000)),
                                       (character.OTHER,
                                            ('Low Psg', '+1 Intel', '+1 Educ', 'Gun', 'High Psg', None),
                                            (1000, 5000, 10000, 10000, 10000, 50000, 100000)),
                                       ):
            for i in range(6):
                if career == character.SCOUTS:
                    char = character.Character(fixRolls=scoutrolls+[i+1,i+1])
                elif career == character.OTHER:
                    char = character.Character(fixRolls=otherrolls+[i+1,i+1])
                else:
                    char = character.Character(fixRolls=rolls+[i+1,i+1])
                char.selectCareer(career)
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('Yes')
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                if career == character.SCOUTS:
                    char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('No')
                char.selectMusterTable('Cash')
                self.assertEqual(char.credits, cash[i])
                char.selectMusterTable('Benefits')
                if benefits[i] == 'Blade':
                    char.selectBladeBenefit('Dagger')
                elif benefits[i] == 'Gun':
                    char.selectGunBenefit('Rifle')
                checkBenefit(char, benefits[i])
                char.selectMusterTable('Cash')
                self.assertEqual(char.credits, cash[i])
            if career not in (character.SCOUTS, character.OTHER):
                for i in range(6):
                    char = character.Character(fixRolls=rolls+[i+1,i+1])
                    char.selectCareer(career)
                    char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                    char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                    char.selectReEnlist('Yes')
                    char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                    char.selectReEnlist('No')
                    # cheat rank to get +1 DM
                    char.rank = 5
                    char.selectMusterTable('Benefits')
                    if benefits[i+1] == 'Blade':
                        char.selectBladeBenefit('Dagger')
                    elif benefits[i] == 'Gun':
                        char.selectGunBenefit('Rifle')
                checkBenefit(char, benefits[i+1])
            for i in range(6):
                if career == character.SCOUTS:
                    char = character.Character(fixRolls=scoutrolls+[i+1,i+1])
                elif career == character.OTHER:
                    char = character.Character(fixRolls=otherrolls+[i+1,i+1])
                else:
                    char = character.Character(fixRolls=rolls+[i+1,i+1])
                char.selectCareer(career)
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('Yes')
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                if career == character.SCOUTS:
                    char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
                char.selectReEnlist('No')
                # cheat gambling skill to get +1 DM
                char.addSkill('Gambling')
                char.selectMusterTable('Cash')
                self.assertEqual(char.credits, cash[i+1])

    def testMusteringOutMultiples(self):
        """Test the blade and gun as skills, plus the paying off of the free trader."""
        stats = [1,1,1,1,1,1,1,1,1,1,1,1]
        enlist = [6,6]
        survive = [6,6]
        commission= [6,6]
        promotion = [6,6]
        skillroll = [1]
        noenlist = [1,1]
        aging = [6,6,6,6,6,6]
        rolls = (stats + enlist + survive + commission + promotion + skillroll*4 +
                 (enlist + survive + promotion + skillroll*2) * 2 +
                 (enlist + survive + promotion + skillroll*2 + aging) +
                 (enlist + survive + skillroll + aging) * 3 +
                 noenlist)
        char = character.Character(fixRolls=rolls+[4,4,3,3,6,6,6,6,6,6])
        char.selectCareer(character.MERCHANTS)
        for _ in range(4):
            char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
        char.selectReEnlist('Yes')
        for _ in range(6):
            for _ in range(2):
                char.selectSkillTable(character.SKILL_TABLE_NAMES[0])
            char.selectReEnlist('Yes')
        char.selectReEnlist('No')

        char.selectMusterTable('Benefits')
        char.selectBladeBenefit('Cutlass')
        self.assertEqual(char.possessions['Cutlass'], 1)
        char.selectMusterTable('Benefits')
        char.selectBladeBenefit('Cutlass (skill)')
        self.assertEqual(char.possessions['Cutlass'], 1)
        self.assertEqual(char.skills['Cutlass'], 1)
        char.selectMusterTable('Benfits')
        char.selectGunBenefit('Shotgun')
        self.assertEqual(char.possessions['Shotgun'], 1)
        char.selectMusterTable('Benfits')
        char.selectGunBenefit('Shotgun (skill)')
        self.assertEqual(char.possessions['Shotgun'], 1)
        self.assertEqual(char.skills['Shotgun'], 1)
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        char.selectMusterTable('Benfits')
        self.assertEqual(char.possessions['Free Trader (0 years paid off)'], 1)
        char.selectMusterTable('Benfits')
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        self.assertEqual(char.possessions['Free Trader (10 years paid off)'], 1)
        char.selectMusterTable('Benfits')
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (10 years paid off)', char.possessions)
        self.assertEqual(char.possessions['Free Trader (20 years paid off)'], 1)
        char.selectMusterTable('Benfits')
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (10 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (20 years paid off)', char.possessions)
        self.assertEqual(char.possessions['Free Trader (30 years paid off)'], 1)
        char.selectMusterTable('Benfits')
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (10 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (20 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (30 years paid off)', char.possessions)
        self.assertEqual(char.possessions['Free Trader (paid off)'], 1)
        char.selectMusterTable('Benfits')
        self.assertNotIn('Free Trader (0 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (10 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (20 years paid off)', char.possessions)
        self.assertNotIn('Free Trader (30 years paid off)', char.possessions)
        self.assertEqual(char.possessions['Free Trader (paid off)'], 1)

    def testSkillTables(self):
        """Test the skill tables."""
        stats = [4,4,4,4,4,4,4,4,4,4,4,4]
        self._checkSkillTable(character.NAVY, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', '+1 Intel', '+1 Educ', '+1 Social'], stats)
        self._checkSkillTable(character.NAVY, 'Service Skills', ["Ship's Boat", 'Vacc Suit', 'Forward Observer', 'Gunnery', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.NAVY, 'Advanced Education', ['Vacc Suit', 'Mechanical', 'Electronic', 'Engineering', 'Gunnery', 'Jack-of-all-Trades'], stats)
        self._checkSkillTable(character.NAVY, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin'], stats)
        self._checkSkillTable(character.MARINES, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', 'Gambling', 'Brawling', 'Blade Cbt'], stats)
        self._checkSkillTable(character.MARINES, 'Service Skills', ['Vehicle', 'Vacc Suit', 'Blade Cbt', 'Gun Cbt', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.MARINES, 'Advanced Education', ['Vehicle', 'Mechanical', 'Electronic', 'Tactics', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.MARINES, 'Advanced Education 2', ['Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin'], stats)
        self._checkSkillTable(character.ARMY, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', 'Gambling', '+1 Educ', 'Brawling'], stats)
        self._checkSkillTable(character.ARMY, 'Service Skills', ['Vehicle', 'Air/Raft', 'Gun Cbt', 'Forward Observer', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.ARMY, 'Advanced Education', ['Vehicle', 'Mechanical', 'Electronic', 'Tactics', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.ARMY, 'Advanced Education 2', ['Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin'], stats)
        self._checkSkillTable(character.SCOUTS, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', '+1 Intel', '+1 Educ', 'Gun Cbt'], stats)
        self._checkSkillTable(character.SCOUTS, 'Service Skills', ['Vehicle', 'Vacc Suit', 'Mechanical', 'Navigation', 'Electronics', 'Jack-of-all-Trades'], stats)
        self._checkSkillTable(character.SCOUTS, 'Advanced Education', ['Vehicle', 'Mechanical', 'Electronic', 'Jack-of-all-Trades', 'Gunnery', 'Medical'], stats)
        self._checkSkillTable(character.SCOUTS, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Jack-of-all-Trades'], stats)
        self._checkSkillTable(character.MERCHANTS, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', '+1 Stren', 'Blade Cbt', 'Bribery'], stats)
        self._checkSkillTable(character.MERCHANTS, 'Service Skills', ['Vehicle', 'Vacc Suit', 'Jack-of-all-Trades', 'Steward', 'Electronic', 'Gun Cbt'], stats)
        self._checkSkillTable(character.MERCHANTS, 'Advanced Education', ['Streetwise', 'Mechanical', 'Electronic', 'Navigation', 'Gunnery', 'Medical'], stats)
        self._checkSkillTable(character.MERCHANTS, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin'], stats)
        self._checkSkillTable(character.OTHER, 'Personal Development', ['+1 Stren', '+1 Dext', '+1 Endur', 'Blade Cbt', 'Brawling', '-1 Social'], stats)
        self._checkSkillTable(character.OTHER, 'Service Skills', ['Vehicle', 'Gambling', 'Brawling', 'Bribery', 'Blade Cbt', 'Gun Cbt'], stats)
        self._checkSkillTable(character.OTHER, 'Advanced Education', ['Streetwise', 'Mechanical', 'Electronic', 'Gambling', 'Brawling', 'Forgery'], stats)
        self._checkSkillTable(character.OTHER, 'Advanced Education 2', ['Medical', 'Forgery', 'Electronics', 'Computer', 'Streetwise', 'Jack-of-all-Trades'], stats)

    def testAdvancedEducaton2Cutoff(self):
        """Test that Advanced Education 2 only works at EDU 8+."""
        for statroll in self._getAll2DSums():
            stats = statroll * 6
            if sum(statroll) < 8:
                self._checkSkillTable(character.NAVY, 'Advanced Education 2', ['Vacc Suit', 'Mechanical', 'Electronic', 'Engineering', 'Gunnery', 'Jack-of-all-Trades'], stats)
                self._checkSkillTable(character.MARINES, 'Advanced Education 2', ['Vehicle', 'Mechanical', 'Electronic', 'Tactics', 'Blade Cbt', 'Gun Cbt'], stats)
                self._checkSkillTable(character.ARMY, 'Advanced Education 2', ['Vehicle', 'Mechanical', 'Electronic', 'Tactics', 'Blade Cbt', 'Gun Cbt'], stats)
                self._checkSkillTable(character.SCOUTS, 'Advanced Education 2', ['Vehicle', 'Mechanical', 'Electronic', 'Jack-of-all-Trades', 'Gunnery', 'Medical'], stats)
                self._checkSkillTable(character.MERCHANTS, 'Advanced Education 2', ['Streetwise', 'Mechanical', 'Electronic', 'Navigation', 'Gunnery', 'Medical'], stats)
                self._checkSkillTable(character.OTHER, 'Advanced Education 2', ['Streetwise', 'Mechanical', 'Electronic', 'Gambling', 'Brawling', 'Forgery'], stats)
            else:
                self._checkSkillTable(character.NAVY, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin'], stats)
                self._checkSkillTable(character.MARINES, 'Advanced Education 2', ['Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin'], stats)
                self._checkSkillTable(character.ARMY, 'Advanced Education 2', ['Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin'], stats)
                self._checkSkillTable(character.SCOUTS, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Jack-of-all-Trades'], stats)
                self._checkSkillTable(character.MERCHANTS, 'Advanced Education 2', ['Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin'], stats)
                self._checkSkillTable(character.OTHER, 'Advanced Education 2', ['Medical', 'Forgery', 'Electronics', 'Computer', 'Streetwise', 'Jack-of-all-Trades'], stats)

    def testRankAndServiceSkillsNavy(self):
        """Test the rank and service skills for Navy."""
        char = character.Character(fixRolls=[6]*100)
        char.selectCareer(character.NAVY)
        for _ in range(4):
            char.selectSkillTable('Advanced Education 2')
        for _ in range(3):
            char.selectReEnlist('Yes')
            char.selectSkillTable('Advanced Education 2')
            char.selectSkillTable('Advanced Education 2')
        self.assertEqual(char.stats[character.SOC], 13)
        char.selectReEnlist('Yes')
        self.assertEqual(char.stats[character.SOC], 14)

    def testRankAndServiceSkillsMarine(self):
        char = character.Character(fixRolls=[1,1]*6+[6,6, 6,6, 1,1, 1,1, 6,6, 6,6, 6,6, 1,1])
        char.selectCareer(character.MARINES)
        self.assertEqual(char.skills['Cutlass'], 1)
        self.assertNotIn('Revolver', char.skills)
        char.selectSkillTable('Personal Development')
        char.selectSkillTable('Personal Development')
        char.selectReEnlist('Yes')
        self.assertEqual(char.skills['Revolver'], 1)

    def testRankAndServiceSkillsArmy(self):
        char = character.Character(fixRolls=[1,1]*6+[6,6, 6,6, 1,1, 1,1, 6,6, 6,6, 6,6, 1,1])
        char.selectCareer(character.ARMY)
        self.assertEqual(char.skills['Rifle'], 1)
        self.assertNotIn('SMG', char.skills)
        char.selectSkillTable('Personal Development')
        char.selectSkillTable('Personal Development')
        char.selectReEnlist('Yes')
        self.assertEqual(char.skills['SMG'], 1)

    def testRankAndServiceSkillsScout(self):
        """Test the scout tank and service skills."""
        char = character.Character(fixRolls=[1,1]*6+[6,6]+[6,6])
        char.selectCareer(character.SCOUTS)
        self.assertEqual(char.skills['Pilot'], 1)

    def testBladeOptions(self):
        """Test the blade options for skills and benefits."""
        blades = ['Dagger', 'Blade', 'Foil', 'Sword', 'Cutlass', 'Broadsword', 'Bayonet', 'Spear', 'Halberd', 'Pike', 'Cudgel']
        rolls = [6,6]*6 + [6,6, 6,6, 6,6, 1,1, 1,5,5, 1,1, 4,4]
        for blade in blades:
            char = character.Character(fixRolls=rolls)
            char.selectCareer(character.NAVY)
            char.selectSkillTable('Personal Development')
            char.selectSkillTable('Service Skills')
            char.selectBladeSkillTable(blade)
            self.assertEqual(char.skills[blade], 1)
            char.selectSkillTable('Service Skills')
            char.selectBladeSkillTable(blade)
            self.assertEqual(char.skills[blade], 2)
            char.selectReEnlist('No')
            char.selectMusterTable('Benefits')
            char.selectBladeBenefit(blade)
            self.assertEqual(char.possessions[blade], 1)
            char.selectMusterTable('Benfits')
            char.selectBladeBenefit(blade + ' (skill)')
            self.assertEqual(char.skills[blade], 3)

    def testGunOptions(self):
        """Test the gun options for skills and benefits."""
        guns = ['Body Pistol', 'Auto Pistol', 'Revolver', 'Carbine', 'Rifle', 'Auto Rifle', 'Shotgun', 'SMG', 'Laser Carbine', 'Laser Rifle']
        rolls = [6,6]*6 + [6,6, 6,6, 6,6, 1,1, 1,6,6, 1,1, 4,4]
        for gun in guns:
            char = character.Character(fixRolls=rolls)
            char.selectCareer(character.MERCHANTS)
            char.selectSkillTable('Personal Development')
            char.selectSkillTable('Service Skills')
            char.selectGunSkillTable(gun)
            self.assertEqual(char.skills[gun], 1)
            char.selectSkillTable('Service Skills')
            char.selectGunSkillTable(gun)
            self.assertEqual(char.skills[gun], 2)
            char.selectReEnlist('No')
            char.selectMusterTable('Benefits')
            char.selectGunBenefit(gun)
            self.assertEqual(char.possessions[gun], 1)
            char.selectMusterTable('Benfits')
            char.selectGunBenefit(gun + ' (skill)')
            self.assertEqual(char.skills[gun], 3)
            
    def testVehicleOptions(self):
        """Test the vehicle options for skills."""
        vehicles = ['Ground Car', 'ATV', 'Sail Boat', 'Motor Boat', 'Submersible', 'Fixed Wing Aircraft', 'Helicopter', 'Hovercraft', 'Air/Raft', 'Grav Belt']
        rolls = [6,6]*6 + [6,6, 6,6, 1,1, 1,1]
        for vehicle in vehicles:
            char = character.Character(fixRolls=rolls)
            char.selectCareer(character.MERCHANTS)
            char.selectSkillTable('Service Skills')
            char.selectVehicleSkillTable(vehicle)
            self.assertEqual(char.skills[vehicle], 1)
            char.selectSkillTable('Service Skills')
            char.selectVehicleSkillTable(vehicle)
            self.assertEqual(char.skills[vehicle], 2)

            
    def _checkSkillTable(self, career, tablename, expected, statRolls):
        """Check the results for one skill table."""
        rolls = statRolls + [6,6,6,6]
        stats = [statRolls[i]+statRolls[i+1] for i in range(0,12,2)]
        if career not in (character.SCOUTS, character.OTHER):
            rolls = rolls + [1,1]
        for choices in ([1,2], [3,4], [5,6]):
            char = character.Character(fixRolls=rolls+choices)
            char.selectCareer(career)
            for choice in choices:
                previousSkill = char.skills.get(expected[choice-1], 0)
                char.selectSkillTable(tablename)
                if expected[choice-1] == 'Blade Cbt':
                    char.selectBladeSkillTable('Dagger')
                    self.assertEqual(char.skills['Dagger'], 1)
                elif expected[choice-1] == 'Gun Cbt':
                    char.selectGunSkillTable('Carbine')
                    self.assertEqual(char.skills['Carbine'], 1)
                elif expected[choice-1] == 'Vehicle':
                    char.selectVehicleSkillTable('Helicopter')
                    self.assertEqual(char.skills['Helicopter'], 1)
                elif expected[choice-1] == '+1 Stren':
                    self.assertEqual(char.stats[character.STR], stats[character.STR]+1)
                elif expected[choice-1] == '+1 Dext':
                    self.assertEqual(char.stats[character.DEX], stats[character.DEX]+1)
                elif expected[choice-1] == '+1 Endur':
                    self.assertEqual(char.stats[character.END], stats[character.END]+1)
                elif expected[choice-1] == '+1 Intel':
                    self.assertEqual(char.stats[character.INT], stats[character.INT]+1)
                elif expected[choice-1] == '+1 Educ':
                    self.assertEqual(char.stats[character.EDU], stats[character.EDU]+1)
                elif expected[choice-1] == '+1 Social':
                    self.assertEqual(char.stats[character.SOC], stats[character.SOC]+1)
                elif expected[choice-1] == '-1 Social':
                    self.assertEqual(char.stats[character.SOC], stats[character.SOC]-1)
                else:
                    self.assertEqual(char.skills[expected[choice-1]], previousSkill+1)                          

    def _getAll2DSums(self):
        return [[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6]]
