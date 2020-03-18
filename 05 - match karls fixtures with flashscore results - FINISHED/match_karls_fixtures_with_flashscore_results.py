# ==============================================================================
import datetime
# ==============================================================================
def main():

    match_karls_fixtures_with_flashscore_results()

    print()
    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# ==============================================================================
def match_karls_fixtures_with_flashscore_results():

    # read karls fixtures from csv file
    karls_fixtures = read_karls_fixtures_from_csv_file()
    print('Total Karl fixtures =', str(len(karls_fixtures)))

    # read flashscore results records from csv file
    flashscore_results = read_flashscore_results_from_csv_file()

    # normalise all the team names so that they correspond to the
    # flashscore team names
    karls_fixtures = normalise_karls_fixture_team_names(karls_fixtures)

    # fix a bug where a tranche of karl's fixtures don't have the correct year
    karls_fixtures = fix_incorrect_year_in_tranche_of_fixtures(karls_fixtures)

    # match flashscore ht/ft scores to karls fixtures
    karls_fixtures = match_flashscore_htft_scores_to_karls_fixtures(karls_fixtures,
                                                    flashscore_results)

    # sort Karls fixtures into time order (from oldest to most recent)
    karls_fixtures = sort_karls_fixtures_into_time_order(karls_fixtures)

    # Write new csv file containing karls fixtures with htft scores matched
    # to them. Call it 'karls_fixtures_matched_with_flashscore_results.csv'
    write_karls_fixtures_to_csv(karls_fixtures)

    return
# ==============================================================================
# Build a list of all the team names in:
# 1. Karls fixtures
# 2. the flashscore results
# ==============================================================================
def analyse_team_names(karls_fixtures, flashscore_results):

    # build a list of all team names in karls fixtures
    karls_fixture_team_names = []
    for fixture in karls_fixtures:
        team_name = fixture["home_team"]
        if not team_name in karls_fixture_team_names:
            karls_fixture_team_names.append(team_name)
        team_name = fixture["away_team"]
        if not team_name in karls_fixture_team_names:
            karls_fixture_team_names.append(team_name)
    karls_fixture_team_names.sort()
    
    # build a list of all team names in flashscore results
    flashscore_team_names = []
    for flashscore_result in flashscore_results:
        team_name = flashscore_result["home_team"]
        if not team_name in flashscore_team_names:
            flashscore_team_names.append(team_name)
        team_name = flashscore_result["away_team"]
        if not team_name in flashscore_team_names:
            flashscore_team_names.append(team_name)
    flashscore_team_names.sort()

    # build the text for a csv file with the first column containing team names
    # from Karls fixtures and the second column empty for a flashscore team name
    csv_text = 'KARLS_FIXTURE_TEAM_NAME,FLASHSCORE_RESULT_NAME'
    for team_name in karls_fixture_team_names:
        csv_text += "\n" + team_name + ','

    # write the csv text to a local file named 'proto_team_name_conversions.csv'
    outfile = open('proto_team_name_conversions.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Normalise the team names for Karls fixtures so that they match the flashscore
# result team names.
# ==============================================================================
def normalise_karls_fixture_team_names(karls_fixtures):

    # read names conversions from local csv file
    infile = open('team_name_conversions.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # loop through second line onwards. Remove any line that's less than
    # five characters in length
    kept_lines = []
    for line in lines[1:]:
        line = line.strip()
        if len(line) > 5:
            kept_lines.append(line)
    lines = kept_lines

    # build a dictionary with karls team names for keys and flashscore team
    # names for values
    karl_team_names_and_flashscore_names = {}
    for line in lines:
        line = line.strip()
        elements = line.split(',')
        the_key = elements[0].strip()
        the_value = elements[1].strip()
        karl_team_names_and_flashscore_names[the_key] = the_value

    # loop through karls fixtures and replace all the team names with
    # flashscore team names. If we encounter a karl team name that cannot be
    # replaced with a flashscore team name, alert the user to enter the
    # conversion in local file 'team_name_conversions.csv', then stop.
    karls_team_names = list(karl_team_names_and_flashscore_names.keys())
    rebuilt_karls_fixtures = []
    for fixture in karls_fixtures:
        if fixture["home_team"] in karls_team_names:
            fixture["home_team"] = karl_team_names_and_flashscore_names[
                                                        fixture["home_team"]]
        else:
            print('Please add a flashscore team name conversion for the')
            print('name', fixture["home_team"], 'to the local file')
            print('team_name_conversions.csv')
        if fixture["away_team"] in karls_team_names:
            fixture["away_team"] = karl_team_names_and_flashscore_names[
                                                        fixture["away_team"]]
        else:
            print('Please add a flashscore team name conversion for the')
            print('name', fixture["home_team"], 'to the local file')
            print('team_name_conversions.csv')
        rebuilt_karls_fixtures.append(fixture)
    karls_fixtures = rebuilt_karls_fixtures

    return karls_fixtures
# ==============================================================================
def read_karls_fixtures_from_csv_file():
    
    # read karls fixtures from csv file
    filename = '../04 - parse karls spreadsheet fixtures from admin webpage'
    filename += ' - FINISHED/all_karls_fixtures.csv'
    karls_fixtures = read_dictionaries_from_csv_file(filename)

    first_karl_fixture = karls_fixtures[0]

    dict_keys = list(first_karl_fixture.keys())

    # rebuild the fixture dictionaries with the correct score points strings
    # changed to dictionaries and the htft_result string transformed into a
    # four integer list
    rebuilt_fixture_dictionaries = []
    for fixture_dict in karls_fixtures:
        if fixture_dict["home_team_correct_score_info"] != '':
            home_team_correct_score_dict = parse_correct_score_string(
                                fixture_dict["home_team_correct_score_info"])
            fixture_dict["home_team_correct_score_info"] = home_team_correct_score_dict
        if fixture_dict["away_team_correct_score_info"] != '':
            away_team_correct_score_dict = parse_correct_score_string(
                                fixture_dict["away_team_correct_score_info"])
            fixture_dict["away_team_correct_score_info"] = away_team_correct_score_dict
        if fixture_dict["draw_correct_score_info"] != '':
            draw_correct_score_dict = parse_correct_score_string(
                                fixture_dict["draw_correct_score_info"])
            fixture_dict["draw_correct_score_info"] = draw_correct_score_dict
        if fixture_dict["htft_result"] != '':
            htft_result_list = parse_htft_result_string(fixture_dict["htft_result"])
            fixture_dict["htft_result"] = htft_result_list
        rebuilt_fixture_dictionaries.append(fixture_dict)
        
    fixture_dictionaries = rebuilt_fixture_dictionaries

    return fixture_dictionaries
# ==============================================================================
# Transform a correct score string in the format:
# '0_0__31p09___1_1__28p13___Other__45p8'
# into a dictionary in the form:
# {"0-0" : 31.09, "1-1" : 28.13, "Other" : 45.8}
# ==============================================================================
def parse_correct_score_string(correct_score_string):

    correct_score_dict = {}

    correct_score_string = correct_score_string.strip()
    elements = correct_score_string.split('___')
    for element in elements:
        correct_score_and_points = element.split('__')
        correct_score_string = correct_score_and_points[0].strip().replace('_', '-')
        correct_score_value = float(correct_score_and_points[1].strip().replace('p', '.'))
        correct_score_dict[correct_score_string] = correct_score_value

    return correct_score_dict
# ==============================================================================
# Transform a htft result string in the form:
# '4_0_4_1'
# into a list in the form:
# [4, 0, 4, 1]
# ==============================================================================
def parse_htft_result_string(htft_string):

    htft_string = htft_string.strip()

    if len(htft_string) == 0:
        return []

    elements = htft_string.split('_')
    htft_list = []
    for element in elements:
        element = element.strip()
        element = int(element)
        htft_list.append(element)

    return htft_list
# ==============================================================================
# Read a bunch of records from the csv file with filename filename.
# Use the column names (changed to lowercase) for dictionary keys and the
# cell values for values, with each line after the first representing a
# single record/dictionary.
# ==============================================================================
def read_dictionaries_from_csv_file(filename):

    # read lines from file
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    # build list of dictionary keys
    first_line = lines[0].strip()
    elements = first_line.split(',')
    dictionary_keys = []
    for element in elements:
        dictionary_key = element.lower()
        dictionary_keys.append(dictionary_key)

    # loop through lines 1 to end and build all the dictionaries for each record
    # in the csv file
    list_of_dictionaries = []
    for line in lines[1:]:
        line = line.strip()
        elements = line.split(',')
        rebuilt_elements = []
        for element in elements:
            element = element.strip()
            rebuilt_elements.append(element)
        elements = rebuilt_elements
        # if all elements are zero length, continue with building a dictionary
        # for the current line
        total_non_zero_length_elements = 0
        for element in elements:
            if len(element) > 0:
                total_non_zero_length_elements += 1
        if total_non_zero_length_elements == 0:
            continue
        # build a dictionary for the current line
        current_dictionary = {}
        for count in range(len(dictionary_keys)):
            current_key = dictionary_keys[count]
            current_value = ''
            if count < len(elements):
                current_value = elements[count]
            current_dictionary[current_key] = current_value
        list_of_dictionaries.append(current_dictionary)

    return list_of_dictionaries
# ==============================================================================
# Read the flashscore results from the csv file.
# ==============================================================================
def read_flashscore_results_from_csv_file():

    filename = '../02 - build result csv spreadsheet from flashscore results '
    filename += 'text file - FINISHED/flashscore premier league results '
    filename += '2019 to 2020.csv'

    flashscore_results = read_dictionaries_from_csv_file(filename)
    
    return flashscore_results
# ==============================================================================
# Loop through all the fixtures in karls fixtures. If any of Karls fixtures
# don't have a htft score, attempt to find and match a htft score from
# flashscore_results.
# ==============================================================================
def match_flashscore_htft_scores_to_karls_fixtures(karls_fixtures,
                                                        flashscore_results):

    # count how many of karls fixtures don't have a htft_result
    total_non_htft_fixtures = 0
    for fixture in karls_fixtures:
        fixture_keys = list(fixture.keys())
        if not 'htft_result' in fixture_keys:
            total_non_htft_fixtures += 1
            continue
        if fixture["htft_result"] == '':
            total_non_htft_fixtures += 1
            continue
        if fixture["htft_result"] == []:
            total_non_htft_fixtures += 1
            continue
    print('Before resulting, total Karls fixtures without a result:')
    print(str(total_non_htft_fixtures))

    # Build two lists.
    # (1) a list of Karls fixtures that have htft results
    # (2) a list of Karl fixture that don't have htft results
    resulted_karls_fixtures = []
    unresulted_karls_fixtures = []
    for fixture in karls_fixtures:
        fixture_keys = list(fixture.keys())
        if not 'htft_result' in fixture_keys:
            unresulted_karls_fixtures.append(fixture)
            continue
        if fixture["htft_result"] == '':
            unresulted_karls_fixtures.append(fixture)
            continue
        if fixture["htft_result"] == []:
            unresulted_karls_fixtures.append(fixture)
            continue
        # if we've fallen through, the fixture has a htft result
        resulted_karls_fixtures.append(fixture)

    # loop through unresulted Karls fixtures; for each unresulted fixture, try
    # to find a matching result in flashscore_results
    newly_resulted_fixtures = []
    for unresulted_fixture in unresulted_karls_fixtures:
        newly_resulted_fixture = use_flashscore_results_to_result_fixture(
                                        unresulted_fixture, flashscore_results)
        newly_resulted_fixtures.append(newly_resulted_fixture)

    # work out how many fixtures we've been able to result
    total_newly_resulted_fixtures = 0
    for fixture in newly_resulted_fixtures:
        fixture_keys = list(fixture.keys())
        if 'htft_result' in fixture_keys:
            if type(fixture["htft_result"]) is list:
                if len(fixture["htft_result"]) == 4:
                    total_newly_resulted_fixtures += 1

    print('total newly resulted fixtures =', str(total_newly_resulted_fixtures))

    # make a big list with karls_resulted_fixtures plus the list
    # newly_resulted_fixtures (some of which may not actually have been
    # resulted...
    all_karls_fixtures = resulted_karls_fixtures + newly_resulted_fixtures


    return all_karls_fixtures
# ==============================================================================
# Loop through the list flashscore_results and attempt to find a result that
# matches Karls unresulted fixture unresulted_fixture. If a matching flashscore
# result is found, stick the result in unresulted_fixture and return it,
# otherwise just return it without the result.
# ==============================================================================
def use_flashscore_results_to_result_fixture(unresulted_fixture,
                                                    flashscore_results):

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # for matching, we're going to look for a flashscore result where the
    # following values match those of the unresulted fixture:
    # year
    # month
    # day
    # hour
    # minute
    # home team
    # away team
    # How to do this?
    # Build a string in the form:
    # <year>_<month>_<day>_<hour>_<minute>_<home_team>_<away_team>
    # for both dictionaries (with all substrings in lowercase), then use the
    # two strings to search for a match
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    karl_fixture_match_string = build_matching_string_from_dict(
                                                    unresulted_fixture)
    for flashscore_result in flashscore_results:
        flashscore_match_string = build_matching_string_from_dict(
                                                        flashscore_result)
        if karl_fixture_match_string == flashscore_match_string:
            ht_ft_result = [
                int(flashscore_result["home_ht"]),
                int(flashscore_result["away_ht"]),
                int(flashscore_result["home_ft"]),
                int(flashscore_result["away_ft"])
                            ]
            unresulted_fixture["htft_result"] = ht_ft_result
            break

    return unresulted_fixture
# ==============================================================================
# Helper function for use_flashscore_results_to_result_fixture().
# From dictionary the_dict, build a string in the form:
# <year>_<month>_<day>_<hour>_<minute>_<home_team>_<away_team>
# with all substrings in lowercase and return it.
# ==============================================================================
def build_matching_string_from_dict(the_dict):

    matching_string = the_dict["year"].lower()
    matching_string += '_' + the_dict["month"].lower()
    matching_string += '_' + the_dict["day"].lower()
    matching_string += '_' + the_dict["hour"].lower()
    matching_string += '_' + the_dict["minute"].lower()
    matching_string += '_' + the_dict["home_team"].lower()
    matching_string += '_' + the_dict["away_team"].lower()

    return matching_string
# ==============================================================================
# Print the dictionary dict_to_print with all keys and values on separate lines.
# ==============================================================================
def pretty_print_dictionary(dict_to_print):

    dict_keys = list(dict_to_print.keys())

    for dict_key in dict_keys:
        print(dict_key)
        print(dict_to_print[dict_key])

    return
# ==============================================================================
# Fix incorrect year in some of Karl's fixtures by looping through all Karls
# fixtures and setting the year to be the first element when the filename is
# split by '_' substrings.
# ==============================================================================
def fix_incorrect_year_in_tranche_of_fixtures(karls_fixtures):

    rebuilt_karls_fixtures = []
    for fixture in karls_fixtures:
        elements = fixture["filename"].split('_')
        fixture["year"] = elements[0].strip()
        rebuilt_karls_fixtures.append(fixture)
    karls_fixtures = rebuilt_karls_fixtures

    return karls_fixtures
# ==============================================================================
# Sort Karls fixtures into time order, then return them.
# ==============================================================================
def sort_karls_fixtures_into_time_order(karls_fixtures):

    # build a list of unique epoch datetimes from karls fixtures
    epoch_datetimes = []
    for count in range(len(karls_fixtures)):
    # for fixture in karls_fixtures:
        fixture = karls_fixtures[count]
        epoch_datetime = build_epoch_datetime_from_karl_fixture(fixture)
        if not epoch_datetime in epoch_datetimes:
            epoch_datetimes.append(epoch_datetime)

    # sort the epoch datetimes into order
    epoch_datetimes.sort()

    # loop through epoch datetime and use the list to rebuilt karls fixtures in
    # time order
    karls_fixtures_in_time_order = []
    for current_epoch_datetime in epoch_datetimes:
        # loop through Karls fixtures, find all fixtures that match the current
        # epoch datetime and append them to the list karls_fixtures_in_time_order
        for fixture in karls_fixtures:
            fixture_epoch_datetime = build_epoch_datetime_from_karl_fixture(
                                                                        fixture)
            if fixture_epoch_datetime == current_epoch_datetime:
                karls_fixtures_in_time_order.append(fixture)

    print('Total Karls fixtures in time order:')
    print(str(len(karls_fixtures_in_time_order)))

    return karls_fixtures_in_time_order
# ==============================================================================
# Helper function for sort_karls_fixtures_into_time_order().
# Builds an epoch datetime from a fixture.
# ==============================================================================
def build_epoch_datetime_from_karl_fixture(karl_fixture):

    epoch_datetime = datetime.datetime(
                                int(karl_fixture["year"]),
                                int(karl_fixture["month"]),
                                int(karl_fixture["day"]),
                                int(karl_fixture["hour"]),
                                int(karl_fixture["minute"])
                                            ).timestamp()
    epoch_datetime = int(epoch_datetime)

    return epoch_datetime
# ==============================================================================
# Write new csv file containing karls fixtures with htft scores matched
# to them. Call it 'karls_fixtures_matched_with_flashscore_results.csv'
# ==============================================================================
def write_karls_fixtures_to_csv(karls_fixtures):

    first_fixture = karls_fixtures[0]
    keys_in_first_fixture = list(first_fixture.keys())
    print('keys in first fixture:')
    for fixture_key in keys_in_first_fixture:
        print(fixture_key)
        print(first_fixture[fixture_key])

    # build the csv text for karls fixtures
    # column headers
    csv_text = 'YEAR,MONTH,DAY,HOUR,MINUTE'
    csv_text += ',FILENAME,HOME_TEAM,AWAY_TEAM'
    csv_text += ',HOME_TEAM_WIN_POINTS,DRAW_POINTS,AWAY_TEAM_WIN_POINTS'
    csv_text += ',HOME_TEAM_CORRECT_SCORE_INFO'
    csv_text += ',DRAW_CORRECT_SCORE_INFO'
    csv_text += ',AWAY_TEAM_CORRECT_SCORE_INFO'
    csv_text += ',HTFT_RESULT'
    # fixture rows
    for fixture in karls_fixtures:
        fixture_keys = list(fixture.keys())
        csv_text += "\n"
        if 'year' in fixture_keys:
            csv_text += str(fixture["year"])
        csv_text += ','
        if 'month' in fixture_keys:
            csv_text += str(fixture["month"])
        csv_text += ','
        if 'day' in fixture_keys:
            csv_text += str(fixture["day"])
        csv_text += ','
        if 'hour' in fixture_keys:
            csv_text += str(fixture["hour"])
        csv_text += ','
        if 'minute' in fixture_keys:
            csv_text += str(fixture["minute"])
        csv_text += ','
        if 'filename' in fixture_keys:
            csv_text += fixture["filename"]
        csv_text += ','
        if 'home_team' in fixture_keys:
            csv_text += fixture["home_team"]
        csv_text += ','
        if 'away_team' in fixture_keys:
            csv_text += fixture["away_team"]
        csv_text += ','
        if 'home_team_win_points' in fixture_keys:
            csv_text += str(fixture["home_team_win_points"])
        csv_text += ','
        if 'draw_points' in fixture_keys:
            csv_text += str(fixture["draw_points"])
        csv_text += ','
        if 'away_team_win_points' in fixture_keys:
            csv_text += str(fixture["away_team_win_points"])
        # home team correct score info
        home_team_correct_score_string = build_string_from_correct_score_dict(
                                                fixture["home_team_correct_score_info"])
        csv_text += ',' + home_team_correct_score_string
        # draw correct score info
        draw_correct_score_string = build_string_from_correct_score_dict(
                                                fixture["draw_correct_score_info"])
        csv_text += ',' + draw_correct_score_string
        # away team correct score info
        away_team_correct_score_string = build_string_from_correct_score_dict(
                                                fixture["away_team_correct_score_info"])
        csv_text += ',' + away_team_correct_score_string
        # htft_result
        htft_result_string = ''
        if 'htft_result' in fixture_keys:
            htft_result = fixture["htft_result"]
            if len(htft_result) > 0:
                htft_result_string = str(htft_result[0])
            if len(htft_result) > 1:
                for digit in htft_result[1:]:
                    htft_result_string += '_' + str(digit)
        csv_text += ',' + htft_result_string
    
    # write csv text to outfile
    outfile = open('karls_fixtures_matched_with_flashscore_results.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# From a correct score dictionary in the form:
# {'1-0': 60.7, '2-1': 60.7, 'Other': 47.21}
# build a correct score string in the form
# '1_0__60p7___2_1__60p7___Other'
# and return it.
# ==============================================================================
def build_string_from_correct_score_dict(correct_score_dict):

    # get keys
    correct_score_keys = list(correct_score_dict.keys())
    
    # loop through keys and values and build up the correct score string
    first_key = correct_score_keys[0]
    correct_score_string = first_key.replace('-', '_')
    correct_score_string += '__'
    correct_score_string += str(correct_score_dict[first_key]).replace('.', 'p')

    # loop through remaining keys (if there is more than one)
    if len(correct_score_keys) > 1:
        for count in range(1, len(correct_score_keys)):
            current_key = correct_score_keys[count]
            current_value = correct_score_dict[current_key]
            correct_score_string += '___' + current_key.replace('-', '_')
            correct_score_string += '__'
            correct_score_string += str(current_value).replace('.', 'p')

    return correct_score_string
# ==============================================================================
main()
