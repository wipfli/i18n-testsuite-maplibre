import json
import csv

geojson = {
    "type": "FeatureCollection",
    "features": []
}

with open('tests.csv') as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(row['Longitude']),
                    float(row['Latitude'])
                ]
            },
            "properties": {
                "name": row['English Name'],
                "native_name": row['Native Name'],
                "script": row['Script']
            }
        }
        geojson['features'].append(feature)
    
    with open('tests.geojson', 'w') as f:
        json.dump(geojson, f)
