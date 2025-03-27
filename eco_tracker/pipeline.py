
from abc import abstractmethod
from typing import Protocol, TypeVar, Callable, Iterable, Union, List, Optional

Context = TypeVar('Context')
# NextStep is a function that takes a context and returns an iterable of contexts or exceptions
# It has the same signature as the PipelineCursor.__call__ method
NextStep = Callable[[Context], Iterable[Union[Exception, Context]]]
ErrorHandler = Callable[[Exception, Context, NextStep], None]

class PipelineStep[Context](Protocol):
	@abstractmethod
	def __call__(
		self, context: Context, next_step: NextStep[Context]
	) -> None:
		...

class PipelineCursor[Context]:

	def __init__(self, steps: List[PipelineStep], error_handler: ErrorHandler):
		self.steps = steps
		self.error_handler: ErrorHandler = error_handler

	def __call__(self, context: Context) -> None:
		if not self.steps:
			return

		current_step = self.steps[0]
		next_step = PipelineCursor(self.steps[1:], self.error_handler)

		try:
			current_step(context, next_step)
		except Exception as e:
			self.error_handler(e, context, next_step)

def _default_error_handler(error: Exception, context: Context, next_step: NextStep) -> None:
	raise error

class Pipeline[Context]:
	def __init__(self, *steps: PipelineStep):
		self.steps = [step for step in steps]

	def append(self, step: PipelineStep) -> None:
		self.steps.append(step)

	def __call__(self, context: Context, error_handler: Optional[ErrorHandler] = None) -> None:
		execute = PipelineCursor(self.steps, error_handler or _default_error_handler)
		execute(context)

	def __len__(self) -> int:
		return len(self.steps)

