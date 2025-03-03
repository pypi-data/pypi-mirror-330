import json
import os
import time
from datetime import datetime
from pathlib import Path

import pytest
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from tracker import (
    get_process_md5,
    save_ckpt_online_mutation,
    save_proc_online_mutation,
    save_roadmap_offline_mutation,
)
from tracker.model import ProcType
from tracker.utils import random_hash


@pytest.mark.asyncio
async def test_aiohttp_check_schema():

    url = os.getenv("INTERNTRACK_API_URL")
    sample_transport = AIOHTTPTransport(url=url)
    async with Client(transport=sample_transport) as session:
        await session.fetch_schema()
        assert all(
            mutation in session.client.schema.mutation_type.fields
            for mutation in ["createTrainConfig", "createCheckpoint", "createRoadmap"]
        )


@pytest.mark.asyncio
async def test_aiohttp_create_roadmap():

    url = os.getenv("INTERNTRACK_API_URL")
    with open(os.path.join(Path(__file__).parent.as_posix(), "roadmap.json"), "r") as file:
        data = json.load(file)

    result = await save_roadmap_offline_mutation(data, url)
    assert result["createRoadmap"]["code"] == 0


@pytest.mark.asyncio
async def test_aiohttp_create_roadmap_online():

    url = os.getenv("INTERNTRACK_API_URL")
    with open(os.path.join(Path(__file__).parent.as_posix(), "proc.json"), "r") as file:
        data = json.load(file)
    ckpts = data.pop("ckpts")

    data["startTime"] = datetime.now()
    data["state"] = ProcType.RUNNING
    data["currentStep"] = 0

    procMd5 = get_process_md5()
    ckptMd5 = "774fe76d29fa91a3d4e1ac3c8185d461d7f9622f2279127102e1ed76608a8184"

    result = await save_proc_online_mutation(data, procMd5, ckptMd5, url)
    assert "id" in result["createTrainConfig"]

    for ckpt in ckpts:
        time.sleep(5)
        ckpt["md5"] = random_hash()
        result = await save_ckpt_online_mutation(ckpt, procMd5, url)
        assert "id" in result["createCheckpoint"]
