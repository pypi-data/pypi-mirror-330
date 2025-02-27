import sys
sys.path.insert(0, './src/')
from aTeam_PySparkLibrary.generate_dim_date_table import generate_dim_date_table
import os

# Generate the calendar table
df = generate_dim_date_table(start='01-01-2020', end='12-31-2025', frequency='D', 
                           wanted_columns=['y', 'm', 'd', 'dow_om', 'tot_weekd_in_mo', 
                                        'is_d_leapyr', 'is_workday', 'tertile'])

# Get the current script's directory and create output filename
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'calendar_table_output.csv')

# Write to CSV
df.to_csv(output_file, index=False)
print(f"Output written to: {output_file}")