import time
import pandas as pd
import numpy as np

# Dictionary mapping city names to their respective data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze with error handling.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month? (all, january, february, march, april, may, june)\n").strip().lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month (up to June) or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day? (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n").strip().lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable[cite: 156, 158].
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_idx = months.index(month) + 1
        df = df[df['month'] == month_idx]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print(f"Most Common Month: {df['month'].mode()[0]}")

    # Display the most common day of week
    print(f"Most Common Day: {df['day_of_week'].mode()[0]}")

    # Display the most common start hour
    print(f"Most Common Start Hour: {df['hour'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print(f"Most Common Start Station: {df['Start Station'].mode()[0]}")

    # Display most commonly used end station
    print(f"Most Common End Station: {df['End Station'].mode()[0]}")

    # Display most frequent combination of start station and end station trip
    # Optimized using groupby
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Common Trip: {common_trip[0]} to {common_trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration[cite: 38]."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print(f"Total Travel Time: {df['Trip Duration'].sum()} seconds")

    # Display mean travel time
    print(f"Average Travel Time: {df['Trip Duration'].mean()} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"User Type Counts:\n{df['User Type'].value_counts()}")

    # Display counts of gender (only available for NYC and Chicago)
    if 'Gender' in df.columns:
        print(f"\nGender Counts:\n{df['Gender'].value_counts()}")
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"\nBirth Year Stats:\n"
              f"  Earliest: {int(df['Birth Year'].min())}\n"
              f"  Most Recent: {int(df['Birth Year'].max())}\n"
              f"  Most Common: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Prompts user to see 5 lines of raw data at a time[cite: 71, 72, 190]."""
    row = 0
    while True:
        view_raw = input("\nWould you like to see 5 lines of raw data? Enter 'yes' or 'no'.\n").lower()
        if view_raw == 'yes':
            # Display the next 5 lines 
            print(df.iloc[row : row + 5])
            row += 5
            # Stop if no more data 
            if row >= len(df):
                print("No more data to display.")
                break
        elif view_raw == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()