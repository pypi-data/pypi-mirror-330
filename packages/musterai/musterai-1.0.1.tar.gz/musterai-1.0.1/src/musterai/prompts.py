from textwrap import dedent
from typing import ClassVar
from pydantic.v1 import BaseModel,Field,root_validator
from langchain.prompts import PromptTemplate

class Prompts(BaseModel):
    """Prompts for generic agent."""
    MANAGER_AGENT_PROMPT: ClassVar[str] = PromptTemplate.from_template(dedent("""Evaluate these task states:
        {tasks_states}
        
        Against these end conditions:
        {end_conditions}
        
        Now, examine the folowing list of tasks, this list is :
        {task_desc_nm}

        Your job is to decide, on the basis of task states, and the end conditions required to be fulfilled, what should be the next task to be executed such that:

        Respond ONLY in JSON format with:
        - next_task_id: ID of the task to be executed next. (Note: This field should ONLY have the TASK ID and NOTHING ELSE.) 
        - reasoning: brief explanation
        """))
    CHECK_END_PROMPT: ClassVar[str] = PromptTemplate.from_template(dedent("""Evaluate these task states:
        {task_states}
        
        Against these end conditions:
        {end_conditions}
        
        Respond ONLY in JSON format with:
        - is_complete: boolean indicating completion
        - reasoning: brief explanation"""))
    ANALYZE_HUMAN_INPUT_PROMPT: ClassVar[str] = PromptTemplate.from_template(dedent("""
You are given human feedback about the tasks performed till now.
Parse the human feedback into a JSON structure with these 3 fields:

1. "is_final_output": boolean,  // true if human indicates current output is sufficient/final and no more tasks need to be performed
2. "end_condition_change": string | null    // null if no changes requested,
3. "next_task_feedback":  string | null     // null if no specific feedback for next task 

Remember:

-Only fill fields that are relevant to the human's feedback
-Set unused fields to null
-Always include all three main fields in the output
-Ensure the output is valid JSON
-Interpret the human's intent carefully - they may not use exact phrases but imply their wishes
-Be very clear and rational while assigning values to the fields.

Now, analyze the following human feedback and convert it into the specified JSON format:
{human_feedback}

Note: Remember to output ONLY THE JSON with exactly the 3 FIELDS as instructed to you, however the values in those fields can be null if the human does not intend to fill them.
Your output(Only the JSON):
"""))
    TASK_SLICE: ClassVar[str] = dedent(
        """\
	 Begin! This is VERY important to you, your job depends on it!

	 Current Task: {input}"""
    )

    SCRATCHPAD_SLICE: ClassVar[str] = "\n{agent_scratchpad}"

    MEMORY_SLICE: ClassVar[str] = dedent(
        """\
	This is the summary of your work so far:
	{chat_history}"""
    )

    ROLE_PLAYING_SLICE: ClassVar[str] = dedent(
        """\
	You are {role}.
	{backstory}

	Your personal goal is: {goal}"""
    )

    TOOLS_SLICE: ClassVar[str] = dedent(
        """\


	TOOLS:
	------
	You have access to the following tools:

	{tools}

	To use a tool, please use the exact following format:

	```
	Thought: Do I need to use a tool? Yes
	Action: the action to take, should be one of [{tool_names}], just the name.
	Action Input: the input to the action
	Observation: the result of the action
	```

	When you have a response for your task, or if you do not need to use a tool, you MUST use the format:

	```
	Thought: Do I need to use a tool? No
	Final Answer: [your response here]
	```"""
    )

    VOTING_SLICE: ClassVar[str] = dedent(
        """\
	You are working on a crew with your co-workers and need to decide who will execute the task.

	These are your format instructions:
	{format_instructions}

	These are your co-workers and their roles:
	{coworkers}"""
    )

    TASK_EXECUTION_WITH_MEMORY_PROMPT: ClassVar[str] = PromptTemplate.from_template(
        ROLE_PLAYING_SLICE + TOOLS_SLICE + MEMORY_SLICE + TASK_SLICE + SCRATCHPAD_SLICE
    )

    TASK_EXECUTION_PROMPT: ClassVar[str] = PromptTemplate.from_template(
        ROLE_PLAYING_SLICE + TOOLS_SLICE + TASK_SLICE + SCRATCHPAD_SLICE
    )

    CONSENSUNS_VOTING_PROMPT: ClassVar[str] = PromptTemplate.from_template(
        ROLE_PLAYING_SLICE + VOTING_SLICE + TASK_SLICE + SCRATCHPAD_SLICE
    )
    
