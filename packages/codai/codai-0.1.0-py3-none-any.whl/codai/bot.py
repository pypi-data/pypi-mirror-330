# imports
import os
import ibis
import asyncio

import ibis.expr.datatypes as dt

from typing import Any, Callable
from pydantic import BaseModel
from pydantic_ai.agent import Agent, AgentRunResult
from pydantic_ai.models import Model

from codai.lms import gemini_2_flash, gpt_4o_mini  # noqa
from codai.utils import now, generate_uuid, get_codai_dir

# constants
DEFAULT_MODEL = gemini_2_flash
DEFAULT_SYSTEM_PROMPT = """
# codai

You are codai, a highly technical research and development assistant. You interface with the user to achieve a goal.
""".strip()


# class
class Bot:
    # init
    def __init__(
        self,
        name: str = "bot",
        username: str = "dev",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        tools: list[Callable] = [],
        model: Model = DEFAULT_MODEL,
        result_type: BaseModel | Any = str,
        dbpath: str = "bots.db",
    ) -> None:
        self.uuid = generate_uuid()

        self.name = name
        self.username = username
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools
        self.result_type = result_type
        self.dbpath = os.path.join(get_codai_dir(), dbpath)

        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            tools=self.tools,
            result_type=self.result_type,
        )

        self.wcon, self.rcon = self._cons()

        self.append_bot(
            id=self.uuid,
            name=self.name,
            model=self.model.model_name,
            system_prompt=self.system_prompt,
            tools=",".join([tool.__name__ for tool in self.tools]),
            result_type=str(self.result_type),
        )
        # self.append_message(
        #     bot_id=self.uuid,
        #     to=self.name,
        #     from_="system",
        #     content=self.system_prompt,
        # )

    # call
    def __call__(self, text: str, message_history: list = None) -> AgentRunResult:
        # self.append_message(
        #     bot_id=self.uuid,
        #     to=self.name,
        #     from_=self.username,
        #     content=text,
        # )

        # TODO: go back and forth from pydantic_ai messages
        # _message_history = self.get_message(bot_id=self.uuid)

        # define async function
        async def _call_agent(text: str, message_history: list = None):
            return await self.agent.run(text)

        def call_agent(text: str, message_history: list = None):
            return asyncio.run(_call_agent(text=text, message_history=message_history))

        res = call_agent(text=text, message_history=message_history)
        content = res.data

        # self.append_message(
        #     bot_id=self.uuid,
        #     to=self.username,
        #     from_=self.name,
        #     content=content,
        # )

        return res

    # external state
    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        self.bots_table_name = "bots"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "name": str,
                "model": str,
                "system_prompt": str,
                "tools": str,
                "result_type": str,
            }
        )
        if self.bots_table_name not in wcon.list_tables():
            wcon.create_table(self.bots_table_name, schema=schema)

        self.messages_table_name = "messages"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "bot_id": str,
                "to": str,
                "from": str,
                "content": str,
            }
        )
        if self.messages_table_name not in wcon.list_tables():
            wcon.create_table(self.messages_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        # return connections
        return wcon, rcon

    def bots_t(self, id: str = None, name: str = None):
        # get bots data
        t = self.rcon.table(self.bots_table_name)

        # filter
        if id:
            t = t.filter(ibis._["id"] == id)
        if name:
            t = t.filter(ibis._["name"] == name)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by=ibis._["id"],
                        order_by=ibis.desc("idx"),
                    )
                )
            )
            .filter(ibis._["rank"] == 0)
            .drop("rank")
        )

        # order
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    def messages_t(
        self, id: str = None, bot_id: str = None, to: str = None, from_: str = None
    ):
        # get messages data
        t = self.rcon.table(self.messages_table_name)

        # filter
        if id:
            t = t.filter(ibis._["id"] == id)
        if bot_id:
            t = t.filter(ibis._["bot_id"] == bot_id)
        if to:
            t = t.filter(ibis._["to"] == to)
        if from_:
            t = t.filter(ibis._["from"] == from_)

        # order
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_bot(self, id: str = None, name: str = None) -> bool:
        t = self.bots_t(id=id, name=name)
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    def contains_message(
        self, bot_id: str = None, to: str = None, from_: str = None
    ) -> bool:
        t = self.messages_t(bot_id=bot_id, to=to, from_=from_)
        return t.filter(t["bot_id"] == bot_id).count().to_pyarrow().as_py() > 0

    # get record(s)
    def get_bot(self, id: str = None, name: str = None):
        t = self.bots_t(id=id, name=name)

        if id:
            return t.to_pyarrow().to_pylist()[0]
        else:
            return t.to_pyarrow().to_pylist()

    def get_message(
        self, id: str = None, bot_id: str = None, to: str = None, from_: str = None
    ):
        t = self.messages_t(id=id, bot_id=bot_id, to=to, from_=from_)

        if id:
            return t.to_pyarrow().to_pylist()[0]
        else:
            return t.to_pyarrow().to_pylist()

    # append record
    def append_bot(
        self,
        id: str,
        name: str,
        model: str,
        system_prompt: str,
        tools: str,
        result_type: str,
    ):
        data = {
            "idx": [now()],
            "id": [id],
            "name": [name],
            "model": [model],
            "system_prompt": [system_prompt],
            "tools": [tools],
            "result_type": [result_type],
        }
        self.wcon.insert(self.bots_table_name, data)

        return self.get_bot(name=name)

    def append_message(
        self,
        bot_id: str,
        to: str,
        from_: str,
        content: str,
    ):
        data = {
            "idx": [now()],
            "id": [generate_uuid()],
            "bot_id": [bot_id],
            "to": [to],
            "from": [from_],
            "content": [content],
        }
        self.wcon.insert(self.messages_table_name, data)

        return self.get_message(bot_id=bot_id, to=to, from_=from_)
