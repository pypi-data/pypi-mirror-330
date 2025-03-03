import uuid
import datetime
import calendar


def ConvertDateUTCtoStringITC(date_input_time, tz_minute, dinhdang="%H:%M %d/%m/%Y"):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc.strftime(dinhdang)
    except:
        return ""


def convert_date_to_format(vNgayThang, format="%Y%m%d%H%M%S"):
    try:
        if vNgayThang is not None:
            return vNgayThang.strftime(format)
        else:
            return ""
    except:
        return ""


def convert_str_to_date(date_str, format="%Y%m%d%H%M%S"):
    try:
        return datetime.datetime.strptime(date_str, format).replace(
            tzinfo=datetime.timezone.utc
        )
    except:
        return None


def get_utc_now():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return now


def convert_timestamp_to_date_utc(timestamp):
    try:
        if timestamp is not None:
            return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).replace(
                tzinfo=datetime.timezone.utc
            )
        else:
            return None
    except:
        return None


def convert_date_utc_to_date_itc(date_input_time, tz_minute):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc
    except:
        return None


def convert_date_to_timestamp(vNgayThang):
    try:
        if vNgayThang is not None:
            return round(vNgayThang.replace(tzinfo=datetime.timezone.utc).timestamp())
        else:
            return None
    except:
        return None


def convert_date_ict_to_date_utc(d_ict, tz_minute):
    return d_ict - datetime.timedelta(minutes=tz_minute)


def generate_uuid():
    return str(uuid.uuid1())


class ExtractLicenseLifeCycle:
    """
    - Tryền vào thời gian đầu chu kì và cuối chu kì
    Param:
    - start_time: Thời gian start gói
    - end_time: Thời gian expire. Nếu không truyền lên tự động đi tìm end_time là cuối chu kì
    - period: (chi kì: int, thời gian đầu chi kì: timestamp, thời gian cuối chu kì: timestamp)
    """

    def __init__(self, start_time: int, end_time: int = 0):
        self.start_time = start_time
        self.end_time = end_time
        self.periods = []
        self.time_zone = 420
        self.calculater_add_time_zone()

    def calculater_add_time_zone(self):
        if not self.end_time:
            start_time = self.get_dt(self.start_time)
            # TODO: Check năm sau có ngày 29/2 hay không?
            year = start_time.year
            month = start_time.month
            day = start_time.day
            expire_year = year + 1
            if month == 2 and day == 29:
                expire_day = 28
            else:
                expire_day = day
            self.end_time = self.get_timestamp(start_time.replace(year=expire_year, day=expire_day))

    def generate_period(self):
        start_time = self.get_dt(self.start_time)
        start_day = start_time.day

        self.periods = []

        current_time = self.start_time
        number_of_cycle = 0

        while current_time < self.end_time:
            extract_current_time = self.get_dt(current_time)
            # print('extract_current_time: ', extract_current_time)

            current_year = extract_current_time.year
            current_month = extract_current_time.month
            # print('current_year, current_month: ', current_year, current_month)

            # Tìm tháng hiện tại để tính tính tháng tiếp theo
            if current_month == 12:
                # next_time = extract_current_time.replace(current_year + 1, 1)
                current_year = current_year + 1
                current_month = 1
            else:
                # next_time = extract_current_time.replace(month=current_month + 1)
                current_month = current_month + 1

            # Từ tháng tiếp theo tìm ngày kết thúc của chu kì
            day_of_next_month = self.length_of_month(current_year, current_month)
            if start_day < day_of_next_month:
                day = start_day
            else:
                day = day_of_next_month

            next_time = self.get_timestamp(extract_current_time.replace(current_year, current_month, day=day))

            number_of_cycle += 1

            # print('chu kì', number_of_cycle, 'start: ',
            #       DateTool(timestamp=current_time).convert_timestamp_to_format(), 'end: ',
            #       DateTool(timestamp=next_time).convert_timestamp_to_format())
            self.periods.append((number_of_cycle, current_time, next_time))
            current_time = next_time

    @staticmethod
    def length_of_month(year, month):
        return calendar.monthrange(year, month)[1]

    def get_dt(self, time_stamp):
        # return datetime.fromtimestamp(time)
        d_utc = convert_timestamp_to_date_utc(time_stamp)
        return convert_date_utc_to_date_itc(d_utc, self.time_zone)

    def get_timestamp(self, date_ict):
        d_utc = convert_date_ict_to_date_utc(date_ict, self.time_zone)
        return convert_date_to_timestamp(d_utc)

    def get_period_from_time(self, times_check):
        for item in self.periods:
            ck, start, end = item
            if start < times_check < end:
                return start, end
        return None, None

    def get_period_settlement_from_time(self, times_check):
        # TODO: miss case hai khoảng thời gian gần nhau
        # chua toi thoi han license
        if times_check <= self.periods[0][1]:
            return None, None
        if times_check > self.periods[-1][2]:
            return self.periods[-1][1], self.periods[-1][2]
        period_index = 0
        for index, item in enumerate(self.periods):
            ck, start, end = item
            if start < times_check < end:
                period_index = index
        if period_index > 0:
            period_index -= 1
            return self.periods[period_index][1], self.periods[period_index][2]
        return None, None

    def get_cycle_less_than_time_input(self, time_check):
        list_cycle_less_than_now = list(filter(lambda x: x[2] <= time_check, self.periods))
        return list_cycle_less_than_now

    def get_expire_time_for_module_free(self):
        start_time = self.get_dt(self.start_time)

        year = 2100
        month = start_time.month
        day = start_time.day
        if month == 2 and day == 29:
            expire_day = 28
        else:
            expire_day = day
        self.end_time = self.get_timestamp(start_time.replace(year=year, day=expire_day))

    def get_start_time_by_expire_time(self):
        if not self.start_time:
            end_time = self.get_dt(self.end_time)
            # TODO: Check năm sau có ngày 29/2 hay không?
            year = end_time.year
            month = end_time.month
            day = end_time.day
            expire_year = year - 1
            if month == 2 and day == 28:
                start_day = 29
            else:
                start_day = day
            self.start_time = self.get_timestamp(end_time.replace(year=expire_year, day=start_day))

    def get_expire_time_add_gift_month(self, number_month_gift: int):
        start_time = self.get_dt(self.start_time)
        # TODO: Check năm sau có ngày 29/2 hay không?
        year = start_time.year
        month = start_time.month + number_month_gift
        number_year = 1
        while month > 12:
            number_year += 1

            month = month - 12

        expire_year = year + number_year
        day = start_time.day
        if month == 2 and day == 29:
            expire_day = 28
        else:
            expire_day = day
        self.end_time = self.get_timestamp(start_time.replace(year=expire_year, day=expire_day, month=month))

    def get_time_range_from_date(self, date_check):
        date_check_ict = convert_date_utc_to_date_itc(date_check, self.time_zone)
        current_year = date_check_ict.year
        current_month = date_check_ict.month
        current_day = date_check_ict.day

        start_time = self.get_dt(self.start_time)
        start_day = start_time.day

        if start_day > current_day:
            if current_month == 1:
                start_year = current_year - 1
                start_month = 12
            else:
                start_year = current_year
                start_month = current_month - 1
        else:
            start_year = current_year
            start_month = current_month
        day_of_start_month = self.length_of_month(start_year, start_month)
        if start_day >= day_of_start_month:
            start_day = day_of_start_month

        if start_month == 12:
            next_year = start_year + 1
            next_month = 1
        else:
            next_year = start_year
            next_month = start_month + 1

        day_of_next_month = self.length_of_month(next_year, next_month)
        if start_day < day_of_next_month:
            next_day = start_day
        else:
            next_day = day_of_next_month

        start_cycle = self.get_timestamp(start_time.replace(start_year, start_month, day=start_day))
        end_cycle = self.get_timestamp(start_time.replace(next_year, next_month, day=next_day))

        return start_cycle, end_cycle


if __name__ == '__main__':
    # , end_time=1711904400
    a = ExtractLicenseLifeCycle(start_time=1706720400, end_time=1706720400)
    # a.generate_period()
    # print(a.periods)
    # for item in a.periods:
    #     ck, start, end = item
    #     # start = datetime.datetime.fromtimestamp(start, tz=datetime.timezone.utc)
    #     # end = datetime.datetime.fromtimestamp(end, tz=datetime.timezone.utc)
    #     start = convert_timestamp_to_date_utc(start)
    #     end = convert_timestamp_to_date_utc(end)
    #     print('chu kì', ck, 'start: ', start, 'end: ', end)
    start_cycle, end_cycle = a.get_time_range_from_date(get_utc_now())
    print('start: ', start_cycle, 'end: ', end_cycle)