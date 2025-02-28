# Copyright (c) [2025] [SqueezeAILab/TinyAgent]
# Licensed under the MIT License
# Source: [https://github.com/SqueezeAILab/TinyAgent]


import datetime
import platform
import subprocess
from dria_agent.agent.tool import tool
from .cmd import run_applescript, run_applescript_capture, run_command
import difflib
import os
import webbrowser
from urllib.parse import quote_plus
from typing import Literal
from bs4 import BeautifulSoup

calendar_app = "Calendar"
messages_app = "Messages"
notes_app = "Notes"
mail_app: str = "Mail"
_DEFAULT_FOLDER = "Notes"


@tool
def create_event(
    title: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    location: str = "",
    invitees: list[str] = [],
    notes: str = "",
    calendar: str | None = None,
) -> str:
    """
        Creates a new calendar event on macOS using AppleScript.

    This function creates an event with the specified title, start date, end date, location,
    invitees, and additional notes in the specified calendar. If the calendar parameter is not provided
    or is invalid, it defaults to the first available calendar. The function is supported only on macOS.
    On other platforms, it returns a message indicating that the method is unsupported.

    :param title: The title of the event.
    :param start_date: The start date and time of the event (datetime.datetime).
    :param end_date: The end date and time of the event (datetime.datetime).
    :param location: (Optional) The location where the event will take place. Defaults to an empty string.
    :param invitees: (Optional) A list of email addresses to invite to the event. Defaults to an empty list.
    :param notes: (Optional) Additional notes or description for the event. Defaults to an empty string.
    :param calendar: (Optional) The name of the calendar in which to create the event. If not provided,
                     the first available calendar is used. If provided but invalid, the first calendar is used.

    :returns: A string message indicating the outcome of the event creation. Returns a success message if the event
              is created successfully, or an error message if an issue occurs (e.g., unsupported platform, invalid calendar).
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    # start_date = start_date.strftime("%-d/%-m/%Y %I:%M:%S %p")
    # end_date = end_date.strftime("%-d/%-m/%Y %I:%M:%S %p")

    # Check if the given calendar parameter is valid
    if calendar is not None:
        script = f"""
        tell application "{calendar_app}"
            set calendarExists to name of calendars contains "{calendar}"
        end tell
        """
        exists = run_applescript(script)
        if not exists:
            calendar = _get_first_calendar()
            if calendar is None:
                return f"Can't find the calendar named {calendar}. Please try again and specify a valid calendar name."

    # If it is not provided, default to the first calendar
    elif calendar is None:
        calendar = _get_first_calendar()
        if calendar is None:
            return "Can't find a default calendar. Please try again and specify a calendar name."

    invitees_script = []
    for invitee in invitees:
        invitees_script.append(
            f"""
            make new attendee at theEvent with properties {{email:"{invitee}"}}
        """
        )
    invitees_script = "".join(invitees_script)

    script = f"""
    tell application "System Events"
        set calendarIsRunning to (name of processes) contains "{calendar_app}"
        if calendarIsRunning then
            tell application "{calendar_app}" to activate
        else
            tell application "{calendar_app}" to launch
            delay 1
            tell application "{calendar_app}" to activate
        end if
    end tell
    tell application "{calendar_app}"
        tell calendar "{calendar}"
            set startDate to current date
            set year of startDate to {start_date.year}
            set month of startDate to {start_date.month}
            set day of startDate to {start_date.day}
            set hours of startDate to {start_date.hour}
            set minutes of startDate to {start_date.minute}
            set seconds of startDate to {start_date.second}
            
            set endDate to current date
            set year of endDate to {end_date.year}
            set month of endDate to {end_date.month}
            set day of endDate to {end_date.day}
            set hours of endDate to {end_date.hour}
            set minutes of endDate to {end_date.minute}
            set seconds of endDate to {end_date.second}
            set theEvent to make new event at end with properties {{summary:"{title}", start date:startDate, end date:endDate, location:"{location}", description:"{notes}"}}
            {invitees_script}
            switch view to day view
            show theEvent
        end tell
        tell application "{calendar_app}" to reload calendars
    end tell
    """

    try:
        run_applescript(script)
        return f"""Event created successfully in the "{calendar}" calendar."""
    except subprocess.CalledProcessError as e:
        return str(e)


def _get_first_calendar() -> str | None:
    script = f"""
        tell application "System Events"
            set calendarIsRunning to (name of processes) contains "{calendar_app}"
            if calendarIsRunning is false then
                tell application "{calendar_app}" to launch
                delay 1
            end if
        end tell
        tell application "{calendar_app}"
            set firstCalendarName to name of first calendar
        end tell
        return firstCalendarName
        """
    stdout = run_applescript_capture(script)
    if stdout:
        return stdout[0].strip()
    else:
        return None


@tool
def open_anything(name_or_path: str) -> str:
    """
    Open a local file/folder/application on macOS using Spotlight.

    This function attempts to open an application, file, or folder by either directly opening the file
    if an absolute path is provided, or by using macOS's Spotlight search (via 'mdfind') to locate the item.
    It first checks for an exact match using the display name. If no exact match is found, it performs a fuzzy
    search using difflib to determine the best match. The function returns the path of the item opened or an
    error message if the operation fails or if executed on a non-macOS platform.

    :param (str) name_or_path: A string representing either the name of the item to open or its absolute file path.
                         If an absolute path is provided (starting with "/") and the file exists, the file is opened directly.
    :returns: A string indicating the path of the item that was opened, or an error message if the item could not
              be found or opened.

    Note:
        This function is only supported on macOS.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    # Check if input is a path and file exists
    if name_or_path.startswith("/") and os.path.exists(name_or_path):
        try:
            subprocess.run(["open", name_or_path])
            return name_or_path
        except Exception as e:
            return f"Error opening file: {e}"

    # Use mdfind for fast searching with Spotlight
    command_search_exact = ["mdfind", f"kMDItemDisplayName == '{name_or_path}'"]
    stdout, _ = run_command(command_search_exact)

    if stdout:
        paths = stdout.strip().split("\n")
        path = paths[0] if paths else None
        if path:
            subprocess.run(["open", path])
            return path

    # If no exact match, perform fuzzy search on the file names
    command_search_general = ["mdfind", name_or_path]
    stdout, stderr = run_command(command_search_general)

    paths = stdout.strip().split("\n") if stdout else []

    if paths:
        best_match = difflib.get_close_matches(name_or_path, paths, n=1, cutoff=0.0)
        if best_match:
            _, stderr = run_command(["open", best_match[0]])
            if len(stderr) > 0:
                return f"Error: {stderr}"
            return best_match[0]
        else:
            return "No file found after fuzzy matching."
    else:
        return "No file found with exact or fuzzy name."


@tool
def open_location(query: str):
    """
    Opens a specified location in Apple Maps using a search query.

    This function constructs an Apple Maps URL based on the provided query,
    which can be a place name, an address, or geographical coordinates.
    It then opens the URL in the default web browser, allowing the user to
    view the location directly in Apple Maps.

    :param query: The search query representing the location to be opened.
                  This can be a place name, an address, or coordinates.
    :type query: str
    :returns: A confirmation message containing the Apple Maps URL that was opened.
    """
    base_url = "https://maps.apple.com/?q="
    query_encoded = quote_plus(query)
    full_url = base_url + query_encoded
    webbrowser.open(full_url)
    return f"Location of {query} in Apple Maps: {full_url}"


@tool
def show_directions(end: str, start: str = "", transport: Literal["d", "w", "r"] = "d"):
    """
    Opens Apple Maps with directions from a start location to an end location.

    Constructs a URL for Apple Maps using the specified destination, an optional
    starting point (defaults to the current location if empty), and a transport mode.
    The transport mode is specified as a single character:
      - 'd': Driving (default)
      - 'w': Walking
      - 'r': Public transit

    :param end: The destination address or location.
    :type end: str
    :param start: (Optional) The starting address or location. If empty, the current location is used.
    :type start: str
    :param transport: (Optional) Mode of transportation ('d', 'w', or 'r'). Defaults to 'd'.
    :type transport: Literal["d", "w", "r"]
    :returns: A message string containing the Apple Maps URL for the directions.
    """
    base_url = "https://maps.apple.com/?"
    if len(start) > 0:
        start_encoded = quote_plus(start)
        start_param = f"saddr={start_encoded}&"
    else:
        start_param = ""  # Use the current location
    end_encoded = quote_plus(end)
    transport_flag = f"dirflg={transport}"
    full_url = f"{base_url}{start_param}daddr={end_encoded}&{transport_flag}"
    webbrowser.open(full_url)
    return f"Directions to {end} in Apple Maps: {full_url}"


@tool
def send_sms(to: list[str], message: str) -> str:
    """
    Compose an SMS draft in the macOS Messages app by simulating keystrokes.

    This method opens the Messages app, creates a new SMS draft, and fills in the recipient(s)
    and message text by simulating keyboard input. It does not send the SMS automatically.
    Note: This functionality is only supported on macOS.

    :param to: A list of recipient phone numbers or email addresses.
    :type to: list[str]
    :param message: The message content to include in the SMS draft.
    :type message: str
    :returns: A confirmation message indicating that the SMS draft was composed,
              or an error message if the operation failed.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    to_script = []
    for recipient in to:
        recipient = recipient.replace("\n", "")
        to_script.append(
            f"""
            keystroke "{recipient}"
            delay 0.5
            keystroke return
            delay 0.5
        """
        )
    to_script = "".join(to_script)

    escaped_message = message.replace('"', '\\"').replace("'", "’")

    script = f"""
    tell application "System Events"
        tell application "{messages_app}"
            activate
        end tell
        tell process "{messages_app}"
            set frontmost to true
            delay 0.5
            keystroke "n" using command down
            delay 0.5
            {to_script}
            keystroke tab
            delay 0.5
            keystroke "{escaped_message}"
        end tell
    end tell
    """
    try:
        run_applescript(script)
        return "SMS draft composed"
    except subprocess.CalledProcessError as e:
        return f"An error occurred while composing the SMS: {str(e)}"


@tool
def get_phone_number(contact_name: str) -> str:
    """
    Retrieves the phone number of a contact from the macOS Contacts app.

    This function uses AppleScript to locate a contact by the provided name and returns
    the phone number of the first matching person. If an exact match is not found, it
    attempts to locate similar contacts by using the first name and recursively returns
    the phone number of the first similar contact found. This method is supported only on macOS.

    :param contact_name: The full name of the contact whose phone number is to be retrieved.
    :type contact_name: str
    :returns: The phone number of the contact, or an error message if no matching contact is found.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    script = f"""
    tell application "Contacts"
        set thePerson to first person whose name is "{contact_name}"
        set theNumber to value of first phone of thePerson
        return theNumber
    end tell
    """
    stout, stderr = run_applescript_capture(script)
    # If the person is not found, try to find similar contacts
    if "Can’t get person" in stderr:
        first_name = contact_name.split(" ")[0]
        names = get_full_names_from_first_name(first_name)
        if "No contacts found" in names or len(names) == 0:
            return "No contacts found"
        else:
            # Return the phone number of the first similar contact
            return get_phone_number(names[0])
    else:
        return stout.replace("\n", "")


@tool
def get_email_address(contact_name: str) -> str:
    """
    Retrieves the email address of a contact from the macOS Contacts app.

    This function uses AppleScript to search for a contact by name and returns the email
    address of the first matching person. If an exact match is not found, it attempts to
    find similar contacts by searching for contacts with the same first name and returns
    the email address of the first found. This method is only supported on macOS.

    :param contact_name: The full name of the contact to search for.
    :returns: The email address of the contact or an error message if no matching contact is found.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    script = f"""
    tell application "Contacts"
        set thePerson to first person whose name is "{contact_name}"
        set theEmail to value of first email of thePerson
        return theEmail
    end tell
    """
    stout, stderr = run_applescript_capture(script)
    # If the person is not found, we will try to find similar contacts
    if "Can’t get person" in stderr:
        first_name = contact_name.split(" ")[0]
        names = get_full_names_from_first_name(first_name)
        if "No contacts found" in names or len(names) == 0:
            return "No contacts found"
        else:
            # Just find the first person
            return get_email_address(names[0])
    else:
        return stout.replace("\n", "")


def get_full_names_from_first_name(first_name: str) -> list[str] | str:
    """
    Returns a list of full names of contacts that contain the first name provided.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    script = f"""
    tell application "Contacts"
        set matchingPeople to every person whose first name contains "{first_name}"
        set namesList to {{}}
        repeat with aPerson in matchingPeople
            set end of namesList to name of aPerson
        end repeat
        return namesList
    end tell
    """
    names, _ = run_applescript_capture(script)
    names = names.strip()
    if len(names) > 0:
        # Turn name into a list of strings
        names = list(map(lambda n: n.strip(), names.split(",")))
        return names
    else:
        return "No contacts found."


@tool
def create_note(name: str, content: str, folder: str | None = None) -> str:
    """
    Create and focus a new note.

    Creates a note with the provided content in the specified folder (or default folder)
    and brings it to focus. Only supported on MacOS.

    Args:
        name (str): The note's name.
        content (str): The note's content.
        folder (str | None, optional): Target folder for the note.

    Returns:
        str: Success or error message.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    folder_line = _get_folder_line(folder)
    html_content = content.replace('"', '\\"').replace("'", "’")

    script = f"""
    tell application "{notes_app}"
        tell account "iCloud"
            {folder_line}
                set newNote to make new note with properties {{body:"{html_content}"}}
            end tell
        end tell
        activate
        tell application "System Events"
            tell process "Notes"
                set frontmost to true
                delay 0.5 -- wait a bit for the note to be created and focus to be set
            end tell
        end tell
        tell application "{notes_app}"
            show newNote
        end tell
    end tell
    """

    try:
        run_applescript(script)
        return "Note created and focused successfully."
    except subprocess.CalledProcessError as e:
        return str(e)


@tool
def open_note(
    name: str,
    folder: str | None = None,
    return_content: bool = False,
) -> str:
    """
    Opens an existing note by its name and optionally returns its content.
    If no exact match is found, attempts fuzzy matching to suggest possible notes.
    If return_content is True, returns the content of the note.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    folder_line = _get_folder_line(folder)

    # Adjust the script to return content if required
    content_line = (
        "return body of theNote"
        if return_content
        else 'return "Note opened successfully."'
    )

    # Attempt to directly open the note with the exact name and optionally return its content
    script_direct_open = f"""
    tell application "{notes_app}"
        tell account "iCloud"
            {folder_line}
                set matchingNotes to notes whose name is "{name}"
                if length of matchingNotes > 0 then
                    set theNote to item 1 of matchingNotes
                    show theNote
                    {content_line}
                else
                    return "No exact match found."
                end if
            end tell
        end tell
    end tell
    """

    try:
        stdout, _ = run_applescript_capture(script_direct_open)
        if "Note opened successfully" in stdout or "No exact match found" not in stdout:
            if return_content:
                return _convert_note_to_text(stdout.strip())
            return stdout.strip()  # Successfully opened a note with the exact name

        # If no exact match is found, proceed with fuzzy matching
        note_to_open = _do_fuzzy_matching(name)

        # Focus the note with the closest matching name after fuzzy matching
        script_focus = f"""
        tell application "{notes_app}"
            tell account "iCloud"
                {folder_line}
                    set theNote to first note whose name is "{note_to_open}"
                    show theNote
                    {content_line}
                end tell
            end tell
            activate
        end tell
        """
        result = run_applescript(script_focus)
        if return_content:
            return _convert_note_to_text(result.strip())
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}"


@tool
def append_to_note(name: str, append_content: str, folder: str | None = None) -> str:
    """
    Append content to a note.

    Appends `append_content` to the note identified by `name`. If an exact match is not found,
    a fuzzy match is used to locate the closest note. This function is only supported on MacOS.

    Args:
        name (str): The name of the note.
        append_content (str): The content to append.
        folder (str, optional): An optional folder specifier for the note.

    Returns:
        str: A status message indicating the result.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    folder_line = _get_folder_line(folder)

    # Try to directly find and append to the note with the exact name
    script_find_note = f"""
    tell application "{notes_app}"
        tell account "iCloud"
            {folder_line}
                set matchingNotes to notes whose name is "{name}"
                if length of matchingNotes > 0 then
                    set theNote to item 1 of matchingNotes
                    return name of theNote
                else
                    return "No exact match found."
                end if
            end tell
        end tell
    end tell
    """

    try:
        note_name, _ = run_applescript_capture(
            script_find_note.format(notes_app=notes_app, name=name)
        )
        note_name = note_name.strip()

        if "No exact match found" in note_name or not note_name:
            note_name = _do_fuzzy_matching(name)
            if note_name == "No notes found after fuzzy matching.":
                return "No notes found after fuzzy matching."

        # If an exact match is found, append content to the note
        html_append_content = append_content.replace('"', '\\"').replace("'", "’")
        script_append = f"""
        tell application "{notes_app}"
            tell account "iCloud"
                {folder_line}
                    set theNote to first note whose name is "{note_name}"
                    set body of theNote to (body of theNote) & "<br>{html_append_content}"
                    show theNote
                end tell
            end tell
        end tell
        """

        run_applescript(script_append)
        return f"Content appended to note '{name}' successfully."
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}"


def _get_folder_line(folder: str | None) -> str:
    if folder is not None and len(folder) > 0 and _check_folder_exists(folder):
        return f'tell folder "{folder}"'
    return f'tell folder "{_DEFAULT_FOLDER}"'


def _do_fuzzy_matching(name: str) -> str:
    script_search = f"""
        tell application "{notes_app}"
            tell account "iCloud"
                set noteList to name of every note
            end tell
        end tell
    """
    note_names_str, _ = run_applescript_capture(script_search)
    note_names = note_names_str.split(", ")
    closest_matches = difflib.get_close_matches(name, note_names, n=1, cutoff=0.0)
    if not closest_matches:
        return "No notes found after fuzzy matching."

    note_to_open = closest_matches[0]
    return note_to_open


def _check_folder_exists(folder: str) -> bool:
    # Adjusted script to optionally look for a folder
    folder_check_script = f"""
    tell application "{notes_app}"
        set folderExists to false
        set folderName to "{folder}"
        if folderName is not "" then
            repeat with eachFolder in folders
                if name of eachFolder is folderName then
                    set folderExists to true
                    exit repeat
                end if
            end repeat
        end if
        return folderExists
    end tell
    """

    folder_exists, _ = run_applescript_capture(folder_check_script)
    folder_exists = folder_exists.strip() == "true"

    return folder_exists


def _convert_note_to_text(note_html: str) -> str:
    """
    Converts an HTML note content to plain text.
    """
    soup = BeautifulSoup(note_html, "html.parser")
    return soup.get_text().strip()


@tool
def compose_email(
    recipients: list[str],
    subject: str,
    content: str,
    attachments: list[str],
    cc: list[str],
) -> str:
    """
    Composes a new email with the given recipients, subject, content, and attaches files from the given paths.
    Adds cc recipients if provided. Does not send it but opens the composed email to the user.

    :param recipients: A list of email addresses to send the email to.
    :param subject: The subject of the email.
    :param content: The content of the email.
    :param attachments: A list of file paths to attach to the email.
    :param cc: A list of email addresses to cc on the email.
    :return: A message indicating the success or failure of the operation.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    # Format recipients and cc recipients for AppleScript list
    recipients_list = _format_email_addresses(recipients)
    cc_list = _format_email_addresses(cc)
    attachments_str = _format_attachments(attachments)

    content = content.replace('"', '\\"').replace("'", "’")
    script = f"""
    tell application "{mail_app}"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{content}" & return & return}}
        tell newMessage
            repeat with address in {recipients_list}
                make new to recipient at end of to recipients with properties {{address:address}}
            end repeat
            repeat with address in {cc_list}
                make new cc recipient at end of cc recipients with properties {{address:address}}
            end repeat
            {attachments_str}
        end tell
        activate
    end tell
    """

    try:
        run_applescript(script)
        return "New email composed successfully with attachments and cc."
    except subprocess.CalledProcessError as e:
        return str(e)


@tool
def reply_to_email(self, content: str, cc: list[str], attachments: list[str]) -> str:
    """
    Replies to the currently selected email in Mail with the given content.

    :param content: The content of the reply email.
    :param cc: A list of email addresses to cc on the reply email.
    :param attachments: A list of file paths to attach to the reply email.
    :return: A message indicating the success or failure of the operation.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    cc_list = _format_email_addresses(cc)
    attachments_str = _format_attachments(attachments)

    content = content.replace('"', '\\"').replace("'", "’")
    script = f"""
    tell application "{self.mail_app}"
        activate
        set selectedMessages to selected messages of message viewer 1
        if (count of selectedMessages) < 1 then
            return "No message selected."
        else
            set theMessage to item 1 of selectedMessages
            set theReply to reply theMessage opening window yes
            tell theReply
                repeat with address in {cc_list}
                    make new cc recipient at end of cc recipients with properties {{address:address}}
                end repeat
                set content to "{content}"
                {attachments_str}
            end tell
        end if
    end tell
    """

    try:
        run_applescript(script)
        return "Replied to the selected email successfully."
    except subprocess.CalledProcessError:
        return "An email has to be viewed in Mail to reply to it."


@tool
def forward_email(recipients: list[str], cc: list[str], attachments: list[str]) -> str:
    """
    Forwards the currently selected email in Mail to the given recipients with the given content.

    :param recipients: A list of email addresses to forward the email to.
    :param cc: A list of email addresses to cc on the forwarded email.
    :param attachments: A list of file paths to attach to the forwarded email.
    :return: A message indicating the success or failure of the operation.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    # Format recipients and cc recipients for AppleScript list
    recipients_list = _format_email_addresses(recipients)
    cc_list = _format_email_addresses(cc)
    attachments_str = _format_attachments(attachments)

    script = f"""
    tell application "{mail_app}"
        activate
        set selectedMessages to selected messages of message viewer 1
        if (count of selectedMessages) < 1 then
            return "No message selected."
        else
            set theMessage to item 1 of selectedMessages
            set theForward to forward theMessage opening window yes
            tell theForward
                repeat with address in {recipients_list}
                    make new to recipient at end of to recipients with properties {{address:address}}
                end repeat
                repeat with address in {cc_list}
                    make new cc recipient at end of cc recipients with properties {{address:address}}
                end repeat
                {attachments_str}
            end tell
        end if
    end tell
    """

    try:
        run_applescript(script)
        return "Forwarded the selected email successfully."
    except subprocess.CalledProcessError:
        return "An email has to be viewed in Mail to forward it."


@tool
def get_email_content() -> str:
    """
    Gets the content of the currently viewed email in Mail.

    returns: The content of the email or an error message if no email is selected.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    script = f"""
    tell application "{mail_app}"
        activate
        set selectedMessages to selected messages of message viewer 1
        if (count of selectedMessages) < 1 then
            return "No message selected."
        else
            set theMessage to item 1 of selectedMessages
            -- Get the content of the message
            set theContent to content of theMessage
            return theContent
        end if
    end tell
    """

    try:
        return run_applescript(script)
    except subprocess.CalledProcessError:
        return "No message selected or found."


@tool
def find_and_select_first_email_from(sender: str) -> str:
    """
    Finds and selects an email in Mail based on the sender's name.

    :param sender: The name of the sender to search for.
    :returns: A confirmation message if the email is found and selected, or an error message if no message is found.
    """
    if platform.system() != "Darwin":
        return "This method is only supported on MacOS"

    script = f"""
    tell application "{mail_app}"
        set theSender to "{sender}"
        set theMessage to first message of inbox whose sender contains theSender
        set selected messages of message viewer 1 to {{theMessage}}
        activate
        open theMessage
    end tell
    """

    try:
        run_applescript(script)
        return "Found and selected the email successfully."
    except subprocess.CalledProcessError:
        return "No message found from the sender."


def _format_email_addresses(emails: list[str]) -> str:
    return "{" + ", ".join([f'"{email}"' for email in emails]) + "}"


def _format_attachments(attachments: list[str]) -> str:
    attachments_str = []
    for attachment in attachments:
        attachment = attachment.replace('"', '\\"')
        attachments_str.append(
            f"""
            make new attachment with properties {{file name:"{attachment}"}} at after the last paragraph
        """
        )
    return "".join(attachments_str)


APPLE_TOOLS = [
    create_event,
    open_anything,
    open_location,
    show_directions,
    send_sms,
    get_phone_number,
    get_email_address,
    create_note,
    open_note,
    append_to_note,
    find_and_select_first_email_from,
    get_email_content,
    compose_email,
    reply_to_email,
    forward_email,
]
