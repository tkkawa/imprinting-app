import argparse
import datetime
import sqlite3

from config import DB_PATH


class WorkingTimeReader:
    
    @staticmethod
    def read_working_time(db_path : str, target_user: str, date: str) -> None:
        """Insert the user's information into database
        Args:
            db_path(str): path to the git_slack.db
            new_data(tuple): user information, (slack_user_id, github_username)
        """
        assert type(db_path) == str, "The type of db_path should be string"
        assert type(target_user) == str, "The type of target_user should be string"
        assert type(date) == str, "The type of date should be string"

        with sqlite3.connect(db_path) as con:
            try:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT slack_user_id FROM usernames WHERE username=?", (target_user,)
                )
                slack_id = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT * FROM time_data"
                )
                cursor.execute(
                    "SELECT working_time FROM time_data WHERE slack_user_id=? AND date=?", (slack_id, date)
                )

                print(f"{target_user}'s working time on {date} is ", cursor.fetchone()[0])

                con.commit()
            except KeyError:
                con.rollback()
                print("An error has occurred in the database processing.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="target_user")
    parser.add_argument("-param2", type=str, default=None, help="date")
    args = parser.parse_args()
    
    target_user = args.param1
    date = args.param2
    db_path = DB_PATH.format(DB_NAME="imprinting.db")

    WorkingTimeReader.read_working_time(db_path, target_user, date)
