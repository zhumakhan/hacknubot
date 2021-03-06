#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "388e1e83-7392-4296-9124-8cae7c0e5918")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "fWp6&<>tDZ3o1D^E?<")
    # APP_ID = ""
    # APP_PASSWORD = ""
    DB_URL = "postgresql+psycopg2://rootadmin@hachnudb:@Pass123@hachnudb.postgres.database.azure.com:5432/postgres"
    ML_URL = "http://b146ab87-3af0-4754-ab49-0b3a0b0de090.eastasia.azurecontainer.io/score"
