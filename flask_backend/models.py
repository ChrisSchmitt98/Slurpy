from app import db
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


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
class SlippiActionCounts():
    """A slippi action counts"""

    def __init__(self, filename, connect_code, wavedash, waveland, airdodge, dashdance, spotdodge, ledgegrab, roll, lcancel_success_ratio, grab_success, grab_fail, tech_away, tech_in, tech, tech_fail, wall_tech_success_ratio, datetime):
        self.filename = filename
        self.connect_code = connect_code
        self.wavedash = wavedash
        self.waveland = waveland
        self.airdodge = airdodge
        self.dashdance = dashdance
        self.spotdodge = spotdodge
        self.ledgegrab = ledgegrab
        self.roll = roll
        self.lcancel_success_ratio = lcancel_success_ratio
        self.grab_success = grab_success
        self.grab_fail = grab_fail
        self.tech_away = tech_away
        self.tech_in = tech_in
        self.tech = tech
        self.tech_fail = tech_fail
        self.wall_tech_success_ratio = wall_tech_success_ratio
        self.datetime = datetime

    def __repr__(self):
        return "SlippiActionCount({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(self.filename, self.connect_code, self.wavedash, self.waveland, self.airdodge, self.dashdance, self.spotdodge, self.ledgegrab, self.roll, self.lcancel_success_ratio, self.grab_success, self.grab_fail, self.tech_away, self.tech_in, self.tech, self.tech_fail, self.wall_tech_success_ratio, self.datetime)

class SlippiOverall:
    """A slippi action counts"""

    def __init__(self, filename, lcancel, datetime=""):
        self.filename = filename
        self.lcancel = lcancel
        self.datetime = datetime

    def __repr__(self):
        return "Slippi('{}','{}')".format(self.filename, self.lcancel)


