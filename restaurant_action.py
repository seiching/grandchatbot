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


def Hello():
    """Hello."""
    return (f"您好需要甚麼服務\n")


def time_change(time, sun):
    print(time, sun)
    night_time_dict = {"五點": "17:00", "六點": "18:00", "七點": "19:00", "八點": "20:00",
                       "九點": "21:00", "十點": "22:00", "五點半": "17:30", "六點半": "18:30",
                       "七點半": "19:30", "八點半": "20:30", "九點半": "21:30",
                       "十點半": "22:30"}
    lunch_time_dict = {"十一點": "11:00", "十二點": "12:00", "一點": "13:00",
                       "兩點": "14:00", "十一點半": "11:30", "十二點半": "12:30",
                       "一點半": "13:30", "兩點半": "14:30"}
    if sun.find("晚") >= 0:
        print(night_time_dict[time])
        return night_time_dict[time]
    else:
        print(lunch_time_dict[time])
        return lunch_time_dict[time]


class Action_restaurant(FormAction):
    """Action1."""
    def name(self):
        return "restaurant_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill

            Use `tracker` to request different list of slots
            depending on the state of the dialogue
        """

        return["time", "sun", "date", "num"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked

            Empty dict is converted to a mapping of
            the slot to the extracted entity with the same name
        """

        return {"time": [self.from_entity(entity="time")],
                "date": [self.from_entity(entity="date")],
                "sun": [self.from_entity(entity="sun")],
                "num": [self.from_text(intent=None)]}

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        try:
            date = tracker.get_slot("date")
            sun = tracker.get_slot("sun")
            time = tracker.get_slot("time")
            num = tracker.get_slot("num")
            num = "".join(re.findall(r'[0-9]+', num))
            
            output_sun = f""
            print(tracker.current_slot_values())
            print(num)
            date_num = re.findall(r'[0-9]+[.]*[0-9]*', date)
            if sun.find("晚") >= 0:
                output_sun = f"晚餐"
            else:
                output_sun = f"午餐"
            num_dict = {"1": "一", "2": "兩", "3": "三", "4": "四", "5": "五",
                        "6": "六",  "7": "七",  "8": "八",  "9": "九",  "10": "十"}
            sql_1 = f"SELECT * FROM restaurant_table WHERE 日期 = '2020/{date_num[0]}/{date_num[1]}' AND 時段 = '{output_sun}'"
            con = sqlite3.connect('SQL/restaurant.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            output_date = f"{date_num[0]}月{date_num[1]}日星期{rows[0][1]}"
            output_people = f"{num}人"
            ouput_time = f"{time_change(time, sun)}"
            if float(num) <= 2 and float(rows[0][3]) > 0:
                dispatcher.utter_message(f"沒問題，跟您確定一下，訂位時間: {date_num[0]}月{date_num[1]}日星期{rows[0][1]}{sun}{time}，共{num_dict[num]}位。")
            elif float(num) <= 4 and float(rows[0][4]) > 0:
                dispatcher.utter_message(f"沒問題，跟您確定一下，訂位時間: {date_num[0]}月{date_num[1]}日星期{rows[0][1]}{sun}{time}，共{num_dict[num]}位。")
            elif float(num) <= 10 and float(rows[0][5]) > 0:
                dispatcher.utter_message(f"沒問題，跟您確定一下，訂位時間: {date_num[0]}月{date_num[1]}日星期{rows[0][1]}{sun}{time}，共{num_dict[num]}位。")
            else:
                dispatcher.utter_message(f"您訂的時間沒有空位，請問要改訂別的時間麻")
                cur.close()
                con.close()
                return [AllSlotsReset()]
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()

        return[SlotSet("output_sun", output_sun if output_sun is not None else []),
               SlotSet("ouput_time", ouput_time if ouput_time is not None else []),
               SlotSet("output_people", output_people if output_people is not None else []),
               SlotSet("output_date", output_date if output_date is not None else [])]


class Action_info(FormAction):
    """Action2."""
    def name(self):
        return "info_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill

            Use `tracker` to request different list of slots
            depending on the state of the dialogue
        """

        return["name", "phone_num"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked

            Empty dict is converted to a mapping of
            the slot to the extracted entity with the same name
        """

        return {"name": [self.from_text(intent=None)],
                "phone_num": [self.from_text(intent=None)]}

    # def validate_phone(self, value, dispatcher, tracker, domain):
    #     print(tracker.slots["phone"])
    #     print(value)
    #     tracker.slots["name"] = value
    #     tracker.slots["phone"] = None
    #     print(tracker.slots["phone"])
    #     return value

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        try:
            time = tracker.get_slot("time")
            output_sun = tracker.get_slot("output_sun")
            ouput_time = tracker.get_slot("ouput_time")
            output_people = tracker.get_slot("output_people")
            output_date = tracker.get_slot("output_date")
            sun = tracker.get_slot("sun")
            name = tracker.get_slot("name")
            phone_num = tracker.get_slot("phone_num")
            print(tracker.current_slot_values())
            dispatcher.utter_message(f"好的，{output_date}{sun}{time}，共{output_people[0]}位，已為您訂位完成。")
        except Exception as e:
            logging.error(str(e))
        return[SlotSet("output_sun", output_sun if output_sun is not None else []),
               SlotSet("ouput_time", ouput_time if ouput_time is not None else []),
               SlotSet("output_people", output_people if output_people is not None else []),
               SlotSet("output_date", output_date if output_date is not None else []),
               SlotSet("name", name if name is not None else []),
               SlotSet("phone_num", phone_num if phone_num is not None else [])]


class Action_Output(Action):
    """Action3."""
    def name(self):
        return "action_output"

    def run(self, dispatcher, tracker, domain):
        try:
            output_sun = tracker.get_slot("output_sun")
            ouput_time = tracker.get_slot("ouput_time")
            output_people = tracker.get_slot("output_people")
            output_date = tracker.get_slot("output_date")
            name = tracker.get_slot("name")
            phone_num = tracker.get_slot("phone_num")
            end = tracker.get_slot("end")
            if end:
                if end.replace(" ", "") == "輸出表單":
                    dispatcher.utter_message(f"連絡人：{name.replace(' ', '')}\n"
                                             f"用餐人數：{output_people}\n"
                                             f"連絡電話：{phone_num.replace(' ', '')}\n"
                                             f"用餐日期：{output_date}\n"
                                             f"用餐時間：{ouput_time}\n"
                                             f"用餐時段：{output_sun}")
                    return [AllSlotsReset()]
        except Exception as e:
            logging.error(str(e))

        return[SlotSet("output_sun", output_sun if output_sun is not None else []),
               SlotSet("ouput_time", ouput_time if ouput_time is not None else []),
               SlotSet("output_people", output_people if output_people is not None else []),
               SlotSet("output_date", output_date if output_date is not None else []),
               SlotSet("name", name if name is not None else []),
               SlotSet("phone", phone_num if phone_num is not None else [])]


class Action_None(Action):
    """Action4."""
    def name(self):
        return "action_none"

    def run(self, dispatcher, tracker, domain):
        output_sun = tracker.get_slot("output_sun")
        ouput_time = tracker.get_slot("ouput_time")
        output_people = tracker.get_slot("output_people")
        output_date = tracker.get_slot("output_date")
        print(tracker.current_slot_values())
        print("listen")

        return[SlotSet("output_sun", output_sun if output_sun is not None else []),
               SlotSet("ouput_time", ouput_time if ouput_time is not None else []),
               SlotSet("output_people", output_people if output_people is not None else []),
               SlotSet("output_date", output_date if output_date is not None else [])]