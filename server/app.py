from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Campers(Resource):
    def get(self):
        campers_list = []
        for c in Camper.query.all():
            c_dict = {
                'id': c.id,
                'name': c.name,
                'age': c.age
            }
            campers_list.append(c_dict)
        return make_response(campers_list, 200)
    def post(self):
        data = request.get_json()
        ca = Camper( name = data['name'], 
                    age = data['age']
                               )
        try:
            db.session.add( ca )
            db.session.commit()
            return make_response( ca.to_dict(), 201 )
        except Exception as ex:
            return make_response({
                'error': ['validation error']
            }, 422)
    
api.add_resource(Campers, '/campers')

class CampersById(Resource):
    def get(self, id):
        c = Camper.query.filter_by(id = id).first()
        if c == None:
            return make_response({'error': 'Camper not found'}, 404)
        return make_response(c.to_dict(), 200)
    
api.add_resource(CampersById, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        a_list = []
        for a in Activity.query.all():
            a_dict = {
                'id': a.id,
                'name': a.name,
                'difficulty': a.difficulty
            }
            a_list.append(a_dict)
        return make_response(a_list, 200)

api.add_resource(Activities, '/activities')

class ActivitiesById(Resource):
    def delete(self, id):
        a_instance = Activity.query.filter_by(id = id).first()
        if a_instance == None:
            return make_response({'error': 'activity not found'}, 404)
        db.session.delete(a_instance)
        db.session.commit()
        return make_response('', 204)

api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        data = request.get_json()
        signups = Signup( camper_id = data['camper_id'], 
                    activity_id = data['activity_id'],
                    time = data['time']
                               )
        try:
            db.session.add( signups )
            db.session.commit()
            return make_response(signups.activity.to_dict(), 201 )
        except Exception as ex:
            return make_response({
                'error': [ex.__str__()]
            }, 422)

api.add_resource( Signups, '/signups' )





if __name__ == '__main__':
    app.run(port=5555, debug=True)
