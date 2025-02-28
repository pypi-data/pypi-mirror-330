from unittest.mock import MagicMock

import pytest
from psychopy.tests.test_experiment.test_components.test_base_components import (
    BaseComponentTests,
)

from psychopy_bids.bids_event import BidsEventComponent


class TestBidsEventComponent(BaseComponentTests):
    comp = BidsEventComponent

    def test_disabled_code_muting(self):
        pytest.skip(
            "validateBIDSEventParams raise ValueError won't work with this test"
        )

    def test_validateBIDSEventParams_with_all_valid_conditions(self):
        component = self.comp(MagicMock(), "parent")

        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["onset"] = MagicMock(val="1.0")
        component.params["bids_duration"] = MagicMock(val="2.0")
        component.params["linked_attributes"] = MagicMock(
            val=["onset", "bids_duration"]
        )
        component.params["overwrite_linked"] = MagicMock(val=True)
        component.params["link_component"] = MagicMock(val="valid_component")

        # Mock self.exp.routines to include a 'BIDSexport' routine
        mock_routine = MagicMock()
        mock_routine.type = "BIDSexport"
        routine_name = "someRoutine"
        component.exp.routines = {routine_name: mock_routine}

        # Mock self.exp.flow to include the routine name
        mock_flow_element = MagicMock()
        mock_flow_element.name = routine_name
        component.exp.flow = [mock_flow_element]

        # Mock linked component
        linked_component = MagicMock()
        linked_component.parentName = "parentComponent"
        component.exp.getComponentFromName = MagicMock(return_value=linked_component)

        try:
            component.validateBIDSEventParams()
        except ValueError as e:
            pytest.fail(f"validateBIDSEventParams raised ValueError unexpectedly: {e}")
        except AttributeError as e:
            pytest.fail(
                f"validateBIDSEventParams raised AttributeError unexpectedly: {e}"
            )

    def test_validateBIDSEventParams_missing_routine(self):
        component = self.comp(MagicMock(), "parent")

        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["onset"] = MagicMock(val="1.0")
        component.params["bids_duration"] = MagicMock(val="2.0")
        component.params["linked_attributes"] = MagicMock(val=[])
        component.params["overwrite_linked"] = MagicMock(val=True)

        # No routines present
        component.exp.routines = {}

        with pytest.raises(
            ValueError, match="A routine with type 'BIDSexport' is required"
        ):
            component.validateBIDSEventParams()

    def test_validateBIDSEventParams_routine_not_in_flow(self):
        component = self.comp(MagicMock(), "parent")

        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["onset"] = MagicMock(val="1.0")
        component.params["bids_duration"] = MagicMock(val="2.0")
        component.params["linked_attributes"] = MagicMock(val=[])
        component.params["overwrite_linked"] = MagicMock(val=True)

        # Mock self.exp.routines to include a 'BIDSexport' routine
        mock_routine = MagicMock()
        mock_routine.type = "BIDSexport"
        component.exp.routines = {"someRoutine": mock_routine}

        # Routine not in flow
        component.exp.flow = []

        with pytest.raises(ValueError, match="exists but is not included in the flow"):
            component.validateBIDSEventParams()

    def test_validateBIDSEventParams_invalid_linked_component(self):
        component = self.comp(MagicMock(), "parent")

        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["onset"] = MagicMock(val="1.0")
        component.params["bids_duration"] = MagicMock(val="2.0")
        component.params["linked_attributes"] = MagicMock(val=["onset"])
        component.params["overwrite_linked"] = MagicMock(val=False)
        component.params["link_component"] = MagicMock(val="nonexistent_component")

        # Mock self.exp.routines to include a 'BIDSexport' routine
        mock_routine = MagicMock()
        mock_routine.type = "BIDSexport"
        component.exp.routines = {"someRoutine": mock_routine}

        # Mock self.exp.flow to include the routine name
        mock_flow_element = MagicMock()
        mock_flow_element.name = "someRoutine"
        component.exp.flow = [mock_flow_element]

        # Linked component does not exist
        component.exp.getComponentFromName = MagicMock(return_value=None)

        with pytest.raises(
            AttributeError,
            match="The linked component 'nonexistent_component' specified in the link textbox is invalid",
        ):
            component.validateBIDSEventParams()

    def test_validateBIDSEventParams_missing_onset_and_duration(self):
        component = self.comp(MagicMock(), "parent")

        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["onset"] = MagicMock(val="")
        component.params["bids_duration"] = MagicMock(val="")
        component.params["linked_attributes"] = MagicMock(val=[])
        component.params["overwrite_linked"] = MagicMock(val=True)

        # Mock self.exp.routines to include a 'BIDSexport' routine
        mock_routine = MagicMock()
        mock_routine.type = "BIDSexport"
        component.exp.routines = {"someRoutine": mock_routine}

        # Mock self.exp.flow to include the routine name
        mock_flow_element = MagicMock()
        mock_flow_element.name = "someRoutine"
        component.exp.flow = [mock_flow_element]

        with pytest.raises(
            ValueError, match="Please verify your inputs and linked attribute settings."
        ):
            component.validateBIDSEventParams()

    def test_writeRoutineEndCode(self):
        component = self.comp(MagicMock(), "parent")

        # Mock buffer and initialization values
        mock_buff = MagicMock()
        mock_buff.indentLevel = 0

        component.params["name"] = MagicMock(val="testEvent")
        component.params["onset"] = MagicMock(val="1.0")
        component.params["bids_duration"] = MagicMock(val="2.0")
        component.params["response_time"] = MagicMock(val="0.5")
        component.params["linked_attributes"] = MagicMock(val=[])
        component.params["custom"] = MagicMock(val="{'extra_column': 'value'}")
        component.params["bids_event_type"] = MagicMock(val="TaskEvent")
        component.params["link_component"] = MagicMock(val="")
        component.exp.flow._loopList = [
            MagicMock(type="TrialHandler", params={"name": "trialLoop"})
        ]

        try:
            component.writeRoutineEndCode(mock_buff)
        except Exception as e:
            pytest.fail(f"writeRoutineEndCode raised an unexpected exception: {e}")

        mock_buff.writeIndentedLines.assert_called()
        mock_buff.writeIndentedLines.assert_any_call("bids_event = BIDSTaskEvent(\n")

    def test_writeRoutineEndCode_no_loop(self):
        component = self.comp(MagicMock(), "parent")

        # Mock buffer and remove loopList
        mock_buff = MagicMock()
        component.exp.flow._loopList = []

        try:
            component.writeRoutineEndCode(mock_buff)
        except Exception as e:
            pytest.fail(
                f"writeRoutineEndCode raised an unexpected exception without loops: {e}"
            )