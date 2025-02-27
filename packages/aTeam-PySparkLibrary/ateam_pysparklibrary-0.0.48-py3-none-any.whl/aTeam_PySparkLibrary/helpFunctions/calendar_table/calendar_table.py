'''
Modified version of calendar_table function @ https://github.com/TeneoPython01/calendar_table
'''

import pandas as pd
import numpy as np
from datetime import datetime
from .udfs import  date_udfs, df_udfs

def generate_calendar_table(start, end, frequency, wanted_columns=[], norwegian_names_for_days_and_months=False):
    #set pandas display options for printing to screen
    pd.set_option('display.max_rows', 1000) #allow printing lots of rows to screen
    pd.set_option('display.max_columns', 1000) #allow printsin lots of cols to screen
    pd.set_option('display.width', 1000) #don't wrap lots of columns
    #print metadata about the script and the user to start the script
    #set important user-defined variables
    start_dt = start
    end_dt= end
    freq = frequency
    wanted_columns = wanted_columns
    norwegian_names_for_days_and_months = norwegian_names_for_days_and_months

    df = pd.DataFrame()
    #create base date range
    df['dt'] = pd.date_range(start=start_dt, end=end_dt, freq=freq)
    #year as int
    df['y'] = pd.DatetimeIndex(df['dt']).year
    #month as int
    df['m'] = pd.DatetimeIndex(df['dt']).month
    #calendar day as int
    df['d'] = pd.DatetimeIndex(df['dt']).day
    #yearmonth as int
    df['ym'] = df['y']*100 + df['m']
    #date in yyyymmdd as int
    df['dt_int'] = df['y']*10000 + df['m']*100 + df['d']
    #day of week name (Monday, Tuesday, ...)
    df['dow_name'] = df['dt'].dt.day_name()
    #day of week number as int (Monday=0, Sunday=6)
    df['dow'] = df['dt'].dt.dayofweek
    #day of year number as int
    df['doy'] = df['dt'].dt.dayofyear
    #month name (January, February, ...)
    df['m_name'] = df['dt'].dt.month_name()
    
    if norwegian_names_for_days_and_months:
        # Translate the values to Norwegian
        df = df.replace({
            'dow_name': {
                'Monday': 'Mandag',
                'Tuesday': 'Tirsdag',
                'Wednesday': 'Onsdag',
                'Thursday': 'Torsdag',
                'Friday': 'Fredag',
                'Saturday': 'Lørdag',
                'Sunday': 'Søndag'
            },
            'm_name': {
                'January': 'Januar',
                'February': 'Februar',
                'March': 'Mars',
                'April': 'April',
                'May': 'Mai',
                'June': 'Juni',
                'July': 'Juli',
                'August': 'August',
                'September': 'September',
                'October': 'Oktober',
                'November': 'November',
                'December': 'Desember'
            }
        })
        
    #week number of year, using iso conventions (Monday is first DOW)
    df['iso_week'] = df['dt'].dt.isocalendar().week
    #normalized week number of year, using logic where first week (partial or full) is always 1
    #and where Sunday is first DOW
    #strftime"(%U" ) finds the week starting on Sunday; isoweek starts on sat
    #strftime starts with week 0 in some cases; adjust to add 1 to all weeks for years with
    #this situation so the first week of the year (partial or full) is always week 1.  note
    #this differs from the isoweek approach above in addition to the starting DOW noted.
    #TODO: modularize this code
    df['norm_week'] = df['dt'].apply(lambda x: x.strftime("%U")).astype(int)
    df['norm_week_adj'] = np.where(
        (df['doy']==1) & (df['norm_week']==0),
        1,
        np.where(
            (df['doy']==1),
            0,
            np.nan
            )
        )
    df['norm_week_adj'] = df[['y','norm_week_adj']].groupby('y')['norm_week_adj'].ffill()
    df['norm_week_adj'] = df['norm_week_adj'].fillna(0)
    df['norm_week'] = df['norm_week'] + df['norm_week_adj']
    df['norm_week'] = df['norm_week'].astype(int)
    df.drop('norm_week_adj', axis=1, inplace=True)
    #quarter number of year
    df['q'] = ((df['m']-1) // 3) + 1
    #yearquarter as int
    df['yq'] = df['y']*10+df['q']
    #half number of year
    df['h'] = ((df['q']-1) // 2) + 1
    #yearhalf as int
    df['yh'] = df['y']*10+df['h']
    #tertile number of year
    df['tertile'] = df['m'].apply(lambda x: 1 if x <= 4 else (2 if x <= 8 else 3))
    #yearmonth name
    df['ym_name'] = df['m_name'] + ', ' + df['y'].apply(lambda x: str(x))
    #ordinal dom suffix
    df['dom_suffix'] = df['d'].apply(lambda x: date_udfs.ordinalSuffix(x))
    #date name
    df['dt_name'] = df['m_name'] + ' ' + df['d'].apply(lambda x: str(x)) + df['dom_suffix'] + ', ' + df['y'].apply(lambda x: str(x))
    #is weekday (1=True, 0=False)
    df['is_weekd'] = np.where(df['dow'].isin([0,1,2,3,4,]), 1, 0)
    #weekdays in yearmonth through date
    df['weekdom'] = df[['ym','is_weekd']].groupby('ym')['is_weekd'].cumsum()
    #total weekdays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_weekd_in_mo', 'ym', 'is_weekd', 'sum')
    #weekdays remaining in ym
    df['weekd_remain_ym'] = df['tot_weekd_in_mo'] - df['weekdom']
    #total caldays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_cald_in_mo', 'ym', 'dt_int', 'count')
    #calendar days remaining in yearmonth
    df['cald_remain_ym'] = df['tot_cald_in_mo'] - df['d']
    #weekdays in year through date
    df['weekdoy'] = df[['y','is_weekd']].groupby('y')['is_weekd'].cumsum()
    #total weekdays in year
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_weekd_in_y', 'y', 'is_weekd', 'sum')
    #weekdays remaining in year
    df['weekd_remain_y'] = df['tot_weekd_in_y'] - df['weekdoy']
    #total caldays in year
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_cald_in_y', 'y', 'dt_int', 'count')
    #calendar days remaining in year
    df['cald_remain_y'] = df['tot_cald_in_y'] - df['doy']
    #is monday (1=True, 0=False)
    df['is_dow_mon'] = (df['dow']==0).astype(int)
    #is tuesday 1=True, 0=False)
    df['is_dow_tue'] = (df['dow']==1).astype(int)
    #is wednesday (1=True, 0=False)
    df['is_dow_wed'] = (df['dow']==2).astype(int)
    #is thursday 1=True, 0=False)
    df['is_dow_thu'] = (df['dow']==3).astype(int)
    #is friday 1=True, 0=False)
    df['is_dow_fri'] = (df['dow']==4).astype(int)
    #is saturday (1=True, 0=False)
    df['is_dow_sat'] = (df['dow']==5).astype(int)
    #is sunday (1=True, 0=False)
    df['is_dow_sun'] = (df['dow']==6).astype(int)
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_mon_in_ym', 'ym', 'is_dow_mon', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_tue_in_ym', 'ym', 'is_dow_tue', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_wed_in_ym', 'ym', 'is_dow_wed', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_thu_in_ym', 'ym', 'is_dow_thu', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_fri_in_ym', 'ym', 'is_dow_fri', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_sat_in_ym', 'ym', 'is_dow_sat', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_sun_in_ym', 'ym', 'is_dow_sun', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_mon_in_y', 'y', 'is_dow_mon', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_tue_in_y', 'y', 'is_dow_tue', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_wed_in_y', 'y', 'is_dow_wed', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_thu_in_y', 'y', 'is_dow_thu', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_fri_in_y', 'y', 'is_dow_fri', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_sat_in_y', 'y', 'is_dow_sat', 'sum')
    #total mondays in yearmonth
    df = df_udfs.addColumnFromGroupbyOperation(df, 'tot_sun_in_y', 'y', 'is_dow_sun', 'sum')
    #mondays of yearmonth through date
    df['dow_mon_om'] = df[['ym','is_dow_mon']].groupby('ym')['is_dow_mon'].cumsum()
    #tuesdays of yearmonth through date
    df['dow_tue_om'] = df[['ym','is_dow_tue']].groupby('ym')['is_dow_tue'].cumsum()
    #wednesdays of yearmonth through date
    df['dow_wed_om'] = df[['ym','is_dow_wed']].groupby('ym')['is_dow_wed'].cumsum()
    #thursdays of yearmonth through date
    df['dow_thu_om'] = df[['ym','is_dow_thu']].groupby('ym')['is_dow_thu'].cumsum()
    #fridays of yearmonth through date
    df['dow_fri_om'] = df[['ym','is_dow_fri']].groupby('ym')['is_dow_fri'].cumsum()
    #saturdays of yearmonth through date
    df['dow_sat_om'] = df[['ym','is_dow_sat']].groupby('ym')['is_dow_sat'].cumsum()
    #sundays of yearmonth through date
    df['dow_sun_om'] = df[['ym','is_dow_sun']].groupby('ym')['is_dow_sun'].cumsum()
    #mondays of year through date
    df['dow_mon_oy'] = df[['y','is_dow_mon']].groupby('y')['is_dow_mon'].cumsum()
    #tuesdays of year through date
    df['dow_tue_oy'] = df[['y','is_dow_tue']].groupby('y')['is_dow_tue'].cumsum()
    #wednesdays of year through date
    df['dow_wed_oy'] = df[['y','is_dow_wed']].groupby('y')['is_dow_wed'].cumsum()
    #thursdays of year through date
    df['dow_thu_oy'] = df[['y','is_dow_thu']].groupby('y')['is_dow_thu'].cumsum()
    #fridays of year through date
    df['dow_fri_oy'] = df[['y','is_dow_fri']].groupby('y')['is_dow_fri'].cumsum()
    #saturdays of year through date
    df['dow_sat_oy'] = df[['y','is_dow_sat']].groupby('y')['is_dow_sat'].cumsum()
    #sundays of year through date
    df['dow_sun_oy'] = df[['y','is_dow_sun']].groupby('y')['is_dow_sun'].cumsum()

    #is day Leap Year day
    df['is_d_leapyr'] = np.where(
        (df['m']==2) & (df['d']==29),
        1,
        0
        )
    #is yearmonth a Feb that contains Leap Year day
    df = df_udfs.addColumnFromGroupbyOperation(df, 'is_ym_leapyr', 'ym', 'is_d_leapyr', 'sum')
    #is year a leap year
    df = df_udfs.addColumnFromGroupbyOperation(df, 'is_y_leapyr', 'y', 'is_d_leapyr', 'sum')
    #first day of month datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_dom_dt', 'ym', 'dt', 'min')
    #first day of month int
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_dom_int', 'ym', 'dt_int', 'min')
    #last day of month datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_dom_dt', 'ym', 'dt', 'max')
    #last day of month datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_dom_int', 'ym', 'dt_int', 'max')
    #first day of yearquarter datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doyq_dt', 'yq', 'dt', 'min')
    #first day of yearquarter int
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doyq_int', 'yq', 'dt_int', 'min')
    #last day of yearquarter datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doyq_dt', 'yq', 'dt', 'max')
    #last day of yearquarter datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doyq_int', 'yq', 'dt_int', 'max')
    #first day of yearhalf datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doyh_dt', 'yh', 'dt', 'min')
    #first day of yearhalf int
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doyh_int', 'yh', 'dt_int', 'min')
    #last day of yearhalf datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doyh_dt', 'yh', 'dt', 'max')
    #last day of yearhalf datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doyh_int', 'yh', 'dt_int', 'max')
    #first day of year datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doy_dt', 'y', 'dt', 'min')
    #first day of year int
    df = df_udfs.addColumnFromGroupbyOperation(df, 'first_doy_int', 'y', 'dt_int', 'min')
    #last day of year datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doy_dt', 'y', 'dt', 'max')
    #last day of year datetime
    df = df_udfs.addColumnFromGroupbyOperation(df, 'last_doy_int', 'y', 'dt_int', 'max')

    # Norwegian holidays
    # read csv file from this blob storage url: https://ateamlibrarystorage.blob.core.windows.net/helligdager/helligdagskalender.csv
    norwegian_holidays = pd.read_csv('https://ateamlibrarystorage.blob.core.windows.net/helligdager/helligdagskalender.csv')

    # make the "dato" column a datetime object
    norwegian_holidays['dato'] = pd.to_datetime(norwegian_holidays['dato'], format='%d.%m.%Y')
    # merge the Norwegian holidays dataframe with the calendar table dataframe on the date column
    df = pd.merge(df, norwegian_holidays, how='left', left_on='dt', right_on='dato')
    # i am now interested in the "navn" column from the Norwegian holidays dataframe and i will rename it to "holiday_name"
    df.rename(columns={'navn':'holiday_name'}, inplace=True)
    # create a new column "is_holiday" that is 1 if the "holiday_name" column is not null and 0 otherwise
    df['is_holiday'] = np.where(df['holiday_name'].notnull(), 1, 0)
    # drop the other colums from the Norwegian holidays dataframe
    df.drop(columns=['år', 'dato', 'dag', 'uke'], inplace=True)

    # column for if the day is a working day, meaning it is not a weekend or a holiday based on the is_holiday column and the dow column
    df['is_workday'] = np.where((df['is_holiday']==0) & (df['dow'].isin([0,1,2,3,4])), 1, 0)

    # Filter the DataFrame based on wanted_columns
    if wanted_columns:
        df = df[[col for col in wanted_columns if col in df.columns]]
  
    #timestamp when the calendar table was generated by this script
    df['created_on'] = datetime.now()

    return df
