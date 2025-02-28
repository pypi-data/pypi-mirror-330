import logging
import sqlite3
from os import PathLike
from pathlib import Path
from typing import NamedTuple, Optional

SCHEMA = """
CREATE TABLE server(
  id INTEGER PRIMARY KEY,
  server TEXT UNIQUE
);

CREATE TABLE user(
  id INTEGER PRIMARY KEY,
  server_id INTEGER NON NULL,
  user_id TEXT NON NULL,
  username TEXT NON NULL,

  FOREIGN KEY(server_id) REFERENCES server(id),
  UNIQUE (server_id, user_id),
  UNIQUE (server_id, username)
);

CREATE TABLE direct_channel(
  id INTEGER PRIMARY KEY,
  server_id INTEGER NON NULL,
  me INTEGER NON NULL,
  them INTEGER NON NULL,
  direct_channel_id TEXT NON NULL,

  FOREIGN KEY(server_id) REFERENCES server(id),
  FOREIGN KEY(me) REFERENCES user(id),
  FOREIGN KEY(them) REFERENCES user(id),
  UNIQUE(me, them, direct_channel_id)
);

CREATE INDEX user_server_id ON user(server_id);
CREATE INDEX user_user_id ON user(user_id);
CREATE INDEX user_username ON user(username);
"""


class MattermostUser(NamedTuple):
    user_id: str
    username: str


def user_factory(_cursor: sqlite3.Cursor, row: tuple[str, str]) -> MattermostUser:
    return MattermostUser(*row)


ORDER_USER = "SELECT user_id, username FROM user WHERE "
SERVER = "(SELECT id FROM server WHERE server = ?)"


class Cache:
    def __init__(self, filename: PathLike):
        exists = Path(filename).exists()

        self.con = con = sqlite3.connect(filename)

        self.user_cur = self.con.cursor()
        self.user_cur.row_factory = user_factory  # type:ignore

        # (slidge_user_id, channel_id) → message_id
        self.__last_msg_id = dict[tuple[str, str], str]()

        if exists:
            log.debug("File exists")
            return
        with con:
            log.debug("Creating schema")
            con.executescript(SCHEMA)

    def add_server(self, server: str):
        with self.con:
            self.con.execute(
                "INSERT OR IGNORE INTO server(server) VALUES(?)", (server,)
            )

    def add_user(self, server: str, user_id: str, username: str):
        with self.con:
            query = (
                f"INSERT OR IGNORE INTO user(server_id, user_id, username) "
                f"VALUES({SERVER}, ?, ?)"
            )
            values = [server, user_id, username]
            log.debug("Query: %s -> %s", query, values)
            self.con.execute(query, values)

    def __get(self, server: str, key: str, value: str) -> MattermostUser:
        query = ORDER_USER + f"{key} = ? AND server_id = {SERVER}"
        with self.con:
            res = self.user_cur.execute(query, (value, server))
            return res.fetchone()

    def get_by_user_id(self, server: str, user_id: str) -> MattermostUser:
        return self.__get(server, "user_id", user_id)

    def get_user_by_direct_channel_id(
        self, server: str, slidge_user_id: str, direct_channel_id: str
    ) -> MattermostUser:
        with self.con:
            res = self.user_cur.execute(
                "SELECT user_id, username FROM user WHERE "
                "id = (SELECT them FROM direct_channel WHERE direct_channel_id = ? "
                "AND server_id = (SELECT id FROM server WHERE server = ?) "
                "AND me = (SELECT id FROM user WHERE user_id = ?))",
                (direct_channel_id, server, slidge_user_id),
            )
            return res.fetchone()

    def add_direct_channel(
        self,
        server: str,
        slidge_user_id: str,
        other_user_id: str,
        direct_channel_id: str,
    ):
        with self.con:
            self.con.execute(
                "INSERT OR IGNORE INTO direct_channel(server_id, me, them, direct_channel_id) "
                "VALUES ((SELECT id FROM server WHERE server = ?),"
                "(SELECT id FROM user WHERE user_id = ?),"
                "(SELECT id FROM user WHERE user_id = ?),"
                "?)",
                (server, slidge_user_id, other_user_id, direct_channel_id),
            )

    def get_direct_channel_id(
        self, server: str, slidge_user_id: str, other_user_id: str
    ) -> Optional[str]:
        with self.con:
            row = self.con.execute(
                "SELECT direct_channel_id FROM direct_channel WHERE "
                "server_id = (SELECT id FROM server where server = ?) "
                "AND me = (SELECT id FROM user where user_id = ?) "
                "AND them = (SELECT id FROM user where user_id = ?)",
                (server, slidge_user_id, other_user_id),
            ).fetchone()
            if row is None:
                return None
            return row[0]

    def get_by_username(self, server: str, username: str) -> MattermostUser:
        return self.__get(server, "username", username)

    def msg_id_get(self, slidge_user_id: str, channel_id: str) -> Optional[str]:
        return self.__last_msg_id.get((slidge_user_id, channel_id))

    def msg_id_store(self, slidge_user_id: str, channel_id: str, post_id: str):
        self.__last_msg_id[(slidge_user_id, channel_id)] = post_id


log = logging.getLogger(__name__)
