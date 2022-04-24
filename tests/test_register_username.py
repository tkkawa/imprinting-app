import datetime

from scripts.register_username import Username
from scripts.register_attendance_and_leaving import TimeManager
from scripts.read_working_time import WorkingTimeReader


db_path = "test.db"
user = "test_user"
user_id = "0A5GW"


def test_username():
    Username.insert_username(db_path, (user_id, user))


def test_insert_time():
    TimeManager.insert_arrival_time(db_path, user_id)
    TimeManager.insert_departure_time(db_path, user_id)


def test_read_working_time():
    date = str(datetime.date.today())
    WorkingTimeReader.read_working_time(db_path, user, date)
