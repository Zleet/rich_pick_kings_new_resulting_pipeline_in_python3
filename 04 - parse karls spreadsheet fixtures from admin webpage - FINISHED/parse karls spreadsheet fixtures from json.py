# ==============================================================================
# Read Karl's spreadsheet fixtures, downloaded from the fixtures page on the
# Rich Pick Kings Admin webpage and build a spreadsheet containing all the
# fixtures, named 'all_karls_fixtures.csv'
# ==============================================================================
import json
# ==============================================================================
def main():

    build_csv_spreadsheet_from_karls_spreadsheet_fixtures()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
def build_csv_spreadsheet_from_karls_spreadsheet_fixtures():

    # read text from local file
    infile = open('karls_fixtures_from_admin_webpage.txt', 'r')
    text = infile.read()
    infile.close()

    text = text.strip()

    # parse the fixtures as json
    karls_fixtures = json.loads(text)
    
    print('Total Karls fixtures =', str(len(karls_fixtures)))
    print('karls_fixtures[0]:')
    print(karls_fixtures[0])

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Each dictionary in the list karls_fixtures represents all the fixtures
    # for one of karl's spreadsheet files that was uploaded to the Rich Pick
    # Kings website.
    # In each dictionary:
    # 1. file_name is the online filename under which the json formatted
    #    fixtures were saved, and
    # 2. file_text is a list of dictionaries, with each dictionary containing
    #    Karl's points information for a single football match
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    keys_in_first_dict = list(karls_fixtures[0].keys())
    first_fixture = karls_fixtures[0]["file_text"][0]

    # build a big list of karls fixtures
    all_fixtures = build_big_list_of_individual_fixtures(karls_fixtures)

    print('Total fixtures =', str(len(all_fixtures)))
    first_fixture = all_fixtures[0]
    print('first fixture:')
    print(first_fixture)

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
    for fixture in all_fixtures:
        # if it's a bogus fixture, continue to the next fixture
        if is_bogus_fixture(fixture):
            continue
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

    # write the csv text to the local file 'all_karls_fixtures.csv'
    outfile = open('all_karls_fixtures.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Helper function for build_csv_spreadsheet_from_karls_spreadsheet_fixtures()
# Detect whether a fixture is bogus or not.
# A bogus fixture has home team and away team names that consist solely of the
# characters '0', '1', '/' or ' '
# ==============================================================================
def is_bogus_fixture(fixture):

    string_to_test = fixture["home_team"].strip() + fixture["away_team"].strip()

    invalid_characters = ['0', '1', '/']

    for character in string_to_test:
        if character in invalid_characters:
            return 1

    # if we've fallen through, all of the characters in both team names are
    # valid characters, so it's not a bogus fixture
    return 0
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
# Loop through karls fixtures and build a big list of fixtures where each
# individual fixture dictionary contains the filename for the file in which
# the fixture was saved.
# ==============================================================================
def build_big_list_of_individual_fixtures(karls_fixtures):

    fixtures = []

    # loop through individual file dictionaries
    for file_info_dict in karls_fixtures:
        filename = file_info_dict["file_name"]
        fixtures_in_file = file_info_dict["file_text"]
        # loop through individual fixtures in file. For each fixture dictionary
        # stick the filename in the dictionary, then append the fixture
        # dictionary to the list fixtures
        for fixture_dict in fixtures_in_file:
            fixture_dict["filename"] = filename
            fixtures.append(fixture_dict)

    return fixtures
# ==============================================================================
main()
