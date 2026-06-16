import pandas as pd
import os
from datetime import datetime

FILE_NAME = "posts.csv"

# Create CSV if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "ID",
        "Caption",
        "Platform",
        "Schedule Date",
        "Status"
    ])
    df.to_csv(FILE_NAME, index=False)


def load_data():
    return pd.read_csv(FILE_NAME)


def save_data(df):
    df.to_csv(FILE_NAME, index=False)


def add_post():
    df = load_data()

    caption = input("Enter Caption: ")
    platform = input("Platform (Instagram/Facebook/LinkedIn/X): ")
    schedule = input("Schedule (YYYY-MM-DD HH:MM): ")

    try:
        datetime.strptime(schedule, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid Date Format")
        return

    if len(df) == 0:
        post_id = 1
    else:
        post_id = int(df["ID"].max()) + 1

    new_post = pd.DataFrame([{
        "ID": post_id,
        "Caption": caption,
        "Platform": platform,
        "Schedule Date": schedule,
        "Status": "Scheduled"
    }])

    df = pd.concat([df, new_post], ignore_index=True)
    save_data(df)

    print("Post Scheduled Successfully!")


def view_posts():
    df = load_data()

    if df.empty:
        print("No Posts Found")
    else:
        print(df)


def delete_post():
    df = load_data()

    try:
        pid = int(input("Enter Post ID: "))
    except ValueError:
        print("Invalid ID")
        return

    if pid not in df["ID"].values:
        print("Post Not Found")
        return

    df = df[df["ID"] != pid]
    save_data(df)

    print("Deleted Successfully")


def mark_posted():
    df = load_data()

    try:
        pid = int(input("Enter Post ID: "))
    except ValueError:
        print("Invalid ID")
        return

    if pid not in df["ID"].values:
        print("Post Not Found")
        return

    df.loc[df["ID"] == pid, "Status"] = "Posted"
    save_data(df)

    print("Status Updated")


def check_due_posts():
    df = load_data()

    now = datetime.now()

    for index, row in df.iterrows():
        if row["Status"] == "Scheduled":
            schedule = datetime.strptime(
                row["Schedule Date"],
                "%Y-%m-%d %H:%M"
            )

            if schedule <= now:
                print("--------------------------------")
                print("POST READY")
                print("Platform :", row["Platform"])
                print("Caption  :", row["Caption"])
                print("--------------------------------")


def menu():

    while True:

        print("\n===== SOCIAL MEDIA AUTOMATION =====")
        print("1. Add New Post")
        print("2. View Posts")
        print("3. Delete Post")
        print("4. Mark as Posted")
        print("5. Check Due Posts")
        print("6. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_post()

        elif choice == "2":
            view_posts()

        elif choice == "3":
            delete_post()

        elif choice == "4":
            mark_posted()

        elif choice == "5":
            check_due_posts()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    menu()