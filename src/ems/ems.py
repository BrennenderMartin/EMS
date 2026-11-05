import time
import pandas as pd

class EMS:
    def __init__(self) -> None:
        self.path = f"src/ems/data/"
        self.oilbrent: pd.DataFrame = pd.read_csv(f"{self.path}oil-prices/brent-daily.csv")
        self.oilwti: pd.DataFrame = pd.read_csv(f"{self.path}oil-prices/wti-daily.csv")

    def getData(self, day):
        return (
            self.getWeather(day),
            self.getOil(day)
        )
    
    def getWeather(self, day: str) -> str:
        data: pd.DataFrame = pd.read_csv(f"{self.path}wetterdaten/City_Wetter_{day[:4]}.csv")
        return day[:4]

    def getOil(self, day: str) -> float:
        data: pd.DataFrame = pd.read_csv(f"{self.path}oil-prices/brent-monthly.csv")
        price: float = 0.0
        for i in range(len(data)):
            if data.at[i, "Date"][:8] == day[:8]: # type: ignore
                price = float(data.at[i, "Price"]) # type: ignore
        #print(data)
        return price

    def getDate(self, date):
        print(self.oilbrent.at[0, "Date"])

        # Define the date format
        date_format = "%Y-%m-%d"

        # Convert to time tuples, then to timestamps
        t1 = time.mktime(time.strptime(date, date_format))
        t2 = time.mktime(time.strptime(date, date_format))
        days = int((t2 - t1) / 86400)
        print(days, "days")

if __name__ == "__main__":
    ems = EMS()
    print(ems.getDate("2020-12-26"))
