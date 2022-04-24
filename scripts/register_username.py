import argparse
import sqlite3

from config import DB_PATH


class Username:
    
    @staticmethod
    def insert_username(db_path : str, new_data: tuple) -> None:
        """Insert the user's information into database
        Args:
            db_path(str): path to the git_slack.db
            new_data(tuple): user information, (slack_user_id, github_username)
        """
        assert type(db_path) == str, "The type of db_path should be string"
        assert type(new_data[0]) == str, "The type of user_id should be string"
        assert type(new_data[1]) == str, "The type of user should be string"
        
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
                print('The username has been registered in the database.')
            else:
                con.rollback()
                print('The username is already registered in the database.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="slack_user")
    parser.add_argument("-param2", type=str, default=None, help="username")
    args = parser.parse_args()
    new_data = (args.param1, args.param2)

    db_path = DB_PATH.format(DB_NAME="imprinting.db")

    Username.insert_username(db_path, new_data) 
