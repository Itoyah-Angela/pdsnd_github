import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter a city(chicago,new york city,washington): ").lower().strip()
    city_list = ['chicago', 'new york city', 'washington']
    while city not in city_list:
        print("invalid entry")
        city = input("Kindly Enter any of the following city name(chicago,new york city,washington): ").lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter a month(january,february,march,...,june or enter \"all\"): ").lower().strip()
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_list:
        print("invalid entry")
        month = input(
            "Kindly Enter any of the following month name january,february,march,...,june or enter \"all\": ").lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter a day(monday,tuesday,wednesday,...,sunday or enter \"all\"): ").lower().strip()
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in day_list:
        print("invalid entry")
        day = input(
            "Kindly Enter any of the following days monday,tuesday,wednesday,...,sunday or enter \"all\": ").lower().strip()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load raw data
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to date time data type
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extracting month and day from start time
    df["Start Month"] = df["Start Time"].dt.month
    df["Start Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour

    # Use user entry to filter month and day
    if month != "all":
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month) + 1
        df = df[df["Start Month"] == month]

    if day != "all":
        df = df[df["Start Day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    most_common_month = df["Start Month"].mode()[0] - 1

    month_list = ["january", "february", "marcch", "april", "may", "june"]

    print("\t The most common month is :  {}\n".format(month_list[most_common_month]))

    # display the most common day of week
    most_common_week_day = df["Start Day"].mode()[0]

    print("\t The most common week day is : {}\n".format(most_common_week_day))

    # display the most common start hour
    most_common_start_hour = df["Start Hour"].mode()[0]


    print("\t The most common start hour is : {} \n".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("\t The most commonly used start station is {} \n".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("\t The most popular end station is {} \t".format(most_common_end_station))

    # display most frequent combination of start station and end station trip

    df["Station combination"] = df["Start Station"] + df["End Station"]

    start = df['Start Station'][df["Station combination"] == df["Station combination"].mode()[0]].unique()[0]
    end = df['End Station'][df["Station combination"] == df["Station combination"].mode()[0]].unique()[0]

    print("\t The most frequent combination of start and end station :  \"{}\" and \"{}\". \n".format(start, end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    duration_sum = df["Trip Duration"].sum()

    print("\t The total travel time is : {} \n".format(duration_sum))

    # display mean travel time
    duration_mean = df["Trip Duration"].mean()
    print("\t The mean travel time is :  {} \n".format(duration_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_of_users = dict(df.groupby(["User Type"])["User Type"].count())
    print("\n \t Counts of user types:")
    for type in type_of_users.keys():
        print("\t\t {} : \t {}".format(type, type_of_users[type]))

    # Display counts of gender
    try:
        genders = dict(df.groupby(["Gender"])["Gender"].count())
        print("\n \t Counts of gender:")
        for gender in genders.keys():
            print("\t\t {} : \t {}".format(gender, genders[gender]))
    except:
        print("\t No gender data \n")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = list(df["Birth Year"].dropna().sort_values(ascending=True).head(1))
        print("\n \t The earliest year of birth is : {} \n".format(int(earliest[0])))

        most_recent = list(df["Birth Year"].dropna().sort_values(ascending=False).head(1))
        print("\t The most recent year of birth is : {} \n".format(int(most_recent[0])))

        most_common = int(df["Birth Year"].mode()[0])
        print("\t The most common year of birth is : {} \n".format(most_common))
    except:
        print("\t No birth data \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):

    """Getting raw data for user"""

    df = df.drop(columns=["Station combination"], axis=1)

    response = input("View first 5 rows of raw data? [enter yes or no]: ").lower().strip()

    begin = 0
    end = 5

    # while loop to keep requesting user consent to see more of the raw data
    while response == "yes" and end <= df.size:
        print(df[begin: end])
        begin = end
        end += 5
        response = input("Want to view more raw data? (yes or no) : ").lower().strip()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
