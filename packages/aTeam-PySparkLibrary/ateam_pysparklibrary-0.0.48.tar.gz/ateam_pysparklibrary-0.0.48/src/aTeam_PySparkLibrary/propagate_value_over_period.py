### author: Ludvig Løite

from pyspark.sql.functions import  lit
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from datetime import timedelta
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from copy import deepcopy


def propagate_value_over_period(read_path, write_path, start_date_column_in_input_table, end_date_column_in_input_table, date_column_in_output_table, months_added_in_case_of_null_end_date, time_period, spark):

    silver_df = spark.read.format("delta").load(read_path)
    silver_df_new = silver_df.withColumn(date_column_in_output_table, lit(None))

    silver_pd_df = silver_df_new.toPandas()

    # Forklaring av koden under:
    # Vi ønsker å gjøre om en rad hvor det står en startdato og en slutdato til en rad per måned/kvartal/år i dette intervallet. 
    # Koden går først gjennom alle rader. Deretter sjekker den om startdato er null. Da vil vi ikke ha noen mulighet til å lage et intervall, og vi kaster en exeption.
    # Deretter sjekker koden om sluttdato er null. Dersom den er det antar vi at raden er gyldig i 12 mnd. Det er ikke videre diskutert om dette er en gyldig antakelse. Her burde vi også utløse en alert.
    # Nå vet vi at vi har både en gyldig startdato og en gyldig sluttdato. Siden vi ønsker at alle måneder skal bli identifisert av sin first_date_in_month setter vi loopens første dato til den første dagen i den måneden startdato er i. Dersom energimerkingen ble utstedt den 18/08/2016 vil den første raden få first_date_in_month=01/08/2016.
    # Deretter har vi en loop som for hver måned/kvartal/år setter kolonnen first_date_in_month og legger raden til arrayet data[]. Dette blir senere skrevet som Delta til sølv.

    data = []

    for _, row in silver_pd_df.iterrows():
    
        if not row[start_date_column_in_input_table]:
            print("Start date is null")
            data.append(deepcopy(row))
            raise Exception(f'Start date column is null.') 
            

        if not row[end_date_column_in_input_table]:
            loop_end_date = loop_starting_date + relativedelta(months=months_added_in_case_of_null_end_date) - timedelta(days=1)
            print(f"End date column is null. Setting end date to {months_added_in_case_of_null_end_date} months from start date.")
            # TODO Implement alert if expireDate is null?

        loop_starting_date = row[start_date_column_in_input_table] - timedelta(days=row[start_date_column_in_input_table].day-1)
        loop_end_date = row[end_date_column_in_input_table]

        if time_period == "monthly":
            period_rrule_freq = rrule.MONTHLY
            period_rrule_opts = {}
        elif time_period == "quarterly":
            # Quarterly is achieved by setting MONTHLY with an interval of 3
            period_rrule_freq = rrule.MONTHLY
            period_rrule_opts = {"interval": 3}
        elif time_period == "yearly":
            period_rrule_freq = rrule.YEARLY
            period_rrule_opts = {}
        else:
            raise Exception(f'Time period {time_period} is not supported.')
        
        for dt in rrule.rrule(period_rrule_freq, dtstart=loop_starting_date, until=loop_end_date, **period_rrule_opts):
            row[date_column_in_output_table] = dt.date()
            data.append(deepcopy(row))


    # Forklaring av koden under:
    # I tilfellet med energimerking er koden under implementert for å håndtere tilfeller hvor det er overlappende energimerkinger.
    # Koden er implementert for å håndtere de tilfeller hvor en gyldigheten til en energimerking er ferdig og en ny begynner, for samme eiendom.
    # Eksempel: En eiendom har en energimerking som er gyldig fra 18/08/2016 til 19/09/2016, og en annen energimerking som er gyldig fra 19/09/2016 til 19/09/2026. I September 2016 vil det da i utgangspunktet være 2 rader for den aktuelle eiendommen, noe vi ikke ønsker. Koden over regner ut hvor mange dager hver av energimerkingen har i gjeldene måned, og velger den energimerkingen som har flest dager. I dette eksemplet har den første energimerkingen 19 dager av September 2016, mens den andre har de resterende 11 dagene. Derfor vil den første energimerkingen være gjeldene for September 2016.
    # Koden sammenlikner alle rader i datasettet med seg selv, hhv. row_i og row_j. Vi vil luke ut de tilfellene hvor starttidspunktet til en energimerking er lik som sluttidspunktet på en annen.
    # Vi starter med å for hver rad i sjekke om den aktuelle måneden vi er på er den siste gyldige måneden i energimerkingen(samme måned som expireDate.) Grunnen til at vi sammenlikner med first_date_in_month er at vi tidligere gjør om alle måneder til first_date_in_month. Fra eksemplet over vil derfor både den første og den andre energimerkingen ha 01/09/2016 på sin kolonne first_date_in_month for måned september 2016.
    # Deretter sammenlikner vi denne siste gyldige måneden med alle andre energimerkinger. Hvis vi finner en annen energimerking på samme eiendom som starter i samme måned som denne slutter, regner vi ut hvilken av de to energimerkingene som ar flest dager. Deretter sletter vi den raden som har færrest dager.

    # The code beneath fixes overlapping certifications
    # LOGIC: The certification with the most days in the given month "gets" the month
    
    """    
    for i, row_i in enumerate(data):
        if row_i[end_date_column_in_input_table] - timedelta(days=row_i[end_date_column_in_input_table].day-1) == row_i[date_column_in_output_table]:
            for j, row_j in enumerate(data):
                # Skip comparing the row with itself
                if i == j:
                    continue
                if row_j[start_date_column_in_input_table] - timedelta(days=row_j[start_date_column_in_input_table].day-1) == row_j[date_column_in_output_table] and row_i[end_date_column_in_input_table] == row_j[start_date_column_in_input_table] and row_i[business_key_in_input_table] == row_j[business_key_in_input_table]:
                    if row_i[end_date_column_in_input_table].day > ((row_j[start_date_column_in_input_table]+MonthEnd(0)).day-row_j[start_date_column_in_input_table].day):
                        #i has most days -> delete j
                        del data[j]
                    else:
                        del data[i] 
                        
    """


    new_pd_df = pd.DataFrame(data)
    new_spark_df = spark.createDataFrame(new_pd_df)

    print(("\nFinished processing, writing to delta\n"))
    new_spark_df.write.format("delta").mode("overwrite").save(write_path)