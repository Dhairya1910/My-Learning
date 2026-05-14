from typing import Annotated
from typing import Literal
from pydantic import Field
from typing import Optional
from typing import List
from fastapi import FastAPI, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel, field_validator, model_validator, computed_field

# -----------------------------------------------
#      basic Fastapi and pydantic tutorials     |
# -----------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class car_details(BaseModel):
    name: str
    model: str
    showroom_price: float
    manufacture_year: int
    condition: Literal["bad", "good", "excellent"]
    rarity: Literal["common", "rare", "Antique"]


def load_data():
    with open(r"D:\My-Learning\FastApi_tutorials\carsdealership.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open(r"D:\My-Learning\FastApi_tutorials\carsdealership.json", "w+") as f:
        json.dump(data, f)


@app.get("/")
def welcome():
    return {"Welcome to car dealership"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.post("/add")
def add_new_vehicle(body: dict):
    car_id, car_data = next(iter(body.items()))
    car = car_details(**car_data)
    data = load_data()
    data[car_id] = car.model_dump()
    save_data(data)
    return {"message": "Car added successfully", "car_id": car_id}


# ----------------------------------------
#           Pydantic basics             |
# ----------------------------------------

"""
Summary : 
1. field_validator : for validating a particular field
2. model_validator : for complete model validation setting, does need to be returned every time
"""


# class Car_details(BaseModel):
#     name: str
#     model: str
#     price: float
#     manufacture: int
#     available_color: List[str]
#     horsepower: int
#     uniquness: Optional[str] = None

#     # field validator example
#     @field_validator("price", mode="before")
#     @classmethod
#     def discount_coupons(cls, value):
#         if value >= 8000000.0:
#             print("50% discount on the vehicle.")
#             print(f"discounted price : {float(value * 0.50)}")
#         return value

#     # model validator example
#     @model_validator(mode="before")
#     @classmethod
#     def manufacture_year(cls, model):
#         if model["manufacture"] < 1990:
#             model["uniquness"] = "Antique"
#         else:
#             model["uniquness"] = "rare"
#         return model

#     # Computed field
#     @computed_field
#     @property
#     def final_price(self) -> float:
#         """
#         this function is used to calculate final price of vehical based on its manufacture date
#         """
#         if self.manufacture < 1990:
#             final_price = self.price * 0.20 + self.price
#         else:
#             final_price = self.price * -0.05 + self.price
#         return final_price


# def update_car_details(car: Car_details):
#     print(car.name)
#     print(car.model)
#     print(car.price)
#     print(car.available_color)
#     print(car.horsepower)
#     print(car.uniquness)
#     print(car.final_price)


# car_info = {
#     "name": "Rolls royces",
#     "model": "Phantom",
#     "manufacture": 1910,
#     "price": 10000000.0,
#     "available_color": ["red", "blue"],
#     "horsepower": 400,
# }


# rolls = Car_details(**car_info)

# update_car_details(rolls)
