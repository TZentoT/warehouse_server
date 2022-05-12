import datetime


class DatetimeConverter:

    def convert(self, date):
        data = ""

        try:
            print(data)
            data = datetime.date(int(data[0]), int(data[1]), int(data[2]))
        except Exception as e:
            print(f"convert went wrong: {e}")
        return data
