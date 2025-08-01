from flask import Flask, render_template, request
from flask import *
from datetime import datetime, timedelta
import os 
import json
import textwrap
import pandas as pd


app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'assets/shared_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#  for ishare

with open('assets/data_share/data.json') as json_file:
    dynamic_variables = json.load(json_file)
content=""

        
@app.route('/share/<share_string>',methods=['GET'])
def share_data_get(share_string):
    with open('assets/data_share/data.json') as json_file:
        dynamic_variables = json.load(json_file)

    if share_string not in dynamic_variables.keys():
        dynamic_variables[share_string]=''
    return render_template('share_page.html',editable_data= dynamic_variables[share_string],share_string=share_string,dynamic_variables=dynamic_variables)


# for ishare
@app.route('/share/<share_string>',methods=['POST'])
def share_data(share_string):
    content = request.form.get('content')
    if share_string not in dynamic_variables.keys():
        dynamic_variables[share_string]=  textwrap.dedent(str(content))
        with open('assets/data_share/data.json', 'w') as fp:
              json.dump(dynamic_variables, fp)
    else:
        
          dynamic_variables[share_string]= textwrap.dedent(str(content))
          with open('assets/data_share/data.json', 'w') as fp:
              json.dump(dynamic_variables, fp)

    
    with open('assets/data_share/data.json', 'w') as fp:
        json.dump(dynamic_variables, fp)

    return render_template('share_page.html',editable_data= dynamic_variables[share_string],share_string=share_string,dynamic_variables=dynamic_variables)



# for file share

@app.route('/file', methods=['POST','GET'])
def file_share():
    success_message = None
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files.sort()
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success_message = "File '{}' uploaded successfully.".format(filename)
    return render_template('file_share.html',files=files,success_message=success_message)


@app.route('/delete/<filename>', methods=['POST','DELETE','GET'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File deleted successfully'
    except FileNotFoundError:
        return 'File not found'
    except Exception as e:
        return 'An error occurred: {}'.format(str(e))


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

    

 
if __name__ == '__main__':
        
    app.run(host="0.0.0.0",port="5000")
    # app.run(debug= True)
