from datetime import datetime, date

today= datetime.now().date()
print(today)

def replace_year(date_obj:date, now_year:date)->date:

    try:
        date_python_format = date(date_obj.year, date_obj.month, date_obj.day)
        return date_python_format.replace(year=now_year)
    except ValueError:
        return date_python_format.replace(year=now_year, day=date_obj.day - 1)