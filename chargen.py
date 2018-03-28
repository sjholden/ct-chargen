
import logging
from flask import Flask, jsonify, render_template, request
import character
import autogenerator


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('chargen.html', charid='')

@app.route('/sheet/<charid>')
def sheet(charid):
    char = character.Character.load(charid)
    return render_template('charsheet.html', charblock=char.toCharacterSheet())


@app.route('/new_character')
def new_character():
    char = character.Character()
    char.save()
    return jsonify(char.convertForClient())

@app.route('/random_character')
def random_character():
    char = autogenerator.RandomGenerator().makeCharacter()
    char.save()
    return jsonify(char.convertForClient())

@app.route('/random_character_nosave')
def random_character_nosave():
    char = autogenerator.RandomGenerator().makeCharacter()
    return jsonify(char.convertForClient())    

@app.route('/load_character')
def load_character():
    char = character.Character.load(request.args.get('charid'))
    return jsonify(char.convertForClient())

@app.route('/select_career')
def select_career():
    char = character.Character.load(request.args.get('charid'))
    if char.selectCareer(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())

@app.route('/select_skill_table')
def select_skill_table():
    char = character.Character.load(request.args.get('charid'))
    if char.selectSkillTable(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())

@app.route('/select_blade_skilltable')
def select_blade_skilltable():
    char = character.Character.load(request.args.get('charid'))
    if char.selectBladeSkillTable(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())

@app.route('/select_gun_skilltable')
def select_gun_skilltable():
    char = character.Character.load(request.args.get('charid'))
    if char.selectGunSkillTable(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())
    
@app.route('/select_vehicle_skilltable')
def select_vehicle_skilltable():
    char = character.Character.load(request.args.get('charid'))
    if char.selectVehicleSkillTable(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())
    
@app.route('/select_reenlist')
def select_reenlist():
    char = character.Character.load(request.args.get('charid'))
    if char.selectReEnlist(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())

@app.route('/select_muster_table')
def select_muster_table():
    char = character.Character.load(request.args.get('charid'))
    if char.selectMusterTable(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())

@app.route('/select_gun_benefit')
def select_gun_benefit():
    char = character.Character.load(request.args.get('charid'))
    if char.selectGunBenefit(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())    

@app.route('/select_blade_benefit')
def select_blade_benefit():
    char = character.Character.load(request.args.get('charid'))
    if char.selectBladeBenefit(request.args['selection']):
        char.save()
        return jsonify(char.convertForClient())  


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
