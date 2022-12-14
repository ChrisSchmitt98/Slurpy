from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from slippi.parse import parse
from slippi.parse import ParseEvent
from slippi import Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ultra_secret_key'
app.config['UPLOAD_FOLDER'] = 'static\\files'
global db 
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=['POST','GET'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        new_file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(new_file.filename))
        new_file.save(file_path) # Then save the file
        current_game = Game(file_path)
        print(current_game.metadata.players)
        player1_tag = current_game.metadata.players[0].netplay.code
        player2_tag = current_game.metadata.players[1].netplay.code
        new_slippi_file = SlippiFile(filename=new_file.filename,connect_code1=player1_tag,connect_code2=player2_tag)
        
        try:
            db.session.add(new_slippi_file)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the slippi file'
        return "File has been uploaded."
    
    slippi_files = SlippiFile.query.order_by(SlippiFile.id).all()
    return render_template('index.html', slippi_files=slippi_files, form=form)

if __name__ == '__main__':
    app.run(debug=True)