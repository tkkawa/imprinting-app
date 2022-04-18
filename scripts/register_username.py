import argparse
import sqlite3

from logging import getLogger, config

from config import DB_PATH, CONF_PATH


class Username:
    
    @staticmethod
    def insert_username(db_path : str, new_data: tuple) -> None:
        """Insert the user's information into database
        Args:
            db_path(str): path to the git_slack.db
            new_data(tuple): user information, (slack_user_id, github_username)
        """
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS usernames(\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                slack_user_id TEXT,\
                username TEXT,\
                created_at TEXT NOT NULL DEFAULT\
                (DATETIME('now', 'utc')),\
                updated_at TEXT NOT NULL DEFAULT\
                (DATETIME('now', 'utc')))"
            )

            cursor.execute(
                'SELECT * FROM usernames WHERE\
                (slack_user_id=? AND username=?)',
                (new_data)
            )

            entry = cursor.fetchone()

            if entry is None:
                cursor.execute(
                    'INSERT INTO usernames(slack_user_id, username)\
                    VALUES (?,?)',
                    (new_data[0], new_data[1])
                )
                con.commit()
                logger.info('The username has been registered in the database.')
            else:
                logger.warning('The username is already registered in the database.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="slack_user")
    parser.add_argument("-param2", type=str, default=None, help="username")
    args = parser.parse_args()
    new_data = (args.param1, args.param2)

    db_path = DB_PATH.format(DB_NAME="imprinting.db")
    logger = getLogger(__name__)

    Username.insert_username(db_path, new_data) 
