from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='_includes')
app.config['SECRET_KEY'] = 'secret!'


app.config['MONGO_DBNAME'] = 'admin'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/admin'

mongo = PyMongo(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurants', methods=['GET'])
def get_all_stars():
  star = mongo.db.restaurants
  output = []
  for s in star.find()[:10]:
    output.append({'name' : s['name'], 'restaurant_id' : s['restaurant_id'],
                   'address' : s['address'], 'borough' : s['borough'],
                   'cuisine' : s['cuisine'], 'grades' : s['grades']})
  return jsonify({'result' : output})

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)
