import pandas as pd

# Load the data from a CSV file
try:
    df = pd.read_csv('Assignment.csv')
except FileNotFoundError:
    print("File not found. Please make sure the file 'employee_data.csv' exists.")
    exit()

# Convert "Time In" and "Time Out" columns to datetime
df['Time In'] = pd.to_datetime(df['Time In'], format='%m/%d/%Y %I:%M %p', errors='coerce')
df['Time Out'] = pd.to_datetime(df['Time Out'], format='%m/%d/%Y %I:%M %p', errors='coerce')

# Convert the "Timecard Hours" column to a numeric type (float)
df['Timecard Hours'] = pd.to_numeric(df['Timecard Hours'], errors='coerce')

# Sort the DataFrame by "Employee Name" and "Time In"
df.sort_values(by=['Employee Name', 'Time In'], inplace=True)

# Initialize variables to track consecutive days and previous end time
consecutive_days = 1
prev_end_time = None

# Initialize a list to store employees who meet the criteria
results = []

# Iterate through the DataFrame to analyze shifts
for index, row in df.iterrows():
    employee_name = row['Employee Name']
    position = row['Position ID']
    time_in = row['Time In']
    time_out = row['Time Out']
    hours_worked = row['Timecard Hours']

    # Check for long shifts
    if hours_worked > 14:
        print(f"{employee_name} ({position}) worked more than 14 hours on {time_in}")

    # Check for consecutive days
    if prev_end_time is not None and (time_in - prev_end_time).days == 1:
        consecutive_days += 1
    else:
        consecutive_days = 1  # Reset consecutive days count

    if consecutive_days == 7:
        results.append((employee_name, position))

    prev_end_time = time_out

# Create a DataFrame for the results including "Timecard Hours"
results_df = pd.DataFrame(results, columns=['Employee Name', 'Position ID'])
results_df['Timecard Hours'] = None

# Print employees who worked 7 consecutive days
if not results_df.empty:
    print("Employees who worked 7 consecutive days:")
    print(results_df)

# Filter employees who have less than 10 hours between shifts and greater than 1 hour
time_between_shifts = df['Time In'].diff().shift(-1)
filtered_df = df[(time_between_shifts >= pd.Timedelta(hours=1)) & (time_between_shifts < pd.Timedelta(hours=10))]

# Print employees who meet the time between shifts criteria
if not filtered_df.empty:
    print("Employees who have less than 10 hours between shifts but greater than 1 hour:")
    print(filtered_df[['Employee Name', 'Position ID', 'Time In', 'Time Out', 'Timecard Hours']])

# Export the filtered data to a CSV file including "Timecard Hours"
if not filtered_df.empty:
    filtered_df.to_csv('filtered_shifts_result.csv', index=False)
    print("Filtered shift data exported to 'filtered_shifts_result.csv'.")

# Export the results to a CSV file
results_df.to_csv('consecutive_days_result.csv', index=False)

# Export the results to an Excel file
# results_df.to_excel('consecutive_days_result.xlsx', index=False)

print("Analysis complete. Results exported to CSV and Excel files.")
