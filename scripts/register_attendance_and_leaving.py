import argparse
import datetime
import sqlite3

from config import DB_PATH


class TimeManager:
    
    @staticmethod
    def insert_arrival_time(db_path : str, user_id: str) -> None:
        """Insert the arrival time into database
        Args:
            db_path(str): Path to the imprinting.db
            user_id(str): User's id for which the arrival time is to be registered
        """
        assert type(db_path) == str, "The type of db_path should be string"
        assert type(user_id) == str, "The type of user_id should be string"

        with sqlite3.connect(db_path) as con:
            try:
                cursor = con.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS time_data(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    slack_user_id TEXT,\
                    date TEXT,\
                    arrival_time TEXT,\
                    departure_time TEXT,\
                    working_time TEXT)"
                )

                date = str(datetime.datetime.now().date())
                time = str(datetime.datetime.now().time())
                cursor.execute(
                    "SELECT arrival_time FROM time_data WHERE slack_user_id=? AND date=?", (user_id, date)
                )
                entry = cursor.fetchone()

                if entry is None:
                    cursor.execute(
                        'INSERT INTO time_data(slack_user_id, date, arrival_time)\
                        VALUES (?, ?, ?)', (user_id, date, time)
                    )

                    con.commit()
                    print('The arrival time  has been registered in the database.')
                else:
                    con.rollback()
                    print("The arrival time is already  registered in the database.")

            except KeyError:
                con.rollback()
                print("An error has occurred in the database processing")

    @staticmethod
    def insert_departure_time(db_path : str, user_id: str) -> None:
        """Insert the departure into database
        Args:
            db_path(str): Path to the imprinting.db
            user_id(str): User's id for which the departure time is to be registered
        """
        assert type(db_path) == str, "The type of db_path should be string"
        assert type(user_id) == str, "The type of user_id should be string"

        with sqlite3.connect(db_path) as con:
            try:
                cursor = con.cursor()
                
                date = str(datetime.datetime.now().date())
                time = str(datetime.datetime.now().time())

                cursor.execute(
                    "SELECT departure_time FROM time_data WHERE slack_user_id=? AND date=?", (user_id, date)
                )
                entry = cursor.fetchone()

                if entry is None:
                    cursor.execute(
                        "SELECT arrival_time FROM time_data WHERE slack_user_id=? AND date=?", (user_id, date)
                    )
                    arrival_time = cursor.fetchall()[0][0]
                    arrival_time = datetime.datetime.strptime(arrival_time, "%H:%M:%S.%f")
                    time = datetime.datetime.strptime(time, "%H:%M:%S.%f")
                    working_time = time - arrival_time

                    time = str(time)
                    working_time = str(working_time)
                    cursor.execute(
                        f"UPDATE time_data SET departure_time=?, working_time=? WHERE date=?\
                        AND slack_user_id=?", (time, working_time, date, user_id)
                    )
                    con.commit()
                    print("The departure time has been registered in the database.")
                else:
                    con.rollback()
                    print("The departure time is already  registered in the database.")

            except KeyError:
                con.rollback()
                print("An error has occurred in the database processing")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="slack_user")
    parser.add_argument("-param2", type=str, default=None, help="mode")
    args = parser.parse_args()
    
    user_id = args.param1
    db_path = DB_PATH.format(DB_NAME="imprinting.db")

    if args.param2 == "start":
        TimeManager.insert_arrival_time(db_path, user_id)
    elif args.param2 == "end":
        TimeManager.insert_departure_time(db_path, user_id)
