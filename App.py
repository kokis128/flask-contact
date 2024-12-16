from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL


app = Flask('__name__')
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='flaskcontacts'
app.secret_key = 'a1b2c3d4e5f6g7h8' 
mysql=MySQL(app)
@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('select * from contacts')
    data=cur.fetchall()
  
    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
       fullname = request.form['fullname']
       phone= request.form['phone']
       email= request.form['email']
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO contacts(fullname,phone,email) values (%s, %s, %s)',
                   (fullname,phone,email))
       mysql.connection.commit() 
       
       flash('contacto agregado')
       return redirect(url_for('index'))
   
        

@app.route('/edit/<id>')
def get_contact(id):
   cur=mysql.connection.cursor()
   cur.execute('select * from contacts where id=%s',(id))
   data = cur.fetchall()
   print(data[0])
   return render_template('edit-contact.html', contact=data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method=='POST':
        fullname=request.form['fullname']
        phone=request.form['phone']
        email=request.form['email']
        cur = mysql.connection.cursor()
        
    
    cur.execute(""" 
                UPDATE contacts 
                set fullname = %s,
                email = %s,
                phone =%s
                Where id = %s
                
                
                """,(fullname,phone,email,id))
    mysql.connection.commit()
    flash('contacto actualizado satisfactoriamente')
    return redirect(url_for('index'))
   

@app.route('/delete/<string:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('delete from contacts where id ={0}'.format(id))
    mysql.connection.commit()
    flash('contacto eliminado satisfactoriamente')
    return redirect(url_for('index'))
    
   

if __name__=='__main__':
    app.run(port=3000, debug =True)