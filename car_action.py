# !/usr/bin/env python
# -*-coding: utf-8 -*-
"""This is View action script."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction
# from rasa_core_sdk.executor import CollectingDispatcher
import sqlite3
import logging
import re


class Action_car(FormAction):
    """Action1."""
    def name(self):
        return "car_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""

        return ["date", "num", "car", "name", "start_time",
                "carname"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked

            Empty dict is converted to a mapping of
            the slot to the extracted entity with the same name
        """

        return {"name": [self.from_text(intent="name")],
                "start_time": [self.from_entity(entity="time")],
                "carname": [self.from_entity(entity="carname")]}

    def validate_name(self, value, dispatcher, tracker, domain):
        data = tracker.get_slot("data")
        date = tracker.get_slot("date")
        sql_1 = f"SELECT * FROM car_store"
        try:
            con = sqlite3.connect('SQL/car.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            data = (f"{value}您好\n跟您確認一下，請問您{date[0]}要幾點取車？要在哪一間分店取車？分店資訊參考如下：\n"
                    f"1. {rows[0][1]} ({rows[0][2]})\n"
                    f"2. {rows[1][1]} ({rows[1][2]})。")

            tracker.slots["data"] = data
            # print(tracker.get_slot("data"))
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return value

    def validate_start_time(self, value, dispatcher, tracker, domain):
        data = tracker.get_slot("data")
        date = tracker.get_slot("date")
        sun = tracker.get_slot("sun")
        location = tracker.get_slot("location")
        car = tracker.get_slot("car")
        time = tracker.get_slot("time")
        tracker.slots["start_sun"] = sun
        tracker.slots["start_location"] = location
        date_num = re.findall(r'[0-9]+[.]*[0-9]*', date[0])
        sql_1 = f"SELECT * FROM car_storage WHERE 日期 = '2020/{date_num[0]}/{date_num[1]}' AND 所在分店 = '{location}' AND 類型 = '{car}' AND 數量 > 0"
        try:
            con = sqlite3.connect('SQL/car.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            car_num = len(rows)
            num_dict = {1: "一", 2: "兩", 3: "三", 4: "四", 5: "五",
                        6: "六",  7: "七",  8: "八",  9: "九", 10: "十"}
            if car_num == 1:
                sql_2 = f"SELECT * FROM car_price WHERE 車款 = '{rows[0][3]}'"
                data = f"好的，經查詢後，{date[0]}{sun}{time}於{location}尚有「{rows[0][3]}」{num_dict[car_num]}款客車，詳細資訊如下：\n"
            else:
                data = f"好的，經查詢後，{date[0]}{sun}{time}於{location}尚有「{rows[0][3]}」"
                sql_2 = f"SELECT * FROM car_price WHERE 車款 = '{rows[0][3]}'"
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    sql_2 = sql_2 + f" OR 車款 = '{row[3]}'"
                    data = data + f"及「{row[3]}」"
                data = data + f"{num_dict[car_num]}款客車，請問您要哪一款？詳細資訊如下：\n"
                # print(data)
            cur.execute(sql_2)
            rows = cur.fetchall()
            for i, row in enumerate(rows):
                data = data + f"{i+1}. {row[0]}的廠牌為{row[1]}、平日價格為{row[3]}元/日，假日價格為 {row[4]}元/日"
                if car_num == 1:
                    data = data + f"。"
                elif i < car_num-1:
                    data = data + f";\n"
                else:
                    data = data + f"。"
            # print(data)
            tracker.slots["data"] = data
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return value

    def validate_carname(self, value, dispatcher, tracker, domain):
        sun = tracker.get_slot("sun")
        location = tracker.get_slot("location")
        data_return = tracker.get_slot("data_return")
        date = tracker.get_slot("date")
        tracker.slots["start_sun"] = sun
        tracker.slots["start_location"] = location
        sql_1 = f"SELECT * FROM car_store"
        try:
            con = sqlite3.connect('SQL/car.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            data_return = (f"好的，跟您確認一下，{date[1]}還車的時間及地點為？\n"
                           f"分店資訊參考如下：\n"
                           f"1.	{rows[0][1]} ({rows[0][2]})\n"
                           f"2.	{rows[1][1]} ({rows[1][2]})。")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        tracker.slots["data_return"] = data_return
        print(tracker.current_slot_values())

        return value

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        print(tracker.current_slot_values())
        date = tracker.get_slot("date")
        # time = tracker.get_slot("time")
        # sun = tracker.get_slot("sun")
        # location = tracker.get_slot("location")
        car = tracker.get_slot("car")
        name = tracker.get_slot("name")
        start_sun = tracker.get_slot("start_sun")
        start_time = tracker.get_slot("start_time")
        start_location = tracker.get_slot("start_location")
        carname = tracker.get_slot("carname")
        data_return = tracker.get_slot("data_return")
        return [SlotSet("date", date if date is not None else []),
                SlotSet("car", car if car is not None else []),
                SlotSet("name", name if name is not None else []),
                SlotSet("start_sun", start_sun if start_sun is not None else []),
                SlotSet("start_time", start_time if start_time is not None else []),
                SlotSet("start_location", start_location if start_location is not None else []),
                SlotSet("carname", carname if carname is not None else []),
                SlotSet("data_return", data_return if data_return is not None else [])]


class Action_car2(FormAction):
    """Action1."""
    def name(self):
        return "car2_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""

        return ["end_time", "phone"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked

            Empty dict is converted to a mapping of
            the slot to the extracted entity with the same name
        """

        return {"end_time": [self.from_entity(entity="time")],
                "phone": [self.from_entity(entity="phone")]}

    def validate_end_time(self, value, dispatcher, tracker, domain):
        sun = tracker.get_slot("sun")
        location = tracker.get_slot("location")
        tracker.slots["end_sun"] = sun
        tracker.slots["end_location"] = location
        return value

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        print(tracker.current_slot_values())
        sun = tracker.get_slot("sun")
        location = tracker.get_slot("location")
        tracker.slots["end_sun"] = sun
        tracker.slots["end_location"] = location
        date = tracker.get_slot("date")
        car = tracker.get_slot("car")
        name = tracker.get_slot("name")
        start_sun = tracker.get_slot("start_sun")
        start_time = tracker.get_slot("start_time")
        start_location = tracker.get_slot("start_location")
        carname = tracker.get_slot("carname")
        end_time = tracker.get_slot("end_time")
        end_sun = tracker.get_slot("end_sun")
        end_location = tracker.get_slot("end_location")
        phone = tracker.get_slot("phone")
        print(tracker.current_slot_values())
        rent_price = 0
        sql_1 = f"SELECT * FROM car_price WHERE 車款 = '{carname}'"
        sql_2 = f"SELECT * FROM car_days"
        try:
            con = sqlite3.connect('SQL/car.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            Weekday_price = rows[0][3]
            holiday_price = rows[0][4]
            cur.execute(sql_2)
            rows = cur.fetchall()
            start = 0
            for row in rows:
                if row[0].find(date[0]) >= 0:
                    start = 1
                elif row[0].find(date[1]) >= 0:
                    if row[1] == "假日":
                        rent_price = rent_price + holiday_price
                    else:
                        rent_price = rent_price + Weekday_price
                    break
                if start:
                    if row[1] == "假日":
                        rent_price = rent_price + holiday_price
                    else:
                        rent_price = rent_price + Weekday_price
            print(rent_price)
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return [SlotSet("date", date if date is not None else []),
                SlotSet("car", car if car is not None else []),
                SlotSet("name", name if name is not None else []),
                SlotSet("start_sun", start_sun if start_sun is not None else []),
                SlotSet("start_time", start_time if start_time is not None else []),
                SlotSet("start_location", start_location if start_location is not None else []),
                SlotSet("carname", carname if carname is not None else []),
                SlotSet("end_time", end_time if end_time is not None else []),
                SlotSet("phone", phone if phone is not None else []),
                SlotSet("end_sun", end_sun if end_sun is not None else []),
                SlotSet("end_location", end_location if end_location is not None else []),
                SlotSet("rent_price", rent_price if rent_price is not None else [])]


class Action_Output(Action):
    """Action2."""
    def name(self):
        return "action_output"

    def run(self, dispatcher, tracker, domain):
        night_time_dict = {"五點": "17:00", "六點": "18:00", "七點": "19:00", "八點": "20:00",
                           "九點": "21:00", "十點": "22:00"}
        morning_time_dict = {"五點": "5:00", "六點": "6:00", "七點": "7:00", "八點": "8:00",
                             "九點": "9:00", "十點": "10:00", "十一點": "11:00", "十二點": "12:00"}
        try:
            date = tracker.get_slot("date")
            # num = tracker.get_slot("num")
            car = tracker.get_slot("car")
            name = tracker.get_slot("name")
            start_sun = tracker.get_slot("start_sun")
            start_time = tracker.get_slot("start_time")
            start_location = tracker.get_slot("start_location")
            carname = tracker.get_slot("carname")
            end_sun = tracker.get_slot("end_sun")
            end_time = tracker.get_slot("end_time")
            end_location = tracker.get_slot("end_location")
            phone = tracker.get_slot("phone")
            rent_price = tracker.get_slot("rent_price")
            end = tracker.get_slot("end")
            if end:
                if end.replace(" ", "") == "輸出表單":
                    if start_sun.find("晚上") >= 0:
                        num_start_time = night_time_dict[start_time]
                    else:
                        num_start_time = morning_time_dict[start_time]
                    if end_sun.find("晚上") >= 0:
                        num_end_time = night_time_dict[end_time]
                    else:
                        num_end_time = morning_time_dict[end_time]
                    dispatcher.utter_message(f"訂購人：{name}\n"
                                             f"連絡電話：{phone.replace(' ', '')}\n"
                                             f"訂購車款：{carname}\n"
                                             f"取車時間：{date[0]}，{num_start_time}\n"
                                             f"取車地點：平安租車-{start_location}\n"
                                             f"還車時間：{date[1]}，{num_end_time}\n"
                                             f"還車地點：平安租車-{end_location}\n"
                                             f"價格：{rent_price}元")
                    return [AllSlotsReset()]
        except Exception as e:
            logging.error(str(e))

        return [SlotSet("date", date if date is not None else []),
                SlotSet("car", car if car is not None else []),
                SlotSet("name", name if name is not None else []),
                SlotSet("start_sun", start_sun if start_sun is not None else []),
                SlotSet("start_time", start_time if start_time is not None else []),
                SlotSet("start_location", start_location if start_location is not None else []),
                SlotSet("carname", carname if carname is not None else []),
                SlotSet("end_sun", end_sun if end_sun is not None else []),
                SlotSet("end_time", end_time if end_time is not None else []),
                SlotSet("end_location", end_location if end_location is not None else []),
                SlotSet("phone", phone if phone is not None else []),
                SlotSet("rent_price", rent_price if rent_price is not None else [])]
