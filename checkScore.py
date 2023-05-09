import time

while True:
    time.sleep(1)
    import os
    import pickle

    if os.path.exists("total.pkl"):
        with open("total.pkl", "rb") as f:
            number = pickle.load(f)

    else:
        number = 0

    print(number)
