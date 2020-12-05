import sqlite3
import relbot.json.json_reader
from relbot.json import json_reader
from relbot.singleton import Singleton

CONFIG_NAME = 'db_cfg.json'


class DatabaseManager(Singleton):
    def init(self, *args, **kwds):
        self.config = json_reader.read(CONFIG_NAME)
        self.verify_table_exists('users')
        self.connection = None

    def _open_connection(self):
        self.connection = sqlite3.connect(self.config['db']['filename'])

    def _close_connection(self):
        self.connection.close()

    def create_users_table(self):
        self._open_connection()
        cur = self.connection.cursor()

        cur.execute(''' CREATE TABLE `users` (`user_id` INTEGER PRIMARY KEY, `positive_relationship` INTEGER, `negative_relationship` INTEGER) ''')

        self.connection.commit()
        self._close_connection()

    def insert_user(self, user_id, positive_rep: int = 0, negative_rep: int = 0):
        self._open_connection()
        cur = self.connection.cursor()

        cur.execute(''' INSERT INTO `users` (`user_id`, `positive_relationship`, `negative_relationship`) VALUES (?, ?, ?) ''', (user_id, positive_rep, negative_rep))
        print('Added entry {0}'.format(user_id))

        self.connection.commit()
        self._close_connection()

    def update_user(self, user_id: int, positive_rep: int, negative_rep: int):
        self._open_connection()
        cur = self.connection.cursor()

        cur.execute(''' UPDATE `users` SET `positive_relationship` = ?, `negative_relationship` = ? WHERE `user_id` = ? ''', (positive_rep, negative_rep, user_id))
        print('Updated entry {0}'.format(user_id))

        self.connection.commit()
        self._close_connection()

    def verify_user_exists(self, user_id: int):
        self._open_connection()
        cur = self.connection.cursor()

        cur.execute(''' SELECT * FROM `users` WHERE `user_id` = ? ''', (user_id,))
        result = cur.fetchone()

        self._close_connection()
        return result

    def verify_table_exists(self, table_name: str):
        self._open_connection()
        cur = self.connection.cursor()

        cur.execute(''' SELECT count(`name`) as 'exists' FROM `sqlite_master` WHERE `type` = 'table' AND `name` = 'users' ''')

        if cur.fetchone()[0] == 1:
            return

        self.connection.commit()
        self._close_connection()
        self.create_users_table()
