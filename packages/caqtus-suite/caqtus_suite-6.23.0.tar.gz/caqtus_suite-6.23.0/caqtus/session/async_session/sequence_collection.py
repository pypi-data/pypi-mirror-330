import abc
import datetime
from collections.abc import Mapping
from typing import Protocol, Optional

from caqtus.types.data import DataLabel, Data
from caqtus.types.iteration import IterationConfiguration
from caqtus.types.parameter import Parameter, ParameterNamespace
from caqtus.types.timelane import TimeLanes
from caqtus.types.variable_name import DottedVariableName
from caqtus.utils.result import Success, Failure
from .._data_id import DataId
from .._exception_summary import TracebackSummary
from .._path import PureSequencePath
from .._path_hierarchy import PathNotFoundError
from .._sequence_collection import (
    PathIsNotSequenceError,
    SequenceNotEditableError,
    SequenceStats,
    SequenceNotCrashedError,
    SequenceNotRunningError,
    InvalidStateTransitionError,
    SequenceNotLaunchedError,
)
from .._shot_id import ShotId
from .._state import State


class AsyncSequenceCollection(Protocol):
    @abc.abstractmethod
    async def is_sequence(
        self, path: PureSequencePath
    ) -> Success[bool] | Failure[PathNotFoundError]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_stats(
        self, path: PureSequencePath
    ) -> (
        Success[SequenceStats]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
    ):
        raise NotImplementedError

    async def get_state(
        self, path: PureSequencePath
    ) -> Success[State] | Failure[PathNotFoundError] | Failure[PathIsNotSequenceError]:

        return (await self.get_stats(path)).map(lambda stats: stats.state)

    @abc.abstractmethod
    async def reset_to_draft(
        self, path: PureSequencePath
    ) -> (
        Success[None]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[InvalidStateTransitionError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_traceback_summary(
        self, path: PureSequencePath
    ) -> (
        Success[Optional[TracebackSummary]]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[SequenceNotCrashedError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_iteration_configuration(
        self, path: PureSequencePath
    ) -> IterationConfiguration:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_iteration_configuration(
        self, path: PureSequencePath, iteration_configuration: IterationConfiguration
    ) -> (
        None
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[SequenceNotEditableError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_time_lanes(
        self, path: PureSequencePath
    ) -> TimeLanes | Failure[PathNotFoundError] | Failure[PathIsNotSequenceError]:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_time_lanes(
        self, path: PureSequencePath, time_lanes: TimeLanes
    ) -> (
        None
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[SequenceNotEditableError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_global_parameters(
        self, path: PureSequencePath
    ) -> (
        Success[ParameterNamespace]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[SequenceNotLaunchedError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_shots(
        self, path: PureSequencePath
    ) -> (
        Success[list[ShotId]]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_shot_parameters(
        self, path: PureSequencePath, shot_index: int
    ) -> Mapping[DottedVariableName, Parameter]:

        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_shot_data(
        self, path: PureSequencePath, shot_index: int
    ) -> Mapping[DataLabel, Data]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_shot_data_by_label(self, data: DataId) -> Data:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_shot_start_time(
        self, path: PureSequencePath, shot_index: int
    ) -> datetime.datetime:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_shot_end_time(
        self, path: PureSequencePath, shot_index: int
    ) -> datetime.datetime:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_shot(
        self,
        shot_id: ShotId,
        shot_parameters: Mapping[DottedVariableName, Parameter],
        shot_data: Mapping[DataLabel, Data],
        shot_start_time: datetime.datetime,
        shot_end_time: datetime.datetime,
    ) -> (
        Success[None]
        | Failure[PathNotFoundError]
        | Failure[PathIsNotSequenceError]
        | Failure[SequenceNotRunningError]
    ):
        raise NotImplementedError
