import os
from flask import Flask, request, render_template
import phoenixdb
import phoenixdb.cursor
from datetime import datetime

# Explicit absolute path to your project directory
BASE_DIR = "/home/cdsw/phoenix_customer_app"

# Create Flask app with correct template/static folder references
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# Phoenix Query Server via Knox Gateway
DATABASE_URL = 'https://cdpm1.cloudeka.ai:8443/gateway/cdp-proxy-api/avatica'
PHOENIX_USER = 'cmluser'
PHOENIX_PASSWORD = 'hwj5GpM8rVgy'

# Utility function to create a new connection + cursor
def get_cursor():
    conn = phoenixdb.connect(
        DATABASE_URL,
        autocommit=True,
        authentication='BASIC',
        avatica_user=PHOENIX_USER,
        avatica_password=PHOENIX_PASSWORD
    )
    return conn.cursor()

# Format milliseconds to readable dates
def format_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d")
    except:
        return ts

# Root route: render the form and show results
@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        cif = request.form.get("cif")
        try:
            cursor = get_cursor()
            cursor.execute("SELECT * FROM CUSTOMER.CUSTOMER_DEMOGRAPHY WHERE CIF = ?", (int(cif),))
            result = cursor.fetchone()
            if result:
                colnames = [desc[0] for desc in cursor.description]
                data = dict(zip(colnames, result))
                for field in ["BIRTHDATE", "OPENDATE", "VALUATION_DATE"]:
                    if field in data and data[field]:
                        data[field] = format_timestamp(data[field])
            else:
                data = {"error": f"No record found for CIF {cif}"}
        except Exception as e:
            data = {"error": str(e)}
    return render_template("index.html", data=data)

# Start the app in CML environment
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_APP_PORT"]))