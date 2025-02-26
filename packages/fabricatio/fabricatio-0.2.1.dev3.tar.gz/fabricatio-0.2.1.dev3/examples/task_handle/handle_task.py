"""Example of using the library."""

import asyncio
from typing import Any, Set, Unpack

from fabricatio import Action, Event, PythonCapture, Role, Task, ToolBox, WorkFlow, fs_toolbox, logger
from pydantic import Field


class WriteCode(Action):
    """Action that says hello to the world."""

    name: str = "write code"
    output_key: str = "dump_text"

    async def _execute(self, task_input: Task[str], **_) -> str:
        return await self.aask_validate(
            task_input.briefing,
            system_message=task_input.dependencies_prompt,
            validator=PythonCapture.capture,
        )


class DumpText(Action):
    """Dump the text to a file."""

    name: str = "dump text"
    description: str = "dump text to a file"
    toolboxes: Set[ToolBox] = Field(default_factory=lambda: {fs_toolbox})
    output_key: str = "task_output"

    async def _execute(self, task_input: Task, dump_text: str, **_: Unpack) -> Any:
        logger.debug(f"Dumping text: \n{dump_text}")
        task_input.update_task(
            ["dump the text contained in `text_to_dump` to a file", "only return the path of the written file"]
        )

        path = await self.handle(
            task_input,
            {"text_to_dump": dump_text},
        )
        if path:
            return path[0]

        return None


class WriteDocumentation(Action):
    """Action that says hello to the world."""

    name: str = "write documentation"
    description: str = "write documentation for the code in markdown format"
    output_key: str = "dump_text"

    async def _execute(self, task_input: Task[str], **_) -> str:
        return await self.aask(task_input.briefing, system_message=task_input.dependencies_prompt)


async def main() -> None:
    """Main function."""
    role = Role(
        name="Coder",
        description="A python coder who can ",
        registry={
            Event.instantiate_from("coding").push_wildcard().push("pending"): WorkFlow(
                name="write code", steps=(WriteCode, DumpText)
            ),
            Event.instantiate_from("doc").push_wildcard().push("pending"): WorkFlow(
                name="write documentation", steps=(WriteDocumentation, DumpText)
            ),
        },
    )

    prompt = "i want you to write a cli app implemented with python , which can calculate the sum to a given n, all write to a single file names `cli.py`, put it in `output` folder."

    proposed_task = await role.propose(prompt)
    path = await proposed_task.move_to("coding").delegate()
    logger.success(f"Code Path: {path}")

    proposed_task = await role.propose(f"write Readme.md file for the code, source file {path},save it in `README.md`")
    proposed_task.override_dependencies([path])
    doc = await proposed_task.move_to("doc").delegate()
    logger.success(f"Documentation: \n{doc}")


if __name__ == "__main__":
    asyncio.run(main())
