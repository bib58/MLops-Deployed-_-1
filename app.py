import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from uvicorn import run
from src.pipeline.prediction_pipeline import (VehicleData, VehicleDataClassifier)
from fastapi.responses import Response
from src.pipeline.training_pipeline import TrainPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request = request
    async def get_vehicle_data(self):
        form = await self.request.form()

        self.Gender = int(form.get("Gender"))
        self.Age = int(form.get("Age"))
        self.Driving_License = int(form.get("Driving_License"))
        self.Region_Code = float(form.get("Region_Code"))
        self.Previously_Insured = int(form.get("Previously_Insured"))
        self.Annual_Premium = float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = float(form.get("Policy_Sales_Channel"))
        self.Vintage = int(form.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = int(form.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = int(form.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = int(form.get("Vehicle_Damage_Yes"))


@app.get("/train")
async def trainRouteClient():
    """Endpoint to initiate the model training pipeline."""
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"context": None})


@app.post("/")
async def predict(request: Request):
    try:
        form = DataForm(request)
        await form.get_vehicle_data()

        vehicle = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes,
        )

        df = vehicle.get_vehicle_input_data_frame()

        predictor = VehicleDataClassifier()

        prediction = predictor.predict(df)[0]

        result = (
            "Customer is Interested"
            if prediction == 1
            else "Customer is Not Interested"
        )

        return templates.TemplateResponse(request=request, name="index.html", context={"context": result})

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"context": f"Error: {e}"}
        )


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5000))
    run(app, host=host, port=port)
