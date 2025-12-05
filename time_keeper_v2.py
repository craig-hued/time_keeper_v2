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



#   ╔═╗┌─┐┌┬┐┬ ┬  ╦ ╦┌─┐┬  ┌─┐┌─┐┬─┐┌─┐
#   ╠═╝├─┤ │ ├─┤  ╠═╣├┤ │  ├─┘├┤ ├┬┘└─┐
#   ╩  ┴ ┴ ┴ ┴ ┴  ╩ ╩└─┘┴─┘┴  └─┘┴└─└─┘



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



#   ╔═╗┌─┐┬  ┬┌─┐   ┬   ╦  ┌─┐┌─┐┌┬┐
#   ╚═╗├─┤└┐┌┘├┤   ┌┼─  ║  │ │├─┤ ││
#   ╚═╝┴ ┴ └┘ └─┘  └┘   ╩═╝└─┘┴ ┴─┴┘


                                                                                            
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


