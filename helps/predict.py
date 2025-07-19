import logging

import pandas as pd
from prophet import Prophet


class Predict:
    def __init__(self, term: int):
        """
        Get predict
        :param term:
        """
        self.term = term

    def build(self, data: list) -> list | None:
        """
        Build predict
        :param data:
        :return:
        """
        try:
            df = pd.DataFrame(data, columns=["total", "published"])
            df["published"] = pd.to_datetime(df["published"])
            df = df.groupby("published").count().reset_index()
            df.columns = ["ds", "y"]
            df = df.set_index("ds").resample("D").sum().reset_index()

            if df.empty or len(df) <= self.term:
                raise ValueError("Not enough data")
            model = Prophet()
            model.fit(df)

            future = model.make_future_dataframe(periods=self.term, freq='D')
            forecast = model.predict(future)

            last_date = df["ds"].max()
            (model.plot_components(forecast)
             .savefig("frontend/src/assets/img/predict_components.png"))
            (model.plot(forecast)
             .savefig("frontend/src/assets/img/predict_forecast.png"))
            result = forecast[forecast["ds"]
                              > last_date][
                [
                    "ds",
                    "yhat",
                    "yhat_lower",
                    "yhat_upper"
                ]]
            result["ds"] = pd.to_datetime(result["ds"]).dt.date.astype("str")
            result = result.to_numpy()
            predict = [
                {
                    "ds": el[0],
                    "yhat": el[1],
                    "yhat_lower": el[2],
                    "yhat_upper": el[3],
                } for el in result
            ]
            return predict
        except Exception as e:
            logging.error(e)
            return None
