from numpy import genfromtxt
from os import listdir
from dateutil import parser


def create_csv():
    fout = open("../data/personality_assay_data.csv", "w")
    fout.write("Bird_ID\t" +
               "Observation_ID\t" +
               "Cage_Num\t" +
               "Date\t" +
               "days_since_Sep1\t" +
               "flight_duration_sec\t" +
               "hop_duration_sec\t" +
               "light\t" +
               "tree\t" +
               "hatch\t" +
               "floor\t" +
               "unknown\t" +
               "A1\t" +
               "A2\t" +
               "A3\t" +
               "A4\t" +
               "A5")
    fout.write("\n")
    fout.close()


def data_writer(bird_id, observation_id, cage_num, date,
                days_since_sept, flight_duration,
                hop_duration, fixture_counter, location_counter):
    fout = open("../data/personality_assay_data.csv", "a")
    fout.write(str(bird_id) + "\t" +
               str(observation_id) + "\t" +
               str(cage_num) + "\t" +
               str(date) + "\t" +
               str(days_since_sept) + "\t" +
               str(flight_duration) + "\t" + str(hop_duration) + "\t")

    for fixture in fixture_counter:
        fout.write(str(fixture) + "\t")

    for i in range(len(location_counter)):
        if i < 4 :
            fout.write(str(location_counter[i]) + "\t")
        else:
            fout.write(str(location_counter[i]))

    fout.write("\n")
    fout.close()


def switch_case(code, location_counter, fixture_counter):
    if code[0] == "C":
        location_counter[0] += 1

    elif code[0] == "I":
        location_counter[1] += 1

    elif code[0] == "O":
        location_counter[2] += 1

    elif code[0] == "U":
        location_counter[3] += 1

    elif code[0] == "Y":
        location_counter[4] += 1

    if code[1] == "A":
        fixture_counter[0] += 1

    elif code[1] == "G":
        fixture_counter[1] += 1

    elif code[1] == "M":
        fixture_counter[2] += 1

    elif code[1] == "S":
        fixture_counter[3] += 1

    elif code[1] == "®":
        fixture_counter[4] += 1

    return location_counter, fixture_counter


def extract_data(file):
    f = open(file, "r")
    num_lines = sum(1 for line in open(file))
    lines = f.read().split('\n')

    # get the easy data
    bird_id = file[-11:-4]
    observation_id = lines[5]
    cage_num = lines[1]
    date = lines[6]
    d1 = parser.parse("1/9/2018", dayfirst=True)
    d2 = parser.parse(date, dayfirst=True)
    rd = d2 - d1
    days_since_sept = rd.days

    # limit the array to just the timed entries, ignoring header and footer
    times = (lines[8:(num_lines-3)])
    a = genfromtxt(times, dtype=None, encoding=None)

    # hops
    hops = 0
    for row in a:
        if row[1] == "L":
            hops += 1

    # print(str(hops) + " hops")
    hop_duration = hops * .5

    # total flight duration
    flight_times = []
    for index in range(len(a)):
        if a[index][1] == "F":
            begin_flight = a[index][0]
            end_flight = a[index+1][0]
            temp_duration = end_flight - begin_flight
            flight_times.append(temp_duration)
    flight_duration = sum(flight_times)
    flight_duration = round(flight_duration, 2)
    # print(str(flight_duration) + " seconds of flight")

    location_counter = [0] * 5
    fixture_counter = [0] * 5

    # passes the movement codes to a tallying function
    for row in a:
        if len(row[1]) == 2:
            location_counter, fixture_counter = switch_case(row[1], location_counter, fixture_counter)

    # print(location_counter)
    # print(fixture_counter)

    # writes data to csv in the same directory
    data_writer(bird_id, observation_id, cage_num, date,
                days_since_sept, flight_duration,
                hop_duration, fixture_counter, location_counter)


# run this with the path of folder containing .txt files to convert as a string
def convert_assay(path):

    create_csv()

    # replace directory string with wherever the txt files are located
    for filename in listdir(path):
        if filename != ".DS_Store":
            print(filename)
            extract_data(path + str(filename))

convert_assay('../data/raw_data/personality_data/')
