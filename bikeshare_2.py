import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#HELPFUL LINKS
#https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
#Mentor forum on Udacity

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
        city = input("\n Which city would you like to analyze? chicago, new york city or washington?\n").lower()
        if city not in ('new york city','chicago','washington'):
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(" \n Which month would you like to analyze? January, February, March, April, May, June? You may also type 'all' to view all months. \n")
        if month not in ('January','February','March', 'April', 'May', 'June', 'all'):
            print("This was not a valid input, please try again and check Spelling/Cap.")
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(" \n Please select a specific day in the following format: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or enter 'all' if you are not looking for any specific day. \n")
        if day not in ('Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'):
            print("This was not a valid input, please try again.")
            continue
        else:
            break



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
    #loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #converts the Start Time column into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Get month and the day of the week so you can filter by them from Start Time
    #Similar to Pracitce Problem #1 extracting hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_the_week'] = df['Start Time'].dt.day_name()

    #Filter by month is applicable
    #This is similar to Practice Problem 3
    if month != 'all':
        #use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        #Filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # filter by the day of week if applicable
    if day != 'all':
        # filter by the day of the week to create the new DataFrame
        df = df[df['day_of_the_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # Similar to Practice Problem 1
    most_common_month = df['month'].mode()
    print('Most Common Month:', most_common_month)


    # display the most common day of week
    most_common_day = df['day_of_the_week'].mode()
    print('Most common day:', most_common_day)

    # display the most common start hour
    #First, extract hour from Start Time
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()
    print('Most common start hour:', most_common_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station: idxmax not max()
    # Also similar to Practice Problem 2
    Start_Station = df['Start Station'].mode()[0]
    print('Most commonly used start startion:', Start_Station)


    # display most commonly used end station:
    End_Station = df['End Station'].mode()[0]
    print('Most commonly used end station:', End_Station)


    # display most frequent combination of start station and end station trip
    Start_End_Station_Combo = df.groupby(['Start Station', 'End Station']).count()
    print('Most frequent combination of start and end station trip:', Start_Station, End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time. Use methods from Pandas section
    tot_travel_time = sum(df['Trip Duration'])
    print('Total Travel Time:', tot_travel_time/86400,"Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #Similar to Practice Problem 2
    user_types = df['User Type'].value_counts()
    print('User Types:', user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('Gender Types:', gender)
    except KeyError:
        print("There is no gender data detectable.")



    # Display earliest, most recent, and most common year of birth

    #Earliest birth year
    try:
        earliest_birthyear = df['Birth Year'].min()
        print('\nEarliest Birth Year:', earliest_birthyear)
    except KeyError:
        print("There was no data available")

    #Most Recent Birth year
    try:
        Most_Recent = df['Birth Year'].max()
        print('Most Recent Birth Year:', Most_Recent)
    except:
        print("There was no data available for Most Recent Birth Year.")

    #Most Common Birth year
    try:
        Most_Common = df['Birth Year'].value_counts().idxmax()
        print('Most Common Birth Year:', Most_Common)
    except:
        print("There was no data available for the most common birth year.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row = 0
        while True:
            viewData = input("Would you like to see the raw data? Type 'Yes' or 'No'.")
            if viewData == "Yes":

                print(df.iloc[row : row+5])
                row += 5
            else:
                break
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'Yes':
                break

if __name__ == "__main__":
    main()
