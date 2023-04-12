import random
import streamlit as st
from yt_extractor import get_info
import database_service as dbs


st.title("Workout App")


# @st.cache_resource
def get_workouts():
    return dbs.get_all_workout()


def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / 3600) % 24)

    text = ""
    if hours > 0:
        text += f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
    else:
        text += f"{minutes:02d}m:{seconds:02d}s"
    return text


menu_options = ("Today's workout", "All Workouts", "Add Workout")
selection = st.sidebar.selectbox("Menu", menu_options)


if selection == "All Workouts":
    st.markdown(f"## All Workouts")

    workouts = get_workouts()
    for wo in workouts:
        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo["title"])

        st.text(f'{wo["channel"]} - {get_duration_text(wo["duration"])}')

        ok = st.button("Delete Workout", key=wo["video_id"])

        if ok:
            dbs.delete_workout(wo["video_id"])
            st.runtime.legacy_caching.clear_cache()
            st.experimental_rerun()

        st.video(url)

    if not workouts:
        st.text("No Workouts in Database!")

elif selection == "Today's workout":
    st.markdown(f"## Today's workout")

    workouts = get_workouts()
    if not workouts:
        st.text("No Workouts in Database! Add a few to start working out.")
    else:
        wo = dbs.get_workout_today()

        if not wo:
            # workout is not defined for today
            workouts = get_workouts()
            n = len(workouts)
            idx = random.randint(0, n - 1)
            wo = workouts[idx]
            dbs.update_workout_today(wo, insert=True)
        else:
            wo = wo[0]

        if st.button("choose another workout"):
            workouts = get_workouts()
            n = len(workouts)
            if n > 1:
                idx = random.randint(0, n - 1)
                wo_new = workouts[idx]
                while wo_new["video_id"] == wo["video_id"]:
                    idx = random.randint(0, n - 1)
                    wo_new = workouts[idx]

                wo = wo_new
                dbs.update_workout_today(wo)
                st.runtime.legacy_caching.clear_cache()

        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo["title"])

        st.text(f'{wo["channel"]} - {get_duration_text(wo["duration"])}')
        st.video(url)

else:
    st.markdown(f"## Add Workout")

    url = st.text_input("Please Enter Video URL!")

    if url:
        workout_data = get_info(url)
        if workout_data is None:
            st.text("Could not find video")
        else:
            st.text(workout_data["title"])
            st.text(workout_data["channel"])
            st.video(url)
            if st.button("Add Workout"):
                dbs.insert_workout(workout_data)
                st.text("Added Workout")
                st.runtime.legacy_caching.clear_cache()
