from datetime import datetime
import inspect
# TODO i18n multiple files

class BaseModel(object):
    def __init__(self, id):
        self.id = id

    def to_json(self):
        return self.__dict__  #Equivalent to vars(object)

    @classmethod
    def build_from_json(cls, json_data):
        if json_data is not None:
            build_list = []
            par_list = inspect.getargspec(cls.__init__).args[1:] #Get parameters names removing self
            try:
                for i in par_list:
                    build_list.append(json_data[i])
                return cls(*build_list)
            except KeyError as e:
                raise Exception("Key not found in json_data: %s" % (repr(e)))
        else:
            raise Exception("No data to create Project from!")

class TerrariaStatus(BaseModel):
    def __init__(self, user, status, ip, date=datetime.utcnow()):
        self.user = user
        self.status = status
        self.ip = ip
        self.date = date
        self.is_milestone = False

    def get_update_message(self, with_date=False):
        text= ""

        if with_date:
            fdate = self.date.strftime("%d/%m/%y %H:%M")
            text+= "[%s] " % fdate
        if self.status:
            text+= _("(%s) Terraria server is On (IP:%s)") % (self.user , self.ip)
        else:
            text+= _("(%s) Terraria server is Off")  % (self.user)

        return text

class TerrariaMilestone(BaseModel):
    def __init__(self, user, milestone_text, date=datetime.utcnow()):
        self.user = user
        self.milestone_text = milestone_text
        self.date = date
        self.is_milestone = True

    def get_update_message(self, with_date=False):
        if with_date:
            fdate = self.date.strftime("%d/%m/%y %H:%M")
            return _("[%s] (%s) Milestone: %s") % (fdate, self.user , self.milestone_text)
        else:
            return _("(%s) Milestone: %s") % (self.user , self.milestone_text)