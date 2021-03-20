#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "388e1e83-7392-4296-9124-8cae7c0e5918")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "fWp6&<>tDZ3o1D^E?<")
