from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()


def load_data():
    with open(r"d:\My-Learning\FastApi_tutorials\carsdealership.json", "r") as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {"message": "Welcome user"}


@app.get("/car/{car_id}")
def view_car(car_id: str = Path(..., description="ID of car", example="C001")):
    data = load_data()
    if car_id in data:
        return data[car_id]
    raise HTTPException(status_code=404, detail="The following code does not exist")
