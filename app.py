from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def show_flats():
    """
    Show the list of flats from the database as HTML with images and titles. 
    """
    # Read database connection parameters from environment variables
    conn_params = {
        'host': os.getenv('POSTGRES_HOST'),
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD')
    }
    # Connect to the database
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()

    # Execute query
    cursor.execute("SELECT title, image_url FROM flats;")
    flats = cursor.fetchall()

    # CSS to enhance the page appearance
    style = """
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
        .flat { margin-bottom: 20px; }
        .flat h2 { margin: 0 0 10px 0; padding: 0; text-align: center; }
        .flat img { width: 100%; height: auto; border-radius: 10px; } /* Adjusted for consistent image sizing */
        .container { max-width: 800px; margin: auto; }
        .title { background-color: lightblue; border-radius: 10px; padding: 10px 20px; display: inline-block; text-align: center; margin-bottom: 20px; }
    </style>
    """

    # Generate HTML to display images within a grid layout
    flats_info = "".join([
        f"<div class='flat'><h2>{flat[0]}</h2><img src='{flat[1]}' alt='Image of {flat[0]}'></div>"
        for flat in flats
    ])

    # Close the database connection
    cursor.close()
    connection.close()

    return f"{style}<div class='title'><h1>List of Flats</h1></div><div class='container'><div class='grid'>{flats_info}</div></div>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
