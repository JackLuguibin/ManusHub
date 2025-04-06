from abc import ABC
from asyncio import sleep
from contextlib import asynccontextmanager
from typing import Optional, List

from pydantic import BaseModel, Field, model_validator

from hub.base.llm import LLM
from hub.base.memory import Memory
from hub.base.message import MESSAGE_MAKERS
from hub.base.role import ROLE_TYPE, Role
from hub.base.state import AgentState
from hub.logger import logger


class Agent(BaseModel, ABC):
    name: str = Field(..., description="Unique name of the agent")
    description: Optional[str] = Field(None, description="Optional agent description")

    llm: LLM = Field(default_factory=LLM, description="Language model instance")
    memory: Memory = Field(default_factory=Memory, description="Agent's memory store")
    state: AgentState = Field(
        default=AgentState.IDLE, description="Current agent state"
    )
    max_steps: int = Field(default=10, description="Maximum steps before termination")
    current_step: int = Field(default=0, description="Current step in execution")

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # Allow extra fields for flexibility in

    @model_validator(mode="after")
    def initialize_agent(self) -> "Agent":
        if self.llm is None or not isinstance(self.llm, LLM):
            self.llm = LLM(config_name=self.name.lower())
        if not isinstance(self.memory, Memory):
            self.memory = Memory()
        return self

    @asynccontextmanager
    async def state_context(self, new_state: AgentState):
        if not isinstance(new_state, AgentState):
            raise ValueError(f"Invalid state: {new_state}")
        original_state = self.state
        self.state = new_state
        try:
            yield
        except Exception as e:
            self.state = original_state
            raise e
        finally:
            self.state = original_state

    def update_memory(self, role: ROLE_TYPE, content: str, **kwargs) -> None:
        if role not in MESSAGE_MAKERS:
            raise ValueError(f"Invalid role: {role}")

        message_maker = MESSAGE_MAKERS[role]
        message = message_maker(
            content=content,
            **kwargs
        )
        self.memory.add_message(message)

    def is_stuck(self) -> bool:
        """Check if the agent is stuck in a loop."""
        if len(self.memory.messages) < 2:
            return False

        last_message = self.memory.messages[-1]
        if not last_message.content:
            return False

        duplicate_count = sum(
            1
            for msg in reversed(self.memory.messages[:-1])
            if msg.role == Role.ASSISTANT and msg.content == last_message.content
        )

        return duplicate_count >= self.duplicate_threshold

    async def cleanup(self) -> None:
        await sleep(0)

    async def run(self, request: Optional[str] = None) -> str:
        if self.state != AgentState.IDLE:
            raise RuntimeError("Agent is not in IDLE state.")

        if request:
            self.update_memory(Role.USER, request)

        results:List[str] = []

        async with self.state_context(AgentState.RUNNING):
            while (
                self.current_step < self.max_steps and
                self.state != AgentState.FINISHED
            ):
                self.current_step += 1
                logger.info(f"Executing step {self.current_step}/{self.max_steps}")

                step_result = await self.step()
                if self.is_stuck():
                    self.handle_stuck_state()
                results.append(f"Step {self.current_step}: {step_result}")

            if self.current_step >= self.max_steps:
                self.current_step = 0
                self.state = AgentState.IDLE
                results.append(f"Terminated: Reached max steps ({self.max_steps})")
        await self.cleanup()
