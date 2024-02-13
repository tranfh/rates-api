from libs.rates.dto import number_to_days_mapping, Rate


class RateOutput:
    def __init__(self, days: str, times: str, timezone: str, price: int):
        """
        Initialize a RateOutput object with the specified attributes.

        Parameters:
            days (str): A string representing the days of the week.
            times (str): A string representing the time interval.
            timezone (str): A string representing the timezone.
            price (int): An integer representing the price.

        Returns:
            RateOutput: A RateOutput object with the specified attributes.
        """
        self.days = days
        self.times = times
        self.timezone = timezone
        self.price = price

    @classmethod
    def from_model(cls, rate: Rate) -> 'RateOutput':
        """
        Convert a Rate object into a RateOutput object.

        Parameters:
            rate (Rate): The Rate object to convert.

        Returns:
            RateOutput: The converted RateOutput object.
        """
        start_time_str = f"{rate.period.start:04d}"
        end_time_str = f"{rate.period.end:04d}"
        interval_str = f"{start_time_str}-{end_time_str}"
        days = ','.join([number_to_days_mapping[day] for day in rate.days_of_week])

        return RateOutput(days=days, times=interval_str, timezone=rate.timezone, price=rate.price)

    def to_json(self) -> dict:
        """
        Convert the RateOutput object into a dictionary in JSON format.

        Returns:
            dict: A dictionary containing the RateOutput attributes in JSON format.
        """
        return {
            "days": self.days,
            "price": self.price,
            "times": self.times,
            "tz": self.timezone
        }