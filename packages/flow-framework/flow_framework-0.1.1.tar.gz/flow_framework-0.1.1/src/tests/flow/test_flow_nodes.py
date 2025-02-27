import pytest

from flow_framework.flow.constants import FlowNodeStatus
from flow_framework.flow.exceptions import (FlowValidationError,
                                            RegisterParentError)
from flow_framework.flow.flow_nodes import Flow, FlowStep


@pytest.fixture
def dummy_function():
    return lambda step: "output"


def test_flow_step_initialization(dummy_function):
    step = FlowStep(id="step1", calls=dummy_function)
    assert step.id == "step1"
    assert step._calls == dummy_function
    assert step.status == FlowNodeStatus.PENDING
    assert step.parent_steps == []


def test_flow_step_run(dummy_function):
    step = FlowStep(id="step1", calls=dummy_function)
    step.run()
    assert step.status == FlowNodeStatus.COMPLETED
    assert step.output == "output"


def test_flow_initialization(dummy_function):
    step1 = FlowStep(id="step1", calls=dummy_function)
    step2 = FlowStep(id="step2", calls=dummy_function, parent_steps=[step1])
    flow = Flow(id="flow1", steps=[step1, step2])
    assert flow.id == "flow1"
    assert flow._steps == [step1, step2]
    assert flow.status == FlowNodeStatus.PENDING
    assert step1.flow == flow
    assert step2.flow == flow


def test_flow_run(dummy_function):
    step1 = FlowStep(id="step1", calls=dummy_function)
    step2 = FlowStep(id="step2", calls=dummy_function, parent_steps=[step1])
    flow = Flow(id="flow1", steps=[step1, step2])
    flow.run()
    assert flow.status == FlowNodeStatus.COMPLETED
    assert step1.status == FlowNodeStatus.COMPLETED
    assert step2.status == FlowNodeStatus.COMPLETED


def test_flow_validation_unique_ids(dummy_function):
    step1 = FlowStep(id="step1", calls=dummy_function)
    step2 = FlowStep(id="step1", calls=dummy_function)  # Duplicate ID
    flow = Flow(id="flow1", steps=[step1, step2])
    with pytest.raises(
        FlowValidationError, match="The step id step1 is not unique to the flow."
    ):
        flow.validate()


def test_flow_validation_circular_dependency(dummy_function):
    step1 = FlowStep(id="step1", calls=dummy_function)
    step2 = FlowStep(id="step2", calls=dummy_function, parent_steps=[step1])
    step1.register_parent(step2)  # Circular dependency
    flow = Flow(id="flow1", steps=[step1, step2])
    with pytest.raises(
        FlowValidationError, match="Circular dependency detected: step1"
    ):
        flow.validate()


def test_register_step_after_adding_flow(dummy_function):
    step1 = FlowStep(id="step1", calls=dummy_function)
    step2 = FlowStep(id="step2", calls=dummy_function, parent_steps=[step1])
    step3 = FlowStep(id="step3", calls=dummy_function)
    flow = Flow(id="flow1", steps=[step1, step2, step3])  # noqa: F841
    with pytest.raises(
        RegisterParentError,
        match="A parent cannot be registered after the flow has been initialized.",
    ):
        step3.register_parent(step2)
