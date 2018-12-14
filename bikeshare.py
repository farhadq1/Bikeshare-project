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
        (str) month - name of the month to filter by, or "all" to apply no month
	      #filter 
	(str) day - name of the day of week to filter by, or "all" to apply no 
	      #day filter
    """



    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a 
    #while loop to handle invalid inputs
    while True:
        city=input("Enter a city (Chicago, New York City or Washington) to begin: \n").lower()
        if city in CITY_DATA:
            print('\nYou selected {}!\n'.format(city.title()))
            restart = input('Write \'yes\' now if this is not what you wanted to enter 
			    and \'no\' otherwise.\n')
            if restart.lower() != 'yes':
                break
    city=city.lower()
    # get user input for month (all, january, february, ... , june)We
    months=['all','jan','feb','mar','apr','may','jun']
    while True:
        month=input("Enter a month (Jan,Feb,Mar,Apr,May or Jun) to filter by month or
		    'all' for no filters: \n").lower()
        if month.lower() in months:
            break
    days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday','All']

    while True:
        #try:
        day=input("Enter day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday) 
		  to filter by day or 'all' for no filters: \n")
        if day.title() in days:
            break


    print('-'*40)
    return city, month, day

def max_occurance(column):
    """ This functions takes in a column of a dataframe and finds the maximum count.
        Returns all the values with maximum count."""

    l=len(column.mode())

    if l > 1:
        maxocc= column.mode()[0:l]
    else:
        maxocc=column.value_counts().idxmax()

    return maxocc



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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['Hour'] = df['Start Time'].dt.hour
    df['Month(1-12)'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    #print (df['Month(1-12)'])
    months=['jan','feb','mar','apr','may','jun']
    if (month!='all'): #or (month!='all'):
        for i in range(len(months)):
            if months[i]==month:
                month=i+1
        df= df.loc[df['Month(1-12)'] == month]
    else:
        #frequent_month=months[(df['Month(1-12)'].value_counts().mode()[0])-1]
        print ("\nCalculating most frequent month of travel . . .")

        frequent_month=max_occurance(df['Month(1-12)'])
        print ("Most frequent month of travel was {}".format(months[frequent_month - 1]))

    if (day != 'all'):
        df= df.loc[df['Day'] == day.title()]
    else:
        frequent_day=max_occurance(df['Day'])
        print ("\nCalculating most frequent day of travel . . .")
        print ("Most frequent day of travel was {}".format(frequent_day))


    return df
#

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month

    frequent_hour=max_occurance(df['Hour'])

    print ("Most frequent hour of travel was {}".format(frequent_hour))

    print("This took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
    return None
#
def station_stats(df):
#     """Displays statistics on the most popular stations and trip."""
#
    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station

    most_common_startstation=max_occurance(df['Start Station'])
    # display most commonly used end station
    most_common_endstation=max_occurance(df['End Station'])

    # display most frequent combination of start station and end station trip
    combo= df['Start Station'] + ' to ' + df['End Station']


    print ("Most common start station was {}, most common end station was {} 
	   ".format(most_common_startstation,most_common_endstation))
    print ('Most common combination(s) of start and end stations:\n{}.\nCount:{}'
	   .format(max_occurance(combo),combo.value_counts().max()))
    print ("This took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

#
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time=df['Trip Duration'].sum()

    # display mean travel time
    Mean_Travel_Time=df['Trip Duration'].mean()
    print ('Total travel time: {} hours.\n'.format(Total_Travel_Time//3600))
    print ('Mean travel time: {} minutes.\n'.format(Mean_Travel_Time//60))
    print("This took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
#
#
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.value_counts(df['User Type'])
    print ('Distribution of user types:\n',user_types)
    # Display counts of gender
    if 'Gender' in df.columns:
        genders=pd.value_counts(df['Gender'])
        print ('Distribution of user gender:\n',genders)
    else:
        print("\nNo gender data available")
    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year=df['Birth Year'].min()
        recent_birth_year=df['Birth Year'].max()
        common_birth_year=max_occurance(df['Birth Year'])
        print('The earliest birth year was: {}.\nMost recent birth year was: 
	      {}.\nMost common birth year was {}'.format(earliest_birth_year,
	      recent_birth_year,common_birth_year))
    else:
        print("No birth year data available")

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    """This function takes in a dataframe as input and prints 5 enteries at a time"""

    count=0
    while True:
        display=input("\nDo you want to display individual trip data 
		      (5 entries everytime you type 'yes')? : ").lower()
        if (display == 'yes') and (count<len(df)):
            print("Printing ...")
            print(df[count:count+5])
            count+=5
            if ((count) >= len(df)):
                print(df[count:len(df)])
                print("\nNo more enteries to print!\n")
                break
        else:
            break

#
#
def main():
    while True:
        city, month, day = get_filters()
        print ("Applying filters:\nCity:{}\nMonth:{}\nDay:{}".format(city.title(), month.title(),day.title()))
        print('-'*40,'\n')
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_info=input('\nWould you like to see user stats, gender and birth year information? Enter \'yes\' or \'no\': \n')
        if user_info.lower() =='yes':
            user_stats(df)
        display_data(df)
        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
