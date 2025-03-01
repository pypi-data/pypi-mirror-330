# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT license. See LICENSE for more info.

"""SMX pipeline subclass."""

import logging
from uuid import UUID

import numpy as np
import tango

from lima2.client import utils
from lima2.client.devencoded import (
    dense_frame,
    sparse_frame,
    structured_array,
)
from lima2.client.pipeline import FrameSource, Pipeline
from lima2.client.topology import TopologyKind

# Create a logger
logger = logging.getLogger(__name__)


class Smx(Pipeline):
    tango_class = "LimaProcessingSmx"

    # Members of type "saving_params" in the corresponding lima2 "proc_params" struct.
    SAVING_PARAMS_NAMES = [
        "saving_dense",
        "saving_sparse",
        "saving_accumulation_corrected",
        "saving_accumulation_peak",
    ]

    FRAME_SOURCES = {
        "frame": FrameSource(getter_name="getFrame", decoder=dense_frame.decode),
        "sparse_frame": FrameSource(
            getter_name="getSparseFrame", decoder=sparse_frame.decode
        ),
        "acc_corrected": FrameSource(
            getter_name="getAccCorrected", decoder=dense_frame.decode
        ),
        "acc_peaks": FrameSource(getter_name="getAccPeaks", decoder=dense_frame.decode),
    }
    """Available frame sources."""

    def __init__(
        self,
        uuid: UUID,
        proc_devs: list[tango.DeviceProxy],
        topology_kind: TopologyKind,
        timeout: int = Pipeline.DEFAULT_TANGO_TIMEOUT,
    ):
        super().__init__(
            uuid=uuid, proc_devs=proc_devs, topology_kind=topology_kind, timeout=timeout
        )

    @property
    def radius1d(self):
        """Returns the radius1d"""
        return [dense_frame.decode(dev.radius1d).data for dev in self._devs]

    @property
    def radius2d_mask(self):
        """Returns the radius2d_mask as np.array"""
        return [dense_frame.decode(dev.radius2d_mask).data for dev in self._devs]

    def pop_peak_counters(self) -> tuple[np.ndarray, np.ndarray]:
        """Pop peak counters from the server, return them ordered by frame index.

        Returns:
            A tuple (frame_indices, peak_counts) for each frame available from the server
            at the time of calling, where:
            - frame_indices is a ndarray of frame indices for each peak_count
            - peak_counts is a ndarray (of the same size) of the number of peaks on a frame
        """
        dtype = [
            ("frame_idx", "i4"),
            ("recv_idx", "i4"),
            ("nb_peaks", "i4"),
        ]

        # Use cached data from previous call
        cache = self.get_cached_byproduct(
            "peak_counters", default=np.array([], dtype=dtype)
        )

        # Pop counters for new frames from each receiver and concatenate, mixing in cached data.
        # Data comes from server as 1D array with size (num_frames)
        new_data = np.concatenate(
            [cache.flatten()]
            + [
                structured_array.decode(dev.popPeakCounters(), dtype)
                for dev in self._devs
            ]
        )

        logger.debug(f"Received peak counters for {new_data.shape[0]} frames")

        frame_indices = new_data["frame_idx"]
        frame_order = np.argsort(frame_indices)
        first_gap = utils.find_first_gap(frame_indices[frame_order])

        # Sort data by frame order
        data = new_data[frame_order]

        # Cache any data after the first frame gap for later
        self.cache_byproduct("peak_counters", data[first_gap:])

        # Now our data is contiguous
        data = data[:first_gap]

        logger.debug(f"Returning peak counters for frames: {data['frame_idx']}")

        return (data["frame_idx"], data["nb_peaks"])
