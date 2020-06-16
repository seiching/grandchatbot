# !/usr/bin/env python
# -*-coding: utf-8 -*-
"""This is train model and test nlu model script."""
import warnings
from rasa_nlu.training_data import load_data
# from rasa_nlu import config
# from rasa_nlu.model import Trainer
# from rasa_nlu.model import Metadata
from rasa_nlu.model import Interpreter
import pprint as aa
# from rasa_nlu_gao.training_data import load_data
from rasa_nlu_gao import config
from rasa_nlu_gao.model import Trainer
# from rasa_nlu_gao.model import Interpreter
# import monpa
# import tensorflow as tf
import os
import logging
import datetime
warnings.simplefilter(action='ignore', category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


def record_log():
    log_filename = datetime.datetime.now().strftime(f"../%Y-%m-%d_%H_%M_%S.log")
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(log_filename, 'w', 'utf-8')])
    # output to screen
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 設定輸出格式
    formatter = logging.Formatter('%(asctime)s %(name)s: '
                                  '%(levelname)s %(message)s')
    # handler 設定輸出格式
    console.setFormatter(formatter)
    # 加入 hander 到 root logger
    logging.getLogger('').addHandler(console)
    logging.info('Start!')


def train_nlu(data, configs, model_dir):
    """Train model."""
    training_data = load_data(data)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)
    trainer.persist(model_dir, fixed_model_name='test')


def run_nlu():
    """Run  model."""
    interpreter = Interpreter.load(
        '../models/nlu/default/test')
    # test
    # aa.pprint(interpreter.parse(f"輸出表單"))

    # restaurant
    # aa.pprint(interpreter.parse(f"我要訂位"))
    # aa.pprint(interpreter.parse(f"9月2號晚上七點半"))
    # aa.pprint(interpreter.parse(f"2個人"))
    # aa.pprint(interpreter.parse(f"沒錯"))
    # aa.pprint(interpreter.parse(f"林素芬"))
    # aa.pprint(interpreter.parse(f"0912-222-222"))
    # aa.pprint(interpreter.parse(f"好，感謝！"))
    # aa.pprint(interpreter.parse(f"輸出表單"))
    # aa.pprint(interpreter.parse(f"結束對話"))

    # car
    aa.pprint(interpreter.parse(f"我想要在12/8到12/9租一台客車"))
    aa.pprint(interpreter.parse(f"蔡先生"))
    aa.pprint(interpreter.parse(f"早上十點、台北店"))
    aa.pprint(interpreter.parse(f"孤星"))
    aa.pprint(interpreter.parse(f"晚上七點，在台中店"))
    aa.pprint(interpreter.parse(f"0912-123123"))
    aa.pprint(interpreter.parse(f"沒有"))
    aa.pprint(interpreter.parse(f"輸出表單"))

    # rent
    # aa.pprint(interpreter.parse(f"我想要買房子，要申辦房屋貸款"))
    # aa.pprint(interpreter.parse(f"陳家豪"))
    # aa.pprint(interpreter.parse(f"公務員"))
    # aa.pprint(interpreter.parse(f"38歲"))
    # aa.pprint(interpreter.parse(f"45000元"))
    # aa.pprint(interpreter.parse(f"269萬元"))
    # aa.pprint(interpreter.parse(f"1076萬元"))
    # aa.pprint(interpreter.parse(f"沒有"))
    # aa.pprint(interpreter.parse(f"輸出表單"))


if __name__ == '__main__':
    # data = f"stocks_new.json"
    data = f"restaurant.json"
    try:
        # record_log()
        # print('start')
        # train_nlu(f"../data/{data}",
        #           f"configs/config_CKIP_mitie_sklearn.yml",
        #           f"../models/nlu")
        # logging.info('Finish!')
        run_nlu()
    except Exception as e:
        print(str(e))
    # input()
