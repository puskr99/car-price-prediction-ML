from flask import Flask, render_template, request
import os
import numpy as np
import pickle

app = Flask(__name__)

owner_mapping = {
    'First Owner': 1,
    'Second Owner': 2,
    'Third Owner': 3,
    'Fourth & Above Owner': 4
}

car_brands = [
    "Maruti", "Skoda", "Honda", "Hyundai", "Toyota", "Ford", "Renault", 
    "Mahindra", "Tata", "Chevrolet", "Fiat", "Datsun", "Jeep", "Mercedes-Benz", 
    "Mitsubishi", "Audi", "Volkswagen", "BMW", "Nissan", "Lexus", "Jaguar", 
    "Land", "MG", "Volvo", "Daewoo", "Kia", "Force", "Ambassador", "Ashok", 
    "Isuzu", "Opel", "Peugeot"
]

owner = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]

fuel = ["Petrol", "Diesel"]

bought_year_range = [1950, 2026]

transmission = ["Manual", "Automatic"]

max_power_range = [1, 99999]

seats_range = [2, 14]

engine_cc_range = [1, 99999]

mileage_range = [1, 999]

seller_type = ['Individual', 'Dealer', 'Trustmark Dealer']


from sklearn.preprocessing import LabelEncoder, StandardScaler
car_brands_encoded = []
fuel_encoded = []
transmission_encoded = []
seller_type_encoded = []

le = LabelEncoder()
car_brands_encoded = le.fit_transform(car_brands)
fuel_encoded = le.fit_transform(fuel)
transmission_encoded = le.fit_transform(transmission)
seller_type_encoded = le.fit_transform(seller_type)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "../code/model/car_price_predictor")

predictor = pickle.load(open(model_path, 'rb'))



@app.route("/")
def index():
    return render_template(
        'index.html',
        car_brands = car_brands,
        owner = owner,
        fuel = fuel,
        bought_year_range = bought_year_range,
        transmission = transmission,
        max_power_range = max_power_range,
        seller_type = seller_type,
        mileage_range = mileage_range,
        seats_range = seats_range,
        engine_cc_range = engine_cc_range
    )


@app.route('/', methods=['GET', 'POST'])
def car_price_prediction():

    if request.method == 'POST':
        form_datas = {
            "car_brand": car_brands_encoded[car_brands.index(request.form.get("car_brand"))],
            "bought_year": request.form.get("bought_year"),
            "km_driven": request.form.get("km_driven"),
            "fuel": fuel_encoded[fuel.index(request.form.get("fuel"))],
            "seller": seller_type_encoded[seller_type.index(request.form.get("seller"))],
            "transmission": transmission_encoded[transmission.index(request.form.get("transmission"))],
            "owner": owner_mapping[request.form.get("owner")],
            "mileage": request.form.get("mileage"),
            "engine": request.form.get("engine"),
            "max_power": request.form.get("max_power"),
            "seats": request.form.get("seats"),
        }

        pred_selling_price = get_predicted_selling_price(form_datas.values())
    
    return render_template(
        'index.html',
        car_brands = car_brands,
        owner = owner,
        fuel = fuel,
        bought_year_range = bought_year_range,
        transmission = transmission,
        max_power_range = max_power_range,
        seller_type = seller_type,
        mileage_range = mileage_range,
        seats_range = seats_range,
        engine_cc_range = engine_cc_range,
        selling_price = pred_selling_price
    )


def get_predicted_selling_price(p_user_data):
    selling_price = -1

    scalar = StandardScaler()
    reshaped_array = np.array(list(p_user_data)).reshape(1, -1)
    # final_data = scalar.fit_transform(reshaped_array)
    # print(final_data)
    print(reshaped_array)
    try:
        selling_price = predictor.predict(reshaped_array)
        return np.exp(selling_price[0])
    except:
        selling_price = -1

    return selling_price


if __name__ == '__main__':
    app.run(debug=True)