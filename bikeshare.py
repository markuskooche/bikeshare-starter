import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while not city in CITY_DATA:
        city = input('Please choose a city (chicago, new york city, washington): ').lower()

    # get user input for month (all, january, february, ... , june)
    month = None
    months = MONTHS.copy()
    months.append('all')
    while not month in months:
        month = input('Please choose a month (all, january, february, ..., june): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    days = DAYS.copy()
    days.append('all')
    while not day in days:
        day = input('Please choose a day of week (all, monday, tuesday, ... sunday): ').lower()

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    month_as_name = MONTHS[most_common_month - 1]
    print(f'Most Common Month:      {most_common_month} = {month_as_name.title()}')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day:        {most_common_day}')

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {most_common_start_hour}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print(f'Most Common Start Station: {most_common_start}')

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print(f'Most Common End Station:   {most_common_end}')

    # display most frequent combination of start station and end station trip
    most_common_start_end = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print(f'Most Common Combination:   {most_common_start_end}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time (in seconds): {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time (in seconds):  {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of User Types:', user_types, sep='\n', end='\n\n')

    # Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print('Count of Genders:', genders, sep='\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_yob = int(df['Birth Year'].min())
        print(f'Earliest Year of Birth:    {earliest_yob}')
        recent_yob = int(df['Birth Year'].max())
        print(f'Recent Year of Birth:      {recent_yob}')
        most_common_yob = int(df['Birth Year'].mode()[0])
        print(f'Most Common Year of Birth: {most_common_yob}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        offset = 0
        raw_data = 'yes'
        while raw_data == 'yes':
            raw_data = input('\nWould you like to display raw data? Enter yes or no.\n').lower()
            if raw_data == 'yes' and offset + 4 < len(df.index):
                print(df[offset:offset+5])
                offset += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
