from .helpFunctions.calendar_table.calendar_table import generate_calendar_table




def generate_dim_date_table(start, end, frequency, wanted_columns=[], norwegian_names_for_days_and_months=False):
    """
    This function generates a calendar table. \n
    Parameters:
        start: str
            The start date of the calendar table
        end: str
            The end date of the calendar table
        frequency: str
            The frequency of the calendar table
            For example: 'D' for daily, 'W' for weekly, 'M' for monthly, 'Q' for quarterly, 'Y' for yearly
        wanted_columns: list
            Specify the wanted columns of the calendar table. Leave empty if you want all columns.
            See https://github.com/EgdeConsulting/aTeam-PySparkLibrary/tree/main/src/aTeam_PySparkLibrary/helpFunctions/calendar_table/docs/col_descriptions.csv for column descriptions and which columns are available in wanted_columns
        norwegian_names_for_days_and_months: bool
            If True, the names of the days and months will be in Norwegian, else they will be in English
    Returns:
        DataFrame
            The calendar table
    Example:
        df = generate_dim_date_table(start='01-01-2020', end='12-31-2025', frequency='D', wanted_columns=['y', 'm', 'd', 'dow_om', 'tot_weekd_in_mo', 'is_d_leapyr'])
    """
    df = generate_calendar_table(start=start, end=end, frequency=frequency, wanted_columns=wanted_columns, norwegian_names_for_days_and_months=norwegian_names_for_days_and_months)
    return df