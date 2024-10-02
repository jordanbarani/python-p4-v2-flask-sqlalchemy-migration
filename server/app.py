from flask import Flask, jsonify, request
from models import db, Earthquake  # Import your database and model
from datetime import datetime

app = Flask(__name__)

# Route to query earthquakes by filters
@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_magnitude = request.args.get('min_magnitude')
    max_magnitude = request.args.get('max_magnitude')

    # Build the query
    query = Earthquake.query

    # Filter by date range if provided
    if start_date:
        query = query.filter(Earthquake.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Earthquake.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    # Filter by magnitude range if provided
    if min_magnitude:
        query = query.filter(Earthquake.magnitude >= float(min_magnitude))
    if max_magnitude:
        query = query.filter(Earthquake.magnitude <= float(max_magnitude))

    # Execute the query
    earthquakes = query.all()

    # Format the results as JSON
    results = [{
        'id': quake.id,
        'location': quake.location,
        'date': quake.date.strftime('%Y-%m-%d'),
        'magnitude': quake.magnitude
    } for quake in earthquakes]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
