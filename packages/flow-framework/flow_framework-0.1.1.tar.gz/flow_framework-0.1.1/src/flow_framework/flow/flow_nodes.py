import json
from types import SimpleNamespace
from typing import Callable, List

from .constants import FlowNodeStatus
from .exceptions import FlowValidationError, RegisterParentError


class FlowNode:
    """Base class for flow and flow step."""

    def __init__(self, id: str, steps: List["FlowNode"]) -> None:
        """
        Create an instance of a flow node.
        """
        self.id = id
        self._steps = steps
        self.status = FlowNodeStatus.PENDING

    def run(self) -> None:
        raise NotImplementedError


class FlowStep(FlowNode):
    """Container class for flow step metadata and run function."""

    def __init__(
        self, id: str, calls: Callable, parent_steps: List["FlowStep"] = [], **kwargs
    ):
        """
        Create an instance of a flow step.

        Parameters
        ==========
        id: str - an identifier for the step, this should be unique to the flow
        calls: Callable - the function called by the step
        parent_steps: list[FlowStep], optional - a list of steps in the flow that this step will depend on
        **kwargs - any keyword arguments will be acessible through the FlowStep's `options` property.
        """
        super().__init__(id, parent_steps)
        self._calls = calls
        self._output = None
        self._options = None
        self.flow = None
        if kwargs:
            self.options = kwargs

    @property
    def options(self):
        return json.loads(
            json.dumps(self._options), object_hook=lambda d: SimpleNamespace(**d)
        )

    @options.setter
    def options(self, value: dict) -> None:
        if "inputs" in value.keys():
            raise ValueError('"inputs" is reserved and cannot be used as an option.')

        self._options = value

    @property
    def parent_steps(self):
        return self._steps

    @property
    def output(self):
        return self._output

    def register_parent(self, step: "FlowStep") -> None:
        """
        Add another step to the parents of the step on which the method is called.

        Parameters
        ==========
        step: FlowStep - the step to add to the parents.
        """
        if self.flow is not None:
            raise RegisterParentError(
                "A parent cannot be registered after the flow has been initialized."
            )
        self.parent_steps.append(step)

    def run(self) -> None:
        """
        Run the flow step.
        """
        if self.parent_steps:
            for parent_step in self.parent_steps:
                if parent_step.status == FlowNodeStatus.PENDING:
                    parent_step.run()

        if self._options:
            self._options["inputs"] = {
                parent_step.id: parent_step.output for parent_step in self.parent_steps
            }

        self.status = FlowNodeStatus.IN_PROGRESS
        self._output = self._calls(self)
        self.status = FlowNodeStatus.COMPLETED


class Flow(FlowNode):
    """
    Class for Flow metadata and nodes.
    """

    def __init__(self, id: str, steps: list["FlowStep"]) -> None:
        """
        Create an instance of a flow.
        """
        super().__init__(id, steps)
        for step in self._steps:
            step.flow = self

    def run(self) -> None:
        """
        Run the flow.
        """
        self.validate()
        self.status = FlowNodeStatus.IN_PROGRESS
        for step in self._steps:
            step.run()
        self.status = FlowNodeStatus.COMPLETED

    def validate(self) -> None:
        """
        Validate the flow.
        """
        ids = set()
        stack = set()

        def visit(step):
            if step.id in stack:
                raise FlowValidationError(f"Circular dependency detected: {step.id}")
            stack.add(step.id)
            for parent in step.parent_steps:
                visit(parent)

        for step in self._steps:
            if step.id in ids:
                raise FlowValidationError(
                    f"The step id {step.id} is not unique to the flow."
                )
            ids.add(step.id)
            stack.clear()
            visit(step)
