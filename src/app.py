from flask import Flask, render_template, jsonify, Blueprint
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
import chartkick

app = Flask(__name__, template_folder='_includes')
app.config['SECRET_KEY'] = 'secret!'


app.config['MONGO_DBNAME'] = 'admin'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/admin'

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

mongo = PyMongo(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', my_list=[0,1,2,3,4,5])

@app.route('/restaurants', methods=['GET'])
def get_all_stars():
  star = mongo.db.restaurants
  output = []
  for s in star.find()[:10]:
    output.append({'name' : s['name'], 'restaurant_id' : s['restaurant_id'],
                   'address' : s['address'], 'borough' : s['borough'],
                   'cuisine' : s['cuisine'], 'grades' : s['grades']})
  return jsonify({'result' : output})


@app.route('/chart')
def first_graph():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('first_graph.html', data=data)

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)
