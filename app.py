from flask import *
import pymysql
from flask_cors import CORS
# connection=pymysql.connect(user='Vertexlabs',database='Vertexlabs$default',host='Vertexlabs.mysql.pythonanywhere-services.com',password='michael1234')
connection=pymysql.connect(user='sql7770379',database='sql7770379',host='sql7.freesqldatabase.com',password='zsJSBacLzW')
app=Flask(__name__)
CORS(app)
@app.route('/Api/addArticle',methods=['POST','GET'])
def addArticle():
    if request.method=='POST':
        try:
            data=request.get_json()
            if not(data):
                return jsonify({'error':'No data found'}),404
            title = data.get('title')
            author = data.get('author')
            content = data.get('content')
            date = data.get('date')
            featuredImage = data.get('featuredImage')
            views = data.get('views')
            commentEnabled = data.get('commentEnabled')
            readTime = data.get('readTime')

            sql="INSERT INTO blog(title,author,content,date,featuredImage,views,commentEnabled,readTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            cursor.execute(sql,(title,author,content,date,featuredImage,views,commentEnabled,readTime))
            connection.commit()
            return jsonify({'message':'Article added successfuly'}),200

        except Exception as e:
            return jsonify({'error':f"There was an error {e}"}),500

    return jsonify({'message':'Added sucessully'})
@app.route('/Api/deleteArticles/<id>',methods=['POST','GET'])
def deleteArticles(id):
    if request.method=='post':
        try:
            data = request.get_json()
            if not(data):
                return jsonify({'error':'Error, Supply Article ID'},404)
            id = data.get('id')
            sql="SELECT * FROM blog WHERE id=%s"
            cursor=connection.cursor()
            cursor.execute(sql,(id))
            if cursor.rowcount==0:
                return jsonify({'error':'The Article Was Nof Found'},404)
            else:
                try:
                    deleteArticle = "DELETE * FROM blog WHERE id=%s"
                    cursor=connection.cursor()
                    cursor.execute(deleteArticle,(id))
                    return jsonify({'message':'Article Deleted'},200)
                except Exception as e:
                    return jsonify({'error':f"There was an error {e}"},500)

        except Exception as e:
            return jsonify({'error':'Server Error'},500)
    return jsonify({'message':'deleted successfully'})
if __name__=="__main__":
    app.run(debug=True)