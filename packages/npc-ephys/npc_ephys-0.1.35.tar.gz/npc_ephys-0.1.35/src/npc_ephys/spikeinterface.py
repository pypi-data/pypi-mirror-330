"""
Helper functions for getting paths from spikeinterface output (developed for use
with the aind kilosort 2.5 "pipeline" spike-sorting capsule).
"""

from __future__ import annotations

import contextlib
import dataclasses
import functools
import io
import json
import logging
from typing import Union

import hdmf_zarr
import npc_io
import npc_lims
import npc_session
import numpy as np
import numpy.typing as npt
import packaging.version
import pandas as pd
import pynwb
import upath
import zarr
from typing_extensions import TypeAlias

logger = logging.getLogger(__name__)

SpikeInterfaceData: TypeAlias = Union[
    str, npc_session.SessionRecord, npc_io.PathLike, "SpikeInterfaceKS25Data"
]


class ProbeNotFoundError(FileNotFoundError):
    pass


def get_spikeinterface_data(
    session_or_root_path: SpikeInterfaceData,
) -> SpikeInterfaceKS25Data:
    """Return a SpikeInterfaceKS25Data object for a session.

    >>> paths = get_spikeinterface_data('668759_20230711')
    >>> paths.root == get_spikeinterface_data('s3://codeocean-s3datasetsbucket-1u41qdg42ur9/83754308-0a91-4b54-af79-3c42f6bc831b').root
    True
    """
    if isinstance(session_or_root_path, SpikeInterfaceKS25Data):
        return session_or_root_path
    try:
        session = npc_session.SessionRecord(str(session_or_root_path))
        root = None
    except ValueError:
        session = None
        root = npc_io.from_pathlike(session_or_root_path)
    return SpikeInterfaceKS25Data(session=session, root=root)


@dataclasses.dataclass(unsafe_hash=True, eq=True)
class SpikeInterfaceKS25Data:
    """The root directory of the result data asset produced by the 'pipeline'
    KS2.5 sorting capsule contains `processing.json`, `postprocessed`,
    `spikesorted`, etc. This class just simplifies access to the data in those
    files and dirs.

    Provide a session ID or a root path:
    >>> si = SpikeInterfaceKS25Data('668759_20230711')
    >>> si.root
    S3Path('s3://codeocean-s3datasetsbucket-1u41qdg42ur9/83754308-0a91-4b54-af79-3c42f6bc831b')

    >>> si.template_metrics_dict('probeA')
    {'metric_names': ['exp_decay', 'half_width', 'num_negative_peaks', 'num_positive_peaks', 'peak_to_valley', 'peak_trough_ratio', 'recovery_slope', 'repolarization_slope', 'spread', 'velocity_above', 'velocity_below'], 'sparsity': None, 'peak_sign': 'neg', 'upsampling_factor': 10, 'metrics_kwargs': {'recovery_window_ms': 0.7, 'peak_relative_threshold': 0.2, 'peak_width_ms': 0.1, 'depth_direction': 'y', 'min_channels_for_velocity': 5, 'min_r2_velocity': 0.5, 'exp_peak_function': 'ptp',
    'min_r2_exp_decay': 0.5, 'spread_threshold': 0.2, 'spread_smooth_um': 20, 'column_range': None}}

    >>> si.quality_metrics_df('probeA').columns
    Index(['amplitude_cutoff', 'amplitude_cv_median', 'amplitude_cv_range',
           'amplitude_median', 'drift_ptp', 'drift_std', 'drift_mad',
           'firing_range', 'firing_rate', 'isi_violations_ratio',
           'isi_violations_count', 'num_spikes', 'presence_ratio',
           'rp_contamination', 'rp_violations', 'sliding_rp_violation', 'snr',
           'sync_spike_2', 'sync_spike_4', 'sync_spike_8', 'd_prime',
           'isolation_distance', 'l_ratio', 'silhouette', 'nn_hit_rate',
           'nn_miss_rate'],
          dtype='object')
    >>> si.version
    '0.100.0'
    >>> ''.join(si.probes)
    'ABCDEF'
    >>> si.spike_indexes('probeA')
    array([      145,       491,       738, ..., 143124925, 143125165, 143125201])
    >>> si.unit_indexes('probeA')
    array([ 36,  50,  55, ...,  52, 132,  53])
    >>> len(si.original_cluster_id('probeA'))
    139
    >>> si = SpikeInterfaceKS25Data('712815_2024-05-21')
    >>> si.is_nextflow_pipeline
    True
    """

    session: str | npc_session.SessionRecord | None = None
    root: upath.UPath | None = None

    def __post_init__(self) -> None:
        if self.root is None and self.session is None:
            raise ValueError("Must provide either session or root")
        if self.root is None:
            self.root = npc_lims.get_sorted_data_paths_from_s3(self.session)[0].parent

    @property
    def probes(self) -> tuple[npc_session.ProbeRecord, ...]:
        """Probes available from this SpikeInterface dataset, with full set of
        data (probe is present in "curated" container)."""
        probes = set()
        try:
            dir_path = self.get_path("sorting_precurated")
        except FileNotFoundError:
            dir_path = self.get_path("curated")
        for path in dir_path.iterdir():
            with contextlib.suppress(ValueError):
                probes.add(npc_session.ProbeRecord(path.name))
        return tuple(sorted(probes))

    @property
    def is_nextflow_pipeline(self) -> bool:
        if self.root is not None:
            return (
                "N E X T F L O W" in self.output().read_text()
            )  # update to codeocean, where nextflow folder no longer part of result

        return False

    @property
    def version(self) -> str:
        if not self.is_nextflow_pipeline:
            return self.provenance(self.probes[0])["kwargs"]["parent_sorting"][
                "version"
            ]

        return self.provenance(self.probes[0])["version"]

    @property
    def is_pre_v0_99(self) -> bool:
        return packaging.version.parse(self.version) < packaging.version.parse("0.99")

    @staticmethod
    @functools.cache
    def get_correct_path(*path_components: npc_io.PathLike) -> upath.UPath:
        """SpikeInterface makes paths with '#' in them, which is not allowed in s3
        paths in general - run paths through this function to fix them."""
        if not path_components:
            raise ValueError("Must provide at least one path component")
        path = npc_io.from_pathlike("/".join(str(path) for path in path_components))
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
        return path

    @staticmethod
    def read_json(path: upath.UPath) -> dict:
        return json.loads(path.read_text())

    @staticmethod
    def read_csv(path: upath.UPath) -> pd.DataFrame:
        return pd.read_csv(path, index_col=0)

    def get_json(self, filename: str) -> dict:
        assert self.root is not None
        return self.read_json(self.get_correct_path(self.root, filename))

    def get_path(
        self,
        dirname: str,
        probe: str | None = None,
        excl_name_component: str | None = None,
    ) -> upath.UPath:
        """Return a path to a single dir or file: either `self.root/dirname` or, if `probe` is specified,
        the probe-specific sub-path within `self.root/dirname`."""
        assert self.root is not None
        if not dirname:
            raise ValueError("Must provide a dirname to get path")
        path: upath.UPath | None
        if probe is None:
            path = self.get_correct_path(self.root, dirname)
            if not path.exists():
                raise FileNotFoundError(f"{path} does not exist")
        else:
            path = next(
                (
                    path
                    for path in sorted(
                        self.get_correct_path(self.root, dirname).iterdir()
                    )
                    if npc_session.ProbeRecord(probe)
                    == npc_session.ProbeRecord(path.as_posix())
                    and (
                        excl_name_component is None
                        or excl_name_component not in path.name
                    )
                ),
                None,
            )
            if path is None or not path.exists():
                raise ProbeNotFoundError(
                    f"{path} does not exist - sorting likely skipped by SpikeInterface due to fraction of bad channels"
                )
        return path

    # json data
    processing_json = functools.partialmethod(get_json, "processing.json")
    subject_json = functools.partialmethod(get_json, "subject.json")
    data_description_json = functools.partialmethod(get_json, "data_description.json")
    procedures_json = functools.partialmethod(get_json, "procedures.json")
    visualization_output_json = functools.partialmethod(
        get_json, "visualization_output.json"
    )

    # dirs
    drift_maps = functools.partialmethod(get_path, dirname="drift_maps")
    output = functools.partialmethod(get_path, dirname="output")
    postprocessed = functools.partialmethod(
        get_path, dirname="postprocessed", excl_name_component="sorting"
    )
    spikesorted = functools.partialmethod(
        get_path, dirname="spikesorted", excl_name_component="sorting"
    )

    @functools.cache
    def curated(self, probe: str) -> upath.UPath:
        """Path changed Jan 2024

        https://github.com/AllenNeuralDynamics/aind-ephys-spikesort-kilosort25-full/blob/main/RELEASE_NOTES.md#v30---jan-18-2024
        """
        try:
            dir_path = self.get_path("sorting_precurated")
        except FileNotFoundError:
            dir_path = self.get_path("curated")
        return self.get_path(dir_path.name, probe)

    @functools.cache
    def quality_metrics_dict(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(
                self.postprocessed(probe=probe), "quality_metrics", "params.json"
            )
        )

    @functools.cache
    def postprocessed_params_dict(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(self.postprocessed(probe=probe), "params.json")
        )

    @functools.cache
    def quality_metrics_df(self, probe: str) -> pd.DataFrame:
        return self.read_csv(
            self.get_correct_path(
                self.postprocessed(probe=probe), "quality_metrics", "metrics.csv"
            )
        )

    @functools.cache
    def template_metrics_dict(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(
                self.postprocessed(probe=probe), "template_metrics", "params.json"
            )
        )

    @functools.cache
    def template_metrics_df(self, probe: str) -> pd.DataFrame:
        return self.read_csv(
            self.get_correct_path(
                self.postprocessed(probe=probe), "template_metrics", "metrics.csv"
            )
        )

    def templates_average(self, probe: str) -> npt.NDArray[np.floating]:
        logger.debug("Loading templates_average.npy for %s - typically ~200 MB", probe)
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.postprocessed(probe=probe), "templates_average.npy"
                ).read_bytes()
            )
        )

    def templates_std(self, probe: str) -> npt.NDArray[np.floating]:
        logger.debug("Loading templates_std.npy for %s - typically ~200 MB", probe)
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.postprocessed(probe=probe), "templates_std.npy"
                ).read_bytes()
            )
        )

    @functools.cache
    def sorting_cached(self, probe: str) -> dict[str, npt.NDArray]:
        if not self.is_pre_v0_99:
            raise AttributeError("sorting_cached.npz not used for SpikeInterface>=0.99")
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.curated(probe), "sorting_cached.npz"
                ).read_bytes()
            ),
            allow_pickle=True,
        )

    @functools.cache
    def provenance(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(self.curated(probe), "provenance.json")
        )

    @functools.cache
    def sparsity(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(self.postprocessed(probe=probe), "sparsity.json")
        )

    @functools.cache
    def numpysorting_info(self, probe: str) -> dict:
        if self.is_pre_v0_99:
            raise AttributeError(
                "numpysorting_info.json not used for SpikeInterface<0.99"
            )
        return self.read_json(
            self.get_correct_path(self.curated(probe), "numpysorting_info.json")
        )

    @functools.cache
    def spikes_npy(self, probe: str) -> npt.NDArray[np.floating]:
        """format: array[(sample_index, unit_index, segment_index), ...]"""
        if self.is_pre_v0_99:
            raise AttributeError("spikes.npy not used for SpikeInterface<0.99")
        if self.numpysorting_info(probe)["num_segments"] > 1:
            raise AttributeError("num_segments > 1 not supported yet")
        return np.load(
            io.BytesIO(
                self.get_correct_path(self.curated(probe), "spikes.npy").read_bytes()
            )
        )

    @functools.cache
    def spike_indexes(self, probe: str) -> npt.NDArray[np.floating]:
        if self.is_pre_v0_99:
            original = self.sorting_cached(probe)["spike_indexes_seg0"]
        else:
            original = np.array([v[0] for v in self.spikes_npy(probe)])
        return original

    @functools.cache
    def unit_indexes(self, probe: str) -> npt.NDArray[np.int64]:
        if self.is_pre_v0_99:
            original = self.sorting_cached(probe)["spike_labels_seg0"]
        else:
            original = np.array([v[1] for v in self.spikes_npy(probe)])
        return original

    @functools.cache
    def cluster_indexes(self, probe: str) -> npt.NDArray[np.int64]:
        return np.take_along_axis(
            self.unit_indexes(probe, de_duplicated=False),
            self.original_cluster_id(probe),
            axis=0,
        )

    def device_indices_in_nwb_units(
        self, probe: str | npc_session.ProbeRecord
    ) -> npt.NDArray:
        probe = npc_session.ProbeRecord(probe)
        devices = np.array(
            [
                npc_session.ProbeRecord(device)
                for device in self.nwb_zarr["units/device_name"][:]
            ]
        )

        return np.argwhere(devices == probe).squeeze()

    def get_nwb_units_device_property(self, metric: str, probe: str) -> npt.NDArray:
        return self.nwb_zarr[f"units/{metric}"][
            self.device_indices_in_nwb_units(probe)
        ].squeeze()

    @functools.cache
    def original_cluster_id(self, probe: str) -> npt.NDArray[np.int64]:
        """Array of cluster IDs, one per unit in unique('unit_indexes')"""
        if self.is_nextflow_pipeline:
            return self.get_nwb_units_device_property("ks_unit_id", probe).astype(
                np.int64
            )

        with contextlib.suppress(FileNotFoundError):
            return np.array(
                io.BytesIO(
                    self.get_correct_path(
                        self.curated(probe),
                        "properties",
                        "original_cluster_id.npy",
                    ).read_bytes()
                )
            )

        if self.is_pre_v0_99:
            # TODO! verify this is correct
            return self.sorting_cached(probe)["unit_ids"]

        raise ValueError(
            f"Unknown format of sorted output for SI {self.version=}, {self.is_nextflow_pipeline=}. As of March 2024 only handles 0.100 and lower"
        )

    @npc_io.cached_property
    def nwb_path(self) -> upath.UPath:
        if not self.is_nextflow_pipeline:
            raise ValueError("NWB not part of output from stand alone capsule")

        assert self.root is not None
        return next((self.root / "nwb").glob("*.nwb"))

    @npc_io.cached_property
    def nwb_zarr(self) -> zarr.hierarchy.Group:
        return zarr.open(self.nwb_path, mode="r")

    @npc_io.cached_property
    def nwb_file(self) -> pynwb.NWBFile:
        return hdmf_zarr.NWBZarrIO(path=self.nwb_path.as_posix(), mode="r").read()

        path = next((self.root / "nwb").glob("*.nwb"))
        return hdmf_zarr.NWBZarrIO(path=path.as_posix(), mode="r").read()

    @functools.cache
    def default_qc(self, probe: str) -> npt.NDArray[np.floating]:
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.curated(probe), "properties", "default_qc.npy"
                ).read_bytes()
            )
        )

    @functools.cache
    def decoder_probability(self, probe: str) -> npt.NDArray[np.floating]:
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.curated(probe), "properties", "decoder_probability.npy"
                ).read_bytes()
            )
        )

    @functools.cache
    def decoder_label(self, probe: str) -> npt.NDArray[np.str_]:
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.curated(probe), "properties", "decoder_label.npy"
                ).read_bytes()
            ),
            allow_pickle=True,
        )

    @functools.cache
    def spike_amplitudes(self, probe: str) -> tuple[npt.NDArray[np.floating], ...]:
        """array of amplitudes for each unit in order of unique('unit_indexes')"""
        spike_amplitudes = np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.postprocessed(probe=probe),
                    "spike_amplitudes",
                    "amplitude_segment_0.npy",
                ).read_bytes()
            )
        )
        unit_indexes = self.unit_indexes(probe)
        spike_amplitudes_by_unit: list[npt.NDArray[np.floating]] = []
        for index in sorted(np.unique(unit_indexes)):
            spike_amplitudes_by_unit.append(spike_amplitudes[unit_indexes == index])
        return tuple(spike_amplitudes_by_unit)

    @functools.cache
    def unit_locations(self, probe: str) -> npt.NDArray[np.floating]:
        return np.load(
            io.BytesIO(
                self.get_correct_path(
                    self.postprocessed(probe=probe),
                    "unit_locations",
                    "unit_locations.npy",
                ).read_bytes()
            )
        )

    @functools.cache
    def sorting_json(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(self.postprocessed(probe=probe), "sorting.json")
        )

    @functools.cache
    def recording_attributes_json(self, probe: str) -> dict:
        return self.read_json(
            self.get_correct_path(
                self.postprocessed(probe=probe),
                "recording_info",
                "recording_attributes.json",
            )
        )

    @functools.cache
    def sparse_channel_indices(self, probe: str) -> tuple[int, ...]:
        """SpikeInterface stores channels as 1-indexed integers: "AP1", ...,
        "AP384". This method returns the 0-indexed *integers* for each probe
        recorded, for use in indexing into the electrode table.
        """

        def int_ids(recording_attributes_json: dict) -> tuple[int, ...]:
            """
            >>> int_ids({'channel_ids': ['AP1', '2', 'CH3', ]})
            (0, 1, 2)
            """
            values = tuple(
                sorted(
                    int("".join(i for i in str(id_) if i.isdigit())) - 1
                    for id_ in recording_attributes_json["channel_ids"]
                )
            )
            assert (
                m := min(values)
            ) >= 0, f"Expected all channel_ids from SpikeInterface to be 1-indexed: min = {m + 1}"
            return values

        return int_ids(self.recording_attributes_json(probe))

    @functools.cache
    def electrode_locations_xy(self, probe: str) -> npt.NDArray[np.floating]:
        return np.array(
            self.sorting_json(probe)["annotations"]["__sorting_info__"]["recording"][
                "properties"
            ]["location"]
        )


if __name__ == "__main__":
    from npc_ephys import testmod

    testmod()
