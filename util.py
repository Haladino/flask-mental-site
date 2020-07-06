from datetime import date, timedelta


def current_weekdays():
    days_hu = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
    today = date.today()
    week_no = today.weekday()
    monday = today - timedelta(days=week_no)
    return {days_hu[i]: monday + timedelta(days=i) for i in range(7)}
