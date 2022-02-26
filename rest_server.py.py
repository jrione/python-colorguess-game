from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import mysql.connector as m
from mysql.connector import Error as Err

UPLOAD_FOLDER = 'folder_file'
HOSTNAME = 'http://localhost:2390/' #change with yoxur own domain

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
CORS(app)

response = {}

HOST = 'localhost'
DB   = 'lb_db'
USER = 'root'
PASS = ''

try:
	konek = m.connect(host=HOST,database=DB,user=USER,password=PASS)
except Err as e:
	print('no connection')

class Api(Resource):
	def post(self):
		data = {}

		data['nickname'] = request.form['nickname']
		data['score'] = request.form['score']
		data['date'] = request.form['date']

		try:
			curs = konek.cursor()
			sql = "INSERT INTO lb_tbl (nickname,score,date) VALUE (%s,%s,%s)" 
			val = (data['nickname'],data['score'],data['date'])
			curs.execute(sql,val)
			konek.commit()
			
			response = {'status':'Success!'}
		except:
			response = {'status':'Something Wrong!'}

		return response

api.add_resource(Api,"/api",methods=["POST"])

@app.route('/leaderboard')
def leaderboard():
	try:
		data = {}
		curs = konek.cursor()
		sql = "SELECT nickname,score,date FROM lb_tbl ORDER BY score DESC LIMIT 10" 
		curs.execute(sql)
		result = curs.fetchall()
		
		x = 0
		for res in result:
			data[x] = res
			x+=1
		response = data

	except Exception as e:
		response = {'status': 'Something Wrong!' }
		print(e)

	return response

if __name__ == "__main__":
	app.run(debug=True,port=2390) # tambah host=0.0.0.0 jika deploy ke docker