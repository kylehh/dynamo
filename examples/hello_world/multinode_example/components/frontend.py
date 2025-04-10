# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from components.processor import Processor
from components.utils import GeneralRequest

from dynamo.sdk import api, depends, service
from dynamo.sdk.lib.image import DYNAMO_IMAGE

logger = logging.getLogger(__name__)

@service(
    resources={"cpu": "10", "memory": "20Gi"},
    workers=1,
    image=DYNAMO_IMAGE,
)
class Frontend:

    processor = depends(Processor)

    @api
    async def generate(self, prompt, request_id): # from request body keys
        """Stream results from the pipeline."""
        print(f"-Frontend layer received: {prompt=},{request_id=}")
        frontend_request = GeneralRequest(
            prompt=prompt, 
            request_id=request_id).model_dump_json()
        async for response in self.processor.generate(frontend_request):
           yield f"Response: {response}\n"

