from logging import getLogger
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import Middleware
from pathlib import Path
from typing import Union, Tuple


class ReadOnlyMiddleware(Middleware):
    """
    Make sure no write ever occurs
    """

    def __init__(self, storage_cls=TinyDB.DEFAULT_STORAGE):
        super().__init__(storage_cls)


    def write(self, data):
        raise ReadOnlyException('You cannot write to a readonly db')


class ReadOnlyException(ValueError):
    pass

def only_main(f):
    '''assumes first argument is id, and must be "main"'''
    def wrapper(self, *args, **kwargs):
        _id = args[0]
        db, db_id = EventModel.parse_id(_id)
        if db != 'main':
            raise ReadOnlyException('You called a write operation on a readonly db')
        return f(self, db_id, *args[1:], **kwargs)
    return wrapper


class EventModel(object):
    def __init__(self, uri, additional_db_dir=None):
        self.uri = uri
        self.additional_db_dir = Path(additional_db_dir) if additional_db_dir else None
        self._dbs = {}
        self.log = getLogger(self.__class__.__name__)
        self.reload()

    def reload(self):
        for db in self._dbs.values():
            db.close()
        self._dbs['main'] = TinyDB(self.uri, indent=2)
        if self.additional_db_dir is not None:
            if self.additional_db_dir.is_dir():
                for db_file in self.additional_db_dir.glob('*.db.json'):
                    name = db_file.name[:-8]
                    if name == 'main':
                        self.log.warning("%s db file name is not valid (any other name.db.json would have been ok!", str(db_file.name))
                        continue
                    if not name.isalpha():
                        self.log.warning("%s db file name is not valid: it must be alphabetic only", str(db_file.name))
                        continue
                    try:
                        self._dbs[name] = TinyDB(
                                str(db_file),
                                storage=ReadOnlyMiddleware(JSONStorage),
                                default_table='actions'
                        )
                    except ReadOnlyException:
                        # TinyDB adds the default_table if it is not present at read time.
                        # This should not happen at all for a ReadOnlyMiddleware db, but at least we can notice it and
                        # properly signal this to the user.
                        self.log.error("Could not load db %s: 'actions' table is missing", db_file.name)
                        continue

        self.log.debug('Loaded %d databases: %s', len(self._dbs), ','.join(self._dbs.keys()))

        self._actions = self._dbs['main'].table("actions")
        self._alarms = self._dbs['main'].table("alarms")

    @staticmethod
    def canonicalize(eid_or_aid: Union[str, int]) -> str:
        try:
            int(eid_or_aid)
        except ValueError:
            return eid_or_aid
        return 'main:%d' % int(eid_or_aid)

    @staticmethod
    def parse_id(eid_or_aid: Union[str, int]) -> Tuple[str, int]:
        try:
            int(eid_or_aid)
        except ValueError:
            pass
        else:
            return ('main', int(eid_or_aid))

        dbname, num = eid_or_aid.split(':')
        return (dbname, int(num))
        

    def get_action_by_id(self, action_id: Union[str, int]):
        canonical = self.canonicalize(action_id)
        db, db_action_id = self.__class__.parse_id(canonical)
        out = self._dbs[db].table('actions').get(eid=db_action_id)
        if out is None:
            return None
        out.doc_id = canonical
        return out

    def get_alarm_by_id(self, alarm_id):
        db, alarm_id = self.__class__.parse_id(alarm_id)
        return self._dbs[db].table('alarms').get(eid=alarm_id)

    def get_actions_by_alarm(self, alarm):
        for action_id in alarm.get("actions", []):
            action = self.get_action_by_id(action_id)
            if action is None:
                continue
            yield action

    def get_all_alarms(self) -> list:
        out = []
        for db in self._dbs:
            for alarm in self._dbs[db].table('alarms').all():
                alarm.doc_id = '%s:%s' % (db, alarm.doc_id)
                out.append(alarm)
        return out

    def get_all_actions(self) -> list:
        out = []
        for db in self._dbs:
            for action in self._dbs[db].table('actions').all():
                action.doc_id = '%s:%s' % (db, action.doc_id)
                out.append(action)
        return out

    def get_all_alarms_expanded(self):
        for alarm in self.get_all_alarms():
            for action in self.get_actions_by_alarm(alarm):
                yield alarm, action

    def add_event(self, alarm, actions):
        action_ids = [self.add_action(a) for a in actions]
        alarm["actions"] = action_ids
        return self._alarms.insert(alarm)

    def add_action(self, action):
        return self._actions.insert(action)

    def add_alarm(self, alarm):
        return self.add_event(alarm, [])

    @only_main
    def update_alarm(self, alarmid, new_fields={}):
        return self._alarms.update(new_fields, eids=[alarmid])

    @only_main
    def update_action(self, actionid, new_fields={}):
        return self._actions.update(new_fields, eids=[actionid])

    @only_main
    def delete_alarm(self, alarmid):
        return self._alarms.remove(eids=[alarmid])

    @only_main
    def delete_action(self, actionid):
        return self._actions.remove(eids=[actionid])
