from flask import Flask, render_template, send_from_directory
import os
app = Flask(__name__)

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the analytics page
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# Route to serve the forecast plot image
@app.route('/forecast_plot')
def forecast_plot():
    return send_from_directory('static', 'file:///D:/andrioddd/download.png')
# Route to serve the CSV file
@app.route('/recommendations.csv')
def serve_csv():
    # Assuming the CSV file is in the same directory as the Python script
    csv_path = os.path.join(app.root_path, 'recommendations.csv')
    return send_from_directory(os.path.dirname(csv_path), os.path.basename(csv_path))
if __name__ == '__main__':
    app.run(debug=True)
