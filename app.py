from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse,RedirectResponse
from uvicorn import run as app_run
import sys
from typing import Optional

from pipelinesrc.constants import *
from pipelinesrc.pipline.prediction_pipeline import VehicleData,VehicleDataClassifier
from pipelinesrc.pipline.training_pipeline import TrainPipeline
from pipelinesrc.exception import MyException


app=FastAPI()

app.mount("/statis",StaticFiles(directory="statis"),name="static")

template=Jinja2Templates(directory="templates")
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:

    def __init__(self,request:Request):
        self.request:Request=request
        self.Gender:Optional[int]=None
        self.Age:Optional[int]=None
        self.Driving_License:Optional[int]=None
        self.Region_Code:Optional[int]=None
        self.Previously_Insured:Optional[int]=None
        self.Annual_Premium:Optional[int]=None
        self.Policy_Sales_Channel:Optional[int]=None
        self.Vintage:Optional[int]=None
        self.Vehicle_Age_1t_1_Year:Optional[int]=None
        self.Vehicle_Age_gt_2_Year:Optional[int]=None
        self.Vehicle_Damage_Yes:Optional[int]=None
    
    async def get_vehicle_data(self):

        form=await self.reques.form()
        self.Gender=form.get("Gender")
        self.Age=form.get("Age")
        self.Driving_License=form.get("Driving_License")
        self.Region_Code=form.get("Region_Code")
        self.Previously_Insured=form.get("Previously_Insured")
        self.Annual_Premium=form.get("Annual_Premium")
        self.Policy_Sales_Channel=form.get("Policy_Sales_Channel")
        self.Vintage=form.get("Vintage")
        self.Vehicle_Age_1t_1_Year=form.get("Vehicle_Age_1t_1_Year")
        self.Vehicle_Age_gt_2_Year=form.get("Vehicle_Age_gt_2_Year")
        self.Vehicle_Damage_Yes=form.get("Vehicle_Damage_Yes")

    @app.get("/",tags=["authentication"])
    async def index(request:Request):
        return template.TemplateResponse(
            "vehicledata.html",{"request":request,"context":"Redering"}
        )
    
    @app.get("/train")
    async def trainRouteClient():
        try:
            train_pipeline=TrainPipeline()
            train_pipeline.run_pipeline()
            return Response("Training Successfull")
        except Exception as e:
            raise Response(f"Error Occured:{e}")
        
    @app.post("/")
    async def predicRouteClient(request:Request):
        try:
            form=DataForm(request)
            await form.get_vehicle_data()

            vehicle_data=VehicleData(
Gender=form.Gender,
Age=form.Age,
Driving_License=form.Driving_License,
Region_Code=form.Region_Code,
Previously_Insured=form.Previously_Insured,
Annual_Premium=form.Annual_Premium,
Policy_Sales_Channel=form.Policy_Sales_Channel,
Vintage=form.Vintage,
Vehicle_Age_1t_1_Year=form.Vehicle_Age_1t_1_Year,
Vehicle_Age_gt_2_Year=form.Vehicle_Age_gt_2_Year,
Vehicle_Damage_Yes=form.Vehicle_Damage_Yes
            )


            vehicle_df=vehicle_data.get_vehicle_input_data_frame()
            model_predictor=VehicleDataClassifier()
            value=model_predictor.predict(dataframe=vehicle_df)[0]
            status="Response-Yes" if value ==1 else "Response-No" 
            return template.TemplateResponse(
                "vehicledata.html",
                {"request":request,"context":status}
            )
        except Exception as e:
           return {"status":False,"error":f"{e}"}
        

if __name__ == "__main__":
    app_run(app,host=APP_HOST,port=APP_PORT)


        