import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None


# modeled after def predict() from the Jupyter Notebook lesson
def estimate_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))

    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    # predict price from an ML model read from a saved pickle file
    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __locations


def load_artifacts():
    print('loading saved artifacts...start')
    global __data_columns
    global __locations
    global __model

    # read from columns.json
    with open('./artifacts/columns.json', 'r') as file:
        # columns.json contains a dictionary with key='columns' and value as the list of location names
        __data_columns = json.load(file)['data_columns']
        # ignore the first 3 columns, which are: total_sqft, bath, bhk
        __locations = __data_columns[3:]

    # read from banglore_home_prices_model.pickle
    with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as file:
        __model = pickle.load(file)
    print('loading saved artifacts...done')


if __name__ == "__main__":
    load_artifacts()
    print(get_location_names())
    print(estimate_price('1st Phase JP Nagar', 1000, 3, 3))
    print(estimate_price('1st Phase JP Nagar', 1000, 2, 2))
    # the following 2 locations are in 'other'
    print(estimate_price('Kalhalli', 1000, 2, 2))
    print(estimate_price('Ejipura', 1000, 2, 2))