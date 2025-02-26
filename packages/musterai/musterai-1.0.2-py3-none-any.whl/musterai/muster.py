import json
from typing import Any, Dict, List, Optional, Union
from json_repair import repair_json
from pydantic import (
    BaseModel,
    Field,
    InstanceOf,
    Json,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError
from agent import Agent
from agents import CacheHandler
from process import Process, ManagedProcess,SequentialProcess
from task import Task
from tools.agent_tools import AgentTools
from prompts import Prompts
from memory.long_term_memory.ltmsqlite import LTMSqlite
from agent_monitors.agent_monitor import AgentMonitor,TaskInfo,AgentStatus
import os
import random
from datetime import datetime

class Muster(BaseModel):
    """Class that represents a group of agents, how they should work together and their tasks."""

    class Config:
        arbitrary_types_allowed = True

    tasks: List[Task] = Field(description="List of tasks", default_factory=list)
    agents: List[Agent] = Field(
        description="List of agents in this muster.", default_factory=list
    )
    process: Union[Process,ManagedProcess,SequentialProcess] = Field(
        description="Process that the muster will follow.", default=Process.sequential
    )
    verbose: Union[int, bool] = Field(
        description="Verbose mode for the Agent Execution", default=0
    )
    config: Optional[Union[Json, Dict[str, Any]]] = Field(
        description="Configuration of the muster.", default=None
    )
    cache_handler: Optional[InstanceOf[CacheHandler]] = Field(
        default=CacheHandler(), description="An instance of the CacheHandler class."
    )
    task_states: List[tuple[str,str]] = Field(description="List of task outputs", default_factory=list)
    human_feedback: bool = Field(description="Enable and disable human feedback",default=False)
    long_term_memory: Optional[Union[LTMSqlite]] = Field(description="Long term memory for the muster",default=None)
    short_term_memory: Optional[Union[LTMSqlite]] = Field(description="Short term memory for the muster",default=None)
    long_memory_type: Optional[str] = Field(description="Type of memory to be used for the long-term",default="none")
    short_memory_type: Optional[str] = Field(description="Type of memory to be used for the short-term",default="none")
    has_memory: Optional[bool] = Field(description="Whether the muster has memory or not",default=False)
    agent_monitor: Optional[AgentMonitor] = Field(description="Agent monitor for the muster",default=None)
    has_agent_monitor: Optional[bool] = Field(description="Whether the muster has an agent monitor or not",default=False)
    @classmethod
    @field_validator("config", mode="before")
    def check_config_type(cls, v: Union[Json, Dict[str, Any]]):
        if isinstance(v, Json):
            return json.loads(v)
        return v

    @model_validator(mode="after")
    def check_config(self):
        if not self.config and not self.tasks and not self.agents:
            raise PydanticCustomError(
                "missing_keys", "Either agents and task need to be set or config.", {}
            )

        if self.config:
            if not self.config.get("agents") or not self.config.get("tasks"):
                raise PydanticCustomError(
                    "missing_keys_in_config", "Config should have agents and tasks", {}
                )

            self.agents = [Agent(**agent) for agent in self.config["agents"]]

            tasks = []
            for task in self.config["tasks"]:
                task_agent = [agt for agt in self.agents if agt.role == task["agent"]][
                    0
                ]
                del task["agent"]
                tasks.append(Task(**task, agent=task_agent))

            self.tasks = tasks

        if self.agents:
            for agent in self.agents:
                agent.set_cache_handler(self.cache_handler)
        return self

    def kickoff(self,end_conditions: List[str] = None,task_list: List[Task] = None,end_tasks:List[Task] = None,maximum_iterations:int=None) -> str:
        """Kickoff the muster to work on its tasks.

        Returns:
            Output of the muster for each task.
        """
        kickoff_id = random.randint(1, 99999)
        if self.has_agent_monitor:
            self.agent_monitor = AgentMonitor(tasks=self.tasks,kickoff_id=kickoff_id,process_type=self.process.name)
            print(self.agent_monitor.db.get_columns("agent_monitor"))
        self.task_states = []
        if self.human_feedback == True:
            manager_agent = self.__create_manager_agent()
        for agent in self.agents:
            agent.cache_handler = self.cache_handler
        if self.has_memory:
            if self.long_memory_type == "sqlite":
                self.long_term_memory = self.__create_long_term_memory("sqlite")
            if self.short_memory_type == "sqlite":
                self.short_term_memory = self.__create_short_term_memory("sqlite")
        if isinstance(self.process,SequentialProcess):
            if self.human_feedback == True:
                return self.__sequential_loop(manager_agent)
            else:
                return self.__sequential_loop()
        if isinstance(self.process,ManagedProcess):
            return self.__managed_loop(manager_agent,self.process.end_conditions,self.process.task_list,self.process.end_tasks)
    def __sequential_loop(self,manager: Agent = None) -> str:
        """Loop that executes the sequential process.

        Returns:
            Output of the muster.
        """
        task_outcome = None
        next_feed = None
        agent_monitor = self.agent_monitor
        for task in self.tasks:
            # Add delegation tools to the task if the agent allows it
            if task.agent.allow_delegation:
                tools = AgentTools(agents=self.agents).tools()
                task.tools += tools

            self.__log("debug", f"Working Agent: {task.agent.role}")
            self.__log("info", f"Starting Task: {task.description} ...")
            if next_feed is None:
                if agent_monitor is not None:
                    agent_monitor.start_task(task)
                try:
                    task_outcome = task.execute(task_outcome)
                except Exception as e:
                    if agent_monitor is not None:
                        agent_monitor.error_task(task, str(e))
                    raise e
                if agent_monitor is not None:
                    agent_monitor.completed_task(task, task_outcome)
            else:
                print(task_outcome+"\n Human feedback for the task:"+str(next_feed))
                if agent_monitor is not None:
                    agent_monitor.start_task(task)
                try:
                    task_outcome = task.execute(task_outcome+"\n Human feedback for the task:"+str(next_feed))
                except Exception as e:
                    if agent_monitor is not None:
                        agent_monitor.error_task(task, str(e))
                    raise e
                if agent_monitor is not None:
                    agent_monitor.completed_task(task, task_outcome)
                next_feed = None
            self.task_states.append((task.description,task_outcome))
            print("The task outcome is:")
            print(task_outcome)
            self.__log("debug", f"Task output: {task_outcome}")
            if self.human_feedback == True:
                flag_end,new_endconditions,feedback_next = self.__parse_human_input(manager.llm)
                if flag_end == 1:
                    return task_outcome
                if feedback_next is not None:
                    next_feed = feedback_next
        return task_outcome

    def __log(self, level, message):
        """Log a message"""
        level_map = {"debug": 1, "info": 2}
        verbose_level = (
            2 if isinstance(self.verbose, bool) and self.verbose else self.verbose
        )
        if verbose_level and level_map[level] <= verbose_level:
            print(message)

    def __select_next_task(self,manager_agent: Agent,tasks_states: List[tuple[str,str]],task_desc_list: List,end_conditions: List[str]):
        """selects the next task to be executed."""
        task_desc = [t[1] for t in task_desc_list]
        task_desc_nm = []
        for i, td in enumerate(task_desc):
            task_desc_nm.append((str(i),td))

        manager_llm = manager_agent.llm
        messages = [
    (
        "system",
        "You are a helpful task supervisor that monitors and checks the outputs of the tasks performed.",
    ),
    ("human", Prompts.MANAGER_AGENT_PROMPT.format(tasks_states=tasks_states,end_conditions=end_conditions,task_desc_nm=task_desc_nm)),
]
        response = manager_llm.invoke(
        messages
    )
        repaired_json = json.loads(repair_json(response.content))
        next_task_id = repaired_json.get("next_task_id")
        print("Task ID: "+str(next_task_id))
        for t in task_desc_nm:
            if t[0] == next_task_id:
                next_task_desc = t[1]
        print("Next task:"+str(next_task_desc))
        for t in task_desc_list:
            if t[1] == next_task_desc:
                next_task = t[0]
        return next_task
    def __check_end(self,manager_llm,task_states: List[tuple[str,str]],end_conditions: List[str]):
        """Checks whether the end conditions of the task have been met. Using end conditions and task states."""
        messages = [
    (
        "system",
        "You are a helpful task supervisor that monitors and checks the outputs of the tasks performed.",
    ),
    ("human", Prompts.CHECK_END_PROMPT.format(task_states=task_states,end_conditions=end_conditions))
]
        response = manager_llm.invoke(
        messages
    )
        repaired_json = json.loads(repair_json(response.content))
        is_complete = repaired_json.get("is_complete")
        print("Checking task:")
        print("Status:"+str(is_complete))
        if is_complete == True or False:
            return is_complete
        elif str(is_complete).strip().lower() == "true":
            return True
        else:
            return False
    def __create_manager_agent(self):
        manager = Agent(
    role='Manager',
    goal='Manage worker agents',
    backstory="",
    verbose=True,
    allow_delegation=False
    )
        return manager
    def __get_human_input(self,manager_llm):
        """Inputs and understands human input"""
        analyze_human_input_prompt = Prompts.ANALYZE_HUMAN_INPUT_PROMPT
        print("Here are the task states uptil now:")
        print(self.task_states)
        human_input = input("Enter your feedback on the output. Is the output ready to go? Do we need to make some changes?")
        messages = [
    (
        "system",
        "You are a feedback parser that converts human feedback about a agentic frameowrk's task into structured JSON. Your role is to understand the human's intent and fill only the relevant fields based on what they've specified.",
    ),
    ("human", analyze_human_input_prompt.format(human_feedback=human_input)),
]
        response = manager_llm.invoke(
        messages
    )
        repaired_json = json.loads(repair_json(response.content))
        return repaired_json
    def __parse_human_input(self,manager_llm):
        """Parses the human input and returns the tuple of 3 values: 1. Whether this should be the last task in the process. 2. Is there any change in the end conditons? If yes, what? 3. Is there any feedback for the next task? If yes, what?"""
        repaired_json = self.__get_human_input(manager_llm)
        try:
            is_final_output = repaired_json.get("is_final_output")
            end_condition_change = repaired_json.get("end_condition_change")
            next_task_feedback =  repaired_json.get("next_task_feedback")
        except:
            is_final_output = None
            end_condition_change = None
            next_task_feedback = None
        if next_task_feedback == "null" or next_task_feedback ==None:
            if is_final_output == True or str(is_final_output).lower() == "true":
                return (1,None,None)
            else:
                return (1,end_condition_change,next_task_feedback)
        else:
            return (0,end_condition_change,next_task_feedback)
    def __create_long_term_memory(self,type: str) -> Union[LTMSqlite]:
        """Creates the memory instance depending on the memory type specified by the user. Returns the SQLite database as default."""
        if type == "sqlite":
            sqlite_path = os.getenv("SQLITE_PATH")
            return LTMSqlite(sqlite_path)
        else:
            print("Returning to the default SQLite as the memory type is not supported.")
            return LTMSqlite(sqlite_path)
    def __create_short_term_memory(self, type: str):
        """Creates a short-term memory for the muster."""
    def __managed_loop(self,manager: Agent,end_conditions: List[str], task_list: List[Task] = None,end_tasks:List[Task] = None) -> str:
        """Loop with the agent manager."""
        human_feedback = self.human_feedback
        agent_monitor = self.agent_monitor
        next_feedback = None        
        if task_list == None:
            task_list = self.tasks
        task_outcome = None
        task_desc_list = [(task,task.description) for task in task_list]
        is_end_state = False
        ## DENOTE THE END TASK LIST, IF NONE --> FILL ALL TASKS AS END TASK.  
        if end_tasks == None:
            end_tasks = task_list
        while(is_end_state == False):
                next_task = self.__select_next_task(manager,self.task_states,task_desc_list,end_conditions)
                print("next task selected")
                if next_feedback is not None:
                    human_context = next_feedback
                else:
                    human_context = ""
                if agent_monitor is not None:
                    agent_monitor.start_task(next_task)
                try:
                    task_outcome = next_task.execute(human_context)
                except Exception as e:
                    if agent_monitor is not None:
                        agent_monitor.error_task(next_task, str(e))
                    raise e
                if agent_monitor is not None:
                    agent_monitor.completed_task(next_task, task_outcome)
                print("task outcome:"+str(task_outcome))
                self.task_states.append((next_task.description,task_outcome))
                flag_end,new_endconditions,feedback_next = self.__parse_human_input(manager.llm)
                if flag_end == 1:
                    is_end_state = True
                else:
                    if new_endconditions is not None:
                        end_conditions.append(new_endconditions)
                    if feedback_next is not None:
                        next_feedback = feedback_next
                if next_task in end_tasks:
                    is_end_state = self.__check_end(manager.llm,self.task_states,end_conditions)
        print("Achieved END STATE!")
        return task_outcome