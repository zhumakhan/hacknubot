# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

from fastapi import Depends
import sqlalchemy as sa

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db:sa.orm.Session = Depends(get_db)


# entry1 = models.Dataset1(
#     age = 1,
#     traveltime = 1,
#     studytime = 1,
#     activities = 1,
#     internet = 1,
#     romantic = 1,
#     health = 1,
#     absences = 1,
#     G3 = 1)

# db.add(entry1)
# db.commit()
# db.refresh(entry1)

# all = db.query(models.Dataset1).all()
# for e in all:
#     print(e.G3)

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        self.on_start = False
        self.q_id = 0
        self.option = 0
        self.age = ""
        self.traveltime = ""
        self.studytime = ""
        self.activities = ""
        self.internet = ""
        self.romantic = ""
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
            send_text = MessageFactory.text("What is your age?")
            return await turn_context.send_activity(send_text)
        if self.q_id == 2:
            self.age = turn_context.activity.text.lower()
            send_text = MessageFactory.text(f"What is your travel time?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="<15 min",
                        type=ActionTypes.invoke,
                        value="1"
                    ),
                    CardAction(
                        title="15 to 30 min",
                        type=ActionTypes.invoke,
                        value="2"
                    ),
                    CardAction(
                        title="30 min to 1 hour",
                        type=ActionTypes.invoke,
                        value="3"
                    ),
                    CardAction(
                        title=">1 hour",
                        type=ActionTypes.invoke,
                        value="4"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)

        if self.q_id == 3:
            self.traveltime = turn_context.activity.text.lower()
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

        if self.q_id == 4:
            self.studytime = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Are you enrolled in other activities/clubs?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="Yes",
                        type=ActionTypes.messageBack,
                        value="1"
                    ),
                    CardAction(
                        title="No",
                        type=ActionTypes.messageBack,
                        value="0"
                    )
                ]
            )
            return await turn_context.send_activity(send_text)
        if self.q_id == 5:
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
        if self.q_id == 6:
            self.internet = turn_context.activity.text.lower()
            send_text = MessageFactory.text("Are you in a relanship?")
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
        if self.q_id == 7:
            self.romantic = turn_context.activity.text.lower()
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
        if self.q_id == 8:
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
                    type=ActionTypes.message_back,
                    value="option_show"
                ),
                CardAction(
                    title="Predict my exam score",
                    type=ActionTypes.message_back,
                    value="option_pred"
                ),
                CardAction(
                    title="Improve your performance",
                    type=ActionTypes.message_back,
                    value="option_get_rec"
                ),
            ]
        )

        return await turn_context.send_activity(reply)
