from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector

from BL.create_severity_avg_files import parseJSON


app = Flask(__name__)

# ======== Database ==============================

mydb = mysql.connector.connect(

    host="localhost",
    user="root",
    password="MayanAsifOno8",
    database="primary_db"
)

mycursor = mydb.cursor()

# ======== Upload folder =========================
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER



# =========================================================

@app.route('/')
def index():
        # Set The upload HTML template '\templates\index.html'
        return render_template('index.html')

# =========================================================

@app.route("/", methods=['POST'])
def uploadFiles():
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            parseJSON(file_path, mydb, mycursor)
           
        # save the file
        return redirect(url_for('index'))


# =========================================================

       
app.run()