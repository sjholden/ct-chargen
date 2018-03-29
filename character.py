import logging
import os
import cloudstorage as gcs
from google.appengine.api import app_identity
import random
import uuid
import pickle
from __builtin__ import True


gcs.set_default_retry_params(gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
                             )
GCS_BUCKET = '/' + (os.environ.get('BUCKET_NAME') or app_identity.get_default_gcs_bucket_name())

# stats
STR=0
DEX=1
END=2
INT=3
EDU=4
SOC=5
STAT_NAMES = ['Stength', 'Dexterity', 'Endurance', 'Intellect','Education', 'Social Standing']

#careers
NAVY = 'Navy'
MARINES = 'Marines'
ARMY = 'Army'
SCOUTS = 'Scouts'
MERCHANTS = 'Merchants'
OTHER = 'Other'
CAREER_MEMBER_NAMES = {NAVY: 'Navy', MARINES: 'Marine', ARMY: 'Army', SCOUTS: 'Scout', MERCHANTS: 'Merchant', OTHER: ''}
# The various tables
DRAFT_TABLE = [NAVY, MARINES, ARMY, SCOUTS, MERCHANTS, OTHER]
SERVICE_TABLE = {
    NAVY: {'enlistment': (8, [(1, INT, 8), (2, EDU, 9)]),
             'survival': (5, [(2, INT, 7)]),
             'commission': (10, [(1, SOC, 9)]),
             'promotion': (8, [(1, EDU, 8)]),
             'reenlist': (6, []),
             },
    MARINES: {'enlistment': (9, [(1, INT, 8), (2, STR, 8)]),
                'survival': (6, [(2, END, 8)]),
                'commission': (9, [(1, EDU, 7)]),
                'promotion': (9, [(1, SOC, 8)]),
                'reenlist': (6, []),
                },
    ARMY: {'enlistment': (5, [(1, DEX, 6), (2, END, 5)]),
             'survival': (5, [(2, EDU, 6)]),
             'commission': (5, [(1, END, 7)]),
             'promotion': (6, [(1, EDU, 7)]),
             'reenlist': (7, []),
             },
    SCOUTS: {'enlistment': (7, [(1, INT, 6), (2, STR, 8)]),
               'survival': (7, [(2, END, 9)]),
               'reenlist': (3, []),
               },
    MERCHANTS: {'enlistment': (7, [(1, STR, 7), (2, INT, 6)]),
                  'survival': (5, [(2, INT, 7)]),
                  'commission': (4, [(1, INT, 6)]),
                  'promotion': (10, [(1, INT, 9)]),
                  'reenlist': (4, []),
                  },
    OTHER: {'enlistment': (3, []),
              'survival': (5, [(2, INT, 9)]),
              'reenlist': (5, []),
              },
    }
RANKS = {
    NAVY: ['Ensign', 'Lieutenant', 'Lieutenant Commander', 'Commander', 'Captain', 'Admiral'],
    MARINES: ['Lieutenant', 'Captain', 'Force Commander', 'Lieutenant Colonel', 'Colonel', 'Brigadier'],
    ARMY: ['Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'General'],
    MERCHANTS: ['4th Officer', '3rd Officer', '2nd Officer', '1st Officer', 'Captain'],
    }
JOIN_SKILLS = {
    NAVY: [],
    MARINES: ['Cutlass'],
    ARMY: ['Rifle'],
    SCOUTS: ['Pilot'],
    MERCHANTS: [],
    OTHER: [],
    }
COMMISSION_SKILLS = {
    NAVY: [],
    MARINES: ['Revolver'],
    ARMY: ['SMG'],
    MERCHANTS: [],
    }
RANK_SKILLS = {
    NAVY: [[], [], [], [], ["+1 Social"], ["+1 Social"]],
    MARINES: [[], [], [], [], [], []],
    ARMY: [[], [], [], [], [], []],
    MERCHANTS: [[], [], [], ["Pilot"], [], []],
    }
SKILL_TABLE_NAMES = ['Personal Development', 'Service Skills', 'Advanced Education', 'Advanced Education 2']
SKILL_TABLES = {
    NAVY: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', '+1 Intel', '+1 Educ', '+1 Social'],
        'Service Skills': [None, "Ship's Boat", 'Vacc Suit', 'Forward Observer', 'Gunnery', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education': [None, 'Vacc Suit', 'Mechanical', 'Electronics', 'Engineering', 'Gunnery', 'Jack-of-all-Trades'],
        'Advanced Education 2': [None, 'Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin']
        },
    MARINES: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', 'Gambling', 'Brawling', 'Blade Cbt'],
        'Service Skills': [None, 'Vehicle', 'Vacc Suit', 'Blade Cbt', 'Gun Cbt', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education': [None, 'Vehicle', 'Mechanical', 'Electronics', 'Tactics', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education 2': [None, 'Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin']
        },
    ARMY: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', 'Gambling', '+1 Educ', 'Brawling'],
        'Service Skills': [None, 'Vehicle', 'Air/Raft', 'Gun Cbt', 'Forward Observer', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education': [None, 'Vehicle', 'Mechanical', 'Electronics', 'Tactics', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education 2': [None, 'Medical', 'Tactics', 'Tactics', 'Computer', 'Leader', 'Admin']
        },
    SCOUTS: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', '+1 Intel', '+1 Educ', 'Gun Cbt'],
        'Service Skills': [None, 'Vehicle', 'Vacc Suit', 'Mechanical', 'Navigation', 'Electronics', 'Jack-of-all-Trades'],
        'Advanced Education': [None, 'Vehicle', 'Mechanical', 'Electronics', 'Jack-of-all-Trades', 'Gunnery', 'Medical'],
        'Advanced Education 2': [None, 'Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Jack-of-all-Trades']
        },
    MERCHANTS: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', '+1 Stren', 'Blade Cbt', 'Bribery'],
        'Service Skills': [None, 'Vehicle', 'Vacc Suit', 'Jack-of-all-Trades', 'Steward', 'Electronics', 'Gun Cbt'],
        'Advanced Education': [None, 'Streetwise', 'Mechanical', 'Electronics', 'Navigation', 'Gunnery', 'Medical'],
        'Advanced Education 2': [None, 'Medical', 'Navigation', 'Engineering', 'Computer', 'Pilot', 'Admin']
        },
    OTHER: {
        'Personal Development': [None, '+1 Stren', '+1 Dext', '+1 Endur', 'Blade Cbt', 'Brawling', '-1 Social'],
        'Service Skills': [None, 'Vehicle', 'Gambling', 'Brawling', 'Bribery', 'Blade Cbt', 'Gun Cbt'],
        'Advanced Education': [None, 'Streetwise', 'Mechanical', 'Electronics', 'Gambling', 'Brawling', 'Forgery'],
        'Advanced Education 2': [None, 'Medical', 'Forgery', 'Electronics', 'Computer', 'Streetwise', 'Jack-of-all-Trades']
        },
    }
BLADES = ['Dagger', 'Blade', 'Foil', 'Sword', 'Cutlass', 'Broadsword', 'Bayonet', 'Spear', 'Halberd', 'Pike', 'Cudgel']
GUNS = ['Body Pistol', 'Auto Pistol', 'Revolver', 'Carbine', 'Rifle', 'Auto Rifle', 'Shotgun', 'SMG', 'Laser Carbine', 'Laser Rifle']
VEHICLES = ['Ground Car', 'ATV', 'Sail Boat', 'Motor Boat', 'Submersible', 'Fixed Wing Aircraft', 'Helicopter', 'Hovercraft', 'Air/Raft', 'Grav Belt']
CASH_TABLE = {
    NAVY: (1000, 5000, 5000, 10000, 20000, 50000, 50000),
    MARINES: (2000, 5000, 5000, 10000, 20000, 30000, 40000),
    ARMY: (2000, 5000, 10000, 10000, 10000, 20000, 30000),
    SCOUTS: (20000, 20000, 30000, 30000, 50000, 50000, 50000),
    MERCHANTS: (1000, 5000, 10000, 20000, 20000, 40000, 40000),
    OTHER: (1000, 5000, 10000, 10000, 10000, 50000, 100000),
    }
BENEFITS_TABLE = {
    NAVY: ('Low Psg', '+1 Intel', '+2 Educ', 'Blade', "Travellers'", 'High Psg', '+2 Social'),
    MARINES: ('Low Psg', '+2 Intel', '+1 Educ', 'Blade', "Travellers'", 'High Psg', '+2 Social'),
    ARMY: ('Low Psg', '+1 Intel', '+2 Educ', 'Gun', 'High Psg', 'Mid Psg', '+1 Social'),
    SCOUTS: ('Low Psg', '+2 Intel', '+2 Educ', 'Blade', 'Gun', 'Scout Ship'),
    MERCHANTS: ('Low Psg', '+1 Intel', '+1 Educ', 'Gun', 'Blade', 'Low Psg', 'Free Trader'),
    OTHER: ('Low Psg', '+1 Intel', '+1 Educ', 'Gun', 'High Psg', None),
    }

def toHexStr(number):
    """Convert number to hex representation"""
    if number >= 23:
        return chr(80-23+number)
    elif number >= 18:
        return chr(74-18+number)
    elif number >= 10:
        return chr(65-10+number)
    else:
        return chr(48+number)

ORDINALS = ['zeroth', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
def numberToOrdinal(number):
    """Return the ordinal string representing the number."""
    if number < len(ORDINALS):
        return ORDINALS[number]
    else:
        return '%dth' % (number,)
        
class Character(object):
    def __init__(self, fixRolls=None):
        """Create a character, by rolling the stats.
        
        If fixRolls is not None it must be a list of single die roll results,
        they will be used as the first die results with random rolls being
        used once they are exhausted. 
        """
        if fixRolls:
            self.cheat = [x for x in fixRolls]
        else:
            self.cheat = None
        self.charid = str(uuid.uuid4())
        self.history = []
        self.rolllog = []
        self.career = None
        self.terms = 0
        self.dead = False
        self.retired = False
        self.rank = 0
        self.age = 18
        self.ageextramonths = 0
        self.skills = {}
        self.skillrollsleft = 0
        self.musterrollsleft = 0
        self.cashrolls = 0
        self.credits = 0
        self.possessions = {}
        self.tasmember = False
        self.stats = [self.rollDice(STAT_NAMES[i], 2) for i in range(6)]
        self.next_step = 'select_career'
     
    @classmethod
    def load(cls, charid):
        """Load a character from the store."""       
        gcs_file = gcs.open(GCS_BUCKET + '/' + charid, 'r')
        data = gcs_file.read()
        gcs_file.close()
        return pickle.loads(data)
    
    def save(self): 
        """Save the character to the store."""
        gcs_file = gcs.open(GCS_BUCKET + '/' + self.charid, 'w',
                            content_type='text/plain',
                            retry_params=gcs.RetryParams(backoff_factor=1.1))
        gcs_file.write(pickle.dumps(self))
        gcs_file.close()
        
    def convertForClient(self):
        """Return a dict containing the character data relevant to client, ready to be jsonified"""
        character = {}
        character['charid'] = self.charid
        character['stats'] = [toHexStr(x) for x in self.stats]
        if self.ageextramonths:
            character['age'] = "%d and %d months" % (self.age, self.ageextramonths)
        else:
            character['age'] = self.age
        character['career'] = self.career
        if self.rank:
            character['rank'] = RANKS[self.career][self.rank-1]
        else:
            character['rank'] = ''
        character['terms'] = self.terms
        skills = ["%s-%d" % (k,v) for k,v in self.skills.items()]
        skills.sort()
        character['skills'] = ', '.join(skills)
        possessions = []
        for possession in self.possessions:
            for _ in range(self.possessions[possession]):
                possessions.append(possession)
        possessions.sort()
        character['possessions'] = ', '.join(possessions)
        if self.credits:
            character['credits'] = format(self.credits, ',d')
        else:
            character['credits'] = ''
        character['history'] = self.history
        character['dierolls'] = self.rolllog
        if self.dead:
            character['next_step'] = ['finished']
            character['dead'] = True
        else:
            character['dead'] = False
            if self.next_step == 'select_career':
                character['next_step'] = ['select', 'select_career', 'Choose Career', DRAFT_TABLE]
            elif self.next_step == 'select_skill_table':
                character['next_step'] = ['select', 'select_skill_table', 'Choose Skill Table']
                if self.stats[EDU] >= 8:
                    character['next_step'].append(SKILL_TABLE_NAMES)
                else:
                    character['next_step'].append(SKILL_TABLE_NAMES[:-1])
            elif self.next_step == 'select_blade_skilltable':
                character['next_step'] = ['select', 'select_blade_skilltable', 'Choose Blade', BLADES]
            elif self.next_step == 'select_gun_skilltable':
                character['next_step'] = ['select', 'select_gun_skilltable', 'Choose Gun', GUNS]
            elif self.next_step == 'select_vehicle_skilltable':
                character['next_step'] = ['select', 'select_vehicle_skilltable', 'Choose Vehicle', VEHICLES]
            elif self.next_step == 'select_reenlist':
                character['next_step'] = ['select', 'select_reenlist', 'Apply to re-enlist?', ['Yes', 'No']]
            elif self.next_step == 'select_muster_table':
                character['next_step'] = ['select', 'select_muster_table', 'Choose Mustering Out Table', ['Benefits', 'Cash']]
            elif self.next_step == 'select_gun_benefit':
                guns = []
                for gun in GUNS:
                    guns.append(gun)
                    if gun in self.possessions:
                        guns.append(gun + ' (skill)')
                character['next_step'] = ['select', 'select_gun_benefit', 'Choose Gun', guns]
            elif self.next_step == 'select_blade_benefit':
                blades = []
                for blade in BLADES:
                    blades.append(blade)
                    if blade in self.possessions:
                        blades.append(blade + ' (skill)')
                character['next_step'] = ['select', 'select_blade_benefit', 'Choose Blade', blades]
            elif self.next_step == 'finished':
                character['next_step'] = ['finished']
        return character

    def toCharacterSheet(self):
        """create a text character sheet, ala an index card."""
        title = []
        if self.cheat is not None:
            title.append('Cheating')
        if self.dead:
            title.append('Deceased')
        if self.retired:
            title.append('Retired')
        title.append(CAREER_MEMBER_NAMES[self.career])
        if self.rank:
            title.append(RANKS[self.career][self.rank-1])
        title = ' '.join([x for x in title if x])
        upp = ''.join([toHexStr(x) for x in self.stats])
        age = 'Age ' + str(self.age)
        if self.terms:
            if self.terms == 1:
                terms = str(self.terms) + ' Term'
            else:
                terms = str(self.terms) + ' Terms'
        else:
            terms = ''
        if self.credits:
            crs = 'Cr' + str(self.credits)
        else:
            crs = ''
        skills = ["%s-%d" % (k,v) for k,v in self.skills.items()]
        skills.sort()
        skills = ', '.join(skills)
        possessions = []
        for possession in self.possessions:
            for _ in range(self.possessions[possession]):
                possessions.append(possession)
        possessions.sort()
        possessions = ', '.join(possessions)
        history = '\n'.join(self.history)
        return '%-50s%-10s%-10s\n%-50s%s\n\nSkills: %s\n\nBenefits: %s\n\nService History:\n%s\n' % (title, upp, age, terms, crs, skills, possessions, history)

    #
    # front-end functions to be used to progress through character creation.
    #    
    def selectCareer(self, career):
        """Enlist in career, or be drafted randomly."""
        if self.next_step != 'select_career':
            return False
        self.addHistory("Attempted to enlist in " + career)
        enlistment = SERVICE_TABLE[career]['enlistment']
        enlistroll = self.rollDice(career + ' enlistment', 2, enlistment[1])
        if enlistroll >= enlistment[0]:
            self.addHistory("Accepted into " + career)
            self.career = career
            self.doTerm(firstTerm=True)
        else:
            self.addHistory("Rejected by " + career)
            draftRoll = self.rollDice('Draft', 1)
            career = DRAFT_TABLE[draftRoll-1]
            self.addHistory("Drafted into " + career)
            self.career = career
            self.doTerm(firstTerm=True, drafted=True)
        return True

    def selectSkillTable(self, tablename):
        """Roll on a skill table."""
        if self.next_step!= 'select_skill_table':
            return False
        if tablename == 'Advanced Education 2' and self.stats[EDU] < 8:
            # nice try
            tablename = 'Advanced Education'
        if self.skillrollsleft:
            self.skillrollsleft = self.skillrollsleft - 1
            skillRoll = self.rollDice(tablename + ' Table', 1)
            skill = SKILL_TABLES[self.career][tablename][skillRoll]
            if skill == 'Blade Cbt':
                self.next_step = 'select_blade_skilltable'
            elif skill == 'Gun Cbt':       
                self.next_step = 'select_gun_skilltable'
            elif skill == 'Vehicle':
                self.next_step = 'select_vehicle_skilltable'
            else:
                self.addSkill(skill)
                if self.skillrollsleft == 0:
                    self.doEndTerm()
        else:
            self.doEndTerm()
        return True
    
    def selectBladeSkillTable(self, blade):
        """Select a specific blade due to getting Blade as a skill."""
        if self.next_step != 'select_blade_skilltable':
            return False
        if blade not in BLADES:
            blade = 'Blade'
        self.addSkill(blade)
        self.rolllog.append('[Selected ' + blade + ']')
        if self.skillrollsleft == 0:
            self.doEndTerm()
        else:
            self.next_step = 'select_skill_table'
        return True  

    def selectGunSkillTable(self, gun):
        """Select a specific gun due to getting Gun as a skill."""
        if self.next_step != 'select_gun_skilltable':
            return False
        if gun not in GUNS:
            gun = GUNS[0]
        self.addSkill(gun)
        self.rolllog.append('[Selected ' + gun + ']')
        if self.skillrollsleft == 0:
            self.doEndTerm()
        else:
            self.next_step = 'select_skill_table'        
        return True  

    def selectVehicleSkillTable(self, vehicle):
        """Select a specific vehicle due to getting Vehicle as a skill."""
        if self.next_step != 'select_vehicle_skilltable':
            return False
        if vehicle not in VEHICLES:
            vehicle = VEHICLES[0]
        self.addSkill(vehicle)
        self.rolllog.append('[Selected ' + vehicle + ']')
        if self.skillrollsleft == 0:
            self.doEndTerm()
        else:
            self.next_step = 'select_skill_table'
        return True  

    def selectReEnlist(self, decision):
        """Perform voluntary and manfatory enlistment."""
        if self.next_step!= 'select_reenlist':
            return False
        reenlistRoll = self.rollDice("Reenlist", 2)
        if reenlistRoll == 12 and decision == 'No':
            self.addHistory("Mandatory reenlistment for %s term" % (numberToOrdinal(self.terms+1),))
            self.doTerm()
        elif decision == 'No':
            if self.terms >= 5:
                self.addHistory('Retired after %s term' % (numberToOrdinal(self.terms),))
            else:
                self.addHistory('Voluntarily left service after %s term' % (numberToOrdinal(self.terms),))
            self.startMusterOut()
        else:
            if reenlistRoll >= SERVICE_TABLE[self.career]['reenlist'][0]:
                self.addHistory('Voluntary reenlistment for %s term' % (numberToOrdinal(self.terms+1),))
                self.doTerm()
            else:
                self.addHistory('Denied reenlistment for %s term' % (numberToOrdinal(self.terms+1),))
                self.startMusterOut()
        return True

    def selectMusterTable(self, table):
        """Roll on the muster out table."""
        if self.next_step != 'select_muster_table':
            return False
        if self.musterrollsleft < 1:
            return False
        if table == 'Cash' and self.cashrolls < 3:
            if self.skills.get('Gambling'):
                dms = [(1, STR, -1)]
            else:
                dms = []
            cashRoll = self.rollDice("Mustering Cash Table", 1, dms)
            self.credits += CASH_TABLE[self.career][cashRoll-1]
            self.cashrolls += 1
            self.musterrollsleft = self.musterrollsleft - 1
            if self.musterrollsleft < 1:
                self.next_step = 'finished'
            elif self.musterrollsleft > 0 and self.cashrolls >= 3:
                self.selectMusterTable('Benefits')
        else:
            if self.rank >= 5:
                dms = [(1, STR, -1)]
            else:
                dms = []
            benefitsRoll = self.rollDice("Mustering Benefits Table", 1, dms)
            benefit = BENEFITS_TABLE[self.career][benefitsRoll-1]
            self.addBenefit(benefit)
        return True
            
    def selectGunBenefit(self, gun):
        """Select a specific gun when getting Gun for mustering."""
        if self.next_step!= 'select_gun_benefit':
            return False
        if gun.endswith(' (skill)'): 
            gun = gun[:-8]
            if gun not in GUNS:
                gun = GUNS[0]
            if gun in self.possessions:
                self.addSkill(gun)
                self.rolllog.append('[Selected ' + gun + ' (skill)]')
            else:
                self.possessions[gun] = 1
                self.rolllog.append('[Selected ' + gun + ']')
        else:
            if gun not in GUNS:
                gun = GUNS[0]
            self.rolllog.append('[Selected ' + gun + ']')
            if gun in self.possessions:
                self.possessions[gun] += 1
            else:
                self.possessions[gun] = 1
        self.next_step = 'select_muster_table'
        self.musterrollsleft = self.musterrollsleft - 1
        if self.musterrollsleft < 1:
            self.next_step = 'finished'
        elif self.musterrollsleft > 0 and self.cashrolls >= 3:
            self.selectMusterTable('Benefits')
        return True
             
    def selectBladeBenefit(self, blade):
        """Select a specific blade when getting Blade for mustering."""
        if self.next_step!= 'select_blade_benefit':
            return False
        if blade.endswith(' (skill)'): 
            blade = blade[:-8]
            if blade not in BLADES:
                blade = 'Blade'
            if blade in self.possessions:
                self.addSkill(blade)
                self.rolllog.append('[Selected ' + blade + ' (skill)]')
            else:
                self.possessions[blade] = 1
                self.rolllog.append('[Selected ' + blade + ']')
        else:
            if blade not in BLADES:
                blade = 'Blade'
            self.rolllog.append('[Selected ' + blade + ']')
            if blade in self.possessions:
                self.possessions[blade] += 1
            else:
                self.possessions[blade] = 1
        self.next_step = 'select_muster_table'
        self.musterrollsleft = self.musterrollsleft - 1
        if self.musterrollsleft < 1:
            self.next_step = 'finished'
        elif self.musterrollsleft > 0 and self.cashrolls >= 3:
            self.selectMusterTable('Benefits')
        return True
    
    #
    # Internal helper functions.
    #    
    def doTerm(self, firstTerm=False, drafted=False):
        """Run a term until skill table selection."""
        self.terms += 1 
        survived = self.survivalCheck()
        if survived:
            if not drafted:
                commissioned = self.commissionCheck()
                promoted = self.promotionCheck()
            else:
                commissioned = False
                promoted = False            
            if firstTerm:
                skillRolls = 2
                for skill in JOIN_SKILLS[self.career]:
                    self.addSkill(skill)
            elif self.career == SCOUTS:
                skillRolls = 2
            else:
                skillRolls = 1
            if commissioned:
                skillRolls += 1
                for skill in COMMISSION_SKILLS[self.career]:
                    self.addSkill(skill)
            if promoted:
                skillRolls += 1
                for skill in RANK_SKILLS[self.career][self.rank-1]:
                    self.addSkill(skill)
            self.skillrollsleft = skillRolls
            self.next_step = 'select_skill_table'

    def doEndTerm(self):
        """Finish up processing a term."""
        agingCrisis = self.doAging()
        if not self.dead:
            if agingCrisis:
                self.history.append("Unable to reenlist due to aging crisis after %s term" % (numberToOrdinal(self.terms),))
                self.startMusterOut()
            else:
                self.next_step = 'select_reenlist'
                if self.terms  >= 7:
                    self.selectReEnlist("No")
    
    def survivalCheck(self):
        """Check survival for a term."""
        survivalRoll = self.rollDice('Survival', 2, SERVICE_TABLE[self.career]['survival'][1])
        if survivalRoll < SERVICE_TABLE[self.career]['survival'][0]:
            self.addHistory('Death in service')
            self.dead = True
        return not self.dead

    def commissionCheck(self):
        """Check for a commission."""
        if self.rank == 0 and self.career in RANKS:
            commissionRoll = self.rollDice('Apply for commission', 2, SERVICE_TABLE[self.career]['commission'][1])
            if commissionRoll >= SERVICE_TABLE[self.career]['commission'][0]:
                self.rank = 1
                self.addHistory("Commissioned as " + RANKS[self.career][self.rank-1] + " during " + numberToOrdinal(self.terms) + " term")
                return True
        return False
    
    def promotionCheck(self):
        """Check for a promotion."""
        if self.rank > 0 and self.rank < len(RANKS[self.career]):
            promotionRoll = self.rollDice('Apply for promotion', 2, SERVICE_TABLE[self.career]['promotion'][1])
            if promotionRoll >= SERVICE_TABLE[self.career]['promotion'][0]:
                self.rank += 1
                self.addHistory("Promoted to " + RANKS[self.career][self.rank-1] + " during " + numberToOrdinal(self.terms) + " term")
                return True
        return False

    def doAging(self):
        """Apply the aging table, return True of there was an aging crisis."""
        agingCrisis = False
        self.age += 4
        if self.age >= 66:
            self.doAgingSavingThrow(STR, 9, -2)
            self.doAgingSavingThrow(DEX, 9, -2)
            self.doAgingSavingThrow(END, 9, -2)
            self.doAgingSavingThrow(INT, 9, -1)
        elif self.age >= 50:
            self.doAgingSavingThrow(STR, 9, -1)
            self.doAgingSavingThrow(DEX, 8, -1)
            self.doAgingSavingThrow(END, 9, -1)
        elif self.age >= 34:
            self.doAgingSavingThrow(STR, 8, -1)
            self.doAgingSavingThrow(DEX, 7, -1)
            self.doAgingSavingThrow(END, 8, -1)
        for stat in (STR, DEX, END, INT):
            if self.stats[stat] <= 0:
                agingCrisis = True
                deathSave = self.rollDice("Aging crisis (" + STAT_NAMES[stat] + ") death save", 2)
                if deathSave < 8:
                    self.dead = True
                    self.addHistory("Died in aging crisis")
                    break
                else:
                    self.stats[stat] = 1
                    months = self.rollDice('Months to recover from aging crisis', 1)
                    self.addHistory("Spent %d months recovering from aging crisis" % (months,))
                    self.ageextramonths += months
                    if self.ageextramonths >= 12:
                        self.age += 1
                        self.ageextramonths = self.ageextramonths - 12
        return agingCrisis
    
    def doAgingSavingThrow(self, stat, save, penalty):
        """Do saving throw and application of aging to a stat."""
        rollSave = self.rollDice(STAT_NAMES[stat] + " aging saving throw", 2)
        if rollSave < save:
            self.addToStatCapped(stat, penalty)

    def startMusterOut(self):
        """Mustering out"""
        rolls = self.terms
        if self.rank >= 5:
            rolls += 3
        elif self.rank >= 3:
            rolls += 2
        elif self.rank >= 1:
            rolls += 1
        self.musterrollsleft = rolls
        if self.career not in (SCOUTS, OTHER) and self.terms >= 5:
            self.retired = True
            self.addBenefit('%s/yr Retirement Pay' % (format(4000 + (self.terms-5)*2000, ',d'),))
        self.next_step = 'select_muster_table'
           
    def rollDice(self, logEntry, count, dms=None):
        """Roll count dice and apply any specified dms.
        
        dm format is a list of tuples (bonus, stat_to_check, cutoff).
        """
        total = 0
        for _ in range(count):
            if self.cheat:
                total += self.cheat.pop(0)
            else:
                total += random.randint(1,6)
        dm = 0
        if dms is not None:
            for bonus, stat, cutoff in dms:
                    if self.stats[stat] >= cutoff:
                        dm = dm + bonus
        if dm < 0:
            dmText = str(dm)
        elif dm > 0:
            dmText = "+" + str(dm)
        else:
            dmText = ''
        self.rolllog.append(logEntry + ': ' + str(total) + dmText)
        return total + dm

    def addHistory(self, msg):
        """Record a history log."""
        self.history.append(msg + '.')
        
    def addToStatCapped(self, stat, amount):
        """Add amount to stat, but cap at 15 (don't restrict <1 though)."""
        self.stats[stat] += amount
        if self.stats[stat] > 15:
            self.stats[stat] = 15
        
    def addSkill(self, skill):
        """Gain a skill (which could be a stat change)."""
        if skill == '+1 Stren':
            self.addToStatCapped(STR, 1)
        elif skill == '+1 Dext':
            self.addToStatCapped(DEX, 1)
        elif skill == '+1 Endur':
            self.addToStatCapped(END, 1)
        elif skill == '+1 Intel':
            self.addToStatCapped(INT, 1)
        elif skill == '+1 Educ':
            self.addToStatCapped(EDU, 1)
        elif skill == '+1 Social':            
            self.addToStatCapped(SOC, 1)
        elif skill == '+2 Intel':
            self.addToStatCapped(INT, 2)
        elif skill == '+2 Educ':
            self.addToStatCapped(EDU, 2)
        elif skill == '+2 Social':            
            self.addToStatCapped(SOC, 2)
        elif skill == '-1 Social':
            if self.stats[SOC] > 1:            
                self.addToStatCapped(SOC, -1)
        else:
            if skill not in self.skills:
                self.skills[skill] = 1
            else:
                self.skills[skill] += 1
            
    def addBenefit(self, benefit):
        """Add the rolled benefit."""
        if benefit in ('Blade', 'Gun'):
            self.next_step = 'select_%s_benefit' % (benefit.lower(),)
        else:
            if benefit is None:
                pass
            elif benefit.startswith('+'):
                self.addSkill(benefit)
            elif benefit == "Travellers'":
                self.tasmember = True
            elif benefit == 'Scout Ship':
                self.possessions['Scout Ship (on loan)'] = 1
            elif benefit == 'Free Trader':
                if 'Free Trader (paid off)' in self.possessions:
                    pass
                elif 'Free Trader (30 years paid off)' in self.possessions:
                    self.possessions['Free Trader (paid off)'] = 1
                    del self.possessions['Free Trader (30 years paid off)']
                elif 'Free Trader (20 years paid off)' in self.possessions:
                    self.possessions['Free Trader (30 years paid off)'] = 1
                    del self.possessions['Free Trader (20 years paid off)']
                elif 'Free Trader (10 years paid off)' in self.possessions:
                    self.possessions['Free Trader (20 years paid off)'] = 1
                    del self.possessions['Free Trader (10 years paid off)']    
                elif 'Free Trader (0 years paid off)' in self.possessions:
                    self.possessions['Free Trader (10 years paid off)'] = 1
                    del self.possessions['Free Trader (0 years paid off)']
                else:
                    self.possessions['Free Trader (0 years paid off)'] = 1
            else:
                if benefit in self.possessions:
                    self.possessions[benefit] += 1
                else:
                    self.possessions[benefit] = 1
            self.musterrollsleft = self.musterrollsleft - 1
            if self.musterrollsleft < 1:
                self.next_step = 'finished'
            elif self.musterrollsleft > 0 and self.cashrolls >= 3:
                self.selectMusterTable('Benefits')
            


                
