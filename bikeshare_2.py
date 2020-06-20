import sys
import datetime
import time
import pandas as pd
import numpy as np
from scipy import stats

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_mssg = """
What city do you want to analyze?\n
Your input must be an integer. Choices are:
1. Chicago
2. New York City
3. Washington
"""

month_mssg = """
What month do you want to review?\n 
Your input must be an integer. Choices are:
1. January
2. February
3. March
4. April
5. May
6. June
7. July
8. August
9. September
10. October
11. November
12. December
13. All
"""

day_mssg = """
What day do you want to verify?\n
Your input must be an integer. Choices are:
1. Sunday
2. Monday
3. Tuesday
4. Thursday
5. Wednesday
6. Thursday
7. Saturday
8. All
"""

error_mssg = """
Not a valid input. 
If you want to go out, press Ctrl + C.
Lets start again.
"""

city_dict = {
                1:'Chicago',
                2:'New York City',
                3:'Washington',
             }

month_dict = {
                1:'January',
                2:'February',
                3:'March',
                4:'April',
                5:'May',
                6:'June',
                7:'July',
                8:'August',
                9:'September',
                10:'October',
                11:'November',
                12:'December',
                13:'All'
             }

day_dict = {
                1:'Sunday',
                2:'Monday',
                3:'Tuesday',
                4:'Wednesday',
                5:'Thursday',
                6:'Friday',
                7:'Saturday',
                8:'All'
             }

def get_filters(city_mssg, month_mssg, day_mssg, error_mssg):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city_mssg, month_mssg, day_mssg, error_mssg = city_mssg, month_mssg, day_mssg,error_mssg
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    def get_city():
        city = input(city_mssg)
        return city
    
    # get user input for month (all, january, february, ... , june)
    def get_month():
        month = input(month_mssg)
        return month

    # get user input for day of week (all, monday, tuesday, ... sunday)
    def get_day():
        day = input(day_mssg)
        return day  

    while True:
        try:
            city = int(get_city())
            if city not in city_dict.keys():
                raise Exception
            month = int(get_month())
            if month not in month_dict.keys():
                raise Exception
            day = int(get_day())
            if day not in day_dict.keys():
                raise Exception
            break
        except KeyboardInterrupt:
            sys.exit()
        except:
            print(error_mssg)

    city = city_dict[city]
    month = month_dict[month]
    day = day_dict[day]

    print('-'*40)
    print("""So you want to review bike share data from {}, for the month of: {},
        and for the day of: {}\n""".format(city, month, day))
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
    # Converting types of parameters, as they come from the previous function.
    city = city.lower()
    for key, value in month_dict.items():
        if value == month:
            month = key
    for key, value in day_dict.items():
        if value == day:
            day = key

    # Loading CSV file into DataFrame 'df'
    file_name = CITY_DATA[city] 
    df = pd.read_csv(file_name) 
    
    # Converting string dates to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Filtering the 'df' DataFrame by month and day.
    df1 = []
    if month == 13 and day == 8: #No filtering if month and day are 'all'
        pass
    elif month == 13: # Filtering for case all months, one weekday selected
        for date in df['Start Time']:
            if date.weekday() + 1 == day:
                df1.append(True)
            else:
                df1.append(False)
        df = df.loc[df1]
    elif day == 8: # Filtering for case one month selected, all days
        for date in df['Start Time']:
            if date.month == month:
                df1.append(True)
            else:
                df1.append(False)
        df = df.loc[df1]
    else: # Filtering for a specified month and weekday
        for date in df['Start Time']: 
            if date.weekday() + 1 == day and date.month == month:
                df1.append(True)
            else:
                df1.append(False)
        df = df.loc[df1]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = []
    for date in df['Start Time']:
        months.append(date.month)
    month_mode = int(stats.mode(months)[0])
    print('The month with the most registered travels is {}\n'.format(month_dict[month_mode]))
    
    # display the most common day of week
    weekdays = []
    for date in df['Start Time']:
        weekdays.append(date.weekday())
    days_mode = int(stats.mode(weekdays)[0]) + 1
    print('The most congested day is {} \n'.format(day_dict[days_mode]))

    # display the most common start hour
    hours = []
    for date in df['Start Time']:
        hours.append(date.hour)
    hours_mode = int(stats.mode(hours)[0])
    print('The most common start hour is {}\n'.format(hours_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_mode = str(stats.mode(df['Start Station'])[0]).strip("[]")
    print('The station where most voyages begin is {}\n'.format(start_mode))

    # display most commonly used end station
    end_mode = str(stats.mode(df['End Station'])[0]).strip("[]")
    print('The most frequent destination is {}\n'.format(end_mode))

    # display most frequent combination of start station and end station trip
    combination_mode = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most registered travel, is between this two stations: ')
    print(str(combination_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    city, month, day = city, month, day

    # display total travel time
    total_travel = np.sum(df['Trip Duration'])
    print('In the data filtered by the parameters: ')
    print('City: {}'.format(city))
    print('Month: {}'.format(month))
    print('Weekday: {}'.format(day))
    print('The accumulated travel duration is {} seconds.'.format(total_travel))

    # display mean travel time
    mean_travel = np.mean(df['Trip Duration'])
    print('And the mean travel duration is {} seconds.'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_type_count = df.groupby(['User Type'])['User Type'].count()
        print('\nBy user type, the number of users was: ')
        print(user_type_count)
    except:
        print('\nNo user types available in the selected data set.')
    
    # Display counts of gender
    try:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\nBy gender, the number of users was: ')
        print(gender_count)
    except:
        print('\nNo gender available in the selected data set.')

    # Display earliest, most recent, and most common year of birth
    try:
        eldest = df['Birth Year'].min(skipna=True)
        print('\nThe eldest user was born in {}.'.format(round(eldest)))
        youngest = df['Birth Year'].max(skipna=True)
        print('\nThe youngest user was born in {}.'.format(round(youngest)))
        most_common = df['Birth Year'].mode(dropna=True)[0]
        print('\nThe year most of our users were born is {}.'.format(round(most_common)))
    except:
        print('No birth years available in the selected data set.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_sample(df):
    while True:
        print('\nFinally, we are going to see a chunk of the raw data: ')
        sample = df.sample(n=5, replace=True)
        print(sample)
        another_sample = input('\nDo you want to see more of the raw data?\n')
        if another_sample.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters(city_mssg,month_mssg,day_mssg,error_mssg)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, city, month, day)
        user_stats(df)
        display_sample(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
