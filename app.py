
import pymysql.cursors
from flask import *
import pymysql
from flask_cors import CORS
from datetime import datetime
import requests
# connection=pymysql.connect(user='root',database='vertexlabs',host='localhost')
connection=pymysql.connect(user='sql7770379',database='sql7770379',host='sql7.freesqldatabase.com',password='zsJSBacLzW')
app=Flask(__name__)
CORS(app)
@app.route('/Api/addArticle',methods=['POST','GET'])
def addArticle():
    # try:
    #     connection = pymysql.connect(user='sql7770379', database='sql7770379', host='sql7.freesqldatabase.com',password='zsJSBacLzW')
    # except Exception as e:
    #     return jsonify({'message':'Failed to connect to DB'}
    now=datetime.now()
    today=now.strftime("%B %d, %Y")
    if request.method=='POST':
        try:
            data=request.get_json()
            if not(data):
                return jsonify({'error':'No data found'}),404
            title = data.get('title')
            author = data.get('author')
            content = data.get('content')
            date = today
            featuredImage = data.get('featuredImage')
            views = data.get('views')
            comment = data.get('commentEnabled')
            readTime = data.get('readTime')
            if comment==1:
                commentEnabled="True"
            else:
                commentEnabled="False"
            sql="INSERT INTO blog(title,author,content,date,featuredImage,views,commentEnabled,readTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            cursor.execute(sql,(title,author,content,date,featuredImage,views,commentEnabled,readTime))
            connection.commit()
            return jsonify({'message':'Article added successfuly'}),200

        except Exception as e:
            return jsonify({'error':f"There was an error {str(e)}"}),500

    return jsonify({'message':'No Requests made'})

@app.route('/Api/getArticles',methods=['GET','POST'])
def getArticles():
    try:
        sql = "SELECT * FROM blog"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        article = cursor.fetchall()
        return jsonify(article), 200
    except Exception as e:
        return jsonify({'message': f"Server error {str(e)}"}), 500

    # return jsonify({'message':'No requests found'})

@app.route('/Api/getImages')
def images():
    try:
        category = request.args.get('category', 'catgirl')
        res=requests.get(f'https://api.nekosia.cat/api/v1/images/catgirl')
        if res.status_code==200:
            data=res.json()
            if data['success']:
                url = {
                    'imgUrl': data['image']['original']['url']
                }
                return jsonify(url),200
            else:
                return jsonify({'message':'no image found'}),404
        else:
            return jsonify({'message':'Not found'}),404
    except Exception as e:
        return jsonify({'message':'Forbidden'}),500
@app.route('/Api/deleteArticles/<id>',methods=['POST','GET'])
def deleteArticles(id):
    # if request.method=='GET':
        # try:
            # data = request.get_json()
            # if not(data):
            #     return jsonify({'error':'Error, Supply Article ID'},404)
            # id = data.get('id')
        #     sql="SELECT * FROM blog WHERE id=%s"
        #     cursor=connection.cursor()
        #     cursor.execute(sql,(id))
        #     if cursor.rowcount==0:
        #         return jsonify({'error':'The Article Was Nof Found'},404)
        #     else:
        #         try:
        #             deleteArticle = "DELETE FROM blog WHERE id>%s"
        #             cursor=connection.cursor()
        #             cursor.execute(deleteArticle,(id))
        #             connection.commit()
        #             return jsonify({'message':'Article Deleted'},200)
        #         except Exception as e:
        #             return jsonify({'error':f"There was an error {e}"},500)
        #
        # except Exception as e:
        #     return jsonify({'error':f"Server Error {str(e)}"},500)
    try:
        deleteArticle = "DELETE FROM blog"
        cursor = connection.cursor()
        cursor.execute(deleteArticle)
        connection.commit()
        return jsonify({'message': 'deleted successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed terribly'})
if __name__=="__main__":
    app.run(debug=True)