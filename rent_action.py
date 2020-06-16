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


class Action_rent(FormAction):
    """Action1."""
    def name(self):
        return "rent_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill

            Use `tracker` to request different list of slots
            depending on the state of the dialogue
        """

        return["name", "occupation", "old", "income",
               "h_price", "self_rent", "predict_rent"]

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
                "occupation": [self.from_entity(entity="occupation")],
                "old": [self.from_entity(entity="old")],
                "income": [self.from_entity(entity="income")],
                "h_price": [self.from_entity(entity="price")],
                "self_rent": [self.from_entity(entity="price")],
                "predict_rent": [self.from_entity(entity="price")]}

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        try:
            name = tracker.get_slot("name")
            occupation = tracker.get_slot("occupation")
            old = tracker.get_slot("old")
            income = tracker.get_slot("income")
            h_price = tracker.get_slot("h_price")
            self_rent = tracker.get_slot("self_rent")
            predict_rent = tracker.get_slot("predict_rent")
            income_num = re.findall(r'[0-9]+[.]*[0-9]*', income)[0]
            predict_rent_num = re.findall(r'[0-9]+[.]*[0-9]*', predict_rent)[0]
            h_price_num = re.findall(r'[0-9]+[.]*[0-9]*', h_price)[0]
            old_num = re.findall(r'[0-9]+[.]*[0-9]*', old)[0]
            score = 0
            sql_1 = f"SELECT * FROM rent_occupation_score WHERE 職業 = '{occupation}'"
            sql_2 = f"SELECT * FROM rent_income_score WHERE 最低月收入 < '{income_num}' AND 最高月收入 > '{income_num}'"
            sql_3 = f"SELECT * FROM rent_old_score WHERE 最低年齡 < '{old_num}' AND 最高年齡 >'{old_num}'"
            # rule
            """ 信用分數總和 ＝ 職業範圍之信用得分＋月收入範圍之信用得分＋年齡範圍之信用得分
                申請者實際可貸款金額(萬元) = 房屋總價 × 最高貸款比例
                仍需求湊金額(萬元) = 房價－自備款－申貸金額"""
            con = sqlite3.connect('SQL/rent.db')
            cur = con.cursor()
            cur.execute(sql_1)
            rows = cur.fetchall()
            score = score + rows[0][1]
            cur.execute(sql_2)
            rows = cur.fetchall()
            score = score + rows[0][2]
            cur.execute(sql_3)
            rows = cur.fetchall()
            score = score + rows[0][2]
            sql_4 = f"SELECT * FROM rent_info WHERE 最低信用分數總和 < '{score}' AND 最高信用分數總和 > '{score}'"
            cur.execute(sql_4)
            rows = cur.fetchall()
            rate = rows[0][2]
            percent = rows[0][3]
            real_rent = float(h_price_num) * float(percent)/100
            need_money = float(predict_rent_num) - real_rent
            if need_money < 0:
                need_money = 0
            dispatcher.utter_message(f"經過我們的試算，銀行願意貸款給您{real_rent}萬，利率{rate}，扣掉您自備款你仍需{need_money}萬元。謝謝您!請問還有其他問題嗎?")
        except Exception as e:
            logging.error(str(e))
        finally:
            cur.close()
            con.close()

        return[SlotSet("name", name if name is not None else []),
               SlotSet("occupation", occupation if occupation is not None else []),
               SlotSet("old", old if old is not None else []),
               SlotSet("income", income if income is not None else []),
               SlotSet("h_price", h_price if h_price is not None else []),
               SlotSet("self_rent", self_rent if self_rent is not None else []),
               SlotSet("predict_rent", predict_rent if predict_rent is not None else []),
               SlotSet("real_rent", real_rent if real_rent is not None else []),
               SlotSet("rate", rate if rate is not None else []),
               SlotSet("percent", percent if percent is not None else []),
               SlotSet("need_money", need_money if need_money is not None else [])]


class Action_Output(Action):
    """Action2."""
    def name(self):
        return "action_output"

    def run(self, dispatcher, tracker, domain):
        try:
            end = tracker.get_slot("end")
            name = tracker.get_slot("name")
            occupation = tracker.get_slot("occupation")
            old = tracker.get_slot("old")
            income = tracker.get_slot("income").replace(" ", "")
            h_price = tracker.get_slot("h_price").replace(" ", "")
            self_rent = tracker.get_slot("self_rent").replace(" ", "")
            rate = tracker.get_slot("rate")
            percent = tracker.get_slot("percent")
            real_rent = tracker.get_slot("real_rent")
            need_money = tracker.get_slot("need_money")
            print(tracker.current_slot_values())
            if end:
                if end.replace(" ", "") == "輸出表單":
                    dispatcher.utter_message(f"姓名：{name}\n"
                                             f"年齡：{old}\n"
                                             f"職業：{occupation}\n"
                                             f"月收入： {income}\n"
                                             f"可貸利率：利率{rate}%\n"
                                             f"最高貸款比例：{percent}%\n"
                                             f"申請者實際可貸款金額：{real_rent}萬元\n"
                                             f"房屋總價：{h_price}\n"
                                             f"自備首付款：{self_rent}\n"
                                             f"仍需求湊金額：{need_money}萬\n")
                    return [AllSlotsReset()]
        except Exception as e:
            logging.error(str(e))

        return[SlotSet("name", name if name is not None else []),
               SlotSet("occupation", occupation if occupation is not None else []),
               SlotSet("old", old if old is not None else []),
               SlotSet("income", income if income is not None else []),
               SlotSet("h_price", h_price if h_price is not None else []),
               SlotSet("self_rent", self_rent if self_rent is not None else []),
               SlotSet("real_rent", real_rent if real_rent is not None else []),
               SlotSet("rate", rate if rate is not None else []),
               SlotSet("percent", percent if percent is not None else []),
               SlotSet("need_money", need_money if need_money is not None else [])]
