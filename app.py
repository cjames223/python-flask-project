from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)

db = PostgresqlDatabase('pokemon', user='cjames222', password='', host='localhost', port=5433)

class BaseModel(Model):
    class Meta:
        database = db

class Pokemon(BaseModel):
    name = CharField()
    desc = CharField()
    type1 = CharField()
    type2 = CharField()
    height = DecimalField(decimal_places=2)
    weight = DecimalField(decimal_places=1)

db.connect()
db.drop_tables([Pokemon])
db.create_tables([Pokemon])

Pokemon(name='Charmander', desc='Lizard Pokemon', type1='Fire', type2='None', height=2.00, weight=18.7).save()
Pokemon(name='Charmeleon', desc='Flame Pokemon', type1='Fire', type2='None', height=3.07, weight=41.9).save()
Pokemon(name='Charizard', desc='Flame Pokemon', type1='Fire', type2='Flying', height=5.07, weight=199.5).save()
Pokemon(name='Cyndaquil', desc= 'Fire Mouse Pokemon', type1='Fire', type2='None', height=1.08, weight=17.4).save()
Pokemon(name='Quilava', desc= 'Volcano Pokemon', type1='Fire', type2='None', height=2.11, weight=41.9).save()
Pokemon(name='Typhlosion', desc='Volcano Pokemon', type1='Fire', type2='None', height=5.07, weight=175.3).save()
Pokemon(name='Torchic', desc='Chick Pokemon', type1='Fire', type2='None', height=1.04, weight=5.5).save()
Pokemon(name='Combusken', desc='Young Fowl Pokemon', type1='Fire', type2='Fighting', height=2.11, weight=43.0).save()
Pokemon(name='Blaziken', desc='Blaze Pokemon', type1='Fire', type2='Fighting', height=6.03, weight=114.6).save()

@app.route('/pokemon/', methods=['GET', 'POST'])
@app.route('/pokemon/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Pokemon.get(Pokemon.id == id)))
        else:
            pokemon_list=[]
            for pokemon in Pokemon.select():
                pokemon_list.append(model_to_dict(pokemon))
            return jsonify(pokemon_list)

    if request.method == 'PUT':
        body = request.get_json()
        Pokemon.update(body).where(Pokemon.id == id).execute()
        return f"Pokemon {id} has been updated."

    if request.method == 'POST':
        new_pokemon = dict_to_model(Pokemon, request.get_json())
        new_pokemon.save()
        return "Pokemon has been added."

    if request.method == 'DELETE':
        Pokemon.delete().where(Pokemon.id == id).execute()
        return f"Pokemon {id} deleted."

app.run(debug=True)

