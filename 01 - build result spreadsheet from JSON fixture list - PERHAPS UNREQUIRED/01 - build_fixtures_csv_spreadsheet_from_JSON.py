# ==============================================================================
# From the local file 'premier_fixtures_2019_to_2020.txt', build a csv file
# named 'fixtures_2019_to_2020.csv'
# The csv file will have the following columns:
# HOME_TEAM,AWAY_TEAM,YEAR,MONTH,DAY,HOUR,MINUTE
# ==============================================================================
import json
# ==============================================================================
def main():

    build_csv_spreadsheet_from_json()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# ==============================================================================
def build_csv_spreadsheet_from_json():

    # read json file
    infile = open('premier_fixtures_2019_to_2020.txt', 'r')
    json_text = infile.read()
    infile.close()

    # parse the json
    json_text = json_text.replace('var premier_fixtures = ', '')
    json_text = json_text.replace(';', '')
    json_text = json_text.replace('[', '').replace(']', '')
    # split json into json object text blocks
    json_object_text_blocks = json_text.split("}, \n{")
    print('Total json object text blocks =', str(len(json_object_text_blocks)))
    total_blocks = len(json_object_text_blocks)
    print('processing', str(total_blocks), 'fixture blocks...')
    fixtures = []
    # for json_object_text_block in json_object_text_blocks:
    for count in range(len(json_object_text_blocks)):
        json_object_text_block = json_object_text_blocks[count]
        print('Block #', str(count + 1), ' of ', str(total_blocks), sep='')
        # away team
        away_team = extract_substring(json_object_text_block, "away_team':",
                                                                      "'", "'")
        # home team
        home_team = extract_substring(json_object_text_block, "home_team':",
                                                                      "'", "'")
        # year
        loc = json_object_text_block.find("'year':") + 7
        year_string = json_object_text_block[loc:].strip().replace('}', '')
        year = int(year_string)
        # month
        month_string = extract_substring(json_object_text_block, "'month'",
                                                                      ':', ',')
        month = int(month_string)
        # day
        day_string = extract_substring(json_object_text_block, "'day'",
                                                                      ':', ',')
        day = int(day_string)
        # hour
        hour_string = extract_substring(json_object_text_block, "'hour'",
                                                                      ':', ',')
        hour = int(hour_string)
        # minute
        minute_string = extract_substring(json_object_text_block, "'minute'",
                                                                      ':', ',')
        minute = int(minute_string)
        # build fixture dictionary and append it to the list fixtures
        fixture_dictionary = {
                "home_team" : home_team,
                "away_team" : away_team,
                "year"      : year,
                "month"     : month,
                "day"       : day,
                "hour"      : hour,
                "minute"    : minute
                            }
        fixtures.append(fixture_dictionary)

    # test print
    print('first fixture dictionary:')
    print(fixtures[0])

    # build the text for the csv file
    csv_text = 'HOME_TEAM,AWAY_TEAM,YEAR,MONTH,DAY,HOUR,MINUTE,HOME_HT,AWAY_HT,';
    csv_text += 'HOME_FT,AWAY_FT'
    for fixture_dict in fixtures:
        csv_text += "\n" + fixture_dict["home_team"]
        csv_text += ',' + fixture_dict["away_team"]
        csv_text += ',' + str(fixture_dict["year"])
        csv_text += ',' + str(fixture_dict["month"])
        csv_text += ',' + str(fixture_dict["day"])
        csv_text += ',' + str(fixture_dict["hour"])
        csv_text += ',' + str(fixture_dict["minute"])

    # write the csv text to the local file 'fixtures_2019_to_2020.csv'
    outfile = open('fixtures_2019_to_2020.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# From big_string:
# 1. remove everything up to and including sentinel_string
# 2. extract the substring located between start_string and end_string
#    (without start_string and end_string) and return it
# ==============================================================================
def extract_substring(big_string, sentinel_string, start_string, end_string):

    start = big_string.find(sentinel_string) + len(sentinel_string)
    big_string = big_string[start:]

    start = big_string.find(start_string) + len(start_string)
    big_string = big_string[start:]

    end = big_string.find(end_string)
    substring_to_return = big_string[:end]

    return substring_to_return
# ==============================================================================
main()
