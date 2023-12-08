from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime

from MainApp.models import Candle
from MainApp.tasks import convert_data
import os
import csv

from django import forms

class MyForm(forms.Form):
    csv_file = forms.FileField(label="CSV Data File", required=True)
    # Optional fields can be added here

def parse_csv_data(uploaded_file_path):
    # Open the uploaded file
    with open(uploaded_file_path, 'r') as f:
        # Read the CSV data
        data = csv.reader(f)

        # Process each data row and create candle objects or dictionaries
        # ...
        parsed_data = []
        for row in data:
            # ...
            parsed_data.append({
                # ... Populate dictionary with extracted data
            })

    return parsed_data

def upload_data(request):
    if request.method == "POST":
        # Handle uploaded file and timeframe
        uploaded_file = request.FILES['csv_file']
        # Create directory for uploaded files if not exists
        if not os.path.exists('data'):
            os.makedirs('data')

        # Save uploaded file with unique filename
        filename = f'data/{uploaded_file.name}'
        with open(filename, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Create a hidden field for the current timestamp
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        hidden_timeframe_field = forms.CharField(initial=current_time, widget=forms.HiddenInput())

        # Create the form with the hidden field
        form = MyForm(request.POST, request.FILES)
        form.fields['timeframe'] = hidden_timeframe_field

        # Validate the form
        if form.is_valid():
            # Parse uploaded file and retrieve data
            candles = parse_csv_data(f'data/{uploaded_file.name}')
            
            # Get the timeframe from the hidden field
            timeframe = int(form.cleaned_data['timeframe'])

            # Process the upload as usual (save file, parse data, etc.)

            # Run conversion task asynchronously
            convert_data.delay(candles, timeframe)

            # Render confirmation message
            return render(request, 'upload_data.html', {'upload_success': True})
        else:
            # Handle form validation errors
            return render(request, 'upload_data.html', {'form': form})
    else:
        # Get the current time
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the form with the hidden timeframe field
        form = MyForm()
        form.fields['timeframe'] = forms.CharField(initial=current_time, widget=forms.HiddenInput())

        # Render the upload form with the hidden timeframe
        return render(request, 'upload_data.html', context={'form': form})

def get_converted_data(request):
    # Extract timeframe from request parameter
    timeframe = request.GET.get('timeframe')

    # Fetch converted data from database (replace with actual model retrieval)
    candles = Candle.objects.filter(timeframe=timeframe).order_by('date')

    # Check if data conversion is complete
    if not candles.first().converted:
        return JsonResponse({'status': 'processing'})

    # Convert candles to JSON format
    data = [candle.to_dict() for candle in candles]

    # Generate JSON filename
    json_filename = f'converted_data_{timeframe}.json'

    # Write converted data to JSON file
    with open(json_filename, 'w') as f:
        json.dump(data, f)

    # Render visualization page with JSON download link
    return render(request, 'get_data.html', {'data': data, 'download_url': json_filename})