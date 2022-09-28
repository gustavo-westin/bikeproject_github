import time
import pandas as pd
import numpy as np

#dictionary to access data from the csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# function to get valid values for city, month and day
def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    # City values input
    city = str(input("Please, enter city's name: ")).lower().strip()
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        print("sorry, but you has used an incorrect option, please choose one of them: Chicago, New York City or Washington")
        city = str(input("Please, enter city's name: ")).lower().strip()

    # Month values input
    month = str(input("Please, enter month that you want explore from january to june or 'all' to see all them: ")).lower().strip()
    while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month != 'all':
        print('You have used a non available month, please enter a valid option: january throught ju')
        month = str(input("Please, enter month that you want explore from january to june or 'all' to see all them: ")).lower().strip()

    # Week day values input
    day = str(input('Please, enter a name of week day from monday to sunday: ')).strip().lower()
    while day != 'all' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
        print("You have used a non available day's name, please enter a valid option")
        day = str(input('Please, enter a name of week day from monday to sunday: ')).strip().lower()


    print('-'*40)
    return city, month, day

#function to load data from csv file dictionary and convert in a df
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    #transform object in datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #create columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #using index to get filter options
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

# function for most popular time stats by mode
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most popular month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month - 1]
    print(f'the most popular month is {popular_month}')


    #display the most popular week day
    popular_day = df['day_of_week'].mode()[0]
    print(f'the most popular week day is {popular_day}')


    #display the most popular hour day
    popular_hour = df['hour'].mode()[0]
    print(f'the most popular hour is {popular_hour}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function to get some basic stats from df columns
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display the most popular start point in a ride
    popular_start = df['Start Station'].mode()[0]
    print(f'the most frequent start point is {popular_start}')


    #display the most popular end point in a ride
    popular_end = df['End Station'].mode()[0]
    print(f'the most frequent destination is: {popular_end}')


    #display the most popular start-end points combined
    df['combined_station'] = df['Start Station'].str.cat(df['End Station'], sep=' / ')
    most_comb = df['combined_station'].mode()[0]
    print(f'the most frequent "start to end" is: {most_comb}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# function to get info about avg duration of trips
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #get the total duration in seconds
    total_duration = df['Trip Duration'].sum()
    #use divmod function to get hours, minutes etc.
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    days, hour = divmod(hour, 24)
    #display information
    print(f'the total duration is: {days} days, {hour} hours, {minute} minutes, {second} seconds')


    # get the avarage trip time in seconds
    avg_time = df['Trip Duration'].mean()
    #use divmod to get the information and display it
    avg_minute, avg_second = divmod(avg_time, 60)
    avg_second, rest = divmod(avg_second, 1)
    print(f'the avarage duration is: {avg_minute} minutes, {avg_second} seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#funcition to get some generic information about gender and age from customers and subscribers
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #displaying the user types and gender info
    '''the try/except was needed because Washington city doesn't have gender or year birth info'''
    try:
        user_count = df['User Type'].value_counts()
        gender_count = df['Gender'].value_counts()
        print(f'There is these User Types \n{user_count}')
        print(f'There is these peolple in each Gender: \n{gender_count}')
        #check nam values
        gender_nam = df['Gender'].isna().value_counts()
        print(f'True option are gender NaM values: {gender_nam}')
    except:
        print("the city you've chosen doesn't have gender info")

    #Display earliest, most recent, an most common year of birth
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        mode_age = int(df['Birth Year'].mode()[0])
        print(f'the oldest user had born in... \n{oldest}')
        print(f'the youngest user had born in... \n{youngest}')
        print(f'the most common users birth year is... \n{mode_age}')
    except:
        print("the city you've chosen doesn't have customer's age info")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function to allow users to consult some raw data
def display_data(df):
    ask = str(input("Do you want to see some raw data? \nPlease insert 'yes' or 'no': ")).lower().strip()
    count = 0
    #while loop to show so many data a users want, but just 5 lines each
    while ask == 'yes':
        print(df.iloc[count:count+5])
        ask = str(input("Do you want to see more data? 'yes' or 'no': "))
        if ask == 'yes':
            count += 5
        while ask != 'no' and ask != 'yes':
            print('please, reconsider your answer, use yes or no as a response')
            ask = str(input("Do you want to see more data? 'yes' or 'no': "))
    print('Thank you!')

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart53? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
