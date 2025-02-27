# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from math import ceil
from typing import List, Tuple, Dict, Set, Iterable, Union, Optional
from dataclasses import dataclass

from pdkmaster.typing import MultiT, cast_MultiT
from pdkmaster.technology import (
    property_ as _prp, geometry as _geo, primitive as _prm, technology_ as _tch,
)
from pdkmaster.design import cell as _cell, library as _lbry

from c4m import flexcell as _fc

from . import factory as _iofab


__all__ = ["IOSpecification", "TrackSpecification", "IOFrameSpecification"]


class _MetalSpec:
    def __init__(self, *,
        tech: _tch.Technology, spec: "IOSpecification", framespec: "IOFrameSpecification",
        computed: "_ComputedSpecs",
        metal: _prm.MetalWire,
    ):
        self._prim = metal
        self._minwidth_down = tech.computed.min_width(
            metal, up=False, down=True, min_enclosure=True,
        )
        self._minwidth4ext_down = tech.computed.min_width(
            metal, up=False, down=True, min_enclosure=False,
        )
        self._minwidth_up = tech.computed.min_width(
            metal, up=True, down=False, min_enclosure=True,
        )
        self._minwidth4ext_up = tech.computed.min_width(
            metal, up=True, down=False, min_enclosure=False,
        )
        self._minwidth_updown = tech.computed.min_width(
            metal, up=True, down=True, min_enclosure=True,
        )
        self._minwidth4ext_updown = tech.computed.min_width(
            metal, up=True, down=True, min_enclosure=False,
        )
        # Compute min track space
        # first take specific value, otherwise value for None considered default,
        # otherwise metal minimum space
        s = framespec.tracksegment_space
        self.tracksegment_space = s.get(metal, s.get(None, metal.min_space))

        for via in computed.vias:
            if via.bottom[0] == metal:
                self._top_via = via
                break
        else:
            self._top_via = None

    @property
    def prim(self) -> _prm.MetalWire:
        return self._prim
    @property
    def minwidth_down(self) -> float:
        return self._minwidth_down
    @property
    def minwidth4ext_down(self) -> float:
        return self._minwidth4ext_down
    @property
    def minwidth_up(self) -> float:
        return self._minwidth_up
    @property
    def minwidth4ext_up(self) -> float:
        return self._minwidth4ext_up
    @property
    def minwidth_updown(self) -> float:
        return self._minwidth_updown
    @property
    def minwidth4ext_updown(self) -> float:
        return self._minwidth4ext_updown

    @property
    def top_via(self) -> _prm.Via:
        if self._top_via is None:
            raise AttributeError(f"Top via not found for metal '{self.prim.name}'")
        return self._top_via


class _DummyStdCellFactory:
    """This is dummy factory with purpose of being a wrapper around a standard cell library.
    This class is only for internal use and it only provided the functionality needed for
    that purpose.
    """
    def __init__(self, *, lib: _lbry.Library):
        self.lib = lib

    def getcreate_cell(self, *, name: str) -> _cell.Cell:
        return self.lib.cells[name]


class IOSpecification:
    def __init__(self, *,
        stdcelllib: Optional[_lbry.Library]=None, stdcellfab: Optional[_fc.StdCellFactory]=None,
        nmos: _prm.MOSFET, pmos: _prm.MOSFET, ionmos: _prm.MOSFET, iopmos: _prm.MOSFET,
        monocell_width: float,
        metal_bigspace: float, topmetal_bigspace: float,
        clampnmos: Optional[_prm.MOSFET]=None,
        clampnmos_w: float, clampnmos_l: Optional[float]=None, clampnmos_rows: int=1,
        clamppmos: Optional[_prm.MOSFET]=None,
        clamppmos_w: float, clamppmos_l: Optional[float]=None, clamppmos_rows: int=1,
        clampfingers: int, clampfingers_analog: Optional[int],
        clampdrive: Union[int, Dict[str, int]],
        rcclampdrive: Optional[int]=None, rcclamp_rows: Optional[int]=None,
        clampgate_gatecont_space: float, clampgate_sourcecont_space: float,
        clampgate_draincont_space: float,
        add_clampsourcetap: bool=False,
        clampsource_cont_tap_enclosure: Optional[Union[float, _prp.Enclosure]]=None,
        clampsource_cont_tap_space: Optional[float]=None,
        clampdrain_layer: Optional[_prm.DesignMaskPrimitiveT],
        clampgate_clampdrain_overlap: Optional[float], clampdrain_active_ext: Optional[float],
        clampdrain_gatecont_space: Optional[float],
        clampdrain_contcolumns: int, clampdrain_via1columns: int,
        nres: _prm.Resistor, pres: _prm.Resistor, ndiode: _prm.Diode, pdiode: _prm.Diode,
        secondres_width: float, secondres_length: float,
        secondres_active_space: float,
        corerow_height: float, corerow_nwell_height: float,
        iorow_height: float, iorow_nwell_height: float,
        nwell_minspace: Optional[float]=None, levelup_core_space: float,
        resvdd_prim: Optional[_prm.Resistor]=None,
        resvdd_w: Optional[float]=None, resvdd_space: Optional[float]=None,
        resvdd_lfinger: Optional[float]=None, resvdd_fingers: Optional[int]=None,
        capvdd_l: Optional[float]=None, capvdd_w: Optional[float]=None, capvdd_rows: int=1,
        capvdd_mosfet: Optional[_prm.MOSFET]=None, capvdd_fingers: Optional[int]=None,
        invvdd_n_l: Optional[float]=None, invvdd_n_w: Optional[float]=None, invvdd_n_rows: int=1,
        invvdd_n_mosfet: Optional[_prm.MOSFET]=None, invvdd_n_fingers: Optional[int]=None,
        invvdd_p_l: Optional[float]=None, invvdd_p_w: Optional[float]=None, invvdd_p_rows: int=1,
        invvdd_p_mosfet: Optional[_prm.MOSFET]=None, invvdd_p_fingers: Optional[int]=None,
        rcmosfet_row_minspace: Optional[float]=None,
        add_corem3pins: bool=False, corem3pin_minlength: Optional[float]=None,
        add_dcdiodes: bool=False,
        dcdiode_actwidth: Optional[float]=None, dcdiode_actspace: Optional[float]=None,
        dcdiode_actspace_end: Optional[float]=None, dcdiode_inneractheight: Optional[float]=None,
        dcdiode_impant_enclosure: Optional[float]=None,
        dcdiode_diodeguard_space: Optional[float]=None, dcdiode_fingers: int=1,
        dcdiode_indicator: Optional[_prm.DesignMaskPrimitiveT]=None,
        iovdd_ntap_extra: MultiT[_prm.DesignMaskPrimitiveT]=(),
        iovss_ptap_extra: MultiT[_prm.DesignMaskPrimitiveT]=(),
    ):
        if stdcelllib is not None:
            if stdcellfab is not None:
                raise TypeError("You can't specify both stdcelllib and stdcellfab")
            self.stdcellfab = _DummyStdCellFactory(lib=stdcelllib)
        elif stdcellfab is None:
            raise TypeError("Either stdcelllib or stdcellfab needs to be provided")
        else:
            self.stdcellfab = stdcellfab

        self.monocell_width = monocell_width

        self.metal_bigspace = metal_bigspace
        self.topmetal_bigspace = topmetal_bigspace

        self.nmos = nmos
        self.pmos = pmos
        self.ionmos = ionmos
        self.iopmos = iopmos
        self.clampnmos = clampnmos if clampnmos is not None else ionmos
        self.clamppmos = clamppmos if clamppmos is not None else iopmos
        # TODO: Implement proper source implant for transistor
        self.clampnmos_w = clampnmos_w
        if clampnmos_l is not None:
            self.clampnmos_l = clampnmos_l
        else:
            self.clampnmos_l = self.clampnmos.computed.min_l
        self.clampnmos_rows = clampnmos_rows
        self.clamppmos_w = clamppmos_w
        if clamppmos_l is not None:
            self.clamppmos_l = clamppmos_l
        else:
            self.clamppmos_l = self.clamppmos.computed.min_l
        self.clamppmos_rows = clamppmos_rows
        self.clampcount = clampfingers
        self.clampcount_analog = (
            clampfingers_analog if clampfingers_analog is not None
            else clampfingers
        )
        self.clampdrive = clampdrive
        self.rcclampdrive = (
            clampfingers if rcclampdrive is None
            else rcclampdrive
        )
        self.rcclamp_rows = rcclamp_rows

        self.clampgate_gatecont_space = clampgate_gatecont_space
        self.clampgate_sourcecont_space = clampgate_sourcecont_space
        self.clampgate_draincont_space = clampgate_draincont_space

        if add_clampsourcetap:
            assert clampsource_cont_tap_enclosure is not None
            assert clampsource_cont_tap_space is not None
            if not isinstance(clampsource_cont_tap_enclosure, _prp.Enclosure):
                clampsource_cont_tap_enclosure = _prp.Enclosure(clampsource_cont_tap_enclosure)
            clampsource_cont_tap_space = clampsource_cont_tap_space
        self.add_clampsourcetap = add_clampsourcetap
        self.clampsource_cont_tap_enclosure = clampsource_cont_tap_enclosure
        self.clampsource_cont_tap_space = clampsource_cont_tap_space
        self.clamp_clampdrain = clampdrain_layer
        self.clampgate_clampdrain_overlap = clampgate_clampdrain_overlap
        self.clampdrain_active_ext = clampdrain_active_ext
        self.clampdrain_gatecont_space = clampdrain_gatecont_space
        self.clampdrain_contcolumns = clampdrain_contcolumns
        self.clampdrain_via1columns = clampdrain_via1columns

        self.nres = nres
        self.pres = pres
        self.ndiode = ndiode
        self.pdiode = pdiode
        self.secondres_width = secondres_width
        self.secondres_length = secondres_length
        self.secondres_active_space = secondres_active_space

        self.corerow_height = corerow_height
        self.corerow_nwell_height = corerow_nwell_height
        self.iorow_height = iorow_height
        self.iorow_nwell_height = iorow_nwell_height
        self.cells_height = self.corerow_height + self.iorow_height
        self.corerow_pwell_height = self.corerow_height - self.corerow_nwell_height
        self.iorow_pwell_height = self.iorow_height - self.iorow_nwell_height

        self.nwell_minspace = nwell_minspace

        self.levelup_core_space = levelup_core_space

        if resvdd_prim is None:
            assert (
                (resvdd_w is None) and (resvdd_lfinger is None)
                and (resvdd_fingers is None) and (resvdd_space is None)
                and (capvdd_l is None) and (capvdd_w is None) and (capvdd_rows == 1)
                and (capvdd_mosfet is None) and (capvdd_fingers is None)
                and (invvdd_n_w is None) and (invvdd_n_rows == 1) and (invvdd_n_l is None)
                and (invvdd_n_mosfet is None) and (invvdd_n_fingers is None)
                and (invvdd_p_w is None) and (invvdd_p_rows == 1) and (invvdd_p_l is None)
                and (invvdd_p_mosfet is None) and (invvdd_p_fingers is None)
            )
        else:
            assert (
                (resvdd_w is not None) and (resvdd_lfinger is not None)
                and (resvdd_fingers is not None) and (resvdd_space is not None)
                and (capvdd_l is not None) and (capvdd_w is not None)
                and (capvdd_fingers is not None)
                and (invvdd_n_w is not None) and (invvdd_n_l is not None)
                and (invvdd_n_mosfet is not None) and (invvdd_n_fingers is not None)
                and (invvdd_p_w is not None) and (invvdd_p_l is not None)
                and (invvdd_p_mosfet is not None) and (invvdd_p_fingers is not None)
            )
            if (invvdd_n_rows > 1) or (capvdd_rows > 1):
                if invvdd_n_rows != capvdd_rows:
                    raise NotImplementedError("invvdd_n_rows != capvdd_rows")
                if abs(invvdd_n_w - capvdd_w) > _geo.epsilon:
                    raise NotImplementedError(
                        "Multiple rows for n/cap and invvdd_n_w != capvdd_w")
            if capvdd_mosfet is None:
                capvdd_mosfet = invvdd_n_mosfet
        self.resvdd_prim = resvdd_prim
        self.resvdd_w = resvdd_w
        self.resvdd_space = resvdd_space
        self.resvdd_lfinger = resvdd_lfinger
        self.resvdd_fingers = resvdd_fingers
        self.capvdd_l = capvdd_l
        self.capvdd_w = capvdd_w
        self.capvdd_rows = capvdd_rows
        self.capvdd_mosfet = capvdd_mosfet
        self.capvdd_fingers = capvdd_fingers
        self.invvdd_n_l = invvdd_n_l
        self.invvdd_n_w = invvdd_n_w
        self.invvdd_n_rows = invvdd_n_rows
        self.invvdd_n_mosfet = invvdd_n_mosfet
        self.invvdd_n_fingers = invvdd_n_fingers
        self.invvdd_p_l = invvdd_p_l
        self.invvdd_p_w = invvdd_p_w
        self.invvdd_p_rows = invvdd_p_rows
        self.invvdd_p_mosfet = invvdd_p_mosfet
        self.invvdd_p_fingers = invvdd_p_fingers
        self.rcmosfet_row_minspace = rcmosfet_row_minspace

        self.add_corem3pins = add_corem3pins
        self.corem3pin_minlength = corem3pin_minlength

        self.add_dcdiodes = add_dcdiodes
        if not add_dcdiodes:
            assert (
                (dcdiode_actwidth is None) and (dcdiode_actspace is None)
                and (dcdiode_actspace_end is None) and (dcdiode_inneractheight is None)
                and (dcdiode_diodeguard_space is None) and (dcdiode_fingers == 1)
                and (dcdiode_indicator is None)
            )
        else:
            assert (
                (dcdiode_actwidth is not None) and (dcdiode_actspace is not None)
                and (dcdiode_inneractheight is not None) and (dcdiode_diodeguard_space is not None)
                and (dcdiode_fingers > 0)
            )
            if dcdiode_actspace_end is None:
                dcdiode_actspace_end = dcdiode_actspace
            self.dcdiode_actwidth = dcdiode_actwidth
            self.dcdiode_actspace = dcdiode_actspace
            self.dcdiode_actspace_end = dcdiode_actspace_end
            self.dcdiode_inneractheight = dcdiode_inneractheight
            self.dcdiode_implant_enclosure = dcdiode_impant_enclosure
            self.dcdiode_diodeguardspace = dcdiode_diodeguard_space
            self.dcdiode_fingers = dcdiode_fingers
            self.dcdiode_indicator = dcdiode_indicator

        self.iovdd_ntap_extra = cast_MultiT(iovdd_ntap_extra)
        self.iovss_ptap_extra = cast_MultiT(iovss_ptap_extra)


@dataclass
class _SegmentSpecification:
    bottom: float
    top: float

    @property
    def center(self) -> float:
        return 0.5*(self.bottom + self.top)
    @property
    def height(self) -> float:
        return self.top - self.bottom


@dataclass
class TrackSpecification:
    name: str
    bottom: float
    width: float

    @property
    def center(self) -> float:
        return self.bottom + 0.5*self.width
    @property
    def top(self) -> float:
        return self.bottom + self.width

    def track_segments(self, *,
        tech: _tch.Technology, maxpitch: float,
    ) -> Tuple[_SegmentSpecification, ...]:
        n_segments = int((self.width - _geo.epsilon)/maxpitch) + 1
        width = tech.on_grid(self.width/n_segments, mult=2)

        segments: List[_SegmentSpecification] = []
        for i in range(n_segments):
            bottom = self.bottom + i*width
            # For last segment take top as top of the track
            if i < (n_segments - 1):
                top = bottom + width
            else:
                top = self.bottom + self.width
            segments.append(_SegmentSpecification(bottom=bottom, top=top))

        return tuple(segments)


class IOFrameSpecification:
    track_names: Set[str] = {"iovss", "iovdd", "secondiovss", "vddvss"}

    def __init__(self, *,
        cell_height: float, top_metal: Optional[_prm.MetalWire]=None,
        tracksegment_maxpitch: float, tracksegment_space: Dict[Optional[_prm.MetalWire], float]={},
        tracksegment_viapitch: float,
        trackconn_viaspace: Optional[float]=None, trackconn_chspace: Optional[float]=None,
        acttracksegment_maxpitch: Optional[float]=None, acttracksegment_space: Optional[float]=None,
        pad_width: float, pad_height: Optional[float]=None, pad_y: float,
        pad_viapitch: Optional[float], pad_viacorner_distance: float, pad_viametal_enclosure: float,
        padpin_height: Optional[float]=None,
        track_specs: Iterable[TrackSpecification],
    ):
        self.cell_height = cell_height
        self.top_metal = top_metal

        self.tracksegment_maxpitch = tracksegment_maxpitch
        self.tracksegment_space = tracksegment_space
        self.tracksegement_viapitch = tracksegment_viapitch
        self.trackconn_viaspace = trackconn_viaspace
        self.trackconn_chspace = trackconn_chspace

        assert (acttracksegment_maxpitch is None) == (acttracksegment_space is None)
        self.acttracksegment_maxpitch = acttracksegment_maxpitch
        self.acttracksegment_space = acttracksegment_space

        if (pad_height is None) == (padpin_height is None):
            raise TypeError("Either pad_height or padpin_height needs to be provided")

        self.pad_width = pad_width
        if pad_height is not None:
            self.pad_height = pad_height
        self.pad_y = pad_y
        self.pad_viapitch = pad_viapitch
        self.pad_viacorner_distance = pad_viacorner_distance
        self.pad_viametal_enclosure = pad_viametal_enclosure
        if padpin_height is not None:
            self.padpin_height = padpin_height
        self.track_specs = track_specs = tuple(track_specs)
        self._track_specs_dict: Dict[str, TrackSpecification] = {
            spec.name: spec for spec in track_specs
        }

        spec_names = {spec.name for spec in track_specs}
        if self.track_names != spec_names:
            missing = self.track_names - spec_names
            if (len(missing) == 1) and ("secondiovss" in missing):
                self._has_secondiovss = False
            elif missing:
                raise ValueError(
                    f"Missing spec for track(s) '{tuple(missing)}'"
                )
            wrong = spec_names - self.track_names
            if wrong:
                raise ValueError(
                    f"Wrong spec for track name(s) '{tuple(wrong)}'"
                )
        else:
            self._has_secondiovss = True

    @property
    def has_secondiovss(self) -> bool:
        return self._has_secondiovss


class _ComputedSpecs:
    def __init__(self, *,
        fab: "_iofab.IOFactory", framespec: "IOFrameSpecification",
        nmos: _prm.MOSFET, pmos: _prm.MOSFET, ionmos: _prm.MOSFET, iopmos: _prm.MOSFET,
    ):
        self.fab = fab
        spec = fab.spec
        tech = fab.tech

        # assert statements are used for unsupported technology configuration
        # TODO: Implement unsupported technology configurations

        assert nmos.well is None
        assert pmos.well is not None
        assert ionmos.well is None
        assert iopmos.well is not None
        assert pmos.well == iopmos.well

        prims = tech.primitives
        self.nmos = nmos
        self.pmos = pmos
        self.ionmos = ionmos
        self.iopmos = iopmos

        assert nmos.gate == pmos.gate
        assert ionmos.gate == iopmos.gate

        mosgate = nmos.gate
        iomosgate = ionmos.gate

        assert mosgate.oxide is None
        assert iomosgate.oxide is not None
        assert mosgate.active == iomosgate.active
        assert mosgate.poly == iomosgate.poly

        self.active = active = mosgate.active
        self.oxide = iomosgate.oxide
        self.poly = poly = mosgate.poly

        assert active.oxide is not None
        assert active.min_oxide_enclosure is not None
        assert nmos.computed.min_active_substrate_enclosure is not None
        assert ionmos.computed.min_active_substrate_enclosure is not None

        # Following code assumes that either (io)nmos or (io)pmos transistor have implants
        # We also use the first implant of a MOSFET as the main implant layer

        # nmos/pmos & nimplant/pimplan
        if nmos.implant:
            nimplant = nmos.implant[0]
            idx = active.implant.index(nimplant)
            nimplant_enc = active.min_implant_enclosure[idx]
        else:
            nimplant = None
            nimplant_enc = None
        self.nimplant = nimplant
        if pmos.implant:
            pimplant = pmos.implant[0]
            idx = active.implant.index(pimplant)
            pimplant_enc = active.min_implant_enclosure[idx]
        else:
            pimplant = None
            pimplant_enc = None
        self.pimplant = pimplant
        if nimplant is not None:
            try:
                space = tech.computed.min_space(nimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert pimplant_enc is not None
            space = pimplant_enc.max()
        elif pimplant_enc is not None:
            space = max(space, pimplant_enc.max())
        self.min_space_nimplant_active = space
        if pimplant is not None:
            try:
                space = tech.computed.min_space(pimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert nimplant_enc is not None
            space = nimplant_enc.max()
        elif nimplant_enc is not None:
            space = max(space, nimplant_enc.max())
        self.min_space_pimplant_active = space

        # ionmos/iopmos & nimplant/pimplant
        if ionmos.implant:
            ionimplant = ionmos.implant[0]
            idx = active.implant.index(ionimplant)
            ionimplant_enc = active.min_implant_enclosure[idx]
        else:
            ionimplant = None
            ionimplant_enc = None
        self.ionimplant = ionimplant
        if iopmos.implant:
            iopimplant = iopmos.implant[0]
            idx = active.implant.index(iopimplant)
            iopimplant_enc = active.min_implant_enclosure[idx]
        else:
            iopimplant = None
            iopimplant_enc = None
        self.iopimplant = iopimplant
        if ionimplant is not None:
            try:
                space = tech.computed.min_space(ionimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert iopimplant_enc is not None
            space = iopimplant_enc.max()
        elif iopimplant_enc is not None:
            space = max(space, iopimplant_enc.max())
        self.min_space_ionimplant_active = space
        if iopimplant is not None:
            try:
                space = tech.computed.min_space(iopimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert ionimplant_enc is not None
            space = ionimplant_enc.max()
        elif ionimplant_enc is not None:
            space = max(space, ionimplant_enc.max())
        self.min_space_iopimplant_active = space

        # oxide
        oxidx = active.oxide.index(iomosgate.oxide)
        try:
            self.min_oxactive_space = tech.computed.min_space(active.in_(iomosgate.oxide))
        except AttributeError:
            self.min_oxactive_space = active.min_space
        oxenc = iomosgate.min_gateoxide_enclosure
        if oxenc is None:
            oxenc = _prp.Enclosure(tech.grid)
        self.iogateoxide_enclosure = oxenc
        # TODO: add active oxide enclosure
        oxext = oxenc.second
        oxenc = active.min_oxide_enclosure[oxidx]
        if oxenc is None:
            oxenc = _prp.Enclosure(tech.grid)
        self.activeoxide_enclosure = oxenc
        oxext = max((oxext, oxenc.max()))

        # min spacings for active
        min_space_active_poly = tech.computed.min_space(poly, active)
        space = max((
            active.min_space,
            nmos.computed.min_polyactive_extension + min_space_active_poly,
        ))
        if nmos.min_gateimplant_enclosure:
            space = max(
                space,
                nmos.min_gateimplant_enclosure[0].max() + self.min_space_nimplant_active,
            )
        if pimplant is not None:
            try:
                s = tech.computed.min_space(nmos.gate4mosfet, pimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_nimplant_active)
        self.min_space_nmos_active = space
        space = max((
            active.min_space,
            pmos.computed.min_polyactive_extension + min_space_active_poly,
        ))
        if pmos.min_gateimplant_enclosure:
            space = max(
                space,
                pmos.min_gateimplant_enclosure[0].max() + self.min_space_pimplant_active,
            )
        if nimplant is not None:
            try:
                s = tech.computed.min_space(pmos.gate4mosfet, nimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_pimplant_active)
        self.min_space_pmos_active = space
        min_space_iomosgate_active = (
            oxext + tech.computed.min_space(iomosgate.oxide, active)
        )
        space = max((
            active.min_space,
            ionmos.computed.min_polyactive_extension + min_space_active_poly,
            min_space_iomosgate_active,
        ))
        if ionmos.min_gateimplant_enclosure:
            space = max(
                space,
                ionmos.min_gateimplant_enclosure[0].max() + self.min_space_ionimplant_active,
            )
        if iopimplant is not None:
            try:
                s = tech.computed.min_space(ionmos.gate4mosfet, iopimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_ionimplant_active)
        self.min_space_ionmos_active = space
        space = max((
            active.min_space,
            iopmos.computed.min_polyactive_extension + min_space_active_poly,
            min_space_iomosgate_active,
        ))
        if iopmos.min_gateimplant_enclosure:
            space = max(
                space,
                iopmos.min_gateimplant_enclosure[0].max() + self.min_space_iopimplant_active,
            )
        if ionimplant is not None:
            try:
                s = tech.computed.min_space(iopmos.gate4mosfet, ionimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_iopimplant_active)
        self.min_space_iopmos_active = space
        vias = tuple(prims.__iter_type__(_prm.Via))
        metals = tuple(filter(
            lambda m: not isinstance(m, _prm.MIMTop),
            prims.__iter_type__(_prm.MetalWire),
        ))
        # One via below each metal => #vias == #metals
        assert len(vias) == len(metals)
        if framespec.top_metal is not None:
            idx = metals.index(framespec.top_metal)
            metals = metals[:(idx + 1)]
            vias = vias[:(idx + 1)]
        assert all(hasattr(metal, "pin") for metal in metals), "Unsupported configuration"
        self.vias = vias

        # Draw SD regions with vertical implant enclosure the same as the
        # gate implant enclosure
        try:
            gate_enc = nmos.min_gateimplant_enclosure[0]
        except:
            gate_enc = None
        try:
            idx = active.implant.index(nimplant)
            act_enc = active.min_implant_enclosure[idx]
        except:
            act_enc = None
        if gate_enc is None:
            if act_enc is None:
                self.min_nsd_enc = None
            else:
                self.min_nsd_enc = act_enc
        else:
            assert act_enc is not None
            self.min_nsd_enc = _prp.Enclosure((
                act_enc.first, max(act_enc.min(), gate_enc.second),
            ))

        try:
            gate_enc = pmos.min_gateimplant_enclosure[0]
        except:
            gate_enc = None
        try:
            idx = active.implant.index(pimplant)
            act_enc = active.min_implant_enclosure[idx]
        except:
            act_enc = None
        if gate_enc is None:
            if act_enc is None:
                self.min_psd_enc = None
            else:
                self.min_psd_enc = act_enc
        else:
            assert act_enc is not None
            self.min_psd_enc = _prp.Enclosure((
                act_enc.first, max(act_enc.min(), gate_enc.second),
            ))

        try:
            gate_enc = ionmos.min_gateimplant_enclosure[0]
        except:
            gate_enc = None
        try:
            idx = active.implant.index(ionimplant)
            act_enc = active.min_implant_enclosure[idx]
        except:
            act_enc = None
        if gate_enc is None:
            if act_enc is None:
                self.min_ionsd_enc = None
            else:
                self.min_ionsd_enc = act_enc
        else:
            assert act_enc is not None
            self.min_ionsd_enc = _prp.Enclosure((
                act_enc.first, max(act_enc.min(), gate_enc.second),
            ))

        try:
            gate_enc = iopmos.min_gateimplant_enclosure[0]
        except:
            gate_enc = None
        try:
            idx = active.implant.index(iopimplant)
            act_enc = active.min_implant_enclosure[idx]
        except:
            act_enc = None
        if gate_enc is None:
            if act_enc is None:
                self.min_iopsd_enc = None
            else:
                self.min_iopsd_enc = act_enc
        else:
            assert act_enc is not None
            self.min_iopsd_enc = _prp.Enclosure((
                act_enc.first, max(act_enc.min(), gate_enc.second),
            ))

        # Vias are sorted in the technology from bottom to top
        # so first via is the contact layer
        self.contact = contact = vias[0]
        assert (
            (active in contact.bottom) and (poly in contact.bottom)
            and (len(contact.top) == 1)
        ), "Unsupported configuration"

        actidx = contact.bottom.index(active)
        self.chact_enclosure = actenc = contact.min_bottom_enclosure[actidx]
        polyidx = contact.bottom.index(poly)
        self.chpoly_enclosure = polyenc = contact.min_bottom_enclosure[polyidx]
        self.chm1_enclosure = contact.min_top_enclosure[0]

        self.minwidth_activewithcontact = (
            contact.width + 2*actenc.min()
        )
        self.minwidth4ext_activewithcontact = (
            contact.width + 2*actenc.max()
        )

        self.minwidth_polywithcontact = (
            contact.width + 2*polyenc.min()
        )
        self.minwidth4ext_polywithcontact = (
            contact.width + 2*polyenc.max()
        )

        self.minnmos_contactgatepitch = (
            0.5*contact.width + nmos.computed.min_contactgate_space
            + 0.5*nmos.computed.min_l
        )
        self.minpmos_contactgatepitch = (
            0.5*contact.width + pmos.computed.min_contactgate_space
            + 0.5*pmos.computed.min_l
        )

        self.minionmos_contactgatepitch = (
            0.5*contact.width + ionmos.computed.min_contactgate_space
            + 0.5*ionmos.computed.min_l
        )
        self.miniopmos_contactgatepitch = (
            0.5*contact.width + iopmos.computed.min_contactgate_space
            + 0.5*iopmos.computed.min_l
        )

        self.nwell = nwell = pmos.well
        nwellidx = active.well.index(nwell)

        nactenc = nmos.computed.min_active_substrate_enclosure.max()
        pactenc = pmos.computed.min_active_well_enclosure.max()
        try:
            s = tech.computed.min_space(active, contact)
        except AttributeError:
            pass
        else:
            # Be sure that a poly contact can be put in between nmos and pmos
            if (nactenc + pactenc) < (contact.width + 2*s):
                # First make the two enclosures equal
                if pactenc < nactenc:
                    pactenc = nactenc
                else:
                    nactenc = pactenc
                # Then increase both if not enough yet
                if (nactenc + pactenc) < (contact.width + 2*s):
                    d = tech.on_grid(
                        0.5*((contact.width + 2*s) - (nactenc + pactenc)),
                        rounding="ceiling",
                    )
                    nactenc += d
                    pactenc += d
        self.activenwell_minspace = nactenc
        self.activenwell_minenclosure = pactenc

        ionactenc = max(
            nactenc,
            ionmos.computed.min_active_substrate_enclosure.max(),
        )
        if ionmos.min_gateimplant_enclosure:
            ionactenc = max(ionactenc, ionmos.min_gateimplant_enclosure[0].second)
        if pimplant is not None:
            try:
                s = tech.computed.min_space(ionmos.gate4mosfet, pimplant)
            except:
                pass
            else:
                ionactenc = max(ionactenc, s)
        iopactenc = max(
            pactenc,
            iopmos.computed.min_active_well_enclosure.max(),
        )
        if iopmos.min_gateimplant_enclosure:
            iopactenc = max(iopactenc, iopmos.min_gateimplant_enclosure[0].second)
        if nimplant is not None:
            try:
                s = tech.computed.min_space(iopmos.gate4mosfet, nimplant)
            except:
                pass
            else:
                iopactenc = max(iopactenc, s)

        nwellenc = active.min_well_enclosure[nwellidx].max()
        self.guardring_width = w = max(
            contact.width + contact.min_space,
            nwell.min_width - 2*nwellenc,
        )
        nwell_minspace = nwell.min_space
        if spec.nwell_minspace is not None:
            nwell_minspace = max(nwell_minspace, spec.nwell_minspace)
        s = max(
            pactenc + nactenc,
            0.5*(nwell_minspace + 2*pactenc - w), # Minimum NWELL spacing
        )
        self.guardring_space = 2*ceil(s/(2*tech.grid))*tech.grid
        self.guardring_pitch = self.guardring_width + self.guardring_space

        bottom = spec.iorow_height + 0.5*self.minwidth_activewithcontact + self.min_space_nmos_active
        top = spec.iorow_height + spec.corerow_pwell_height - nactenc
        self.maxnmos_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxnmos_y = tech.on_grid(top - 0.5*w)
        self.maxnmos_activebottom = top - w
        self.maxnmos_activetop = top

        bottom = spec.iorow_height + spec.corerow_pwell_height + pactenc
        top = (
            spec.iorow_height + spec.corerow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_pmos_active)
        )
        self.maxpmos_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxpmos_y = bottom + 0.5*w
        self.maxpmos_activebottom = bottom
        self.maxpmos_activetop = bottom + w

        bottom = spec.iorow_nwell_height + ionactenc
        top = (
            spec.iorow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_ionmos_active)
        )
        self.maxionmos_w = w = tech.on_grid(top - bottom,mult=2, rounding="floor")
        self.maxionmos_y = bottom + 0.5*w
        self.maxionmos_activebottom = bottom
        self.maxionmos_activetop = bottom + w

        bottom = 0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active
        top = spec.iorow_nwell_height - iopactenc
        self.maxiopmos_w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxiopmos_y = tech.on_grid(
            0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active
            + 0.5*self.maxiopmos_w,
        )
        self.maxiopmos_activebottom = tech.on_grid(self.maxiopmos_y - 0.5*self.maxiopmos_w)
        self.maxiopmos_activetop = tech.on_grid(self.maxiopmos_y + 0.5*self.maxiopmos_w)

        self.io_oxidebottom = (
            0.5*self.minwidth_activewithcontact
            + tech.computed.min_space(iomosgate.oxide, active)
        )
        self.io_oxidetop = (
            spec.iorow_height
            - 0.5*self.minwidth_activewithcontact
            - tech.computed.min_space(iomosgate.oxide, active)
        )

        # Also get dimensions of io transistor in the core row
        bottom = spec.iorow_height + 0.5*self.minwidth_activewithcontact + self.min_space_ionmos_active
        top = spec.iorow_height + spec.corerow_pwell_height - ionactenc
        self.maxionmoscore_w = w =  tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxionmoscore_y = top - 0.5*w
        self.maxionmoscore_activebottom = top - w
        self.maxionmoscore_activetop = top

        bottom = spec.iorow_height + spec.corerow_pwell_height + iopactenc
        top = (
            spec.iorow_height + spec.corerow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active)
        )
        self.maxiopmoscore_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxiopmoscore_y = bottom + 0.5*w
        self.maxiopmoscore_activebottom = bottom
        self.maxiopmoscore_activetop = bottom + w

        for via in vias[1:]:
            assert all((
                (len(via.bottom) == 1) or isinstance(via.bottom[0], _prm.MetalWire),
                (len(via.top) == 1) or isinstance(via.top[0], _prm.MetalWire),
            )), "Unsupported configuration"

        pads = tuple(tech.primitives.__iter_type__(_prm.PadOpening))
        assert len(pads) == 1
        self.pad = pads[0]

        # self.track_nsegments =
        # Don't start from 0; self.metal[1] corresponds with metal 1
        self.metal = {
            (i + 1): _MetalSpec(
                tech=tech, spec=spec, framespec=framespec, computed=self,
                metal=metal,
            )
            for i, metal in enumerate(metals)
        }

        self.track_metalspecs = tuple(self.metal[i] for i in range(3, (len(metals) + 1)))
