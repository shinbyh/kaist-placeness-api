from firebase import firebase
import json

feedback = {"test":"testtest"}

db_address = "https://placenessdb3.firebaseio.com/"
fb = firebase.FirebaseApplication(db_address, None)
fb.put("/Feedback/hellp", name="123123123", data=10, params={'print': 'silent'})
    