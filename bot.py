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
#     failures = 1,
#     activities = 1,
#     higher = 1,
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
        self.q_id = 0
        self.text1 = ""
        self.text2 = ""
        self.text3 = ""
        self.text4 = ""
        self.text5 = ""
        self.text6 = ""
        self.text7 = ""
        self.text8 = ""

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        return await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        self.q_id = 0
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to the Exam Performance Boost bot, { member.name }."
                        f" Please, follow the instructions."
                    )
                )

                await self._send_suggested_actions(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        self.q_id += 1
        if self.q_id == 1:
            send_text = MessageFactory.text("What is your age?")
            return await turn_context.send_activity(send_text)
        if self.q_id == 2:
            self.text1 = turn_context.activity.text.lower()
            send_text = MessageFactory.text(f"What is your travel time?")
            send_text.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="<15 min",
                        type=ActionTypes.im_back,
                        value="1"
                    ),
                    CardAction(
                        title="15 to 30 min",
                        type=ActionTypes.im_back,
                        value="2"
                    ),
                    CardAction(
                        title="30 min to 1 hour",
                        type=ActionTypes.im_back,
                        value="3"
                    ),
                    CardAction(
                        title=">1 hour",
                        type=ActionTypes.im_back,
                        value="4"
                    ),
                ]
            )
            return await turn_context.send_activity(send_text)

        if self.q_id == 3:
            self.text2 = turn_context.activity.text.lower()
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
            self.text3 = turn_context.activity.text.lower()
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
        if self.q_id == 5:
            self.text4 = turn_context.activity.text.lower()
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
            self.text5 = turn_context.activity.text.lower()
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
            self.text6 = turn_context.activity.text.lower()
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
            self.text7 = turn_context.activity.text.lower()
            send_text = MessageFactory.text("How many times you were absent (0 to 93)?")
            await turn_context.send_activity(send_text)
            self.text8 = turn_context.activity.text.lower()
        # text = turn_context.activity.text.lower()
        response_text = self._process_input()

        await turn_context.send_activity(MessageFactory.text(response_text))

        # return await self._send_suggested_actions(turn_context)


    def _process_input(self):
        return f"{self.text1}, {self.text2}, {self.text3}, {self.text4}"

    async def _send_suggested_actions(self, turn_context: TurnContext):
        reply = MessageFactory.text("Choose your option.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Red",
                    type=ActionTypes.im_back,
                    value="Red"
                ),
                CardAction(
                    title="Yellow",
                    type=ActionTypes.im_back,
                    value="Yellow"
                ),
                CardAction(
                    title="Blue",
                    type=ActionTypes.im_back,
                    value="Blue"
                ),
            ]
        )

        return await turn_context.send_activity(reply)
