# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

import sqlalchemy as sa
from sqlalchemy.sql import func

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions

from database import SessionLocal, engine
from config import DefaultConfig

import json
import requests
import models

CONFIG = DefaultConfig()

#to create if not exist all tables that extends Base
models.Base.metadata.create_all(bind=engine)

#to drop table
# models.Dataset1.__table__.drop(bind=engine)




#CREATING ENTRY
entry1 = models.Dataset1(
    studytime = 1,
    activities = 1,
    freetime = 1,
    internet = 1,
    health = 1,
    absences = 10,
    G3 = 'A')


def create_entry(e):
    with SessionLocal() as db:
        db.add(e)
        db.commit()
        db.refresh(e)

#GETTING AVERAGE OF COLUMNS
def get_avg(grade):
    with SessionLocal() as db:
        avg=db.query(
            func.avg(models.Dataset1.studytime).label('avg_studytime'),
            func.avg(models.Dataset1.activities).label('avg_activities'),
            func.avg(models.Dataset1.freetime).label('avg_freetime'),
            func.avg(models.Dataset1.internet).label('avg_internet'),
            func.avg(models.Dataset1.health).label('avg_health'),
            func.avg(models.Dataset1.absences).label('avg_absences')
            ).filter(models.Dataset1.G3==grade).first()
    return avg


def get_model_prediction():
    payload="{\n  \"data\": [\n    {\n      \"studytime\": 0,\n      \"activities\": 0,\n      \"internet\": 0,\n      \"freetime\": 0,\n      \"health\": 0,\n      \"absences\": 0\n    }\n  ]\n}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(CONFIG.ML_URL, headers=headers, data=payload)
    data = json.loads(response.json())
    return data['result'][0]


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        self.on_start = False
        self.q_id = 0
        self.option = 0
        self.studytime = ""
        self.activities = ""
        self.freetime = ""
        self.internet = ""
        self.health = ""
        self.absences = ""

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        return await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        self.q_id = 0
        self.option = 0
        self.on_start = False
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to the Exam Performance Boost bot, { member.name }."
                        f" Please, follow the instructions."
                    )
                )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()
        if text == "/start" or text == "/restart":
            self.option = 0
            self.q_id = 0
            self.on_start = True
            return await self._send_suggested_actions(turn_context)

        if text == "option_show" or self.option == 1: 
            self.option = 1
            # await turn_context.send_activity(MessageFactory.text(response_text))

        if text == "option_pred" or self.option == 2:
            self.option = 2
        
        if text == "option_get_rec" or self.option == 3:
            self.option = 3

        await self._get_user_performance(text, turn_context)

        
    async def _get_user_performance(self, text : str, turn_context: TurnContext):
        if self.on_start:
            self.q_id += 1
        if self.q_id == 1:
            send_text = MessageFactory.text("Choose your study time?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="<2 hours",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="2 to 5 hours",
                        type=ActionTypes.im_back,
                        value="2"
                    ),
                    CardAction(
                        title="5 to 10 hours",
                        type=ActionTypes.im_back,
                        value="3"
                    ),
                    CardAction(
                        title=">10 hours",
                        type=ActionTypes.im_back,
                        value="4"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 2:
            self.studytime = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Please, evalute your free time after school (1 - very bad to 5 - very good).")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="1",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="2",
                        type=ActionTypes.im_back,
                        value="2"
                    ),
                    CardAction( 
                        title="3",
                        type=ActionTypes.im_back,
                        value="3"
                    ),
                    CardAction(
                        title="4",
                        type=ActionTypes.im_back,
                        value="4"
                    ),
                    CardAction(
                        title="5",
                        type=ActionTypes.im_back,
                        value="5"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 3:
            self.freetime = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Are you enrolled in other activities/clubs?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="Yes",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="No",
                        type=ActionTypes.im_back,
                        value="0"
                    )
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 4:
            self.activities = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Do you have internet acess?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="Yes",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="No",
                        type=ActionTypes.im_back,
                        value="0"
                    )
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 5:
            self.internet = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Please, choose your current health status (1 - very bad to 5 - very good).")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="1",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="2",
                        type=ActionTypes.im_back,
                        value="2"
                    ),
                    CardAction( 
                        title="3",
                        type=ActionTypes.im_back,
                        value="3"
                    ),
                    CardAction(
                        title="4",
                        type=ActionTypes.im_back,
                        value="4"
                    ),
                    CardAction(
                        title="5",
                        type=ActionTypes.im_back,
                        value="5"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 6:
            self.health = turn_context.activity.text.lower()
            send_text = MessageFactory.text("How many times you were absent (0 to 93)?")
            return await turn_context.send_activity(send_text)
            self.absences = turn_context.activity.text.lower()
        text = turn_context.activity.text.lower()
        # response_text = self._process_input()

        # await turn_context.send_activity(MessageFactory.text(response_text))

        # return await self._send_suggested_actions(turn_context)


    def _process_input(self, text : str, turn_context: TurnContext):
        return "No such option"

    async def _send_suggested_actions(self, turn_context: TurnContext):
        reply = MessageFactory.text("Choose your option.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Show performance for certain score",
                    type=ActionTypes.im_back,
                    value="option_show"
                ),
                CardAction(
                    title="Predict my exam score",
                    type=ActionTypes.im_back,
                    value="option_pred"
                ),
                CardAction(
                    title="Improve your performance",
                    type=ActionTypes.im_back,
                    value="option_get_rec"
                ),
            ]
        )

        return await turn_context.send_activity(reply)
