from __future__ import absolute_import
import pytz
from dungeon_world.models import TerrariaStatus, TerrariaMilestone

class Terraria(object):
    def __init__(self, db):
        self.db = db
        try:
            last_update = self.db.read_last_one("terraria_updates", query={"is_milestone" : False} )
            self.last_status_update = TerrariaStatus.build_from_json(last_update)
        except:
            self.last_status_update = TerrariaStatus(None, False, None)

        self.tzinfo = pytz.utc

    def get_status(self):
        return self.last_status_update.get_update_message()

    def get_log(self, amount, only_milestone=False, tzinfo=pytz.utc):
        if only_milestone:
            log_list = self.db.read_lastXdocuments("terraria_updates", amount, {"is_milestone" : True})
        else:
            log_list = self.db.read_lastXdocuments("terraria_updates", amount)

        log_text=""
        at_least_one_item = False
        for log in log_list:
            at_least_one_item = True
            log["date"] = pytz.utc.localize(log["date"]).astimezone(tzinfo)
            if log["is_milestone"]:
                tmp_update = TerrariaMilestone.build_from_json(log)
            else:
                tmp_update = TerrariaStatus.build_from_json(log)
            log_text += tmp_update.get_update_message(with_date=True) + "\n"
        if at_least_one_item:
            return log_text
        else:
            return False

    def get_ip(self):
        last_ip = self.last_status_update.ip
        if last_ip:
            return last_ip
        else:
            return _("There is no IP")

    def get_autonot(self, telegram_id):
        user = self.db.read_one("user_data", query={'user_id':telegram_id })
        if user:
            return user["in_autonot"]
        else:
            return False

    def set_autonot(self, autonot, user_id):
        self.db.update("user_data",
                       query={"user_id":user_id},
                       value={"in_autonot":autonot})
        return autonot

    def add_milestone(self, user=None, text=" " ):
        t_update = TerrariaMilestone(user, text)
        self.db.create("terraria_updates", t_update.to_json())
        return t_update.get_update_message()

    def change_status(self, status, user=None, ip=None ):
        t_update = TerrariaStatus(user, status, ip)
        self.db.create("terraria_updates", t_update.to_json())
        self.last_status_update = t_update
        return t_update.get_update_message()