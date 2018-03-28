import logging
import random

import character

class RandomGenerator(object):
    def __init__(self):
        self.selectFuncs = {
            'select_career': self.selectCareer,
            'select_skill_table': self.selectSkillTable,
            'select_blade_skilltable': self.selectBladeSkillTable,
            'select_gun_skilltable': self.selectGunSkillTable,
            'select_vehicle_skilltable': self.selectVehicleSkillTable,
            'select_reenlist': self.selectReEnlist,
            'select_muster_table': self.selectMusterTable,
            'select_gun_benefit': self.selectGunBenefit,
            'select_blade_benefit': self.selectBladeBenefit,
            }
    
    def randomChoice(self, options):
        """Pick at random."""
        return random.choice(options)
    
    def selectCareer(self, char, options):
        char.selectCareer(self.randomChoice(options))

    def selectSkillTable(self, char, options):
        char.selectSkillTable(self.randomChoice(options))
        
    def selectBladeSkillTable(self, char, options):
        char.selectBladeSkillTable(self.randomChoice(options))
        
    def selectGunSkillTable(self, char, options):
        char.selectGunSkillTable(self.randomChoice(options))
        
    def selectVehicleSkillTable(self, char, options):
        char.selectVehicleSkillTable(self.randomChoice(options))
        
    def selectReEnlist(self, char, options):
        char.selectReEnlist(self.randomChoice(options))
        
    def selectMusterTable(self, char, options):
        char.selectMusterTable(self.randomChoice(options))
        
    def selectGunBenefit(self, char, options):
        char.selectGunBenefit(self.randomChoice(options))
        
    def selectBladeBenefit(self, char, options):
        char.selectBladeBenefit(self.randomChoice(options))
        
    
    def makeCharacter(self):
        char = character.Character()
        data = char.convertForClient()
        while data['next_step'][0] != 'finished':
            if data['next_step'][0] == 'select':
                self.selectFuncs[data['next_step'][1]](char, data['next_step'][3])
            else:
                logging.exception('"%s" - unknown action in makeCharacter' % (data['next_step'][0],))
                return None
            data = char.convertForClient()
        return char

        