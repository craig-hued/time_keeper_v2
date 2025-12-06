#
#   ooooooooooooo  o8o                                  oooo    oooo                                                                     .oooo.   
#   8'   888   `8  `"'                                  `888   .8P'                                                                    .dP""Y88b  
#        888      oooo  ooo. .oo.  .oo.    .ooooo.       888  d8'     .ooooo.   .ooooo.  oo.ooooo.   .ooooo.  oooo d8b     oooo    ooo       ]8P' 
#        888      `888  `888P"Y88bP"Y88b  d88' `88b      88888[      d88' `88b d88' `88b  888' `88b d88' `88b `888""8P      `88.  .8'      .d8P'  
#        888       888   888   888   888  888ooo888      888`88b.    888ooo888 888ooo888  888   888 888ooo888  888           `88..8'     .dP'     
#        888       888   888   888   888  888    .o      888  `88b.  888    .o 888    .o  888   888 888    .o  888            `888'    .oP     .o 
#       o888o     o888o o888o o888o o888o `Y8bod8P'     o888o  o888o `Y8bod8P' `Y8bod8P'  888bod8P' `Y8bod8P' d888b            `8'     8888888888 
#                                                                                         888                                                     
#                                                                                        o888o                                                                                                                                                                                                                                                           .oooo. 
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#
# Program: Time Keeper v2
# Description:
#   Portable multi-user, multi-project time tracker.
#   Tracks dev sessions, saves logs to JSON, and generates reports.
#
# Features:
#   - Clock in/out with timestamps
#   - Multi-user support with user switching and summary totals
#   - Per-project JSON log files
#   - Daily / weekly / monthly time reports
#   - Portable paths (default “data” folder next to script)
#   - Automatic folder creation and safe file handling
#   - Optional custom folder for log storage
#
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#
# Function Template (Type Hints Reference)
#
# def function_name(parameter: type, parameter2: type) -> return_type:
#     """
#     What the function does (short description).
#
#     Parameters:
#       parameter (type): Meaning or purpose of this input.
#       parameter2 (type): Description of second input.
#
#     Returns:
#       return_type: What this function gives back.
#                    Use 'None' if it returns nothing.
#     """
#
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*



import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DEFAULT_NAME = "default_project"

BASE_DIR = Path(__file__).parent  # folder where this script lives



#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#
#   ╔═╗┌─┐┌┬┐┬ ┬  ╦ ╦┌─┐┬  ┌─┐┌─┐┬─┐┌─┐     #
#   ╠═╝├─┤ │ ├─┤  ╠═╣├┤ │  ├─┘├┤ ├┬┘└─┐     #
#   ╩  ┴ ┴ ┴ ┴ ┴  ╩ ╩└─┘┴─┘┴  └─┘┴└─└─┘     #
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#



def slugify(project_name: str) -> str:

    """
    Convert a project name into a safe file name (lowercase, no spaces or symbols).
    """
    
    formatted_name = project_name.strip().lower().replace(" ", "_")
    allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    
    safe_name = "".join(char for char in formatted_name if char in allowed_characters)
    
    return safe_name or "silly_goose"


def get_log_file(project_name: str, custom_folder_path: str | None) -> Path:

    """
    Build and return the complete file path for this project's JSON log file.
    Uses the custom folder if provided, otherwise defaults to './data'.
    -> JSON folder
    """

    # Determine where the log file should be stored
    if custom_folder_path:
        logs_directory = Path(custom_folder_path).expanduser()
    else:
        logs_directory = BASE_DIR / "data"

    # Create a safe file name based on the project name
    project_slug = slugify(project_name or PROJECT_DEFAULT_NAME)

    # Make sure the directory exists
    logs_directory.mkdir(parents=True, exist_ok=True)

    # Build the full file path, e.g. /data/myproject_time_log.json
    return logs_directory / f"{project_slug}_time_log.json"



#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#
#   ╔═╗┌─┐┬  ┬┌─┐   ┬   ╦  ┌─┐┌─┐┌┬┐    #
#   ╚═╗├─┤└┐┌┘├┤   ┌┼─  ║  │ │├─┤ ││    #
#   ╚═╝┴ ┴ └┘ └─┘  └┘   ╩═╝└─┘┴ ┴─┴┘    #
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#


                                                                                            
def save_data(data_dictionary: dict, log_file_path: Path) -> None:

    """
    Save the data dictionary as formatted JSON inside the file at log_file_path.
    Creates the folder if it does not already exist.
    """
    
    # Make sure the directory exists
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Open file for writing and save JSON inside it
    with log_file_path.open("w", encoding="utf-8") as output_file:
        json.dump(data_dictionary, output_file, indent=2)


def load_data(log_file_path: Path, project_name: str) -> dict:
    
    """
    Load the project's JSON log data from disk.

    If the file exists:
      - Load and return the stored JSON data.
      - Make sure a project name is included.

    If the file does not exist:
      - Create and return a new empty data structure for this project.
    """

    #~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    # Log file already exists on disk
    #~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    
    if log_file_path.exists():
        with log_file_path.open("r", encoding="utf-8") as input_file:
            loaded_data = json.load(input_file)

        # Make sure "project" exists in the data
        if "project" not in loaded_data:
            loaded_data["project"] = project_name

        # Make sure "users" exists in the data
        if "users" not in loaded_data:
            loaded_data["users"] = {}

        return loaded_data

    #~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    # Log file does NOT exist yet
    # Return a brand new structure
    #~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    
    return {
        "project": project_name,
        "users": {}   # username → {sessions: [...], active_session: ...}
    }


def ensure_user(project_data: dict, username: str) -> dict:
    
    """
    Make sure a user entry exists.
    """
    
    if "users" not in project_data:
        project_data["users"] = {}

    if username not in project_data["users"]:
        project_data["users"][username] = {
            "sessions": [],
            "active_session": None,
        }

    return project_data



#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#
#   ╔═╗┌─┐┬─┐┌─┐  ╔═╗┌─┐┌─┐┬─┐┌─┐┌┬┐┬┌─┐┌┐┌┌─┐      #
#   ║  │ │├┬┘├┤   ║ ║├─┘├┤ ├┬┘├─┤ │ ││ ││││└─┐      #
#   ╚═╝└─┘┴└─└─┘  ╚═╝┴  └─┘┴└─┴ ┴ ┴ ┴└─┘┘└┘└─┘      #
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#



def clock_in(user_data: dict) -> dict:
    
    """
    Start a new session for user.

    Parameters:
      user_data (dict): The dictionary for this specific user containing:
                        - "active_session": ISO string or None
                        - "sessions": list of past session dictionaries

    Returns:
      dict: The updated user_data dictionary with:
            - active_session set to the current timestamp
            - unchanged session history
    """

    if user_data.get("active_session") is not None:
        print("\nAlready clocked in.")
        print(f"Started at: {user_data['active_session']}\n")
        return user_data

    # Create new ISO timestamp for session start
    now = datetime.now().isoformat(timespec="seconds")

    # Set as current active session
    user_data["active_session"] = now

    print(f"\nClocked in at {now}\n")

    return user_data


def clock_out(user_data: dict) -> dict:
    
    """
    End the current session and save it.

    Returns:
      dict: The updated user_data dictionary with:
            - active_session set to None -> clocked out
            - new session appended to sessions list
    """

    start = user_data.get("active_session")
    if start is None:
        print("\nYou are not currently clocked in.\n")
        return user_data

    end = datetime.now().isoformat(timespec="seconds")

    # Convert stored ISO strings into datetime objects
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    duration_minutes = round((end_dt - start_dt).total_seconds() / 60, 2)

    user_data["sessions"].append({
        "start": start,
        "end": end,
        "duration_minutes": duration_minutes,
    })

    # Clear the active session
    user_data["active_session"] = None

    print(f"\nClocked out at {end}")
    print(f"Session length: {duration_minutes} minutes\n")

    return user_data


def show_status(user_data: dict, username: str) -> None:
    
    """
    Display whether the specified user is currently clocked in.

    Parameters:
      user_data (dict): The dictionary for this user containing:
                        - "sessions": list of session records
                        - "active_session": current start time or None
      username (str):   The user whose summary is being displayed.

    Returns:
      None: This function only prints status information.
    """

    start = user_data.get("active_session")

    if start:
        print(f"\nStatus for {username}: Clocked in")
        print(f"Started at: {start}\n")
        return

    print(f"\nStatus for {username}: Not clocked in\n")


def show_summary(user_data: dict, username: str) -> None:
    
    """
    Display total time and recent sessions for the specified user.
    """

    sessions = user_data.get("sessions", [])
    if not sessions:
        print(f"\nNo sessions logged yet for {username}.\n")
        return

    total_minutes = sum(s["duration_minutes"] for s in sessions)
    total_hours = round(total_minutes / 60, 2)

    print(f"\n=== Dev Time Summary for {username} ===")
    print(f"Total sessions: {len(sessions)}")
    print(f"Total minutes:  {total_minutes}")
    print(f"Total hours:    {total_hours}")

    print("\nLast 5 sessions:")
    for s in sessions[-5:]:
        print(f"  {s['start']} -> {s['end']}  ({s['duration_minutes']} min)")
    print()


def list_all_users_summary(data: dict) -> None:
    """
    Display total tracked time for all users in the project.

    Parameters:
      data (dict): The full project data containing:
                   - "users": mapping of username → user_data dictionaries

    Returns:
      None: This function prints each user's total time and session count.
    """

    users = data.get("users", {})
    if not users:
        print("\nNo users found yet.\n")
        return

    print("\n=== All Users Summary (this project) ===")

    for username, user_data in users.items():
        sessions = user_data.get("sessions", [])
        total_minutes = sum(s["duration_minutes"] for s in sessions)
        total_hours = round(total_minutes / 60, 2)

        print(
            f"- {username}: {total_minutes} minutes "
            f"({total_hours} hours, {len(sessions)} sessions)"
        )

    print()



#~*~*~*~*~*~*~*~*~*~*~*~*~*~#
#   ╦═╗┌─┐┌─┐┌─┐┬─┐┌┬┐┌─┐   #
#   ╠╦╝├┤ ├─┘│ │├┬┘ │ └─┐   #
#   ╩╚═└─┘┴  └─┘┴└─ ┴ └─┘   #
#~*~*~*~*~*~*~*~*~*~*~*~*~*~#



def time_report(user_data: dict, username: str, days: int) -> None:

    """
    Display a time report for the specified user covering the last N days.

    Parameters:
      user_data (dict): The dictionary for this user containing:
                        - "sessions": list of session records
      username (str):   The user whose report is being displayed.
      days (int):       How many days of history to include.

    Returns:
      None: This function prints a formatted report.
    """

    sessions = user_data.get("sessions", [])
    if not sessions:
        print(f"\nNo sessions logged yet for {username}.\n")
        return

    now = datetime.now()
    cutoff = now - timedelta(days=days)

    # Gather only sessions whose end timestamp is within the cutoff window
    filtered = []
    for session in sessions:
        end_str = session.get("end") or session.get("start")
        try:
            end_dt = datetime.fromisoformat(end_str)
        except Exception:
            continue

        if end_dt >= cutoff:
            filtered.append(session)

    if not filtered:
        print(f"\nNo sessions for {username} in the last {days} days.\n")
        return

    total_minutes = sum(s["duration_minutes"] for s in filtered)
    total_hours = round(total_minutes / 60, 2)

    label = {
        1: "Last 24 hours",
        7: "Last 7 days",
        30: "Last 30 days",
    }.get(days, f"Last {days} days")

    print(f"\n=== {label} Report for {username} ===")
    print(f"Sessions:      {len(filtered)}")
    print(f"Total minutes: {total_minutes}")
    print(f"Total hours:   {total_hours}")

    print("\nSessions:")
    for s in filtered:
        print(f"  {s['start']} -> {s['end']}  ({s['duration_minutes']} min)")
    print()


def report_menu(user_data: dict, username: str) -> None:

    """
    Display a sub-menu of time reports (daily, weekly, monthly)
    and allow the user to choose which report to view.

    Parameters:
      user_data (dict): The dictionary for this user containing session records.
      username (str):   The user requesting the reports.

    Returns:
      None: This function prints menu options and calls report functions.
    """

    while True:
        print(f"\n *_* Reports for {username} *_*")
        print("1) Last 24 hours")
        print("2) Last 7 days")
        print("3) Last 30 days")
        print("4) Back to main menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            time_report(user_data, username, days=1)
        elif choice == "2":
            time_report(user_data, username, days=7)
        elif choice == "3":
            time_report(user_data, username, days=30)
        elif choice == "4":
            break
        else:
            print("\nInvalid choice.\n")

