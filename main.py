import uvicorn
import pandas as pd
from fastapi import Request
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse


app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/prediction")
async def predict(
        request: Request,
        month: str = Form(),
        type_van: str = Form(),
        departure: str = Form(),
        destination: str = Form()
    ) -> _TemplateResponse:

    path = "/home/timur/PycharmProjects/superset/data/rzhd_final/August22_vs_August23_with_cities.xlsx"
    df = pd.read_excel(path)
    df = df.loc[(
            (df['month'] == month) &
            (df['type_van'] == type_van) &
            (df['departure'] == departure) &
            (df['destination'] == destination)
    )]
    price_2022: float = round(df['price_2022'].item(), 1)
    price_forecast_inf: float = round(df['price_forecast_inf'].item(), 1)
    delta_price: float = round(price_forecast_inf - price_2022, 1)
    return templates.TemplateResponse("prediction.html", {
        "request": request,
        "price_2022": price_2022,
        "price_forecast_inf": price_forecast_inf,
        "delta_price": delta_price
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
