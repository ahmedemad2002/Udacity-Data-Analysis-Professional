import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_input_dict = {'all':range(1,7), 'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}
days_input_dict = {'all':range(0,7), 'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}
int_days_dict = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = 0,0,0
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = input("please choose a city to explore it's data: ('chicago', 'new york city', 'washington')\n").lower()
        if city not in CITY_DATA.keys():
            print("Invalid input of city\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    while month not in months_input_dict.keys():
        month = input("please choose a month to filter data by. (all, jan, feb, mar, apr, may , jun)\n").lower()
        if month not in months_input_dict.keys():
            print("Invalid input of month\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days_input_dict.keys():
        day = input("please choose a day to filter data by. (all, mon, tue, wed, thu, fri , sat, sun)\n").lower()
        if day not in days_input_dict.keys():
            print("Invalid input of day")

    print('-'*40)
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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except:
        print("failed to read data, city is typed in wrong way")

    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    try:
        if month != 'all':
            df = df[df['Start Time'].dt.month == months_input_dict[month]]
    except:
        print("failed to filter data by month, month is typed in wrong way")


    try:
        if day != 'all':
            df = df[df['Start Time'].dt.dayofweek == days_input_dict[day]]
    except:
        print("failed to filter data by day, day is typed in wrong way")


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Start Time'].dt.month.mode()[0]
    print("most common month: {}\n".format(common_month))

    # TO DO: display the most common day of week
    common_dayofweek = df['Start Time'].dt.dayofweek.mode()[0]
    print("most common day of week: {}\n".format(int_days_dict[common_dayofweek]))

    # TO DO: display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("most common hour: {}\n".format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("most commonly used start station: {}\n".format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("most commonly used end station: {}\n".format(common_end_station))


    # TO DO: display most frequent combination of start station and end station trip
    pop_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    pop_trip_count = df.groupby(['Start Station', 'End Station']).size().max()
    print("Most popular trip: (Start Station: {}, End Station: {})\nCount: {}\n".format(pop_trip[0], pop_trip[1], pop_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_traveling = df['Trip Duration'].sum()
    print("Total travel time: {}\n".format(total_traveling))

    # TO DO: display mean travel time
    average_time_for_trip = df['Trip Duration'].mean()
    print("Mean travel time: {}".format(average_time_for_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print("No data about gender.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most_pop_birthyear = df['Birth Year'].mode()[0]
        print("oldest: {}, youngest: {}, most popular birthyear: {}".format(oldest, youngest, most_pop_birthyear))
    else:
        oldest, youngest, most_pop_birthyear = 'None', 'None', 'None'
        print(
            "No data about birth years.\noldest: {}, youngest: {}, most popular birthyear: {}".format(oldest, youngest,
                                                                                                      most_pop_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_row_data = input("Do you want to see 5 lines of row data?\t").lower()
        c=0
        while show_row_data == 'yes':
            if c+5 <= len(df):
                print(df[c:c+5])
            else:
                print(df[c:])
            show_row_data = input("Do you want to see 5 lines of row data?\t").lower()
            c += 5

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
