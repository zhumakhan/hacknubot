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

time_spent_per_week_map = {0:"<2 hours", 1:"<2 hours", 2:"2 to 5 hours", 3:"5 to 10 hours", 4:">10 hours"}
#CREATING ENTRY
# entry1 = models.Dataset1(
#     studytime = 1,
#     activities = 1,
#     freetime = 1,
#     internet = 1,
#     health = 1,
#     absences = 10,
#     G3 = 'A')


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
    return avg,f'studytime: {time_spent_per_week_map[ int(avg[0])%5 ]}\n activities: {str(round(avg[1]*100,2))} % yes\n freetime: {str(round(avg[3],2))} hours\n internet: {str(round(avg[2]*100,2))}% yes\n health: {str(round(avg[4],2))}\n absences: {str(round(avg[5],2))}'

def get_model_prediction( studytime, activities, freetime, internet, health, absences):
    payload="{\n  \"data\": [\n    {\n      \"studytime\": " + str(studytime) + ",\n      \"activities\": " + str(activities) + ",\n      \"internet\": " + str(internet) + ",\n      \"freetime\": " + str(freetime) + ",\n      \"health\": " + str(health) + ",\n      \"absences\": " + str(absences) + "\n    }\n  ]\n}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(CONFIG.ML_URL, headers=headers, data=payload)
    data = json.loads(response.json())
    return data['result'][0]

# print(get_model_prediction(0,1,1,1,2,3))

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        self.on_start = False
        self.q_id = 0
        self.on_score = False
        self.on_improve = False
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
                        f"Welcome to the Exam Performance Boost bot, { member.name }. Type '/start' or '/restart' to begin"
                        f" Please, follow the instructions."
                    )
                )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()
        if text == "/start" or text == "/restart":
            self.option = 0
            self.q_id = 0
            self.on_score = False
            self.on_start = True
            self.on_improve = False
            return await self._send_suggested_actions(turn_context)

        if text == "option_show" or self.option == 1: 
            self.option = 1
            if self.on_score:
                _,avg = get_avg(turn_context.activity.text)
                send_text = MessageFactory.text(f"Average perforances: { avg }")
                return await turn_context.send_activity(send_text)
            await self._get_user_prefer_score(text, turn_context)

        if text == "option_pred" or self.option == 2:
            self.option = 2
            await self._get_user_performance(text, turn_context)
            if self.q_id == 7:
                score_predict = get_model_prediction( self.studytime, self.activities, self.freetime, self.internet, self.health, self.absences )
                send_text = MessageFactory.text(f"Probably the score will be '{ score_predict }'")
                return await turn_context.send_activity(send_text)
        
        if text == "option_get_rec" or self.option == 3:
            self.option = 3
            await self._get_user_performance(text, turn_context)
            # avg = get_avg(turn_context.activity.text)
            # send_text = MessageFactory.text(f"Parameteres are { avg }")
            # return await turn_context.send_activity(send_text)
            
                    
    
    async def _get_user_prefer_score(self, text : str, turn_context: TurnContext):
        self.on_score = True
        send_text = MessageFactory.text("Choose the score you want to look at?")
        send_text.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                        title="A",
                        type=ActionTypes.im_back,
                        value="A"
                    ),
                    CardAction(
                        title="B",
                        type=ActionTypes.im_back,
                        value="B"
                    ),
                    CardAction( 
                        title="C",
                        type=ActionTypes.im_back,
                        value="C"
                    ),
                    CardAction(
                        title="D",
                        type=ActionTypes.im_back,
                        value="D"
                    ),
                    CardAction(
                        title="F",
                        type=ActionTypes.im_back,
                        value="F"
                    ),
            ]
        )
        return await turn_context.send_activity(send_text)
        
    async def _get_user_performance(self, text : str, turn_context: TurnContext):
        if self.on_start:
            self.q_id += 1
        if self.q_id == 1:
            send_text = MessageFactory.text("Time spent on study per week?")
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
            send_text = MessageFactory.text("Please, evaluate your free time after school (1 - less to 5 - more).")
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
            send_text = MessageFactory.text("Please, choose your current health status (1 - unsatisfactory to 5 - good).")
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
        if self.q_id == 7:
            self.absences = turn_context.activity.text.lower()

        if self.q_id == 7 and self.option == 3:
            self.on_start = False
            if self.on_improve:
                _,avg = get_avg(turn_context.activity.text)
                studytime,activities,internet,freetime,health,absences = avg

                send_text = MessageFactory.text(f"Parameteres are { avg }")
                return await turn_context.send_activity(send_text)
            self.on_improve = True
            send_text = MessageFactory.text("Choose score you want to look at?")
            send_text.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                        title="A",
                        type=ActionTypes.im_back,
                        value="A"
                    ),
                    CardAction(
                        title="B",
                        type=ActionTypes.im_back,
                        value="B"
                    ),
                    CardAction( 
                        title="C",
                        type=ActionTypes.im_back,
                        value="C"
                    ),
                    CardAction(
                        title="D",
                        type=ActionTypes.im_back,
                        value="D"
                    ),
                    CardAction(
                        title="F",
                        type=ActionTypes.im_back,
                        value="F"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)
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
                    title="Get average performance per score",
                    type=ActionTypes.im_back,
                    value="option_show"
                ),
                CardAction(
                    title="Predict exam score",
                    type=ActionTypes.im_back,
                    value="option_pred"
                ),
                CardAction(
                    title="Get tips for preparation",
                    type=ActionTypes.im_back,
                    value="option_get_rec"
                ),
            ]
        )

        return await turn_context.send_activity(reply)
