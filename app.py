from flask import Flask, render_template, request, jsonify
import sqlite3
import io
import contextlib

app = Flask(__name__)

# Execute Python code
@app.route('/run_python', methods=['POST'])
def run_python():
    code = request.json.get('code')
    output = io.StringIO()  # Capture output
    try:
        with contextlib.redirect_stdout(output):
            exec(code)  # Executing the Python code
        result = output.getvalue()
    except Exception as e:
        result = str(e)
    return jsonify({"output": result})

# Execute SQL query
@app.route('/run_sql', methods=['POST'])
def run_sql():
    query = request.json.get('query')
    conn = sqlite3.connect(':memory:')  # In-memory SQLite DB
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        if query.lower().startswith('select'):
            result = cursor.fetchall()
            return jsonify({"output": result})
        else:
            return jsonify({"output": "Query executed successfully"})
    except Exception as e:
        return jsonify({"output": str(e)})
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
