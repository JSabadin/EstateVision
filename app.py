from flask import Flask
import psycopg2
import os  # Import os to read environment variables

app = Flask(__name__)

@app.route('/')
def show_flats():
    # Read database connection parameters from environment variables
    conn_params = {
        'host': os.getenv('POSTGRES_HOST'),
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD')
    }
        # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT title, image_url FROM flats;")
    flats = cursor.fetchall()

    # Generate HTML to display images
    flats_info = "<br>".join([
        f"<div><h2>{flat[0]}</h2><img src='{flat[1]}' alt='Image of {flat[0]}' style='max-width: 500px;'></div>"
        for flat in flats
    ])

    # Close the database connection
    cursor.close()
    conn.close()

    return f"<h1>List of Flats</h1>{flats_info}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 
