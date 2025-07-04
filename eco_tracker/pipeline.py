from abc import abstractmethod
from typing import Callable, List, Optional, Protocol

# Weglassen des Typparameters Context
NextStep = Callable[[object], None]
ErrorHandler = Callable[[Exception, object, NextStep], None]

class PipelineStep(Protocol):
    @abstractmethod
    def __call__(self, context: object, next_step: NextStep) -> None:
        ...

class PipelineCursor:

    def __init__(self, steps: List[PipelineStep], error_handler: ErrorHandler):
        self.steps = steps
        self.error_handler = error_handler

    def __call__(self, context: object) -> None:
        if not self.steps:
            return

        current_step = self.steps[0]
        next_step = PipelineCursor(self.steps[1:], self.error_handler)

        try:
            current_step(context, next_step)
        except Exception as e:
            self.error_handler(e, context, next_step)

def _default_error_handler(error: Exception, context: object, next_step: NextStep) -> None:
    raise error

class Pipeline:
    def __init__(self, *steps: PipelineStep):
        self.steps = [step for step in steps]

    def append(self, step: PipelineStep) -> None:
        self.steps.append(step)

    def __call__(self, context: object, error_handler: Optional[ErrorHandler] = None) -> None:
        execute = PipelineCursor(self.steps, error_handler or _default_error_handler)
        execute(context)

    def __len__(self) -> int:
        return len(self.steps)
