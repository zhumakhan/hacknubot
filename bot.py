# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

import sqlalchemy as sa


from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)


# db = SessionLocal()


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

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"ECHO '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
