def process_api_data(api_data):
    data_results = api_data.get('results', [])  # Extract 'results' from the API data
    processed_data = []
    
    for entry in data_results:
        date = entry.get('date')
        prcp = None
        snow = None
        tmax = None
        tmin = None
        tobs = None
        
        # Extract relevant data based on 'datatype' field
        if entry.get('datatype') == 'PRCP':
            prcp = entry.get('value')
        elif entry.get('datatype') == 'SNOW':
            snow = entry.get('value')
        elif entry.get('datatype') == 'TMAX':
            tmax = entry.get('value')
        elif entry.get('datatype') == 'TMIN':
            tmin = entry.get('value')
        elif entry.get('datatype') == 'TOBS':
            tobs = entry.get('value')
        
        # Append the processed data to the list
        processed_data.append({
            'date': date,
            'PRCP': prcp,
            'SNOW': snow,
            'TMAX': tmax,
            'TMIN': tmin,
            'TOBS': tobs
        })
    
    return processed_data