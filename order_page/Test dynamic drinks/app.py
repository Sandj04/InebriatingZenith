from flask import Flask, render_template
import yaml

app = Flask(__name__)

# Load drinks data from YAML file
with open('drinks.yaml', 'r') as file:
    drinks_data = yaml.safe_load(file)

# Extract the 'drinks' list from the loaded data
drinks_list = drinks_data['drinks']

@app.route('/')
def index():
    return render_template('index.html', drinks=drinks_list)

if __name__ == '__main__':
    app.run(debug=True)