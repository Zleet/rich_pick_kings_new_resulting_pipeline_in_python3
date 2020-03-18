# ==============================================================================
# Python 3 script to mark all the Rich Pick Kings entries
# ==============================================================================
import datetime
# ==============================================================================
def main():

    mark_all_rich_pick_kings_entries()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# Mark all the Rich Pick Kings entries
# ==============================================================================
def mark_all_rich_pick_kings_entries():

    # read all the entries from the csv spreadsheet
    entries = read_entries_from_csv_file()

    # read all Karls marked fixtures from the csv spreadsheet
    karls_marked_fixtures = read_karls_marked_fixtures_from_csv_file()

    # remove matches that don't have a htft result from karls_marked_fixtures
    karls_marked_fixtures = remove_unmarked_fixtures(karls_marked_fixtures)

    # add unique ids to all the entries and all karls marked fixtures.
    # This will aid when matching entries to fixtures later and analysing
    # the amount of time that has elapsed between an entry being made and
    # the matching fixture taking place.
    entries, karls_marked_fixtures = add_unique_ids_to_entries_and_karls_marked_fixtures(
                                                            entries, karls_marked_fixtures)

    # mark the entries
    marked_entries = mark_all_entries(entries, karls_marked_fixtures)

    # write a csv spreadsheet file containing all the marked entries
    write_marked_entries_to_csv_file(marked_entries)

    # write a csv spreadsheet file containing all the entries
    write_entries_to_csv_file(entries)

    # write a csv spreadsheet containing all karls marked fixtures
    write_karls_marked_fixtures_to_csv_file(karls_marked_fixtures)
    
    # write the following information to three separate javascript files:
    # 1. entries
    # 2. karls_marked_fixtures
    # 3. marked_entries
    write_all_important_info_to_javascript_files(entries,
                                    karls_marked_fixtures, marked_entries)

    return
# ==============================================================================
# Remove fixtures that don't have a htft result from karls marked fixtures.
# ==============================================================================
def remove_unmarked_fixtures(karls_marked_fixtures):

    rebuilt_karls_marked_fixtures = []
    for fixture in karls_marked_fixtures:
        if type(fixture["htft_result"]) is list:
            if len(fixture["htft_result"]) == 4:
                rebuilt_karls_marked_fixtures.append(fixture)
    karls_marked_fixtures = rebuilt_karls_marked_fixtures

    return karls_marked_fixtures
# ==============================================================================
# Add unique ids (beginning with 1) to each of the entries and each of
# karls_marked_fixtures.
# ==============================================================================
def add_unique_ids_to_entries_and_karls_marked_fixtures(entries,
                                                    karls_marked_fixtures):

    # add ids to entries
    rebuilt_entries = []
    for count in range(len(entries)):
        entry = entries[count]
        entry["id"] = count + 1
        rebuilt_entries.append(entry)
    entries = rebuilt_entries

    # add ids to karls_marked_fixtures
    rebuilt_karls_marked_fixtures = []
    for count in range(len(karls_marked_fixtures)):
        karl_fixture = karls_marked_fixtures[count]
        karl_fixture["id"] = count + 1
        rebuilt_karls_marked_fixtures.append(karl_fixture)
    karls_marked_fixtures = rebuilt_karls_marked_fixtures

    return [entries, karls_marked_fixtures]
# ==============================================================================
# ==============================================================================
def read_entries_from_csv_file():

    filename = '../03 - parse entries from admin webpage - FINISHED/'
    filename += 'all_entries.csv'

    entries = read_list_of_dictionaries_from_csv_file(filename)

    # loop through entries and remove entries where team_to_win_match is 0
    kept_entries = []
    for entry in entries:
        if entry["team_to_win_match"] != '0':
            if entry["team_to_win_match"] != '0.00':
                kept_entries.append(entry)
    entries = kept_entries

    return entries
# ==============================================================================
# Read all of Karl's marked fixtures from a csv file.
# ==============================================================================
def read_karls_marked_fixtures_from_csv_file():

    filename = '../05 - match karls fixtures with flashscore results'
    filename += ' - FINISHED/karls_fixtures_matched_with_flashscore_results.csv'

    karls_marked_fixtures = read_list_of_dictionaries_from_csv_file(
                                                                filename)

    # loop through all karls marked fixtures and:
    # 1. parse the correct score dictionaries
    # 2. parse the htft_result from a string into a four integer list
    #    (if it's a string that represents a four integer list)
    rebuilt_karls_fixtures = []
    for fixture in karls_marked_fixtures:
        # rebuild correct score strings as dictionaries
        fixture["home_team_correct_score_info"] = parse_correct_score_string(
                                        fixture["home_team_correct_score_info"])
        fixture["away_team_correct_score_info"] = parse_correct_score_string(
                                        fixture["away_team_correct_score_info"])
        fixture["draw_correct_score_info"] = parse_correct_score_string(
                                        fixture["draw_correct_score_info"])
        # rebuild htft_result string as a four integer list
        fixture["htft_result"] = parse_htft_result_string(
                                            fixture["htft_result"])
        rebuilt_karls_fixtures.append(fixture)
    karls_marked_fixtures = rebuilt_karls_fixtures

    return karls_marked_fixtures
# ==============================================================================
# Parse a correct score string in the format:
# '1_0__60p7___2_1__60p7___Other__47p21'
# and return a correct score dictionary in the form:
# {"1-0" : 60.7, "2-1" : 60.7, "Other" : 47.21}
# ==============================================================================
def parse_correct_score_string(correct_score_string):

    correct_score_string = correct_score_string.strip()
    correct_score_elements = correct_score_string.split('___')
    correct_score_dict = {}
    for correct_score_element in correct_score_elements:
        correct_score_element = correct_score_element.strip()
        elements = correct_score_element.split('__')
        current_key = elements[0].strip().replace('_', '-')
        current_value = float(elements[1].strip().replace('p', '.'))
        correct_score_dict[current_key] = current_value

    return correct_score_dict
# ==============================================================================
# For a htft result string in the format:
# '4_0_4_1'
# return a four integer list in the format:
# [4, 0, 4, 1]
# ==============================================================================
def parse_htft_result_string(htft_string):

    htft_string = htft_string.strip()

    # first, let's see if the htft_string is a valid htft_string
    if len(htft_string) < 7:
        return ''

    digits = '0123456789'
    total_underscores = 0
    total_digits = 0
    for character in htft_string:
        if character in digits:
            total_digits += 1
        if character == '_':
            total_underscores += 1

    if total_underscores < 3:
        return ''
    if total_digits < 4:
        return ''

    # if we've fallen through, we've got a valid htft_string, so parse it
    elements = htft_string.split('_')
    htft_list = []
    for element in elements:
        current_number = int(element)
        htft_list.append(current_number)

    return htft_list
# ==============================================================================
# From a csv file:
# 1. read the first line, lowercase it and use the column headers as keys for
#    a dictionary
# 2. loop through lines 2 onwards and build a dictionary for each line, using
#    the key names built in step 1.
# 3. return a list of all the dictionaries
# ==============================================================================
def read_list_of_dictionaries_from_csv_file(filename):

    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    # build list of dictionary keys
    first_line = lines[0].strip()
    elements = first_line.split(',')
    dict_keys = []
    for element in elements:
        dict_key = element.strip().lower()
        dict_keys.append(dict_key)

    # loop through lines from second line onwards and remove every line that's
    # less than two characters long
    record_lines = []
    for line in lines[1:]:
        line = line.strip()
        if len(line) > 2:
            record_lines.append(line)

    # loop through record lines. Build a dictionary for each record line and
    # append each dictionary to the list list_of_dicts
    list_of_dicts = []
    for line in record_lines:
        current_dict = {}
        line = line.strip()
        elements = line.split(',')
        for count in range(len(dict_keys)):
            dict_key = dict_keys[count]
            value = ''
            if count < len(elements):
                value = elements[count]
            current_dict[dict_key] = value
        list_of_dicts.append(current_dict)

    return list_of_dicts
# ==============================================================================
# Mark all the entries.
# ==============================================================================
def mark_all_entries(entries, karls_marked_fixtures):

    # First, let's build a dictionary where each key is an entry id and each
    # value is a list of all the karl fixture ids that match that entry
    entry_ids_and_matching_karl_fixture_ids = {}
    total_entries = len(entries)
    for count in range(len(entries)):
        if (count % 400) == 0:
            print('Finding karl fixture matches for entry #', str(count + 1),
                                              '/', str(total_entries), sep='')
        current_entry = entries[count]
        current_entry_id = current_entry["id"]
        # get a list containing the ids of all karls marked fixtures which match
        # the current entry
        matching_karl_marked_fixture_ids = find_matching_karl_marked_fixtures(
                                            current_entry, karls_marked_fixtures)
        entry_ids_and_matching_karl_fixture_ids[current_entry_id] = matching_karl_marked_fixture_ids

    # write entry_ids_and_karl_fixture_ids to a local csv file
    csv_text = 'ENTRY_ID,KARL_FIXTURE_ID_1,KARL_FIXTURE_ID_2,KARL_FIXTURE_ID_3'
    all_entry_ids = list(entry_ids_and_matching_karl_fixture_ids.keys())
    for entry_id in all_entry_ids:
        fixture_ids = entry_ids_and_matching_karl_fixture_ids[entry_id]
        # add entry_id to csv line
        csv_text += "\n" + str(entry_id)
        # add first matching fixture id to csv line
        if len(fixture_ids) > 0:
            csv_text += ',' + str(fixture_ids[0])
        # if there is more than one matching fixture id, add the rest of the
        # fixture ids to the csv line
        if len(fixture_ids) > 1:
            for fixture_id in fixture_ids[1:]:
                csv_text += ',' + str(fixture_id)

    # write csv text to local file
    outfile = open('entry_ids_and_matching_karl_fixture_ids.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    # build a dictionary containing only the key/value pairs from
    # entry_ids_and_matching_karl_fixture_ids where the values are lists
    # containing more than one karl fixture id
    entries_with_multiple_matches = {}
    all_keys = list(entry_ids_and_matching_karl_fixture_ids.keys())
    for current_entry_id in all_keys:
        matching_karl_fixture_ids = entry_ids_and_matching_karl_fixture_ids[
                                                            current_entry_id]
        if len(matching_karl_fixture_ids) > 1:
            entries_with_multiple_matches[current_entry_id] = matching_karl_fixture_ids

    # test print
    print('entries_with_multiple_matches:')
    print(entries_with_multiple_matches)

    # loop through entries with multiple matches; for each, print the datetimes
    # for the entry and the datetimes for the matching karl fixtures
    entry_ids = list(entries_with_multiple_matches.keys())
    for entry_id in entry_ids:
        # get the entry
        entry = ''
        for current_entry in entries:
            if current_entry["id"] == entry_id:
                entry = current_entry
                break
        # print entry date/time submission info
        # print('entry_id =', str(entry_id))
        # print the datetime when the entry was submitted
        # e.g. 'Submitted on 1/2/20 at 13:45'
        datetime_string = 'Submitted on ' + str(entry["day"]) + '/'
        datetime_string += str(entry["month"])
        datetime_string += '/' + str(entry["year"])[2:]
        datetime_string += ' at ' + str(entry["hour"]) + ':'
        datetime_string += str(entry["minute"])
        # print(datetime_string)
        # get matching fixtures
        matching_fixture_ids = entries_with_multiple_matches[entry_id]
        # loop through matching fixtures and print their details
        for fixture_id in matching_fixture_ids:
            # get the fixture
            fixture = ''
            for current_fixture in karls_marked_fixtures:
                if current_fixture["id"] == fixture_id:
                    fixture = current_fixture
                    break
            # print the fixture id and the datetime when the fixture took place
            # print('Fixture id =', str(fixture_id))
            datetime_string = 'Took place on ' + str(fixture["day"]) + '/'
            datetime_string += str(fixture["month"]) + '/'
            datetime_string += str(fixture["year"])[2:]
            datetime_string += ' at ' + str(fixture["hour"]) + ':'
            datetime_string += str(fixture["minute"])
            if datetime_string[-2] == ':':
                datetime_string += '0'
            # print(datetime_string)
        # print()

    # work out what fixture should match each entry with multiple fixture matches
    whittled_entry_and_fixture_ids = whittle_entries_with_multiple_matches(
                entries_with_multiple_matches, entries, karls_marked_fixtures)

    # Use entry_ids_and_matching_karl_fixture_ids and
    # whittled_entry_and_fixture_ids to build a dictionary where each
    # key is an entry id and each value is the id of the best matching karl
    # resulted fixture
    entry_ids_and_best_karl_fixture_matches = {}
    entry_ids = list(entry_ids_and_matching_karl_fixture_ids.keys())
    # print('Total entry ids =', str(len(entry_ids)))
    for entry_id in entry_ids:
        matching_fixtures_list = entry_ids_and_matching_karl_fixture_ids[
                                                                    entry_id]
        # if there are no matching fixtures for the entry, skip to the next entry
        if len(matching_fixtures_list) == 0:
            continue
        # if we've fallen through, there's at least one matching fixture for the entry
        best_matching_fixture_id = matching_fixtures_list[0]
        # if there are multiple matching fixtures, look up the best fixture
        # match in whittled_entry_and_fixture_ids
        if len(matching_fixtures_list) > 1:
            best_matching_fixture_id = whittled_entry_and_fixture_ids[entry_id]
        # store the key/value pair in entry_ids_and_best_karl_fixture_matches
        entry_ids_and_best_karl_fixture_matches[entry_id] = best_matching_fixture_id

    # write the entry ids and best karl fixture match ids to the local csv file
    # 'entry_ids_and_best_karl_fixture_matching_id.csv'
    write_entry_ids_and_best_karl_fixture_matching_id_to_csv_file(
                                        entry_ids_and_best_karl_fixture_matches)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # analyse the time differences between when entries are made and when the
    # matches take place. Calculate the time differences, then write a csv file
    # with lines in the form:
    # entry_id,karl_fixture_ids,time_differences_in_days
    #
    # Also build a list containing entry id/fixture id pairs for pairs with
    # positive time differences (i.e. where the entry has been submitted BEFORE
    # the fixture took place. This will remove entries that were submitted after
    # matches took place.
    # These entry id/fixture id pairs should be key/value pairs in the
    # dictionary on_time_entries_and_matching_fixture_ids
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print()
    print('Calculating time differences...')
    on_time_entries_and_fixture_ids = {}
    time_differences_in_days = []
    entry_ids = list(entry_ids_and_best_karl_fixture_matches.keys())
    for entry_id in entry_ids:
        karl_fixture_id = entry_ids_and_best_karl_fixture_matches[entry_id]
        # get entry
        entry = ''
        for current_entry in entries:
            if current_entry["id"] == entry_id:
                entry = current_entry
                break
        # check for no match
        if entry == '':
            print('entry not found!!!')
            exit(0)
        # get fixture
        fixture = ''
        for current_fixture in karls_marked_fixtures:
            if current_fixture["id"] == karl_fixture_id:
                fixture = current_fixture
                break
        # check for no fixture found
        if fixture == '':
            print('fixture not found!!!')
            print('entry_id =', str(entry_id))
            exit(0)
        # work out epoch datetime for entry
        entry_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(entry)
        # work out epoch datetime for fixture
        fixture_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(fixture)
        # calculate the time difference between when the entry was submitted
        # and when the fixture took place
        diff_in_seconds = fixture_epoch_datetime - entry_epoch_datetime
        seconds_in_one_day = 60 * 60 * 24
        diff_in_days = (float(diff_in_seconds) / float(seconds_in_one_day))
        time_differences_in_days.append(diff_in_days)
        if diff_in_days > 0:
            on_time_entries_and_fixture_ids[entry_id] = karl_fixture_id
        
    time_differences_in_days.sort()

    # print('Shortest ten time differences in days:')
    # for time_diff in time_differences_in_days[:10]:
    #    print(str(time_diff))
    # print()
    # print('Greatest ten time differences in days:')
    # for time_diff in time_differences_in_days[-10:]:
    #     print(str(time_diff))

    # write all the time differences to local file
    # 'entry_and_best_matching_fixtures_time_differences.txt'
    write_time_differences_to_local_text_file(time_differences_in_days)

    # print('entries[0]:')
    # print(entries[0])

    # build a list of users
    users = []
    for entry in entries:
        username = entry["username"]
        if not username in users:
            users.append(username)
    # print('users:')
    # print(users)

    # loop through users and mark the entries for each user
    marked_entries_for_all_users = {}
    for user in users:
        marked_entries_for_current_user = mark_entries_for_single_user(
            user, entries, karls_marked_fixtures, on_time_entries_and_fixture_ids)
        marked_entries_for_all_users[user] = marked_entries_for_current_user

    return marked_entries_for_all_users
# ==============================================================================
# Mark the entries for the user with username user.
# ==============================================================================
def mark_entries_for_single_user(user, entries, karls_marked_fixtures,
                                             on_time_entries_and_fixture_ids):

    # build a list of on time entry ids for the current user
    on_time_entry_ids = list(on_time_entries_and_fixture_ids.keys())
    current_user_on_time_entry_ids = []
    for entry in entries:
        if ((entry["id"] in on_time_entry_ids)
                and (entry["username"] == user)):
            current_user_on_time_entry_ids.append(entry["id"])

    print('Marking entries for', user)
    # print('Total on time entries =', str(len(current_user_on_time_entry_ids)))
    # print()
    # print('current user on time entry ids:')
    # print(current_user_on_time_entry_ids)

    # build a list of all the ids of all the fixtures for which the current user
    # has made entries
    fixture_ids = []
    for entry_id in current_user_on_time_entry_ids:
        fixture_id = on_time_entries_and_fixture_ids[entry_id]
        if not fixture_id in fixture_ids:
            fixture_ids.append(fixture_id)
    # print()
    # print('Total fixtures for which the user has made an entry =',
    #                                               str(len(fixture_ids)))

    # loop through fixture_ids and build a dictionary named
    # fixture_ids_and_on_time_entries. The key/value pairs in the dictionary will
    # be in the format:
    # <fixture id> / [list of on time entry ids for the current user]
    fixture_ids_and_on_time_entries = {}
    for current_fixture_id in fixture_ids:
        # find all the entries (for the current user) that match the current_fixture_id
        matching_entries = []
        for on_time_entry_id in current_user_on_time_entry_ids: # changed
            on_time_fixture_id = on_time_entries_and_fixture_ids[on_time_entry_id]
            if on_time_fixture_id == current_fixture_id:
                matching_entries.append(on_time_entry_id)
        fixture_ids_and_on_time_entries[current_fixture_id] = matching_entries

    # test print the dictionary fixture_ids_and_on_time_entries
    # dict_keys = list(fixture_ids_and_on_time_entries.keys())
    # for dict_key in dict_keys:
    #     print(str(dict_key), '-', fixture_ids_and_on_time_entries[dict_key])

    # rebuild fixture_ids_and_on_time_entries so that, for each on time entry list
    # that's matched to a fixture, if there's more than one entry id, extract the
    # entry id for the entry with the latest epoch datetime
    rebuilt_fixture_ids_and_on_time_entries = {}
    fixture_ids = list(fixture_ids_and_on_time_entries.keys())
    for fixture_id in fixture_ids:
        entry_ids = fixture_ids_and_on_time_entries[fixture_id]
        # find the id of the entry with the latest epoch datetime
        latest_entry_id = find_latest_entry_id_from_list_of_entry_ids(entry_ids,
                                                                            entries)
        rebuilt_fixture_ids_and_on_time_entries[fixture_id] = latest_entry_id
    fixture_ids_and_on_time_entries = rebuilt_fixture_ids_and_on_time_entries

    # test print
    # print()
    # print('fixture_ids_and_on_time_entries:')
    # fixture_ids = list(fixture_ids_and_on_time_entries.keys())
    # for fixture_id in fixture_ids:
    #    print(str(fixture_id), '-', str(fixture_ids_and_on_time_entries[fixture_id]))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # loop through each fixture id and on time entry pair. For each pair, we're
    # going to work out:
    # 1. how many match points the user got from this entry
    # 2. how many correct score points the user got from this entry
    # then we're going to build a resulted_entry dictionary in the form:
    #
    # {
    #   "fixture_id"                : 193,
    #   "entry_id"                  : 2048,
    #   "match_points_won"          : 31.78,
    #   "correct_score_points_won"  : 45.38
    # }
    #
    # All of the resulted_entry dictionaries will be appended to a list named
    # single_user_all_resulted_entries
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    single_user_all_resulted_entries = []
    fixture_ids = list(fixture_ids_and_on_time_entries.keys())
    for fixture_id in fixture_ids:
        entry_id = fixture_ids_and_on_time_entries[fixture_id]
        # print('=============================')
        # print('user =', user)
        # print('fixture id =', str(fixture_id))
        # print('entry id =', str(entry_id))
        # print()
        # get entry
        entry = ''
        for current_entry in entries:
            if current_entry["id"] == entry_id:
                entry = current_entry
                break
        # get fixture
        fixture = ''
        for current_fixture in karls_marked_fixtures:
            if current_fixture["id"] == fixture_id:
                fixture = current_fixture
                break
        # print entry and fixture
        # print()
        # print('entry:')
        # pretty_print_dictionary(entry)
        # print()
        # print('fixture:')
        # pretty_print_dictionary(fixture)
        # work out which team won ("home", "draw" or "away")
        htft_result = fixture["htft_result"]
        if len(htft_result) < 1:
            # print()
            # print('Fixture found with no htft_result:')
            # print()
            # pretty_print_dictionary(fixture)
            resulted_entry = {
                    "fixture_id"                : fixture_id,
                    "entry_id"                  : entry_id,
                    "match_points_won"          : 0,
                    "correct_score_points_won"  : 0
                            }
            single_user_all_resulted_entries.append(resulted_entry)
            continue
        ht_home = htft_result[0]
        ht_away = htft_result[1]
        ft_home = htft_result[2]
        ft_away = htft_result[3]
        if ft_home > ft_away:
            match_result = 'home'
        if ft_home < ft_away:
            match_result = 'away'
        if ft_home == ft_away:
            match_result = 'draw'
        # calculate match points won
        match_points_won = 0
        if entry["match_result"] == match_result:
            match_points_won = entry["match_result_points"]
        # calculate correct score points won
        correct_score_points_won = calculate_correct_score_points_won(
                                                            fixture, entry)
        # build dictionary resulted_entry and append it to
        # single_user_all_resulted_entries
        resulted_entry = {
                "fixture_id"                : fixture_id,
                "entry_id"                  : entry_id,
                "match_points_won"          : match_points_won,
                "correct_score_points_won"  : correct_score_points_won
                        }
        single_user_all_resulted_entries.append(resulted_entry)
    
    return single_user_all_resulted_entries
# ==============================================================================
# Calculate how many correct score points a user has won.
# ==============================================================================
def calculate_correct_score_points_won(fixture, entry):

    # print()
    # print('fixture:')
    # pretty_print_dictionary(fixture)
    # print()
    # print('entry:')
    # pretty_print_dictionary(entry)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # first, let's see if the user has predicted the correct correct score
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    user_correct_score_home_draw_or_away = entry["correct_score_team"]
    predicted_correct_score = entry["correct_score"]
    # print('user_home_draw_or_away =', user_home_draw_or_away)
    # print('user_correct_score =', user_correct_score)

    # build a correct score string for the actual full-time result of the match
    actual_ft_result_string = str(fixture["htft_result"][2]) + '-'
    actual_ft_result_string += str(fixture["htft_result"][3])
    # print('actual_ft_result_string =', actual_ft_result_string)

    # If the user has predicted 'away' for correct score team, we need to
    # reverse the digits in the user's predicted correct score before comparing
    # it with the actual full-time result string (unless the user selected
    # 'Other' for correct score...
    if predicted_correct_score != 'Other':
        predicted_correct_score = reverse_correct_score_string(
                                                        predicted_correct_score)

    # get the correct score dictionary for whatever correct score team the user
    # selected
    if user_correct_score_home_draw_or_away == 'home':
        correct_score_dict = fixture['home_team_correct_score_info']
    if user_correct_score_home_draw_or_away == 'draw':
        correct_score_dict = fixture['draw_correct_score_info']
    if user_correct_score_home_draw_or_away == 'away':
        correct_score_dict = fixture['away_team_correct_score_info']

    user_predicted_correct_score_correctly = 0
    # if the user selected 'Other' for correct score prediction
    # AND
    # actual_ft_result_string isn't present in the list of keys for the
    # correct score dictionary for the correct score team he/she has selected
    # (i.e. 'home', 'draw' or 'away'),
    # SET
    # user_predicted_correct_score_correctly
    if predicted_correct_score == 'Other':
        correct_score_dict_keys = list(correct_score_dict.keys())
        if not actual_ft_result_string in correct_score_dict_keys:
            user_predicted_correct_score_correctly = 1

    # If the user didn't select 'Other' for correct score,
    # AND
    # actual_ft_result_string matches predicted_correct_score
    # SET
    # user_predicted_correct_score_correctly
    if predicted_correct_score != 'Other':
        if actual_ft_result_string == predicted_correct_score:
            user_predicted_correct_score_correctly = 1

    # if the user didn't predict the correct score correctly, return zero
    # for zero correct score points
    if not user_predicted_correct_score_correctly:
        return 0

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # if we've fallen through, the user predicted the correct score correctly...
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # look up the value for correct score points in the appropriate home/draw/away
    # correct score dictionary for whatever value the user predicted and return it
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # get predicted_correct_score from entry again
    predicted_correct_score = entry["correct_score"]
    # look up the points value and return it
    correct_score_points_won = correct_score_dict[predicted_correct_score]
    
    return correct_score_points_won
# ==============================================================================
# Helper function for calculate_correct_score_points_won().
# Reverse a correct score string and return it.
# e.g. Given the correct score string '5-3', return '3-5'.
# ==============================================================================
def reverse_correct_score_string(correct_score_string):

    elements = correct_score_string.split('-')
    reversed_correct_score_string = str(elements[1].strip())
    reversed_correct_score_string += '-' + str(elements[0].strip())

    return reversed_correct_score_string
# ==============================================================================
# For a list of entry ids, find the id of the entry with the latest epoch
# datetime.
# ==============================================================================
def find_latest_entry_id_from_list_of_entry_ids(entry_ids, entries):

    # sanity test - if there is only one entry then by default it's the
    # latest entry
    if len(entry_ids) == 1:
        return entry_ids[0]

    # if we've fallen through, there is more than one entry id.
    # Get the first entry and work out the epoch datetime for it.
    first_entry_id = entry_ids[0]
    entry = ''
    for current_entry in entries:
        if current_entry["id"] == first_entry_id:
            entry = current_entry
            break
    first_entry_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(
                                                                        entry)
    # set latest epoch datetime
    latest_epoch_datetime = first_entry_epoch_datetime
    # set latest entry id
    latest_entry_id = first_entry_id
    # loop through the second to last entry id. For each entry id:
    # 1. get the entry
    # 2. build an epoch datetime for the entry
    # 3. if the current entry epoch datetime is later than
    #    latest_epoch_datetime:
    #    1. set latest entry id
    #    2. set latest epoch datetime
    for entry_id in entry_ids[1:]:
        # get entry
        entry = ''
        for current_entry in entries:
            if current_entry["id"] == entry_id:
                entry = current_entry
                break
        # build epoch datetime for entry
        current_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(
                                                                        entry)
        if current_epoch_datetime > latest_epoch_datetime:
            latest_entry_id = entry_id
            latest_epoch_datetime = current_epoch_datetime

    return latest_entry_id
# ==============================================================================
# Write all the time differences (in days) between entries and their best
# matched karl marked fixtures to local file 'time_differences_in_days.txt'
# ==============================================================================
def write_time_differences_to_local_text_file(time_differences_in_days):

    # build the file text
    file_text = ''
    for time_diff in time_differences_in_days:
        file_text += str(time_diff) + "\n"
    file_text = file_text.rstrip()

    # write text to file
    outfile = open('time_differences_in_days.txt', 'w')
    outfile.write(file_text)
    outfile.close()

    return
# ==============================================================================
# Loop through the key/value pairs in the dictionary
# entry_ids_and_best_karl_fixture_matches and write them to the local csv file
# 'entry_ids_and_best_karl_fixture_matching_id.csv'
# ==============================================================================
def write_entry_ids_and_best_karl_fixture_matching_id_to_csv_file(
                                    entry_ids_and_best_karl_fixture_matches):

    # ++++++++++++++
    # build csv text
    # ++++++++++++++
    # column headers
    csv_text = 'ENTRY_ID,KARL_MARKED_FIXTURE_ID'
    # record lines
    entry_ids = list(entry_ids_and_best_karl_fixture_matches.keys())
    for entry_id in entry_ids:
        karl_fixture_id = entry_ids_and_best_karl_fixture_matches[entry_id]
        csv_text += "\n" + str(entry_id) + ',' + str(karl_fixture_id)

    # write csv text to local csv file
    outfile = open('entry_ids_and_best_karl_fixture_matching_id.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# loop through entries with multiple matches. For each entry that matches
# more than one fixture:
# 1. get the epoch datetime for the entry
# 2. get the epoch datetimes for all the matching fixtures
# 3. remove all the fixtures that took place before the entry was submitted
# 4. sort the remaining matching fixtures into time order
# 5. select the fixture that took place soonest after the entry was submitted.
#    We'll use this as the matching fixture.
# ==============================================================================
def whittle_entries_with_multiple_matches(entries_with_multiple_matches,
                                            entries, karls_marked_fixtures):
    
    rebuilt_entries_with_multiple_matches = {}

    entry_ids = list(entries_with_multiple_matches.keys())
    for entry_id in entry_ids:
        # get the entry
        entry = ''
        for current_entry in entries:
            if current_entry["id"] == entry_id:
                entry = current_entry
                break
        # get the ids for the matching karl fixtures
        matching_fixture_ids = entries_with_multiple_matches[entry_id]
        # get the matching fixtures
        matching_fixtures = []
        for fixture_id in matching_fixture_ids:
            # find all the fixtures that match the current fixture_id and push
            # them onto matching_fixtures
            for fixture in karls_marked_fixtures:
                if fixture["id"] == fixture_id:
                    matching_fixtures.append(fixture)
        # work out the epoch datetime for the entry
        entry_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(entry)
        # print('entry_epoch_datetime:')
        # print(entry_epoch_datetime)
        # Work out the epoch datetimes for all the matching fixtures.
        # For each fixture, insert a key/value pair in the form
        # <fixture epoch datetime> / <fixture>
        # into the dictionary epoch_datetimes_and_fixtures
        epoch_datetimes_and_fixtures = {}
        for fixture in matching_fixtures:
            fixture_epoch_datetime = build_epoch_datetime_from_entry_or_fixture(
                                                                        fixture)
            epoch_datetimes_and_fixtures[fixture_epoch_datetime] = fixture
        # build a list of all the epoch datetimes
        fixture_epoch_datetimes = list(epoch_datetimes_and_fixtures.keys())
        # rebuild fixture epoch datetimes so that it only contains fixture
        # epoch datetimes than fall after the entry epoch datetime
        rebuilt_fixture_epoch_datetimes = []
        for fixture_epoch_datetime in fixture_epoch_datetimes:
            if fixture_epoch_datetime > entry_epoch_datetime:
                rebuilt_fixture_epoch_datetimes.append(fixture_epoch_datetime)
        fixture_epoch_datetimes = rebuilt_fixture_epoch_datetimes
        # if more than a single fixture epoch datetime remains, sort the fixture
        # epoch datetimes into order
        if len(fixture_epoch_datetimes) > 1:
            fixture_epoch_datetimes.sort()
        # get the first epoch datetime
        first_epoch_datetime = fixture_epoch_datetimes[0]
        # use the first epoch datetime to look up the best matching fixture in
        # the dictionary epoch_datetimes_and_fixtures
        best_matching_fixture = epoch_datetimes_and_fixtures[first_epoch_datetime]
        # look up the fixture id in best_matching_fixture
        best_matching_fixture_id = best_matching_fixture["id"]
        # stick the key/value pair (entry_id/best_matching_fixture_id) in the
        # dictionary rebuilt_entries_with_multiple_matches
        rebuilt_entries_with_multiple_matches[entry_id] = best_matching_fixture_id

    # test print whittled id pairs
    # print()
    # print('whittled id pairs:')
    # print(rebuilt_entries_with_multiple_matches)
    # exit(0)

    return rebuilt_entries_with_multiple_matches
# ==============================================================================
# Builds an epoch datetime from an entry.
# ==============================================================================
def build_epoch_datetime_from_entry_or_fixture(dictionary):

    epoch_datetime = datetime.datetime(
                                int(dictionary["year"]),
                                int(dictionary["month"]),
                                int(dictionary["day"]),
                                int(dictionary["hour"]),
                                int(dictionary["minute"])
                                            ).timestamp()
    epoch_datetime = int(epoch_datetime)

    return epoch_datetime
# ==============================================================================
# For the user entry entry, find the fixtures in karls_marked_fixtures which
# match that entry. Build a list containing the ids of all the matching fixtures
# and return the list.
# ==============================================================================
def find_matching_karl_marked_fixtures(entry, karls_marked_fixtures):

    matching_karl_fixture_ids = []
    for count in range(len(karls_marked_fixtures)):
        karl_marked_fixture = karls_marked_fixtures[count]
        if entry_matches_karls_marked_fixture(entry, karl_marked_fixture):            
            karl_fixture_id = karl_marked_fixture["id"]
            matching_karl_fixture_ids.append(karl_fixture_id)

    return matching_karl_fixture_ids
# ==============================================================================
# For a user entry and one of karls marked fixtures, check that the following
# items match:
# 1. match result points
# 2. correct score points for the correct score the user has selected
# If both the above conditions have been passed, return 1 for a match,
# otherwise return 0 for no match.
# ==============================================================================
def entry_matches_karls_marked_fixture(entry, karl_marked_fixture):

    # ++++++++++++++++++++++++++++++++++++
    # check that match result points match
    # ++++++++++++++++++++++++++++++++++++
    # get entry match result points and match result selection
    entry_match_result_points = entry["match_result_points"]
    entry_match_result_selection = entry["match_result"]
    # print('entry_match_result_points =', str(entry_match_result_points))
    # print('entry_match_result_selection =', entry_match_result_selection)
    # get karl fixture match result points
    if entry_match_result_selection == 'home':
        karl_match_result_points = karl_marked_fixture["home_team_win_points"]
    if entry_match_result_selection == 'away':
        karl_match_result_points = karl_marked_fixture["away_team_win_points"]
    if entry_match_result_selection == 'draw':
        karl_match_result_points = karl_marked_fixture["draw_points"]
    # print('karl_match_result_points =', str(karl_match_result_points))
    # if entry match result points doesn't match karl fixture match result points
    # return 0 for no match
    if entry_match_result_points != karl_match_result_points:
        # print('entry_match_result_points and karl_match_result_points')
        # print('do not match.')
        return 0

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # check that correct score points for the correct score the user has
    # selected match
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # get entry correct score points
    entry_correct_score_team = entry["correct_score_team"]
    entry_correct_score = entry["correct_score"]
    entry_correct_score_points = entry["correct_score_points"]
    # print()
    # print('entry_correct_score_team =', entry_correct_score_team)
    # print('entry_correct_score =',entry_correct_score)
    # print('entry_correct_score_points =', str(entry_correct_score_points))
    # get karl fixture correct score points
    if entry_correct_score_team == 'home':
        fixture_correct_score_dict = karl_marked_fixture[
                                        "home_team_correct_score_info"]
        dict_keys = list(fixture_correct_score_dict.keys())
        if not entry_correct_score in dict_keys:
            entry_correct_score = 'Other'
        fixture_correct_score_points = fixture_correct_score_dict[
                                                    entry_correct_score]
    if entry_correct_score_team == 'draw':
        fixture_correct_score_dict = karl_marked_fixture[
                                        "draw_correct_score_info"]
        dict_keys = list(fixture_correct_score_dict.keys())
        if not entry_correct_score in dict_keys:
            entry_correct_score = 'Other'
        fixture_correct_score_points = fixture_correct_score_dict[
                                                    entry_correct_score]
    if entry_correct_score_team == 'away':
        fixture_correct_score_dict = karl_marked_fixture[
                                        "away_team_correct_score_info"]
        dict_keys = list(fixture_correct_score_dict.keys())
        if not entry_correct_score in dict_keys:
            entry_correct_score = 'Other'
        fixture_correct_score_points = fixture_correct_score_dict[
                                                    entry_correct_score]
    # print('fixture_correct_score_points =', str(fixture_correct_score_points))
    # convert points to floats
    entry_correct_score_points = float(entry_correct_score_points)
    fixture_correct_score_points = float(fixture_correct_score_points)
    # if entry correct score points doesn't match karl fixture correct score
    # points, return 0 for no match
    if entry_correct_score_points != fixture_correct_score_points:
        # print('entry_correct_score_points does not match')
        # print('fixture_correct_score_points...')
        return 0

    # if we've fallen through, all the tests for matching an entry and a karl
    # marked fixture have been passed
    # print('all matching tests have been passed...')
    return 1
# ==============================================================================
# Print a dictionary with each key and value on a separate line.
# ==============================================================================
def pretty_print_dictionary(the_dict):

    dict_keys = list(the_dict.keys())

    for current_key in dict_keys:
        print(current_key, ':', sep='')
        print(the_dict[current_key])

    return
# ==============================================================================
# Write marked entries to a local csv file named "marked_entries.csv".
# This file will be saved in a subfolder named "output_files"
# Each marked entry is going to be represented by a csv line in the format:
# <user>,<fixture_id>,<entry_id>,<match_points_won>,<correct_score_points_won>
# e.g.
# Miktor,2,3,23.45,49.3
# ==============================================================================
def write_marked_entries_to_csv_file(marked_entries):

    # get a list of the keys in marked_entries (these are the usernames)
    usernames = list(marked_entries.keys())

    # ++++++++++++++++++
    # build the csv text
    # ++++++++++++++++++
    # header line
    csv_text = 'username,fixture_id,entry_id,match_points_won'
    csv_text += ',correct_score_points_won'
    # loop through the usernames and write the lines for the csv file
    for username in usernames:
        result_dicts = marked_entries[username]
        for result_dict in result_dicts:
            csv_text += "\n" + username
            csv_text += ',' + str(result_dict["fixture_id"])
            csv_text += ',' + str(result_dict["entry_id"])
            csv_text += ',' + str(result_dict["match_points_won"])
            csv_text += ',' + str(result_dict["correct_score_points_won"])

    # write csv_text to file
    outfile = open('output_files/marked_entries.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Write a csv spreadsheet file containing all the entries.
# Each entry will be represented by a csv line in the format:
# entry_id,username,year,month,day,hour,minute,second,team_to_win_match,
# match_result,correct_score_team,correct_score,match_result_points,
# correct_score_points
#
# The csv spreadsheet will be named 'entries.csv' and will be saved in the local
# subfolder 'output_files'
# ==============================================================================
def write_entries_to_csv_file(entries):

    # get keys
    entry_keys = list(entries[0].keys())

    # ++++++++++++++
    # build csv text
    # ++++++++++++++
    # column header line
    csv_text = 'ENTRY_ID,USERNAME,YEAR,MONTH,DAY,HOUR,MINUTE,SECOND'
    csv_text += ',TEAM_TO_WIN_MATCH,MATCH_RESULT,CORRECT_SCORE_TEAM'
    csv_text += ',CORRECT_SCORE,MATCH_RESULT_POINTS,CORRECT_SCORE_POINTS'
    # loop through entries and write the result of the csv file
    for entry in entries:
        csv_text += "\n"
        # entry id
        csv_text += str(entry["id"])
        # username
        csv_text += ',' + entry["username"]
        # year
        csv_text += ',' + str(entry["year"])
        # month
        csv_text += ',' + str(entry["month"])
        # day
        csv_text += ',' + str(entry["day"])
        # hour
        csv_text += ',' + str(entry["hour"])
        # minute
        csv_text += ',' + str(entry["minute"])
        # second
        csv_text += ',' + str(entry["second"])
        # team_to_win_match
        csv_text += ',' + entry["team_to_win_match"]
        # match_result
        csv_text += ',' + entry["match_result"]
        # correct_score_team
        csv_text += ',' + entry["correct_score_team"]
        # correct_score
        csv_text += ',' + entry["correct_score"]
        # match_result_points
        csv_text += ',' + str(entry["match_result_points"])
        # correct_score_points
        csv_text += ',' + str(entry["correct_score_points"])

    # write csv text to local file
    outfile = open('output_files/entries.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Write a csv spreadsheet containing all karls marked entries.
# The csv file will be named 'karls_marked_entries.csv'. It will be saved in
# the local subfolder 'output_files'.
# Each csv line will be in the following format:
# fixture_id,filename,year,month,day,hour,minute,home_team,away_team,
# home_team_win_points,draw_points,away_team_win_points,
# home_team_correct_score_info,draw_correct_score_info,
# away_team_correct_score_info,htft_result
# ==============================================================================
def write_karls_marked_fixtures_to_csv_file(karls_marked_fixtures):

    # ++++++++++++++
    # build csv text
    # ++++++++++++++
    # column header line
    csv_text = 'FIXTURE_ID,FILENAME,YEAR,MONTH,DAY,HOUR,MINUTE,HOME_TEAM'
    csv_text += ',AWAY_TEAM'
    csv_text += ',HOME_TEAM_WIN_POINTS,DRAW_POINTS,AWAY_TEAM_WIN_POINTS'
    csv_text += ',HOME_TEAM_CORRECT_SCORE_INFO,DRAW_CORRECT_SCORE_INFO'
    csv_text += ',AWAY_TEAM_CORRECT_SCORE_INFO,HTFT_RESULT'
    # record lines
    for fixture in karls_marked_fixtures:
        csv_text += "\n"
        # fixture_id
        csv_text += str(fixture["id"])
        # filename
        csv_text += ',' + fixture["filename"]
        # year
        csv_text += ',' + str(fixture["year"])
        # month
        csv_text += ',' + str(fixture["month"])
        # day
        csv_text += ',' + str(fixture["day"])
        # hour
        csv_text += ',' + str(fixture["hour"])
        # minute
        csv_text += ',' + str(fixture["minute"])
        # home_team
        csv_text += ',' + fixture["home_team"]
        # away_team
        csv_text += ',' + fixture["away_team"]
        # home_team_win_points
        csv_text += ',' + str(fixture["home_team_win_points"])
        # draw_points
        csv_text += ',' + str(fixture["draw_points"])
        # away_team_win_points
        csv_text += ',' + str(fixture["away_team_win_points"])
        # home_team_correct_score_info
        home_team_correct_score_dict = fixture["home_team_correct_score_info"]
        home_team_correct_score_string = build_correct_score_string(
                                                home_team_correct_score_dict)
        csv_text += ',' + home_team_correct_score_string
        # draw_correct_score_info
        draw_correct_score_dict = fixture["draw_correct_score_info"]
        draw_correct_score_string = build_correct_score_string(
                                                    draw_correct_score_dict)
        csv_text += ',' + draw_correct_score_string
        # away team_correct_score_info
        away_team_correct_score_dict = fixture["away_team_correct_score_info"]
        away_team_correct_score_string = build_correct_score_string(
                                                away_team_correct_score_dict)
        csv_text += ',' + away_team_correct_score_string
        # htft_result
        htft_result = fixture["htft_result"]
        htft_result_string = build_htft_result_string(htft_result)
        csv_text += ',' + htft_result_string

    # write csv text to local file
    # 'karls_marked_entries.csv'
    outfile = open('output_files/karls_marked_entries.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Helper function for write_karls_marked_fixtures_to_csv_file().
# From a correct score dictionary in the format:
# {'1-0': 60.7, '2-1': 60.7, 'Other': 47.21}
# build a correct_score_string in the format:
# '1_0__60p7___2_1__60p7___Other__47p21'
# and return it.
# ==============================================================================
def build_correct_score_string(correct_score_dict):

    correct_score_keys = list(correct_score_dict.keys())

    correct_score_strings_and_price_strings = []    # container list
    for correct_score_key in correct_score_keys:
        # transform correct score key
        correct_score_key_string = correct_score_key.replace('-', '_')
        # transform price
        price = correct_score_dict[correct_score_key]
        price_string = str(price).replace('.', 'p')
        # build two item list and append it to
        # correct_score_strings_and_price_strings
        two_item_list = [correct_score_key_string, price_string]
        correct_score_strings_and_price_strings.append(two_item_list)

    # loop through all the two item lists and build the correct score string
    first_two_item_list = correct_score_strings_and_price_strings[0]
    correct_score_string = first_two_item_list[0] + '__'
    correct_score_string += first_two_item_list[1]
    # if there is more than a single two item list, build the rest of the
    # correct score string
    if len(correct_score_strings_and_price_strings) > 1:
        for two_item_list in correct_score_strings_and_price_strings[1:]:
            current_string = two_item_list[0] + '__' + two_item_list[1]
            correct_score_string += '___' + current_string

    return correct_score_string
# ==============================================================================
# From a htft_result in the format:
# [2, 0, 3, 1]
# build a htft result string in the format
# '2_0_3_1'
# and return it.
# ==============================================================================
def build_htft_result_string(htft_result):

    # sanity test #1 - if htft_result is not a list, return an empty string
    if not type(htft_result) is list:
        print('This htft_result is not a list:')
        print(htft_result)
        return ''

    # sanity test #2 - if htft_result doesn't contain 4 elements, return
    # an empty string
    if len(htft_result) != 4:
        print('This htft_result does not contain 4 elements:')
        print(htft_result)
        return ''

    # if we've fallen through, we know that:
    # 1. htft_result is a list, and...
    # 2. it contains 4 elements
    # so build the string and return it
    htft_result_string = str(htft_result[0])
    for element in htft_result[1:]:
        htft_result_string += '_' + str(element)

    return htft_result_string
# ==============================================================================
# write the following information to three separate javascript files:
# 1. entries
# 2. karls_marked_fixtures
# 3. marked_entries
# in the subfolder 'output_javascript_files'
# ==============================================================================
def write_all_important_info_to_javascript_files(entries,
                                    karls_marked_fixtures, marked_entries):

    # build javascript string for entries
    js_string = str(entries)
    js_string = js_string.replace('},', '},' + "\n")
    js_string = 'var entries = ' + js_string + ';'

    # write javascript string to local file 'entries.js' in subfolder
    # 'javascript_output_files'
    outfile = open('javascript_output_files/entries.js', 'w')
    outfile.write(js_string)
    outfile.close()

    # build javascript string for karls marked fixtures
    js_string = str(karls_marked_fixtures)
    js_string = js_string.replace('},', '},' + "\n")
    js_string = 'var karls_marked_fixtures = ' + js_string + ';'
    
    # write javascript string to local file 'karls_marked_fixtures.js'
    # in subfolder 'javascript_output_files'
    outfile = open('javascript_output_files/karls_marked_fixtures.js', 'w')
    outfile.write(js_string)
    outfile.close()

    # build javascript string for marked entries
    js_string = str(marked_entries)
    js_string = js_string.replace('},', '},' + "\n")
    js_string = 'var marked_entries = ' + js_string + ';'
    
    # write javascript string to local file 'marked_entries.js'
    # in subfolder 'javascript_output_files'
    outfile = open('javascript_output_files/marked_entries.js', 'w')
    outfile.write(js_string)
    outfile.close()

    return
# ==============================================================================
main()
