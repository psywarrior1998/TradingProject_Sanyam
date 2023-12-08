from celery import shared_task
import json
from datetime import timedelta


@shared_task
def convert_data(candles, timeframe):
    """
    Convert a list of candles to a specified timeframe and save the results as a JSON file.

    Args:
        candles: A list of Candle objects.
        timeframe: The desired timeframe (e.g., minutes, hours, days).
        filename: The filename for the generated JSON file.
    """

    # Convert candle data to pandas DataFrame
    import pandas as pd
    data = pd.DataFrame(candles)

    # Set the date as the index
    data.set_index('date', inplace=True)

    # Convert timeframe to timedelta
    timeframe_delta = timedelta(minutes=timeframe)

    # Resample data to the desired timeframe
    resampled_data = data.resample(timeframe_delta).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
    })

    # Store resampled data as a list of dictionaries
    converted_data = []
    for index, row in resampled_data.iterrows():
        converted_data.append({
            'date': str(index),
            'open': row['open'],
            'high': row['high'],
            'low': row['low'],
            'close': row['close'],
        })

    # Generate JSON filename
    json_filename = f'candles_{timeframe}.json'

    # Write converted data to JSON file
    with open(json_filename, 'w') as file:
        json.dump(converted_data, file)