class TimeData:
    def __init__(self, utc_edit_hours: int=0, time12: bool=True, mdy: bool=True, cdat: str=' | ', end: str='', data: bool=True, sec: bool=False):
        self.utc_edit_hours = utc_edit_hours
        self.time12 = time12
        self.mdy = mdy
        self.cdat = cdat
        self.end = end
        self.data = data
        self.sec = sec

def timedata(settings: TimeData=None, utc_edit_hours: int=0, time12: bool=True, mdy: bool=True, cdat: str=' | ', end: str='',data: bool=True,sec: bool=False):
    '''
    TimeData
    :param settings: class yelllovkitten.TimeData.TimeData
    :param utc_edit_hours: add or remove hours to utc
    :param time12: twelve-hour format
    :param mdy: date format MDY if True else YMD
    :param cdat: text between date and time
    :param end: the text at the end
    :param data: show data if True
    :param sec: show sec if True
    :return:
    '''
    if settings is not None:
        utc_edit_hours = settings.utc_edit_hours
        time12 = settings.time12
        mdy = settings.mdy
        cdat = settings.cdat
        end = settings.end
        data = settings.data
        sec = settings.sec
    import datetime
    time_now = datetime.datetime.now(datetime.timezone.utc)
    time_now = time_now + datetime.timedelta(hours=utc_edit_hours)
    if data: mdy_ymd = '%m-%d-%Y' if mdy else '%Y-%m-%d'
    else: mdy_ymd = ''
    if time12: hours_time = '%I'
    else: hours_time = '%H'
    if sec: sec_time = ':%S'
    else: sec_time = ''
    if time12: timeampm = '%p'
    else: timeampm = ''
    return time_now.strftime(f'{mdy_ymd}{cdat}{hours_time}:%M{sec_time}{timeampm}{end}')
