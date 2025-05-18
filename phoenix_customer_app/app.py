from flask import Flask, request, render_template
import phoenixdb
import phoenixdb.cursor

app = Flask(__name__)

# Phoenix Query Server URL (adjust to your env)
database_url = 'jdbc:phoenix:thin:url=https://cdpw1.cloudeka.ai:8765/default;serialization=PROTOBUF;authentication=SPNEGO;principal=cmluser@CLOUDEKA.AI;keytab=/home/nifi/cml2.keytab'
conn = phoenixdb.connect(database_url, autocommit=True)
cursor = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        cif = request.form.get("cif")
        try:
            cursor.execute("SELECT * FROM CUSTOMER.CUSTOMER_DEMOGRAPHY WHERE CIF = ?", (int(cif),))
            result = cursor.fetchone()
            if result:
                colnames = [desc[0] for desc in cursor.description]
                data = dict(zip(colnames, result))
        except Exception as e:
            data = {"error": str(e)}
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)


