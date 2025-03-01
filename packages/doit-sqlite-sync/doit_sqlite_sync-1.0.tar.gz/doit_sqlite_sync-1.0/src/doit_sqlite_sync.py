from doit.dependency import SqliteDB

class SqliteDBSync(SqliteDB):
    """ sqlite3 json backend always synchronized with disk """
    def __init__(self, name, codec):
        super().__init__(name, codec)

    def set(self, task_id, dependency, value):
        super().set(task_id, dependency, value)
        self._conn.execute('insert or replace into doit values (?,?)',
                           (task_id, self.codec.encode(self._cache[task_id])))
        self._conn.commit()
        self._dirty.remove(task_id)  # remove task that has been saved above
