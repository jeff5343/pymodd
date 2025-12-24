def generate_project_from_json_file_content(json_file_content: str) -> None:
    '''Generates a pymodd project from a modd.io game json file

    Args:
        json_file_content (str): content of the modd.io game json file
    '''


def log_success(message: str) -> None:
    '''Logs a success message with colorful formatting

    Args:
        message (str): message to log
    '''


def log_error(message: str) -> None:
    '''Logs an error message with colorful formatting

    Args:
        message (str): message to log
    '''


def log_cli_start_message(action: str, pymodd_project_name: str) -> None:
    '''Logs a start message for pymodd commands with colorful formatting

    Args:
        action (str): the action that the command is doing

        pymodd_project_name (str): name of the project
    '''


def log_cli_end_message(completed_action: str, ended_successfully: bool) -> None:
    '''Logs an end message for pymodd commands with colorful formatting

    Args:
        completed_action (str): the action the command completed

        ended_successfully (bool): did the command end successfully
    '''
