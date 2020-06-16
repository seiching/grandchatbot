# !/usr/bin/env python
# -*-coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from policy.mobile_policy import MobilePolicy
from policy.attention_policy import AttentionPolicy
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.form_policy import FormPolicy

from rasa_core.policies.embedding_policy import EmbeddingPolicy


def train_dialogue_keras(domain_file=f"configs/restaurant_domain.yml",
                         model_path=f"../models/dialogue_keras",
                         training_data_file=f"configs/restaurant_story.md"):

    fallback = FallbackPolicy(
        fallback_action_name="action_none",
        nlu_threshold=0.3,
        core_threshold=0.2
    )
    
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=4),
                            MobilePolicy(epochs=50, batch_size=4), fallback, FormPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_dialogue_embed(domain_file='C:\\Users\\F126488251\\Documents\\rasa_b\\stock_domain.yml',
                   model_path="C:\\Users\\F126488251\\Documents\\rasa_b\\models\\dialogue_embed",
                   training_data_file='C:\\Users\\F126488251\\Documents\\rasa_b\\data\\story.md'):

    fallback = FallbackPolicy(
        fallback_action_name="action_default_fallback",
        nlu_threshold=0.5,
        core_threshold=0.3
    )
    
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=5),
                            EmbeddingPolicy(epochs=100), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_dialogue_transformer(domain_file='C:\\Users\\F126488251\\Documents\\rasa_b\\stock_domain.yml',
                               model_path="C:\\Users\\F126488251\\Documents\\rasa_b\\models\\dialogue_transformer",
                               training_data_file='C:\\Users\\F126488251\\Documents\\rasa_b\\data\\story.md'):

    fallback = FallbackPolicy(
        fallback_action_name="action_default_fallback",
        nlu_threshold=0.5,
        core_threshold=0.3
    )

    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=8),
                            AttentionPolicy(epochs=150), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data,
        validation_split=0.2
    )

    agent.persist(model_path)
    return agent


if __name__ == '__main__':
    train_dialogue_keras()
