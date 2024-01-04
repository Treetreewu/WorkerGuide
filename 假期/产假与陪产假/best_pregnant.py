import datetime
import pprint

import chinese_calendar

# 从受精开始计算的妊娠过程天数。
# 来源：https://www.msdmanuals.cn/home/women-s-health-issues/normal-pregnancy/detecting-and-dating-a-pregnancy
PREGNANCY_DAYS = 266
# 提前多少天开始请假
ADVANCED_DAYS = 15


def best_holiday(days, year=None, blur=1):
    """
    计算最佳的休假日期，可能有多组结果
    :param days: 假期天数
    :param year: 今夕是何年
    :param blur: 可以接受比最优解少几天的结果
    :return: [(假期第一天, 假期最后一天，休假天数), ...]
    """
    if year is None:
        year = datetime.date.today().year
    workday_list = []
    day = datetime.date(year, 1, 1)
    while day < datetime.date(year + 2, 1, 1):
        try:
            workday_list.append(chinese_calendar.is_workday(day))
        except NotImplementedError:
            break
        day += datetime.timedelta(1)
    if len(workday_list) < days:
        # 假期太长了，建议辞职换我来干。
        return []

    total_workday = sum(workday_list[:days])
    total_workday_list = []
    for i in range(days, len(workday_list)):
        start_i = i - days
        start_date = datetime.date(year, 1, 1) + datetime.timedelta(start_i)
        if chinese_calendar.is_workday(start_date):
            # 如果开始请假的那天不是工作日，会有点怪。
            total_workday_list.append(
                (start_date, start_date + datetime.timedelta(days - 1), total_workday)
            )
        total_workday += workday_list[i] - workday_list[start_i]
    total_workday_list.sort(reverse=True, key=lambda x: x[-1])
    max_days = total_workday_list[0][-1]
    i = 0
    for i, info in enumerate(total_workday_list):
        if info[-1] < max_days - blur:
            break
    result = total_workday_list[:i]
    result.sort(key=lambda x: x[0])
    return result


def best_pregnant_date(days, year=None, blur=1):
    """
    可能的最佳怀孕日期，由于时间跨度太久，不确定因素太多，没什么实用性。
    :param days: 产假天数
    :param year: 今夕是何年
    :return: []
    """
    result = best_holiday(days, year, blur)
    pprint.pprint(result)
    pregnant_date = [
        i[0] - datetime.timedelta(PREGNANCY_DAYS + ADVANCED_DAYS)
        for i in result
    ]
    return pregnant_date


if __name__ == '__main__':
    result = best_holiday(98, 2023, 1)
    # pprint.pprint(result)
    for r in result:
        pprint.pprint((r[0].strftime("%Y-%m-%d"), r[1].strftime("%Y-%m-%d"), r[2]))
    # pprint.pprint(best_pregnant_date(98, 2023))
