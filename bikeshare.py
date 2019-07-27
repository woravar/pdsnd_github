import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print('That is not a valid city!')

    while True:
        time_filter = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.').lower()
        if time_filter == 'month' or time_filter == 'day' or time_filter == 'both' or time_filter == 'none':
            break
        else:
            print('That is not a valid time filter!')

    if time_filter == 'none':
        month = 'all'
        day = 'all'
    elif time_filter == 'month':
        day = 'all'
    elif time_filter == 'day':
        month = 'all'

    # get user input for month (all, january, february, ... , june)
    if time_filter == 'month' or time_filter == 'both':
        month_list = ['january','february','march','april','may','june']
        while True:
            month = input('Which month - January, February, March, April, May, or June?:').lower()
            if month in month_list:
                break
            else:
                print('That is not a valid month!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'day' or time_filter == 'both':
        day_list = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        while True:
            try:
                num_day = int(input('Which day? Please type your response as an integer (e.g., 1=Sunday)'))
                if num_day in [1,2,3,4,5,6,7]:
                    day = day_list[num_day-1]
                    break
                else:
                    print('That is not a valid day!')
            except:
                print('That is not a valid day!')

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # display the most common day of week
    popular_month = df['day_of_week'].mode()[0]
    print('Most Popular Start Day of Week:', popular_month)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = 'Start Station: ' + df['Start Station'] + ', End Station: ' + df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print('Most Popular Start & End Station:', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time (seconds):', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time (seconds):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('Counts of User Types:\n', count_user_type)

    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        count_gender = df['Gender'].value_counts()
        print('Counts of Gender:\n', count_gender)

    # Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        mode_birth_year = df['Birth Year'].mode()[0]
        print('Earliest Year of Birth:', min_birth_year)
        print('Most Recent Year of Birth:', max_birth_year)
        print('Most Common Year of Birth:', mode_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        start=0
        while True:
            view_data = input('Would you like to view individual trip data? Type \'yes\' or \'no\'.').lower()
            if view_data == 'yes':
                for i in range(start,start+5):
                    if city == 'chicago' or city == 'new york city':
                        print(df.iloc[i,0:9].to_dict())
                    elif city == 'washington':
                        print(df.iloc[i,0:7].to_dict())
                start=start+5
            elif view_data == 'no':
                break
            else:
                print('That is not a valid input!')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
