import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()
my_file = THIS_FOLDER / "housing_model.pkl"

app = Flask(__name__)

model = joblib.load(my_file)

@app.route('/')
def index():
    return render_template('index.html', prediction='')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        area = float(request.form['area'])
        bedrooms = float(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        floors = float(request.form['floors'])
        parking = float(request.form['parking'])
        mainroad = request.form.get('mainroad')
        guestroom = request.form.get('guestroom')
        basement = request.form.get('basement')
        geyser = request.form.get('geyser')
        ac = request.form.get('ac')
        prefarea = request.form.get('prefarea')
        furnishingstatus = request.form.get('furnishingstatus')

        mainroad_no,mainroad_yes , guestroom_no , guestroom_yes , basement_no , basement_yes , geyser_no , geyser_yes , ac_no , ac_yes = 0,0,0,0,0,0,0,0,0,0
        prefarea_no , prefarea_yes , furnishingstatus_furnished , furnishingstatus_semi , furnishingstatus_unfur = 0,0,0,0,0

        if mainroad == 'yes':
            mainroad_yes = 1
        if guestroom == 'yes':
            guestroom_yes = 1
        if basement == 'yes':
            basement_yes = 1
        if geyser == 'yes':
            geyser_yes = 1
        if ac == 'yes':
            ac_yes = 1
        if prefarea == 'yes':
            prefarea_yes = 1
        if furnishingstatus == 'furnished':
            furnishingstatus_furnished = 1
        elif furnishingstatus == 'semi-furnished':
            furnishingstatus_semi = 1
        elif furnishingstatus == 'unfurnished':
            furnishingstatus_unfur = 1

        input_data = np.array([[area,bedrooms,bathrooms,floors,parking,mainroad_no,mainroad_yes,guestroom_no,guestroom_yes,basement_no,basement_yes,geyser_no,geyser_yes,ac_no,ac_yes,prefarea_no,prefarea_yes,furnishingstatus_furnished,furnishingstatus_semi,furnishingstatus_unfur]])
        prediction = model.predict(input_data)[0]
        rounded_prediction = round(prediction, 2)

        return render_template('index.html', prediction=f' Rs {rounded_prediction}')
    except Exception as e:
        return render_template('index.html', prediction='Error: Invalid input data')

if __name__ == '__main__':
    app.run(debug=True)