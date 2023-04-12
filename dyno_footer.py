from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# HTML code
<footer>
  &copy; {{ current_year }}
</footer>