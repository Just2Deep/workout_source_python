import harperdb
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://cloud-1-just2deep.harperdbcloud.com"

USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


db = harperdb.HarperDB(url=url, username=USERNAME, password=PASSWORD)


SCHEMA = "workout_repo"
TABLE = "workouts"
TABLE_TODAY = "workout_today"


def insert_workout(workout_data):
    return db.insert(SCHEMA, TABLE, [workout_data])


def delete_workout(workout_id):
    return db.delete(SCHEMA, TABLE, [workout_id])


def get_all_workout():
    try:
        return db.sql(
            f"SELECT video_id, title, channel, duration FROM {SCHEMA}.{TABLE}"
        )
    except harperdb.exceptions.HarperDBError as e:
        print(e)
        return []


def get_workout_today():
    return db.sql(f"SELECT * FROM {SCHEMA}.{TABLE_TODAY} WHERE id = 0")


def update_workout_today(workout_data, insert=False):
    workout_data["id"] = 0
    if insert:
        return db.insert(SCHEMA, TABLE, [workout_data])
    return db.update(SCHEMA, TABLE_TODAY, [workout_data])
