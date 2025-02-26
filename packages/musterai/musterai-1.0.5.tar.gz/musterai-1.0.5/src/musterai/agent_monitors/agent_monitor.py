import sqlite3
from typing import List,Tuple, Optional, Any, Union, Dict
from musterai.memory.long_term_memory.ltmsqlite import LTMSqlite
import threading
from datetime import datetime
from musterai.task import Task
from dataclasses import dataclass
from pydantic import (
    BaseModel,
    Field,
    InstanceOf,
    Json,
    field_validator,
    model_validator,
)
import os
from enum import Enum
import random
class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class TaskInfo:
    description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: AgentStatus = AgentStatus.IDLE
    output: Optional[str] = None
    error: Optional[str] = None

class AgentMonitor:
    db_path: str = Field(description="The default database path for the agent monitor",default=os.getenv("MONITORING_DB_PATH"))
    db: Union[LTMSqlite] = Field(default=None)
    db_type: str = Field(description="The type of database to use for the agent monitor",default="sqlite")
    kickoff_id: int = Field(description="The ID of the kickoff that created this monitor.",default=None)
    process_type: str = Field(description="The type of process that the agent monitor is monitoring.",default=None)
    def __init__(self, tasks: List[Task],db_path: str = os.getenv("MONITORING_DB_PATH"),db_type: str = "sqlite",kickoff_id: int = None,process_type: str = None):
        """Intializes the agent monitor."""
        self._lock = threading.Lock()
        self.kickoff_id = kickoff_id
        self.process_type = process_type
        self.init_db(db_path=db_path,db_type=db_type)
        self.task_id_map: Dict[str, int] = {}
        self._agents_status: Dict[str, Dict[str, TaskInfo]] = {}
        for task in tasks:
            self.task_id_map[task.description] = self.generate_agent_id()
            self.register_agent(self.task_id_map[task.description])
    def generate_agent_id(self):
        """Generates an Agent ID for a new agent."""
        with self._lock:
            if len(self.task_id_map.values()) > 10000:
                print("Monitoring more than 10000 at once is not reccomended. Some agent IDs may overlap.")
                randnm = random.randint(1, 99999)
                return randnm
            else:
                flag = 0
                while(flag < 1):
                    randnm = random.randint(1, 99999)
                    if randnm not in self.task_id_map.values():
                        flag = 1
            return randnm
    def register_agent(self, agent: int):
        """Register an agent in the database."""
        with self._lock:
            if agent not in self._agents_status:
                self._agents_status[agent] = {}
    def init_db(self, db_path: str, db_type: str = "sqlite"):
        """Intializes the database to store the logs of the agents. Default: sqlite."""
        if db_type == "sqlite":
            self.db = LTMSqlite(db_path)
            self.db.connect()
            self.db.create_table("agent_monitor",["kickoff_id","process_type","agent", "task", "status", "timestamp", "description", "output", "error", "start_time", "end_time"])
    def start_task(self, task: Task):
        """When an agent starts a task, log the event in the database."""
        with self._lock:
            try:
                agent = self.task_id_map[task.description]
            except KeyError:
                print("Agent ID not found in logging database. Generating new Agent ID...")
                agent = self.generate_agent_id()
                self.task_id_map[task.description] = agent
            task_info = TaskInfo(description=task.description,start_time=datetime.now(),status=AgentStatus.WORKING)
            self._agents_status[agent][task.description] = task_info
            self.log_event(agent, task, AgentStatus.WORKING, task_info)
    def completed_task(self, task: Task, task_output: str):
        """Changes the status of an ongoing task by an agent to COMPLETED."""
        with self._lock:
            try:
                agent = self.task_id_map[task.description]
            except KeyError:
                print("AGENT MONITOR could not fetch the agent ID. Creating New Agent ID...")
                agent = self.generate_agent_id()
                self.task_id_map[task.description] = agent
                self._agents_status[agent][task.description] = TaskInfo(description=task.description,start_time=datetime.now(),status=AgentStatus.WORKING)
            self._agents_status[agent][task.description].status = AgentStatus.COMPLETED
            self._agents_status[agent][task.description].end_time = datetime.now()
            self._agents_status[agent][task.description].output = task_output
            self.log_event(agent, task, AgentStatus.COMPLETED, self._agents_status[agent][task.description])
    def error_task(self, task: Task, error: str):
        """Logs the event when an agent encounters an error executing a task."""
        with self._lock:
            try:
                agent = self.task_id_map[task.description]
            except KeyError as e:
                print("Agent not found in the database, could not register this error under it's ID:"+str(error))
            self._agents_status[agent][task.description].status = AgentStatus.ERROR
            self._agents_status[agent][task.description].error = error
            self._agents_status[agent][task.description].end_time = datetime.now()
            self.log_event(agent, task, AgentStatus.ERROR, self._agents_status[agent][task.description])
    def get_agent_status(self, task: Task):
        with self._lock:
            try:
                agent = self.task_id_map[task.description]
            except KeyError:
                return "Agent not found in the database."
            return self._agents_status[agent][task.description].status
    def get_all_agent_status(self):
        with self._lock:
            return self._agents_status
    def get_agent_status_db(self, agent: int):
        """Fetches all the columns of the agent ID from the database. Orders by timestamp."""
        with self._lock:
            data = self.db.select("agent_monitor",columns=["task","status","timestamp","description","output","error","start_time","end_time"],where_condition="agent=?",params=(agent,))
            return data
    def get_all_agents(self):
        """Gets all the agent IDs from the database."""
        try:
            with self._lock:
                return self.db.select("agent_monitor",columns=["agent"],distinct=True)
        except Exception as e:
            return "Error in fetching all agents: "+str(e) 
    def log_event(self, agent: int, task: Task, status: AgentStatus, task_info: TaskInfo):
        start =  task_info.start_time.isoformat() if task_info.start_time else None
        end = task_info.end_time.isoformat() if task_info.end_time else None
        self.db.insert(
            "agent_monitor",
            [("kickoff_id",self.kickoff_id),("process_type",self.process_type),("agent",agent),("task",task.description),("status",status.value),("timestamp",datetime.now().isoformat()),("description",task_info.description),("output",task_info.output),("error",task_info.error),
             ("start_time",start),("end_time",end)]
        )