from enum import Enum
from typing import Any, Dict, List, Optional, Union


class ManagedProcess:
	def __init__(self, end_conditions: List[str],task_list:Optional[List[str]] = None, end_tasks: Optional[List[Any]] = None):
		self.name='managed'
		self.end_conditions=end_conditions
		self.task_list = task_list
		self.end_tasks = end_tasks
class SequentialProcess:
	def __init__(self):
		self.name='sequential'

class Process:
	"""
	Class representing the different processes that can be used to tackle tasks
	"""
	name='process'
	sequential = SequentialProcess()
	def managed(end_conditions,  
        end_tasks=None,task_list=None):
		manager = ManagedProcess(end_conditions=end_conditions,end_tasks=end_tasks,task_list=task_list)
		return manager

