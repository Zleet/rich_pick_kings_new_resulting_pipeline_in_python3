# ==============================================================================
# Parse entries from admin webpage.
# 1. Read all the entries for Rich Pick Kings that have been copied from the
#    admin webpage and pasted into local file 'entries_from_admin_webpage.txt'
# 2. Build a csv file named 'all_entries.csv' and stick all the entries in it.
# ==============================================================================
import json
# ==============================================================================
# ==============================================================================
def main():

    build_csv_spreadsheet_containing_all_rich_pick_kings_entries()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# ==============================================================================
def build_csv_spreadsheet_containing_all_rich_pick_kings_entries():

    # read entries
    entries = parse_entries_from_local_file()

    print('Total entries =', str(len(entries)))

    print('First entry:')
    print(entries[0])

    # build the csv text
    csv_text = 'USERNAME,YEAR,MONTH,DAY,HOUR,MINUTE,SECOND,'
    csv_text += 'TEAM_TO_WIN_MATCH,MATCH_RESULT,CORRECT_SCORE_TEAM,'
    csv_text += 'CORRECT_SCORE,MATCH_RESULT_POINTS,CORRECT_SCORE_POINTS'
    for entry in entries:
        csv_text += "\n" + entry["username"]
        csv_text += ',' + str(entry["year"])
        csv_text += ',' + str(entry["month"])
        csv_text += ',' + str(entry["day"])
        csv_text += ',' + str(entry["hour"])
        csv_text += ',' + str(entry["minute"])
        csv_text += ',' + str(entry["second"])
        csv_text += ',' + entry["team_to_win_match"]
        csv_text += ',' + entry["match_result"]
        csv_text += ',' + entry["correct_score_team"]
        csv_text += ',' + entry["correct_score"]
        csv_text += ',' + str(entry["match_result_points"])
        csv_text += ',' + str(entry["correct_score_points"])

    # write the csv text to the local file 'all_entries.csv'
    outfile = open('all_entries.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# ==============================================================================
def parse_entries_from_local_file():

    infile = open('entries_from_admin_webpage.txt', 'r')
    text = infile.read()
    infile.close()

    # the string '<file_delimiter>' delimits the contents of each file. Split
    # the text along this substring into chunks of file text
    text = text.strip()
    file_text_chunks = text.split('<file_delimiter>')
    
    # remove first file text chunk (doesn't contain file text)
    file_text_chunks = file_text_chunks[1:]

    # loop through file text chunks and process each entry file
    # (each entry file contains all the entries submitted on a single day)
    entries = []
    for file_text in file_text_chunks:
        file_text = file_text.strip()
        lines = file_text.split("\n")
        entries_in_single_file = parse_entries_from_single_file(lines)
        entries.extend(entries_in_single_file)

    return entries
# ==============================================================================
# Parse the entries from a single file.
# ==============================================================================
def parse_entries_from_single_file(lines):

    # +++++++++++++++++++++++++++++++++++++++++
    # lines are in groups of 3, in the format:
    # username
    # datetime string
    # entries in json array format
    # +++++++++++++++++++++++++++++++++++++++++
    entries = []
    total_entry_chunks = int(len(lines) / 3)
    for count in range(total_entry_chunks):
        username_line = lines[count * 3]
        datetime_line = lines[(count * 3) + 1]
        entries_line = lines[(count * 3) + 2]
        # get username
        username = username_line.strip()
        # parse datetime info from datetime_line
        year, month, day, hour, minute,second = parse_datetime_string(
                                                    datetime_line.strip())
        # parse the entries
        entries_text_block = entries_line.strip()
        entries_from_entries_text_block = json.loads(entries_text_block)
        # loop through the entries and add the username and datetime info to
        # each entry dictionary
        rebuilt_entries_from_entries_text_block = []
        for entry_dict in entries_from_entries_text_block:
            # add username
            entry_dict["username"] = username
            # add datetime info
            entry_dict["year"] = year
            entry_dict["month"] = month
            entry_dict["day"] = day
            entry_dict["hour"] = hour
            entry_dict["minute"] = minute
            entry_dict["second"] = second
            # append entry_dict onto rebuilt_entries_from_entries_text_block
            rebuilt_entries_from_entries_text_block.append(entry_dict)
        entries.extend(rebuilt_entries_from_entries_text_block)

    # print('Total entries =', str(len(entries)))

    return entries
# ==============================================================================
# Parse a datetime string in the format:
# 2019_08_04_18_59_40
# (i.e. '<year>_<month>_<day>_<hour>_<minute>_<second>')
# and return all the datetime information.
# ==============================================================================
def parse_datetime_string(datetime_string):

    elements = datetime_string.split('_')
    year = int(elements[0].strip())
    month = int(elements[1].strip())
    day = int(elements[2].strip())
    hour = int(elements[3].strip())
    minute = int(elements[4].strip())
    second = int(elements[5].strip())

    return [year, month, day, hour, minute, second]
# ==============================================================================
main()
