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
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(app)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class SlippiFile(db.Model):
    """A slippi action counts"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    connect_code1 = db.Column(db.String(10), nullable=False)
    connect_code2 = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "SlippiOverall('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.filename, self.connect_code, self.input_counts, self.total_damage, self.kill_count, self.successful_conversions, self.successful_conversion_ratio, self.inputs_per_minute, self.digital_inputs_per_minute, self.openings_per_kill, self.damage_per_opening, self.neutral_win_ratio, self.counter_hit_ratio, self.beneficial_trade_ratio, self.datetime)

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