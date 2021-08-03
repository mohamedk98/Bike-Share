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
    city = ''

    while city not in CITY_DATA.keys():
        city = input('\n Welcome,Please Select Your City From the Following: (Chicago,New York City,Washington) \n').lower()
        if city not in CITY_DATA.keys():
            print('\n Please Enter A Valid City')
        else:
            print('You Have Selected: ' + city +'\n')
    # get user input for month (all, january, february, ... , june)
    MONTH_DATA = {'all':0,'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
    month = ''

    while month not in MONTH_DATA.keys():
        print('Please Enter month you want (type "all" for selecting all months) \n')
        month = input('Please Enter the desired month:')
        if month not in MONTH_DATA.keys():
            print('Please Type a Correct Month \n')
        else:
            print('You Have Selected:' + month + '\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA = ['all','saturday','sunday','monday','tuesday','wednesday','thursday','friday']
    day = ''
    while day not in DAY_DATA:
        print('Please Enter Day you want (type "all" for selecting all Days) \n')
        day = input('Please Enter the day you like:')
        
        if day not in DAY_DATA:
            print('Please Type a Correct Day \n')
        else:
            print('You Have Selected:' + day + '\n')
            
        # return city, month, day
    return city,month,day

print('-'*40)


def load_data(city,month,day):
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
    #Using to_datetime to change number format to days and months
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    
    if month != 'all':
        MONTH_DATA = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
        month = MONTH_DATA[month]
        df = df[df['month'] == month]
    
    if day != 'all':
        DAYS_DATA=['saturday','sunday','monday','tuesday','wednesday','thursday','friday']
        day = DAYS_DATA.index(day) + 1 
        df = df[df['day'] == day]
    
    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    the 'f' in print statment indicate formattes tring literals
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses mode method to find the most popular month
    popular_month = df['month'].mode()[0]
    MONTH_DATA = {1:'january',2:'february',3:'march',4:'april',5:'may',6:'june'}
    print(f"Most Popular Month is: {MONTH_DATA[popular_month]}")

    #Uses mode method to find the most popular day
    popular_day = df['day'].mode()[0]

    print(f"Most Popular Day: {popular_day}")

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f"Most Popular Start Hour: {popular_hour}\n")

    #Prints the time taken to perform the calculation
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most Popular Start Station is: {popular_start_station}\n")

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"Most Popular End Station is: {popular_end_station}\n")

    # display most frequent combination of start station and end station trip
    df['Start to End']=df['Start Station'] + ' to ' + df['End Station']
    popular_start_end_station = df['Start to End'].mode()[0]
    print(f"Most Popular Start to End Station is: {popular_start_end_station}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    minutes= divmod(total_time,60)
    seconds = minutes[1]
    hours = divmod(minutes[0],60)
    print(f"The Total Travel Time Is : {hours[0]} hours , {minutes[1]} minutes and {seconds} seconds\n")
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    minutes= divmod(mean_time,60)
    seconds = minutes[1]
    hours = divmod(minutes[0],60)
    print(f"The Mean Travel Time Is : {hours[0]} hours , {minutes[1]} minutes and {seconds} seconds\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count =df['User Type'].value_counts()
    print(f"Users Numbers and Types are :\n{count}\n")
    

    # Display counts of gender
    try:
        gender_count =df['Gender'].dropna().value_counts()
        print(f"Genders Counts are :\n{gender_count}\n")
    except:
        print("Gender Column Does not exist, Skipping....")

    # Display earliest, most recent, and most common year of birth
    try:
        most_recent=df['Birth Year'].max()
        earliest = df['Birth Year'].min()
        most_common =df['Birth Year'].mode()[0]
        print(f"The Year of Birth Stats are : \n {most_recent} is the most recent birth year \n {most_common} is the most common birth year \n {earliest} is the earliest birth year\n")
    except:
        print("Birthday Column Does not exist, Skipping....")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
   response=['yes','no']
   start_loc = 0
   view_data = ''
   while view_data not in response:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data =='yes':
            print(df.iloc[start_loc:start_loc+5])
        elif view_data not in response:
            print('Please Check your input\n')
        elif view_data == 'no':
            break
        
   while view_data == 'yes':
        view_data = input('\nWould you like to view 5 more rows of individual trip data? Enter yes or no\n').lower()
        if view_data == 'yes':
            start_loc += 5
            print(df.iloc[start_loc:start_loc+5])
        elif view_data != 'yes':
            break
            
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()



