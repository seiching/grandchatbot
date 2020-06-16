# !/usr/bin/env python
# -*-coding: utf-8 -*-
"""This is View action script."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
# from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import SlotSet
# from rasa_core_sdk.executor import CollectingDispatcher
import sqlite3
import logging


def Hello():
    """Hello."""
    return (f"您好需要甚麼服務\n")


class Action_travel(Action):
    """Action1."""
    def name(self):
        return "action_travel"

    def run(self, dispatcher, tracker, domain):
        child = tracker.get_slot("child")
        # play = tracker.get_slot("play")
        pray = tracker.get_slot("pray")
        climb = tracker.get_slot("climb")
        shower = tracker.get_slot("shower")
        # older = tracker.get_slot("older")
        area = tracker.get_slot("area")
        family = f""
        sql = f""
        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
        # print(tracker.get_slot("family"))
            if child:
                family = f"親子共遊"
                tracker.slots["family"] = family
                sql = f"SELECT * FROM view_info WHERE 地區 = '{area}' AND 親子共遊 = '有'"
                tracker.slots["sql"] = sql
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"您好，{area}「親子共遊」推薦景點如下:")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
            elif pray:
                sql = f"SELECT * FROM view_info WHERE 地區 = '{area}' AND 寺廟祈福 = '有'"
                tracker.slots["sql"] = sql
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"您好，{area}「寺廟祈福」推薦景點如下:")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
            elif climb:
                sql = f"SELECT * FROM view_info WHERE 地區 = '{area}' AND 登山步道 = '有'"
                tracker.slots["sql"] = sql
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"您好，{area}「登山步道」推薦景點如下:")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
            elif shower:
                sql = f"SELECT * FROM view_info WHERE 地區 = '{area}' AND 溫泉好湯 = '有'"
                tracker.slots["sql"] = sql
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"您好，{area}「溫泉好湯」推薦景點如下:")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return [SlotSet("area", area if area is not None else []),
                SlotSet("pray", pray if pray is not None else []),
                SlotSet("climb", climb if climb is not None else []),
                SlotSet("shower", shower if shower is not None else []),
                SlotSet("family", family if family is not None else []),
                SlotSet("sql", sql if sql is not None else [])]


class Action_view(Action):
    """Action2."""
    def name(self):
        return "action_view"

    def run(self, dispatcher, tracker, domain):
        mountain = tracker.get_slot("mountain")
        family = tracker.get_slot("family")
        spring = tracker.get_slot("spring")
        temple = tracker.get_slot("temple")
        area = tracker.get_slot("area")
        shower = tracker.get_slot("shower")
        pray = tracker.get_slot("pray")
        climb = tracker.get_slot("climb")
        sql = tracker.get_slot("sql")
        key_words = sql.split("AND")[1].split()[0]

        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
            if mountain and not climb:
                sql = f"{sql} AND 登山步道 = '有'"
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"{area}有登山步道的「{key_words}」推薦景點如下:\n")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
                    tracker.slots["city"] = data[1]
                    city = tracker.get_slot("city")
            elif spring and not shower:
                sql = f"{sql} AND 溫泉好湯 = '有'"
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"{area}有溫泉好湯的「{key_words}」推薦景點如下:\n")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
                    tracker.slots["city"] = data[1]
                    city = tracker.get_slot("city")
            elif temple and not pray:
                sql = f"{sql} AND 寺廟祈福 = '有'"
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"{area}有寺廟祈福的「{key_words}」推薦景點如下:\n")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
                    tracker.slots["city"] = data[1]
                    city = tracker.get_slot("city")
            elif family:
                sql = f"{sql} AND 親子共遊 = '有'"
                cur.execute(sql)
                rows = cur.fetchall()
                dispatcher.utter_message(f"{area}有登山步道的「{key_words}」推薦景點如下:\n")
                for data in rows:
                    dispatcher.utter_message(f"{data[1]} {data[2]}\n")
                    tracker.slots["city"] = data[1]
                    city = tracker.get_slot("city")

        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()

        return [SlotSet("mountain", mountain if mountain is not None else []),
                SlotSet("family", family if family is not None else []),
                SlotSet("spring", spring if spring is not None else []),
                SlotSet("temple", temple if temple is not None else []),
                SlotSet("area", area if area is not None else []),
                SlotSet("sql", sql if sql is not None else []),
                SlotSet("city", city if city is not None else [])]


class Action_Weather(Action):
    """Action3."""
    def name(self):
        return "action_Weather"

    def run(self, dispatcher, tracker, domain):
        date = tracker.get_slot("date")
        city = tracker.get_slot("city")

        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
            cur.execute(f"SELECT * from view_weather WHERE 縣市 = '{city}'")
            rows = cur.fetchall()
            for data in rows:
                if date.find("5") >= 0:
                    dispatcher.utter_message(f"12月5日，根據中央氣象局資料，當天天氣可能有{data[2]}\n")
                    tracker.slots["weather"] = data[2]
                    weather = tracker.get_slot("weather")
                elif date.find("6") >= 0:
                    dispatcher.utter_message(f"12月5日，根據中央氣象局資料，當天天氣可能有{data[3]}\n")
                    tracker.slots["weather"] = data[3]
                    weather = tracker.get_slot("weather")
                elif date.find("7") >= 0:
                    dispatcher.utter_message(f"12月5日，根據中央氣象局資料，當天天氣可能有{data[4]}\n")
                    tracker.slots["weather"] = data[4]
                    weather = tracker.get_slot("weather")
                elif date.find("8") >= 0:
                    dispatcher.utter_message(f"12月5日，根據中央氣象局資料，當天天氣可能有{data[5]}\n")
                    tracker.slots["weather"] = data[5]
                    weather = tracker.get_slot("weather")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()

        return [SlotSet("date", date if date is not None else []),
                SlotSet("weather", weather if weather is not None else []),
                SlotSet("city", city if city is not None else []),
                SlotSet("mountain", []),
                SlotSet("family", []),
                SlotSet("spring", []),
                SlotSet("temple", [])]


class Action_itinerary(Action):
    """Action4."""
    def name(self):
        return "action_itinerary"

    def run(self, dispatcher, tracker, domain):
        mountain = tracker.get_slot("mountain")
        family = tracker.get_slot("family")
        spring = tracker.get_slot("spring")
        temple = tracker.get_slot("temple")
        easy_use = tracker.get_slot("easy_use")
        inside = tracker.get_slot("inside")
        city = tracker.get_slot("city")
        date = tracker.get_slot("date")
        weather = tracker.get_slot("weather")
        sql = f"SELECT * FROM view_info WHERE 縣市 = '{city}'"
        conditions = []

        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
            for i in [mountain, family, spring, temple, easy_use, inside]:
                if i:
                    conditions.append(i)
                    sql = f"{sql} AND {i.replace(' ','')} = '有'"
            print(sql)
            cur.execute(sql)
            rows = cur.fetchall()
            dispatcher.utter_message(f"{city}{conditions[0].replace(' ','')}且具備"
                                     f"{conditions[1].replace(' ','')}設施景點，推薦")
            for data in rows:
                dispatcher.utter_message(f"{data[2]}\n")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return [SlotSet("city", city if city is not None else []),
                SlotSet("date", date if date is not None else []),
                SlotSet("weather", weather if weather is not None else [])]


class Action_phone(Action):
    """Action5."""
    def name(self):
        return "action_phone"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location").replace(" ", "")
        date = tracker.get_slot("date")
        weather = tracker.get_slot("weather")
        city = tracker.get_slot("city")
        phone = f""
        tracker.slots["phone"] = phone
        sql = f"SELECT * from view_info WHERE 景點 = '{location}'"
        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for data in rows:
                phone = data[4]
                tracker.slots["phone"] = phone
                dispatcher.utter_message(f"{location}的連絡電話是：{data[4]}")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()

        return [SlotSet("location", location if location is not None else []),
                SlotSet("date", date if date is not None else []),
                SlotSet("weather", weather if weather is not None else []),
                SlotSet("city", city if city is not None else []),
                SlotSet("phone", phone if phone is not None else [])]


class Action_Where(Action):
    """Action6."""
    def name(self):
        return "action_Where"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        date = tracker.get_slot("date")
        weather = tracker.get_slot("weather")
        city = tracker.get_slot("city")
        phone = tracker.get_slot("phone")
        address = tracker.get_slot("address")
        sql = f"SELECT * from view_info WHERE 景點 = '{location}'"
        try:
            con = sqlite3.connect('SQL/view.db')
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for data in rows:
                address = data[3]
                tracker.slots["address"] = address
                dispatcher.utter_message(f"{address}")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()
        return [SlotSet("location", location if location is not None else []),
                SlotSet("date", date if date is not None else []),
                SlotSet("weather", weather if weather is not None else []),
                SlotSet("city", city if city is not None else []),
                SlotSet("address", address if address is not None else []),
                SlotSet("phone", phone if phone is not None else [])]


class Action7(Action):
    """Action7."""
    def name(self):
        return "action_output"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        date = tracker.get_slot("date")
        weather = tracker.get_slot("weather")
        city = tracker.get_slot("city")
        address = tracker.get_slot("address")
        phone = tracker.get_slot("phone")
        end = tracker.get_slot("end")
        print(tracker.current_slot_values())
        if end:
            if end.replace(" ", "") == "輸出表單":
                dispatcher.utter_template(tracker=tracker, template="utter_output")
                return [SlotSet("location", []),
                        SlotSet("date", []),
                        SlotSet("weather", []),
                        SlotSet("city", []),
                        SlotSet("address", []),
                        SlotSet("phone", []),
                        SlotSet("area", []),
                        SlotSet("child", []),
                        SlotSet("easy_use", []),
                        SlotSet("family", []),
                        SlotSet("inside", []),
                        SlotSet("sql", []),
                        SlotSet("temple", [])]

        return [SlotSet("location", location if location is not None else []),
                SlotSet("date", date if date is not None else []),
                SlotSet("weather", weather if weather is not None else []),
                SlotSet("city", city if city is not None else []),
                SlotSet("address", address if address is not None else []),
                SlotSet("phone", phone if phone is not None else [])]
