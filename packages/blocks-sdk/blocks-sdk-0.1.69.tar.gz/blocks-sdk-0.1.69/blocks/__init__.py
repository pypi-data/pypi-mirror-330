from .repo import Repo
from .on import OnClass
from .task import TaskClass
from .state import BlocksState
from .utils import bash
from .git import Git

repo = Repo()
state = BlocksState()
task = TaskClass.get_decorator(state)
on = OnClass.get_decorator(state)
