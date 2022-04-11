


from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
# import re


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'          # vm ip
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'      # vm root pass
app.config['MYSQL_DB'] = 'todo1'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE user_name = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['user_id']
			session['username'] = account['user_name']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_name= % s',(username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif 1:
            cursor.execute('INSERT INTO users(user_name,password) VALUES(%s,%s)',(username,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'

        return render_template('login.html', msg = msg)

    msg = 'Please fill out the form !'

    return render_template('register.html', msg = msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("home.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE user_id = % s', (session['id'], ))
		account = cursor.fetchone()	
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/lists")
def lists():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s', (session['id'], ))
        account = cursor.fetchall()
        list_names = []
        for row in account:
            if row['list_name'] not in list_names:
                list_names.append(row['list_name'])
        return render_template("displayList.html", lists = list_names)

@app.route("/list_items/<list_name>")
def list_items(list_name):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s and list_name= % s', (session['id'],list_name))
        account = cursor.fetchall()
        return render_template("displayItems.html", items = account, lname = list_name)
        
@app.route("/addItem/<list_name>", methods =['GET', 'POST'])
def addItem(list_name):
    if 'loggedin' in session and request.method=='POST':
        item = request.form['item']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s and list_name= % s', (session['id'],list_name))
        account = cursor.fetchall()
        list_items = []
        for row in account:
            list_items.append(row['list_item'])
        if item in list_items:
            msg = 'item already exists!!'
            return render_template('displayItems.html',items=account, lname=list_name, msg = msg)
        cursor.execute('INSERT INTO lists VALUES(%s,%s,%s)',(list_name,item,session['id']))
        mysql.connection.commit()
        return redirect(url_for('list_items',list_name=list_name))

@app.route("/deleteItem/<list_name>", methods =['GET', 'POST'])
def deleteItem(list_name):
    if 'loggedin' in session and request.method=='POST':
        item = request.form['item1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s and list_name= % s', (session['id'],list_name))
        account = cursor.fetchall()
        list_items = []
        for row in account:
            list_items.append(row['list_item'])
        if item not in list_items:
            msg = 'item not found!!'
            return render_template('displayItems.html',items=account, lname=list_name, msg1 = msg)
        cursor.execute('DELETE FROM lists WHERE list_name=%s and list_item=%s and user_id=%s',(list_name,item,session['id']))
        mysql.connection.commit()
        return redirect(url_for('list_items',list_name=list_name))

@app.route("/listDel/<list_name>")
def listDel(list_name):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM lists where list_name=%s and user_id=%s',(list_name,session['id']))
        mysql.connection.commit()
        return redirect(url_for('lists'))

@app.route("/createL")
def createL():
    return render_template("createList.html")

@app.route("/verifyList", methods=['GET','POST'])
def verifyList():
    if request.method=='POST' and 'loggedin' in session:
        list_name = request.form['lname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s', (session['id'], ))
        account = cursor.fetchall()
        list_names = []
        for row in account:
            if row['list_name'] not in list_names:
                list_names.append(row['list_name'])
        if list_name in list_names:
            msg = "list already exists, enter a new name!!"
            return render_template('createList.html', val1=list_name, fail = msg)
        msg = "good choice!! add items"
        return render_template('createItem.html', val1=list_name, success = msg)

@app.route("/createList",methods=['GET','POST'])
def createList():
    if request.method=='POST' and 'loggedin' in session:
        l_name = request.form['lname']
        l_item = request.form['item']
        flag = 0
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lists WHERE user_id = % s', (session['id'], ))
        account = cursor.fetchall()
        list_names = []
        for row in account:
            if row['list_name'] not in list_names:
                list_names.append(row['list_name'])

        cursor.execute('SELECT * FROM lists WHERE user_id = % s and list_name= % s', (session['id'],l_name))
        account = cursor.fetchall()
        list_items = []
        for row in account:
            list_items.append(row['list_item'])
        
        if l_item in list_items:
            msg = 'item already exists!!'
            return render_template('createList.html',msg = msg, val1 = l_name)
        
        if l_name not in list_names:
            msg1 = "good choice!!"
            flag = 1
        
        
        cursor.execute("INSERT INTO lists VALUES(%s,%s,%s)",(l_name,l_item,session['id']))
        mysql.connection.commit()
        msg = 'item added successfully'
        if flag==1:
            return render_template('createList.html',msg3 = msg, msg1=msg1, val1 = l_name)
        else:
            msg1=""
            msg = 'item added successfully'
            return render_template('createList.html',msg1 = msg1, msg3 = msg, val1 = l_name)            

@app.route("/tasks")
def tasks():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tasks WHERE user_id = % s', (session['id'], ))
        account = cursor.fetchall()
        return render_template("displayTask.html", account=account)

@app.route("/addTask", methods =['GET', 'POST'])
def addTask():
    msg = ""
    if 'loggedin' in session and request.method == 'POST':
        task = request.form['task']
        if task!="":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO tasks(task_desc,t_status,user_id) VALUES(%s,%s,%s)',(task,'0',session['id']))
            cursor.execute('SELECT * FROM tasks WHERE user_id = % s and task_desc = % s',(session['id'],task))
            row = cursor.fetchone()
            task_id = row['task_id']
            task = task.split()
            for i in task:
                if '#' in i:
                    cursor.execute('INSERT INTO HASHTAGS VALUES(%s,%s,%s)',(i,session['id'],task_id))
            mysql.connection.commit() 
            msg = "task added successfully"
        return redirect(url_for('tasks'))

@app.route("/updateStatus/<int:task_id>")
def updateStatus(task_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from tasks where task_id=%s',(task_id,))
        row = cursor.fetchone()
        if row['t_status']=='0':
            cursor.execute('UPDATE tasks set t_status= %s where task_id=%s',('1',task_id))
        else:
            cursor.execute('UPDATE tasks set t_status= %s where task_id=%s',('0',task_id))
        mysql.connection.commit() 
    return redirect(url_for('tasks'))

@app.route("/deleteTask/<int:task_id>")
def deleteTask(task_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE from tasks where task_id=%s',(task_id, ))
        mysql.connection.commit() 
    return redirect(url_for('tasks'))

@app.route("/updateTask/<int:task_id>",methods=['POST'])
def updateTask(task_id):
    if 'loggedin' in session and request.method=='POST':
        task_desc = request.form['task1'].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE tasks set task_desc= %s where task_id=%s',(task_desc,task_id))
        cursor.execute('SELECT * FROM hashtags where task_id= %s',(task_id,))
        prev_hash = []
        rows = cursor.fetchall()
        for row in rows:
            prev_hash.append(row['hashtag'])
        task = task_desc.split()
        for i in task:
            if '#' in i and i not in prev_hash:
                try:
                    cursor.execute('INSERT INTO HASHTAGS VALUES(%s,%s,%s)',(i,session['id'],task_id))
                except:
                    pass 
            elif '#' in i and i in prev_hash:
                prev_hash.remove(i) 
        if len(prev_hash)>0:
            while len(prev_hash)!=0:
                target = prev_hash.pop()
                cursor.execute('DELETE FROM hashtags where hashtag=%s and task_id=%s',(target,task_id))

        mysql.connection.commit() 
    return redirect(url_for('tasks'))

@app.route("/search",methods=["POST"])
def search():
    msg = ""
    if 'loggedin' in session and request.method=="POST":
        target = request.form['hashtag']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hashtags where user_id=%s',(session['id'],))
        rows = cursor.fetchall()
        task_ids = set()
        for row in rows:
            if row['hashtag']==target:
                task_ids.add(row['task_id'])
        if len(task_ids)>0:
            account = []
            for id in task_ids:
                cursor.execute('SELECT * FROM tasks where task_id = % s',(id,))
                row = cursor.fetchone()
                account.append(row)
            return render_template('searchTag.html',account = account)
        else:
            msg = "No Results Found!"
            cursor.execute('SELECT * FROM tasks WHERE user_id = % s', (session['id'], ))
            account = cursor.fetchall()
            return render_template('displayTask.html',account = account, msg = msg)

@app.route('/viewAllHashtags')
def viewAllHashtags():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hashtags where user_id=%s',(session['id'],))
        rows = cursor.fetchall()
        hash_tags = []
        for row in rows:
            if row['hashtag'] not in hash_tags:
                hash_tags.append(row['hashtag'])
        if len(hash_tags)!=0:
            return render_template('displayHashTags.html',tags = hash_tags)
        else:
            msg = "No HashTags Found!"
            cursor.execute('SELECT * FROM tasks WHERE user_id = % s', (session['id'], ))
            account = cursor.fetchall()
            return render_template('displayTask.html',account = account, hmsg = msg)


if __name__ == "__main__":
    app.run(debug=True)
