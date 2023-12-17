from flask import Flask, request, jsonify
import numpy as np
import pickle
import mysql.connector
from google.cloud import storage
import tensorflow as tf

app = Flask(__name__)
# Download the MinMaxScaler from the new Google Cloud Storage bucket
def download_minmax_scaler():
    bucket_name = 'model_londri'
    blob_name = 'minmax_scaler.pkl'

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename('minmax_scaler.pkl')

# Download the trained model from the new Google Cloud Storage bucket
def download_model():
    bucket_name = 'model_londri'
    blob_name = 'model_rev_final.tflite'

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename('model_rev_final.tflite')

# Load the MinMaxScaler from pickle file
def load_minmax_scaler():
    download_minmax_scaler()
    with open('minmax_scaler.pkl', 'rb') as f:
        return pickle.load(f)

# Load the trained model
def load_trained_model():
    download_model()
    return tf.lite.Interpreter(model_path='model_rev_final.tflite')

minmax_scaler = load_minmax_scaler()
savedModel = load_trained_model()
savedModel.allocate_tensors()

# MySQL database connection configuration
db_host = '34.101.116.210'
db_user = 'londri'
db_password = 'londri'
db_name = 'db_laundry'

# Create a MySQL database connection
db_connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Route input
@app.route('/proses_input', methods=['POST'])
def proses_input():
    try:
        input_json = request.get_json()

        # Extract information from JSON
        laundry_id = input_json.get('laundry_id')

        # Fetch data from MySQL based on the provided laundry id
        cursor = db_connection.cursor()
        laundry_query = "SELECT id, name, latitude, longitude FROM laundry WHERE id = %s"
        cursor.execute(laundry_query, (laundry_id,))
        laundry_data = cursor.fetchone()
        cursor.close()

        if not laundry_data:
            return jsonify({'error': 'Invalid laundry_id'})

        # Use the loaded MinMaxScaler for latitude and longitude
        long_lat = np.array(laundry_data[2:4]).reshape(1, -1)
        long_lat_scaled = minmax_scaler.transform(long_lat)
        latitude_scaled, longitude_scaled = long_lat_scaled.flatten()[:2]

        # Fetch layanan names associated with each laundry result
        layanan_names_query = """
            SELECT layanan.id, layanan.name
            FROM layanan
            WHERE layanan.id_laundry = %s
        """
        cursor = db_connection.cursor()
        cursor.execute(layanan_names_query, (laundry_id,))
        layanan_data = cursor.fetchall()
        cursor.close()

        if not layanan_data:
            return jsonify({'error': 'No layanan data found for the given laundry_id'})

        # Define specific name values for each kategori
        kategori_values = ['cuci', 'dryclean', 'komplit', 'komplit kilat', 'setrika']

        # Initialize boolean lists for each kategori
        kategori_lists = [
            int(any(value in layanan_name[1].lower() for layanan_name in layanan_data))
            for value in kategori_values
        ]

        # Combine all the data into new_data_point
        new_data_point = np.hstack([latitude_scaled, longitude_scaled] + kategori_lists)

        # Reshape new_data_point
        new_data_point = new_data_point.reshape(1, -1)

        # Check the shape of new_data_point
        print(new_data_point.shape)

        # Convert the boolean values to integers (0 for false, 1 for true)
        new_data_point = new_data_point.astype(np.float32)  # Adjust to the appropriate data type

        # If you want to use the machine learning model (example recommendation)
        new_data_point = new_data_point.reshape(1, -1)
        
        savedModel.set_tensor(savedModel.get_input_details()[0]['index'], new_data_point)
        savedModel.invoke()

        recommendation_score = savedModel.get_tensor(savedModel.get_output_details()[0]['index'])
        class_probabilities = recommendation_score[0]
        sorted_indices = np.argsort(class_probabilities)[::-1]
        next_most_likely_indices = sorted_indices[1:6]

        # Fetch data from MySQL based on the next most likely indices
        cursor = db_connection.cursor()

        # Assuming 'laundry' has columns 'id', 'name', 'latitude', 'longitude'
        placeholders = ', '.join(['%s'] * len(next_most_likely_indices))
        laundry_query = f"SELECT id, name FROM laundry WHERE id IN ({placeholders})"
        cursor.execute(laundry_query, tuple(map(int, next_most_likely_indices)))
        laundry_results = cursor.fetchall()

        # Close the cursor after fetching data
        cursor.close()

        # Retrieve layanan names for each laundry result
        final_results = []
        for result in reversed(laundry_results):
            laundry_id = result[0]
            layanan_names_query = """
                SELECT layanan.name
                FROM layanan
                WHERE layanan.id_laundry = %s
            """
            cursor = db_connection.cursor()
            cursor.execute(layanan_names_query, (laundry_id,))
            layanan_names = [layanan[0] for layanan in cursor.fetchall()]
            cursor.close()

            final_result = {
                'id': laundry_id,
                'name': result[1],
                'layanan_names': layanan_names,
            }
            final_results.append(final_result)

        # Respond with additional information
        return jsonify({
            'laundry_results': final_results,  # Include the fetched data from the 'laundry' table      
        })

    except Exception as e:
        # Debugging: Print any exception that occurs
        print("Error:", str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
