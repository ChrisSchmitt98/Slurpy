class SlippiActionCounts(db.model):
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


