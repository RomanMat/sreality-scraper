from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)


@app.route("/")
def index():
    # Connect to the Postgresql database
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_NAME"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host="db",
        port="5432",
    )
    cur = conn.cursor()
    # Execute a query to fetch 500 items from the database
    cur.execute("SELECT title, img_url FROM appartments LIMIT 500")
    items = cur.fetchall()
    # Close the database connection
    cur.close()
    conn.close()
    # Render a template that shows the items on a page
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
