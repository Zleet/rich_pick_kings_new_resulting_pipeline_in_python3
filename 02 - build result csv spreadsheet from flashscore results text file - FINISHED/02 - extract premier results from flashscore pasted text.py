# ==============================================================================
# All the premier league results for 2019/2020 has been copied and pasted into
# the local file
# 'premier league results 2019 to 2020 pasted from flashscore.txt'.
# Read this file, parse the results and write them into a local csv file named
# 'flashscore premier league results 2019 to 2020.csv'
# ==============================================================================
def main():

    read_and_parse_flashscore_premiership_results()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# ==============================================================================
def read_and_parse_flashscore_premiership_results():

    filename = 'premier league results 2019 to 2020 pasted from flashscore.txt'
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    print('Total lines =', str(len(lines)))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # loop through lines.
    # Whenever we encounter a line in the format:
    # (1 - 0)
    # build a result object
    # Whenever we encounter a line in the format:
    # 22.02. 15:00
    # parse the date and time and change the month, day, hour and minute
    # Also: the first time the month changes to 12, decrement the year
    # (since the flashscore page lists the results in reverse time order,
    # from most recent to oldest result)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    year = 2020
    month = 0
    day = 0
    hour = 0
    minute = 0
    year_has_changed = 0
    results = []
    # for line in lines:
    for count in range(len(lines)):
        line = lines[count]
        line = line.strip()
        # if line is a half-time score line, build a result object and push
        # it onto results
        if (('(' in line) and (')' in line)) and ('-' in line):
            # get halftime scores from current line
            line = line.replace('(', '').replace(')', '')
            elements = line.split('-')
            home_ht = int(elements[0].strip())
            away_ht = int(elements[1].strip())
            # get away team from previous line
            previous_line = lines[count - 1]
            away_team = previous_line.strip()
            # get full time scores from two lines before
            ft_line = lines[count - 2].strip()
            elements = ft_line.split('-')
            home_ft = int(elements[0].strip())
            away_ft = int(elements[1].strip())
            # get home team from three lines before
            home_team = lines[count - 3].strip()
            # build result dictionary and push it onto results
            result_dict = {
                "year"      : year,
                "month"     : month,
                "day"       : day,
                "hour"      : hour,
                "minute"    : minute,
                "home_team" : home_team,
                "away_team" : away_team,
                "home_ht"   : home_ht,
                "away_ht"   : away_ht,
                "home_ft"   : home_ft,
                "away_ft"   : away_ft
                            }
            results.append(result_dict)
        # if line is a date line, change month, day, hour and minute
        if line_is_date_line(line):
            month, day, hour, minute = parse_date_line(line)
        # if month is 12 and year hasn't changed, decrement year and set
        # year_has_changed
        if (month == 12) and (not year_has_changed):
            year -= 1
            year_has_changed = 1

    results.reverse()

    # build csv text
    csv_text = 'YEAR,MONTH,DAY,HOUR,MINUTE,HOME_TEAM,AWAY_TEAM,HOME_HT,'
    csv_text += 'AWAY_HT,HOME_FT,AWAY_FT'
    for result in results:
        csv_text += "\n" + str(result["year"])
        csv_text += ',' + str(result["month"])
        csv_text += ',' + str(result["day"])
        csv_text += ',' + str(result["hour"])
        csv_text += ',' + str(result["minute"])
        csv_text += ',' + result["home_team"]
        csv_text += ',' + result["away_team"]
        csv_text += ',' + str(result["home_ht"])
        csv_text += ',' + str(result["away_ht"])
        csv_text += ',' + str(result["home_ft"])
        csv_text += ',' + str(result["away_ft"])

    # write csv text to local file
    # 'flashscore premier league results 2019 to 2020.csv'
    outfile = open('flashscore premier league results 2019 to 2020.csv', 'w')
    outfile.write(csv_text)
    outfile.close()

    return
# ==============================================================================
# Helper function for read_and_parse_flashscore_premiership_results().
# Detects whether a line is a date line, in the format '09.02. 14:00'.
# If so, returns 1, otherwise returns 0.
# ==============================================================================
def line_is_date_line(line):

    line = line.strip()

    digits = '0123456789'

    total_spaces = 0
    total_digits = 0
    total_full_stops = 0
    total_colons = 0

    for character in line:
        if character == ' ':
            total_spaces += 1
        if character in digits:
            total_digits += 1
        if character == '.':
            total_full_stops += 1
        if character == ':':
            total_colons += 1

    if total_spaces != 1:
        return 0
    if total_digits != 8:
        return 0
    if total_full_stops != 2:
        return 0
    if total_colons != 1:
        return 0

    # if we've fallen through, the string has passed all the tests to identify
    # it as a date line
    return 1
# ==============================================================================
# Helper function for read_and_parse_flashscore_premiership_results().
# Parse a date line in the format:
# '09.02. 14:00'
# (i.e. <day>.<month>. <time>)
# and return month, day, hour and minute as integers
# ==============================================================================
def parse_date_line(line):

    line = line.strip()

    # split line into date and time
    elements = line.split(' ')

    # get day and month from first element
    day_and_month_element = elements[0].strip()
    day_and_month_elements = day_and_month_element.split('.')
    day = int(day_and_month_elements[0].strip())
    month = int(day_and_month_elements[1].replace('.', '').strip())

    # get hour and minute from second element
    time_element = elements[1].strip()
    time_elements = time_element.split(':')
    hour = int(time_elements[0].strip())
    minute = int(time_elements[1].strip())

    return [month, day, hour, minute]
# ==============================================================================
main()
