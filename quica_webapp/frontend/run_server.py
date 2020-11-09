from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
from quica.quica import Quica



UPLOAD_FOLDER = '/user_data'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app_flask = Flask(__name__)
app_flask.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app_flask.secret_key = 'some secret key'

@app_flask.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app_flask.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            dataframe = pd.read_excel(file)

            quica = Quica(dataframe=dataframe)
            latex = (quica.get_latex())
            table = (quica.get_results())

            return render_template('index.html', latex=latex, tables=[table.to_html(classes=["table-bordered", "table-striped", "table-hover"])], titles=table.columns.values)

if __name__ == '__main__':
    app_flask.run(debug=True)
