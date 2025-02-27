# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from math import floor
from typing import (
    Tuple, Dict, Iterable, Container, Optional, cast,
)

from pdkmaster.technology import (
    geometry as _geo, property_ as _prp, primitive as _prm,
)
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, factory as _fab,
)

from . import _helpers as _hlp, specification as _spec, factory as _iofab


__all__ = ["FactoryCellT"]


class _IOCellFrame:
    """Default cells for in IO cell framework"""
    def __init__(self, *,
        fab: "_iofab.IOFactory", framespec: "_spec.IOFrameSpecification",
    ):
        self.fab = fab
        self.framespec = framespec
        tech = fab.tech
        comp = fab.computed

        active = comp.active
        actmaxpitch = framespec.acttracksegment_maxpitch
        actspace = framespec.acttracksegment_space

        self._pad = None # Only create pad first time it is accessed
        self._pad_bb: Dict[_prm.DesignMaskPrimitiveT, _geo.RectangularT] = {}
        self.__padpin_shape: Optional[_geo.Rect] = None

        track_segments: Dict[str, Tuple[_spec._SegmentSpecification, ...]] = {
            track_name: track_spec.track_segments(
                tech=fab.tech, maxpitch=self.tracksegment_maxpitch,
            )
            for track_name, track_spec in framespec._track_specs_dict.items()
        }

        l_gd = fab.get_cell("GateDecode").layout
        assert l_gd.boundary is not None
        gd_height = l_gd.boundary.top - l_gd.boundary.bottom
        self.cells_y = cells_y = self.cell_height - gd_height

        l_ld = fab.get_cell("LevelDown").layout
        act_bb = l_ld.bounds(mask=active.mask)

        def act_segs(track_spec: _spec.TrackSpecification) -> Tuple[_spec._SegmentSpecification, ...]:
            if actmaxpitch is None:
                return (
                    _spec._SegmentSpecification(
                        bottom=track_spec.bottom,
                        top=track_spec.top,
                    ),
                )
            else:
                assert actspace is not None
                segs1 = track_spec.track_segments(tech=tech, maxpitch=actmaxpitch)
                segs2 = []
                for i, seg in enumerate(segs1):
                    # TODO: always ad/subtract space
                    bottom = seg.bottom + (0.0 if i == 0 else 0.5*actspace)
                    top = seg.top - (0.0 if i == (len(segs1) - 1) else 0.5*actspace)
                    segs2.append(_spec._SegmentSpecification(bottom=bottom, top=top))
                return tuple(segs2)

        bottom = framespec._track_specs_dict["iovdd"].bottom
        top = cells_y + act_bb.bottom
        track_spec = _spec.TrackSpecification(name="temp", bottom=bottom, width=(top - bottom))
        track_segments["actiovss"] = act_segs(track_spec)

        track_spec = framespec._track_specs_dict["iovss"]
        track_segments["actiovdd"] = act_segs(track_spec)

        self._track_segments = track_segments

    @property
    def cell_height(self) -> float:
        return self.framespec.cell_height
    @property
    def monocell_width(self) -> float:
        return self.fab.spec.monocell_width
    @property
    def top_metal(self) -> Optional[_prm.MetalWire]:
        return self.framespec.top_metal
    @property
    def tracksegment_maxpitch(self) -> float:
        return self.framespec.tracksegment_maxpitch
    @property
    def tracksegment_space(self) -> Dict[Optional[_prm.MetalWire], float]:
        return self.framespec.tracksegment_space
    @property
    def tracksegment_viapitch(self) -> float:
        return self.framespec.tracksegement_viapitch
    @property
    def trackconn_viaspace(self) -> Optional[float]:
        return self.framespec.trackconn_viaspace
    @property
    def trackconn_chspace(self) -> Optional[float]:
        return self.framespec.trackconn_chspace
    @property
    def acttracksegment_maxpitch(self) -> Optional[float]:
        return self.framespec.acttracksegment_maxpitch
    @property
    def acttracksegment_space(self) -> Optional[float]:
        return self.framespec.acttracksegment_space
    @property
    def pad_width(self) -> float:
        return self.framespec.pad_width
    @property
    def pad_height(self) -> float:
        return self.framespec.pad_height
    @property
    def pad_y(self) -> float:
        return self.framespec.pad_y
    @property
    def pad_viapitch(self) -> Optional[float]:
        return self.framespec.pad_viapitch
    @property
    def pad_viacorner_distance(self) -> float:
        return self.framespec.pad_viacorner_distance
    @property
    def pad_viametal_enclosure(self) -> float:
        return self.framespec.pad_viametal_enclosure
    @property
    def padpin_height(self) -> float:
        return self.framespec.padpin_height
    @property
    def track_specs(self) -> Dict[str, "_spec.TrackSpecification"]:
        return self.framespec._track_specs_dict
    @property
    def has_secondiovss(self) -> bool:
        return self.framespec.has_secondiovss

    #
    # Pin support
    #

    def add_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, m2_shape: _geo.RectangularT,
    ):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        shape = _geo.Rect.from_rect(rect=m2_shape, top=self.cell_height)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=shape)

        if spec.add_corem3pins:
            metal2_spec = comp.metal[2]
            metal3_spec = comp.metal[3]
            metal3 = metal3_spec.prim
            via2 = comp.vias[2]

            w = m2_shape.width
            h = max(metal2_spec.minwidth4ext_updown, metal3_spec.minwidth4ext_updown)
            if (metal3.min_area is not None) and ((w*h + _geo.epsilon) < metal3.min_area):
                w = tech.on_grid(metal3.min_area/h, mult=2, rounding="ceiling")

            l_via2 = layouter.add_wire(
                net=net, wire=via2,
                x=m2_shape.center.x, bottom_width=w, top_width=w,
                y=(self.cell_height - 0.5*h), bottom_height=h, top_height=h,
            )
            shape = l_via2.bounds(mask=metal3.mask)
            if (
                (spec.corem3pin_minlength is not None)
                and (spec.corem3pin_minlength > shape.width)
            ):
                shape = _geo.Rect.from_rect(
                    rect=shape,
                    left=(shape.center.x - 0.5*spec.corem3pin_minlength),
                    right=(shape.center.x + 0.5*spec.corem3pin_minlength),
                )
            layouter.add_wire(net=net, wire=metal3, pin=metal3.pin, shape=shape)

    def promote_m1instpin_to_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, inst_layout: _lay.LayoutT,
        align: str,
    ):
        assert align in ("left", "center", "right"), "Internal error"

        fab = self.fab
        comp = fab.computed

        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]

        m1pin_bounds = inst_layout.bounds(net=net, mask=metal1pin.mask, depth=1)
        _l_via1 = layouter.wire_layout(
            net=net, wire=via1, bottom_height=m1pin_bounds.height,
            bottom_enclosure="tall", top_enclosure="wide",
        )
        _m1_bounds = _l_via1.bounds(mask=metal1.mask)
        if align == "left":
            x = m1pin_bounds.right - _m1_bounds.right
        elif align == "center":
            x = m1pin_bounds.center.x
        elif align == "right":
            x = m1pin_bounds.left - _m1_bounds.left
        else:
            assert False, "Internal error"
        y = m1pin_bounds.top - _m1_bounds.top
        l_via = layouter.place(object_=_l_via1, x=x, y=y)
        self.add_corepin(
            layouter=layouter, net=net, m2_shape=l_via.bounds(mask=metal2.mask),
        )

    def promote_m2instpin_to_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, inst_layout: _lay.LayoutT,
    ):
        fab = self.fab
        comp = fab.computed

        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        m2pin_bb = inst_layout.bounds(net=net, mask=metal2pin.mask, depth=1)
        self.add_corepin(layouter=layouter, net=net, m2_shape=m2pin_bb)

    #
    # IO track support
    #

    def add_track_nets(self, *, ckt: _ckt.CircuitT) -> Dict[
        str, _ckt._CircuitNet,
    ]:
        nets = {
            net_name: ckt.new_net(name=net_name, external=True)
            for net_name in ("vss", "vdd", "iovss", "iovdd")
        }
        return nets

    def draw_trackconn(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
        cell_width: float,
        nclamp_lay: Optional[_lay.LayoutT], pclamp_lay: Optional[_lay.LayoutT],
        ndio_lay: Optional[_lay.LayoutT], pdio_lay: Optional[_lay.LayoutT],
    ):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        nets = ckt.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        contact = comp.contact
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        via2 = comp.vias[2]
        metal3 = comp.metal[3].prim

        iopmos = comp.iopmos

        iovdd_trackspec = frame.track_specs["iovdd"]

        layout = layouter.layout

        drive = spec.clampdrive
        if not isinstance(drive, int):
            it = iter(drive.values())
            drive = next(it)
            del it
        c_pclamp = fab.clamp(
            type_="p", n_trans=max(spec.clampcount, drive), n_drive=drive,
        )
        _l_pclamp = c_pclamp.layout
        clact_bounds = _l_pclamp.bounds(mask=active.mask)
        clm1_bounds = _l_pclamp.bounds(mask=metal1.mask)

        nclamp_actbb = None if nclamp_lay is None else nclamp_lay.bounds(mask=active.mask)
        pclamp_actbb = None if pclamp_lay is None else pclamp_lay.bounds(mask=active.mask)
        ndio_actbb = None if ndio_lay is None else ndio_lay.bounds(mask=active.mask)
        pdio_actbb = None if pdio_lay is None else pdio_lay.bounds(mask=active.mask)

        idx = contact.bottom.index(active)
        min_enc = contact.min_bottom_enclosure[idx]
        actenc = max(min_enc.max(), contact.min_space)

        # iovdd
        net = nets.iovdd
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net}, well_net=net,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            bottom_extra=spec.iovdd_ntap_extra,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = frame.cells_y
        x = 0.5*cell_width

        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_ch, x=x, y=y)

        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=2,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = cell_width - _m2_bounds.right - metal2.min_space
        l = layouter.place(_l_via, x=x, y=y)
        m2_bounds1 = l.bounds(mask=metal2.mask)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=2,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        track_spec = frame.framespec._track_specs_dict["iovdd"]
        metal_spec = comp.metal[3]
        track_m3top = track_spec.top - 0.5*metal_spec.tracksegment_space
        y = track_m3top - _m2_bounds.top
        l = layouter.place(_l_via, x=x, y=y)
        m2_bounds2 = l.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=m2_bounds2, top=m2_bounds1.top)
        layouter.add_wire(wire=metal2, net=net, shape=shape)

        # acttrack
        acttrack_segs = frame._track_segments["actiovdd"]

        nw_enc = iopmos.computed.min_active_well_enclosure.max()
        def extend_nwell(*,
            n: int, l: "_lay.LayoutT", bottom: bool, top: bool,
        ):
            nw_bb = l.bounds(mask=nwell.mask)
            args: Dict[str, float] = {}
            if bottom:
                seg1 = acttrack_segs[n - 1]
                seg2 = acttrack_segs[n]
                edge = 0.5*(seg1.top + seg2.bottom)
                if nw_bb.bottom > (edge + _geo.epsilon):
                    args["bottom"] = edge
            if top:
                seg1 = acttrack_segs[n]
                seg2 = acttrack_segs[n + 1]
                edge = 0.5*(seg1.top + seg2.bottom)
                if nw_bb.top < (edge - _geo.epsilon):
                    args["top"] = edge
            if args:
                shape = _geo.Rect.from_rect(rect=nw_bb, **args)
                layouter.add_wire(net=net, wire=nwell, shape=shape)

        n_segs = len(acttrack_segs)
        for n, seg in enumerate(acttrack_segs):
            # Don't draw if it overlaps with pdio
            if (pdio_actbb is not None) and ((pdio_actbb.bottom - _geo.epsilon) < seg.top):
                continue
            if nclamp_actbb is None:
                if ndio_actbb is None:
                    assert pdio_actbb is None
                    # Draw full track
                    shape = _geo.Rect(
                        left=0.0, bottom=seg.bottom, right=cell_width, top=seg.top,
                    )
                    l = layouter.add_wire(
                        net=net, wire=contact, space=frame.trackconn_chspace,
                        well_net=net,
                        bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                        bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                    )
                    extend_nwell(n=n, l=l, bottom=(n > 0), top=(n < (n_segs - 1)))
                else:
                    # ndio is on left
                    if (seg.bottom -_geo.epsilon) < ndio_actbb.top:
                        if (seg.top - _geo.epsilon) < ndio_actbb.top:
                            shape = _geo.Rect(
                                left=ndio_actbb.right, bottom=seg.bottom,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=(n > 0), top=(n < (n_segs - 1)))
                        else:
                            shape = _geo.Rect(
                                left=ndio_actbb.right, bottom=seg.bottom,
                                right=cell_width, top=ndio_actbb.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=(n > 0), top=False)
                            shape = _geo.Rect(
                                left=0.0, bottom=ndio_actbb.top,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=False, top=(n < (n_segs - 1)))
                    else:
                        shape = _geo.Rect(
                            left=0.0, bottom=seg.bottom, right=cell_width, top=seg.top,
                        )
                        l = layouter.add_wire(
                            net=net, wire=contact, space=frame.trackconn_chspace,
                            well_net=net,
                            bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                            bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                        )
                        extend_nwell(n=n, l=l, bottom=(n > 0), top=(n < (n_segs - 1)))
            else:
                if pclamp_actbb is None:
                    # This is now for _PadIOVdd and no track is to be drawn now
                    continue
                if ndio_actbb is None:
                    if (seg.bottom -_geo.epsilon) < nclamp_actbb.top:
                        if (seg.top + _geo.epsilon) > nclamp_actbb.top:
                            shape = _geo.Rect(
                                left=0.0, bottom=nclamp_actbb.top,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=False, top=(n < (n_segs - 1)))
                        else:
                            # Don't draw
                            pass
                    else:
                            shape = _geo.Rect(
                                left=0.0, bottom=seg.bottom,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=(n > 0), top=(n < (n_segs - 1)))
                else:
                    if (seg.bottom -_geo.epsilon) < nclamp_actbb.top:
                        if (ndio_actbb.top + _geo.epsilon) > seg.top:
                            shape = _geo.Rect(
                                left=0.0, bottom=nclamp_actbb.top,
                                right=ndio_actbb.left, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=False, top=(n < (n_segs - 1)))
                            shape = _geo.Rect(
                                left=ndio_actbb.right, bottom=nclamp_actbb.top,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=False, top=(n < (n_segs - 1)))
                        else:
                            shape = _geo.Rect(
                                left=0.0, bottom=nclamp_actbb.top,
                                right=ndio_actbb.left, top=ndio_actbb.top,
                            )
                            layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            shape = _geo.Rect(
                                left=ndio_actbb.right, bottom=nclamp_actbb.top,
                                right=cell_width, top=ndio_actbb.top,
                            )
                            layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            shape = _geo.Rect(
                                left=0.0, bottom=ndio_actbb.top,
                                right=cell_width, top=seg.top,
                            )
                            l = layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                well_net=net,
                                bottom=active, bottom_well=nwell, bottom_extra=spec.iovdd_ntap_extra,
                                bottom_enclosure=actenc, bottom_shape=shape, top_shape=shape,
                            )
                            extend_nwell(n=n, l=l, bottom=False, top=(n < (n_segs - 1)))

        # Draw extra connection on left and right
        acttrack_bottom = acttrack_segs[0].bottom
        acttrack_top = acttrack_segs[-1].top

        left = 0.0
        right = left + metal1.min_width
        shape = _geo.Rect(left=left, bottom=acttrack_bottom, right=right, top=acttrack_top)
        layouter.add_wire(net=net, wire=metal1, shape=shape)
        right = left + active.min_width
        shape = _geo.Rect(left=left, bottom=acttrack_bottom, right=right, top=acttrack_top)
        layouter.add_wire(
            net=net, wire=active, shape=shape, implant=nimplant, well=nwell, well_net=net,
            extra=spec.iovdd_ntap_extra,
        )

        right = cell_width
        left = right - metal1.min_width
        shape = _geo.Rect(left=left, bottom=acttrack_bottom, right=right, top=acttrack_top)
        layouter.add_wire(net=net, wire=metal1, shape=shape)
        left = right - active.min_width
        shape = _geo.Rect(left=left, bottom=acttrack_bottom, right=right, top=acttrack_top)
        layouter.add_wire(
            net=net, wire=active, shape=shape, implant=nimplant, well=nwell, well_net=net,
            extra=spec.iovdd_ntap_extra,
        )

        # vss
        net = nets.vss
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net},
            bottom=active, bottom_implant=pimplant,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = spec.iorow_height + frame.cells_y
        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - _act_bounds.right - contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=8,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = -_m2_bounds.left + metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width -_m2_bounds.right - metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=8,
        )
        _m3_bounds = _l_via.bounds(mask=metal3.mask)
        x = -_m3_bounds.left + metal3.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_via, x=x, y=y)

        # vdd
        net = nets.vdd
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net}, well_net=net,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = spec.cells_height + frame.cells_y
        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - _act_bounds.right- contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=8,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = -_m2_bounds.left + metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width -_m2_bounds.right - metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=8,
        )
        _m3_bounds = _l_via.bounds(mask=metal3.mask)
        x = -_m3_bounds.left + metal3.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_via, x=x, y=y)

        # iovss
        net = nets.iovss
        right = cell_width
        track_spec = frame.framespec._track_specs_dict["iovdd"]
        acttrack_segs = frame._track_segments["actiovss"]
        acttrack_topseg = acttrack_segs[-1]
        # secondary protection is put below iorow cells
        act_top = acttrack_topseg.top
        # active and metal1 edge overlap in secondary protection cell
        m1_top = act_top

        # We currently need top act segment; different connections are now computed
        # with and without pad and this uses some assumptions of current layout
        # and may not be fully generic.
        if self.has_pad:
            bottom = acttrack_topseg.bottom
            if pclamp_actbb is not None:
                bottom = max(bottom, pclamp_actbb.top)
            else:
                ts2 = frame.track_specs["secondiovss"]
                bottom = ts2.bottom
        else:
            bottom = acttrack_topseg.bottom
        shape = _geo.Rect(
            left=0.0, bottom=bottom, right=cell_width, top=acttrack_topseg.top,
        )
        layouter.add_wire(
            net=net, wire=contact, space=frame.trackconn_chspace,
            bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
            bottom_shape=shape, bottom_enclosure=actenc,
            top_shape=shape,
        )

        for seg in acttrack_segs[:-1]:
            if pclamp_actbb is None:
                if pdio_actbb is None:
                    # _PadIOVdd only has top seg at the moment
                    continue
                else:
                    # pdio is on left
                    if (seg.bottom -_geo.epsilon) < pdio_actbb.top:
                        if (seg.top - _geo.epsilon) < pdio_actbb.top:
                            shape = _geo.Rect(
                                left=pdio_actbb.right, bottom=seg.bottom,
                                right=cell_width, top=seg.top,
                            )
                            layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                                bottom_shape=shape, bottom_enclosure=actenc,
                                top_shape=shape,
                            )
                        else:
                            shape = _geo.Rect(
                                left=pdio_actbb.right, bottom=seg.bottom,
                                right=cell_width, top=pdio_actbb.top,
                            )
                            layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                                bottom_shape=shape, bottom_enclosure=actenc,
                                top_shape=shape,
                            )
                            shape = _geo.Rect(
                                left=0.0, bottom=pdio_actbb.top,
                                right=cell_width, top=seg.top,
                            )
                            layouter.add_wire(
                                net=net, wire=contact, space=frame.trackconn_chspace,
                                bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                                bottom_shape=shape, bottom_enclosure=actenc,
                                top_shape=shape,
                            )
                    else:
                        shape = _geo.Rect(
                            left=0.0, bottom=seg.bottom, right=cell_width, top=seg.top,
                        )
                        layouter.add_wire(
                            net=net, wire=contact, space=frame.trackconn_chspace,
                            bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                            bottom_shape=shape, bottom_enclosure=actenc,
                            top_shape=shape,
                        )
            else:
                # Currently pdio is below the pclamp in other track so can be ignored.
                if (seg.bottom -_geo.epsilon) < pclamp_actbb.top:
                    if (seg.top + _geo.epsilon) > pclamp_actbb.top:
                        shape = _geo.Rect(
                            left=0.0, bottom=pclamp_actbb.top,
                            right=cell_width, top=seg.top,
                        )
                        layouter.add_wire(
                            net=net, wire=contact, space=frame.trackconn_chspace,
                            bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                            bottom_shape=shape, bottom_enclosure=actenc,
                            top_shape=shape,
                        )
                    else:
                        # Don't draw
                        pass
                else:
                    shape = _geo.Rect(
                        left=0.0, bottom=seg.bottom,
                        right=cell_width, top=seg.top,
                    )
                    layouter.add_wire(
                        net=net, wire=contact, space=frame.trackconn_chspace,
                        bottom=active, bottom_implant=pimplant, bottom_extra=spec.iovss_ptap_extra,
                        bottom_shape=shape, bottom_enclosure=actenc,
                        top_shape=shape,
                    )

        # Draw extra connection on left and right
        bottom = frame._track_segments["actiovss"][0].bottom
        left = 0.0
        right = left + metal1.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=m1_top)
        layouter.add_wire(net=net, wire=metal1, shape=shape)
        right = left + active.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=act_top)
        layouter.add_wire(
            net=net, wire=active, shape=shape, implant=pimplant, extra=spec.iovss_ptap_extra,
        )

        right = cell_width
        left = right - metal1.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=m1_top)
        layouter.add_wire(net=net, wire=metal1, shape=shape)
        left = right - active.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=act_top)
        layouter.add_wire(
            net=net, wire=active, shape=shape, implant=pimplant, extra=spec.iovss_ptap_extra,
        )

        if frame.has_secondiovss:
            # Connect to second iovss track
            iovss2_trackspec = frame.track_specs["secondiovss"]

            # We assume bottom tracl metal is metal3
            assert comp.metal[3].prim == comp.track_metalspecs[0].prim

            # Take space of the bottom layer of the track layers as segment space
            # draw after full height of the segment, even when
            metal_space = comp.track_metalspecs[0].tracksegment_space
            y = iovss2_trackspec.center
            height = iovss2_trackspec.top - iovss2_trackspec.bottom - metal_space

            _lay = layouter.wire_layout(
                net=net, wire=via1, space=frame.trackconn_viaspace, columns=12,
                bottom_height=height, bottom_enclosure="wide",
                top_height=height, top_enclosure="wide",
            )
            _m2_bb = _lay.bounds(mask=metal2.mask)
            x = metal2.min_space - _m2_bb.left
            layouter.place(_lay, x=x, y=y)

            _lay = layouter.wire_layout(
                net=net, wire=via2, space=frame.trackconn_viaspace, columns=12,
                bottom_height=height, bottom_enclosure="wide",
                top_height=height, top_enclosure="wide",
            )
            _m2_bb = _lay.bounds(mask=metal2.mask)
            x = metal2.min_space - _m2_bb.left
            layouter.place(_lay, x=x, y=y)

    def draw_tracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
        cell_width: Optional[float]=None,
        skip_top: Container[str]=(),
    ):
        spec = self.fab.spec
        nets = ckt.nets

        if cell_width is None:
            cell_width = spec.monocell_width

        # Draw tracks on higher metals
        self.draw_track(
            layouter=layouter, net=nets.iovss, cell_width=cell_width,
            track_segments=self._track_segments["iovss"],
            connect_top=("iovss" not in skip_top),
        )
        self.draw_track(
            layouter=layouter, net=nets.iovdd, cell_width=cell_width,
            track_segments=self._track_segments["iovdd"],
            connect_top=("iovdd" not in skip_top),
        )
        if self.has_secondiovss:
            self.draw_track(
                layouter=layouter, net=nets.iovss, cell_width=cell_width,
                track_segments=self._track_segments["secondiovss"],
                connect_top=("secondiovss" not in skip_top),
            )
        self.draw_duotrack(
            layouter=layouter, net1=nets.vss, net2=nets.vdd, cell_width=cell_width,
            track_segments=self._track_segments["vddvss"],
        )

    def draw_lowertracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT, cell_width: float,
        cells_only: bool,
    ) -> None:
        fab = self.fab
        comp = fab.computed
        frame = fab.frame
        spec = fab.spec

        nets = ckt.nets

        nwell = comp.nwell
        active = comp.active
        contact = comp.contact
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        metal1 = comp.metal[1].prim

        ch_space = (
            frame.trackconn_chspace
            if frame.trackconn_chspace is not None
            else contact.min_space
        )
        ch_pitch = contact.width + ch_space

        idx = contact.bottom.index(active)
        min_enc = contact.min_bottom_enclosure[idx]
        enc = _prp.Enclosure(max(min_enc.max(), ch_space))

        self._draw_tracks_lowerlayers(ckt=ckt, layouter=layouter, cell_width=cell_width)

        if not cells_only:
            # iovss
            net = nets.iovss
            for segment in self._track_segments["actiovss"]:
                shape = _geo.Rect(left=0.0, bottom=segment.bottom, right=cell_width, top=segment.top)
                if cell_width <= 4*ch_pitch:
                    layouter.add_wire(
                        net=net, wire=active, implant=pimplant, extra=spec.iovss_ptap_extra,
                        shape=shape,
                    )
                    layouter.add_wire(net=net, wire=metal1, shape=shape)
                else:
                    layouter.add_wire(
                        net=net, wire=contact, space=ch_space,
                        bottom=active, bottom_implant=pimplant, bottom_enclosure=enc,
                        bottom_extra=spec.iovss_ptap_extra, bottom_shape=shape,
                        top_shape=shape,
                    )
            # iovdd
            net = nets.iovdd
            nws = []
            for segment in self._track_segments["actiovdd"]:
                shape = _geo.Rect(left=0.0, bottom=segment.bottom, right=cell_width, top=segment.top)
                if cell_width <= 4*ch_pitch:
                    l = layouter.add_wire(
                        net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
                        extra=spec.iovdd_ntap_extra, shape=shape,
                    )
                    nws.append(l.bounds(mask=nwell.mask))
                    layouter.add_wire(net=net, wire=metal1, shape=shape)
                else:
                    l = layouter.add_wire(
                        net=net, wire=contact, well_net=net, space=ch_space,
                        bottom=active, bottom_implant=nimplant, bottom_well=nwell,
                        bottom_enclosure=enc, bottom_extra=spec.iovdd_ntap_extra,
                        bottom_shape=shape, top_shape=shape,
                    )
                    nws.append(l.bounds(mask=nwell.mask))
            left = min(r.left for r in nws)
            bottom = min(r.bottom for r in nws)
            right = max(r.right for r in nws)
            top = max(r.top for r in nws)
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(net=net, wire=nwell, shape=shape)

    def draw_corner_tracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
    ):
        nets = ckt.nets

        self.draw_corner_track(
            layouter=layouter, net=nets.iovss,
            track_segments=self._track_segments["iovss"]
        )
        self.draw_corner_track(
            layouter=layouter, net=nets.iovdd,
            track_segments=self._track_segments["iovdd"]
        )
        if self.has_secondiovss:
            self.draw_corner_track(
                layouter=layouter, net=nets.iovss,
                track_segments=self._track_segments["secondiovss"]
            )
        self.draw_corner_duotrack(
            layouter=layouter, net1=nets.vss, net2=nets.vdd,
            track_segments=self._track_segments["vddvss"],
        )

        self._draw_cornertracks_lowerlayers(ckt=ckt, layouter=layouter)

    def draw_track(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet, cell_width: float,
        track_segments: Tuple["_spec._SegmentSpecification", ...],
        connect_top: bool=True,
    ):
        """drawn shapes on the track always stay half minimum space from the
        track edge. This means tracks can be defined without space in between
        them.
        """
        fab = self.fab
        comp = fab.computed

        specs = comp.track_metalspecs
        for n_metal, mspec in enumerate(specs if connect_top else specs[:-1]):
            space = mspec.tracksegment_space

            for segment_spec in track_segments:
                bottom = segment_spec.bottom + 0.5*space
                top = segment_spec.top - 0.5*space

                shape = _geo.Rect(left=0.0, bottom=bottom, right=cell_width, top=top)
                layouter.add_wire(net=net, wire=mspec.prim, pin=mspec.prim.pin, shape=shape)

                if n_metal < (len(comp.track_metalspecs) - (1 if connect_top else 2)): # Not top metal
                    via = mspec.top_via
                    mspec2 = comp.track_metalspecs[n_metal + 1]
                    space2 = mspec2.tracksegment_space

                    top_bottom = segment_spec.bottom + 0.5*space2
                    top_top = segment_spec.top - 0.5*space2

                    via_space = self.tracksegment_viapitch - via.width
                    if cell_width > 10*space: # Don't draw vias for small width
                        layouter.add_wire(
                            wire=via, net=net, space=via_space,
                            bottom_left=via_space, bottom_bottom=(bottom + via_space),
                            bottom_right=(cell_width - via_space), bottom_top=(top - via_space),
                            top_left=via_space, top_bottom=(top_bottom + via_space),
                            top_right=(cell_width - via_space), top_top=(top_top - via_space),
                        )

        if not connect_top:
            # Draw top connection on left and right
            mspec = specs[-2]
            space = mspec.tracksegment_space
            mspec2 = specs[-1]
            space2 = mspec2.tracksegment_space
            via = mspec.top_via
            via_space = self.tracksegment_viapitch - via.width

            # assume spec of top is equal or higher than bottom
            assert (space - _geo.epsilon) < space2

            for segment_spec in track_segments:
                bottom_height = segment_spec.height - space
                top_height = segment_spec.height - space2

                _l_via = layouter.wire_layout(
                    net=net, wire=via, space=via_space, columns=2,
                    bottom_height=bottom_height, top_height=top_height,
                )
                bb = _l_via.bounds()
                y = segment_spec.center
                x = -bb.left
                l_via = layouter.place(_l_via, x=x, y=y)
                topbb = l_via.bounds(mask=mspec2.prim.mask)
                shape = _geo.Rect.from_rect(rect=topbb, left=0.0)
                layouter.add_wire(net=net, wire=mspec2.prim, pin=mspec2.prim.pin, shape=shape)
                x = self.monocell_width - bb.right
                l_via = layouter.place(_l_via, x=x, y=y)
                topbb = l_via.bounds(mask=mspec2.prim.mask)
                shape = _geo.Rect.from_rect(rect=topbb, right=self.monocell_width)
                layouter.add_wire(net=net, wire=mspec2.prim, pin=mspec2.prim.pin, shape=shape)

    def draw_duotrack(self, *,
        layouter: _lay.CircuitLayouterT, net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        cell_width: float, track_segments: Tuple["_spec._SegmentSpecification", ...],
    ):
        fab = self.fab
        tech = fab.tech

        prev_metal: Optional[_prm.MetalWire] = None
        prev_via: Optional[_prm.Via] = None
        prev_bottom_bottom: Optional[float] = None
        prev_bottom_top: Optional[float] = None
        prev_top_bottom: Optional[float] = None
        prev_top_top: Optional[float] = None
        for n, (
            bottom_net, top_net, metal, via, space,
            bottom_bottom, bottom_top, top_bottom, top_top,
        ) in enumerate(self._duotrack_iter(
            net1=net1, net2=net2, track_segments=track_segments,
        )):
            shape = _geo.Rect(left=0.0, bottom=bottom_bottom, right=cell_width, top=bottom_top)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=shape)

            shape = _geo.Rect(left=0.0, bottom=top_bottom, right=cell_width, top=top_top)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=shape)

            # Draw vias
            if n == 0:
                assert (prev_metal is None), "Internal error"
                assert (prev_via is None), "Internal error"
            elif cell_width > 10*space: # Only vias for wide cells
                # Draw via connection with prev_via
                assert prev_metal is not None
                assert prev_via is not None
                assert prev_bottom_bottom is not None
                assert prev_bottom_top is not None
                assert prev_top_bottom is not None
                assert prev_top_top is not None

                via_space = self.tracksegment_viapitch - prev_via.width

                if n == 1:
                    conn_width = tech.on_grid((cell_width - 2*space)/2, mult=2, rounding="floor")

                    via_bottommetal_width = tech.computed.min_width(
                        prev_metal, up=True, down=False, min_enclosure=True,
                    )
                    via_topmetal_width = tech.computed.min_width(
                        metal, up=False, down=True, min_enclosure=True,
                    )
                    ext = 0.5*via_bottommetal_width + 0.5*via_topmetal_width

                    layouter.add_wire(
                        wire=prev_via, net=bottom_net,
                        bottom_left=0.5*space,
                        bottom_bottom=prev_top_bottom,
                        bottom_right=(0.5*space + conn_width),
                        bottom_top=(prev_top_bottom + via_bottommetal_width),
                        bottom_enclosure="wide",
                        top_left=0.5*space,
                        top_bottom=bottom_top,
                        top_right=(0.5*space + conn_width),
                        top_top=(prev_top_bottom + ext),
                        top_enclosure="wide",
                    )
                    layouter.add_wire(
                        wire=prev_via, net=top_net,
                        bottom_left=(cell_width - 0.5*space - conn_width),
                        bottom_bottom=(prev_bottom_top - via_bottommetal_width),
                        bottom_right=(cell_width - 0.5*space),
                        bottom_top=prev_bottom_top,
                        bottom_enclosure="wide",
                        top_left=(cell_width - 0.5*space - conn_width),
                        top_bottom=(prev_bottom_top - ext),
                        top_right=(cell_width - 0.5*space),
                        top_top=top_bottom,
                        top_enclosure="wide",
                    )
                else:
                    layouter.add_wire(
                        wire=prev_via, net=bottom_net, space=via_space,
                        bottom_left=via_space,
                        bottom_bottom=(prev_bottom_bottom + via_space),
                        bottom_right=(cell_width - via_space),
                        bottom_top=(prev_bottom_top - via_space),
                        top_left=via_space, top_bottom=(bottom_bottom + via_space),
                        top_right=(cell_width - via_space), top_top=(bottom_top - via_space),
                    )

                    layouter.add_wire(
                        wire=prev_via, net=top_net, space=via_space,
                        bottom_left=via_space,
                        bottom_bottom=(prev_top_bottom + via_space),
                        bottom_right=(cell_width - via_space),
                        bottom_top=(prev_top_top - via_space),
                        top_left=via_space, top_bottom=(top_bottom + via_space),
                        top_right=(cell_width - via_space), top_top=(top_top - via_space),
                    )

            prev_metal = metal
            prev_via = via
            prev_bottom_bottom = bottom_bottom
            prev_bottom_top = bottom_top
            prev_top_bottom = top_bottom
            prev_top_top = top_top

    def draw_corner_track(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet,
        track_segments: Tuple["_spec._SegmentSpecification", ...],
    ):
        fab = self.fab
        comp = fab.computed

        pin_width = comp.track_metalspecs[0].tracksegment_space

        for mspec in comp.track_metalspecs:
            metal = mspec.prim
            space = mspec.tracksegment_space

            for segment_spec in track_segments:
                bottom = segment_spec.bottom + 0.5*space
                top = segment_spec.top - 0.5*space

                shape, pin1, pin2 = self._corner_segment(
                    bottom=bottom, top=top, pin_width=pin_width, small45=True,
                )
                layouter.add_wire(net=net, wire=mspec.prim, shape=shape)
                layouter.add_wire(net=net, wire=metal, pin=metal.pin, shape=pin1)
                layouter.add_wire(net=net, wire=metal, pin=metal.pin, shape=pin2)

    def draw_corner_duotrack(self, *,
        layouter: _lay.CircuitLayouterT, net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        track_segments: Tuple["_spec._SegmentSpecification", ...],
    ):
        fab = self.fab
        comp = fab.computed

        pin_width = comp.track_metalspecs[0].tracksegment_space

        for (
            bottom_net, top_net, metal, _, _,
            bottom_bottom, bottom_top, top_bottom, top_top,
        ) in self._duotrack_iter(
            net1=net1, net2=net2, track_segments=track_segments,
        ):
            poly, pin1, pin2 = self._corner_segment(
                bottom=bottom_bottom, top=bottom_top, pin_width=pin_width, small45=True,
            )
            layouter.add_wire(net=bottom_net, wire=metal, shape=poly)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=pin1)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=pin2)

            poly, pin1, pin2 = self._corner_segment(
                bottom=top_bottom, top=top_top, pin_width=pin_width, small45=True,
            )
            layouter.add_wire(net=top_net, wire=metal, shape=poly)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=pin1)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=pin2)

    def _draw_tracks_lowerlayers(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
        cell_width: float,
    ) -> None:
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        nets = ckt.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        metal1 = comp.metal[1].prim

        acttap_width = tech.computed.min_width(
            active, up=True, down=False, min_enclosure=True,
        )
        m1tap_width = tech.computed.min_width(
            metal1, up=False, down=True, min_enclosure=True,
        )

        # iovdd
        net = nets.iovdd
        x = 0.5*cell_width
        y = self.cells_y
        l = layouter.add_wire(
            net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
            x=x, y=y, width=cell_width, height=acttap_width,
        )
        nwell_bb = l.bounds(mask=nwell.mask)
        if nwell_bb.height < (nwell.min_width - _geo.epsilon):
            shape = _geo.Rect.from_rect(
                rect=nwell_bb,
                bottom=(nwell_bb.center.y - 0.5*nwell.min_width),
                top=(nwell_bb.center.y + 0.5*nwell.min_width),
            )
            layouter.add_wire(wire=nwell, net=net, shape=shape)

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

        # vss
        net = nets.vss
        x = 0.5*cell_width
        y = self.cells_y + spec.iorow_height
        layouter.add_wire(
            net=net, wire=active, implant=pimplant,
            x=x, y=y, width=cell_width, height=acttap_width,
        )

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

        # vdd
        net= nets.vdd
        x = 0.5*cell_width
        y = self.cells_y + spec.cells_height
        l = layouter.add_wire(
            net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
            x=x, y=y, width=cell_width, height=acttap_width,
        )
        nwell_bb = l.bounds(mask=nwell.mask)
        if nwell_bb.height < (nwell.min_width - _geo.epsilon):
            shape = _geo.Rect.from_rect(
                rect=nwell_bb,
                bottom=(nwell_bb.center.y - 0.5*nwell.min_width),
                top=(nwell_bb.center.y + 0.5*nwell.min_width),
            )
            layouter.add_wire(wire=nwell, net=net, shape=shape)

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

    def _draw_cornertracks_lowerlayers(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
    ) -> None:
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        nets = ckt.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        metal1 = comp.metal[1].prim

        pin_width = tech.grid

        acttap_width = tech.computed.min_width(
            active, up=True, down=False, min_enclosure=True,
        )
        m1tap_width = tech.computed.min_width(
            # we don't use minimal width to work around possible 45deg minimal width
            # violations in the corner cell.
            metal1, up=True, down=True, min_enclosure=False,
        )

        layout = layouter.layout

        # iovss
        net = nets.iovss
        tracksegs = self._track_segments["actiovss"]
        for segment in tracksegs:
            for net2, prim, shape in self._corner_active_segment(
                net=net, bottom=segment.bottom, top=segment.top,
                active=active, implant=pimplant, well=None, extra=spec.iovss_ptap_extra,
                small45=True,
            ):
                layout.add_shape(net=net2, layer=prim, shape=shape)
            shape, _, _ = self._corner_segment(
                bottom=segment.bottom, top=segment.top, pin_width=pin_width, small45=True,
            )
            layouter.add_wire(net=net, wire=metal1, shape=shape)
        if (pimplant is not None) and len(tracksegs) > 1:
            # Fill up pimplant
            idx = active.implant.index(pimplant)
            enc = active.min_implant_enclosure[idx]
            bottom = min(seg.bottom for seg in tracksegs)
            top = max(seg.top for seg in tracksegs)
            shape, _, _, = self._corner_segment(
                bottom=bottom, top=top, pin_width=pin_width, small45=False, ext=enc.first,
            )
            layouter.add_portless(prim=pimplant, shape=shape)

        # iovdd
        net = nets.iovdd
        y = self.cells_y
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=nimplant, well=nwell,
            small45=False,
        ):
            layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
            small45=False,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        tracksegs = self._track_segments["actiovdd"]
        for segment in tracksegs:
            for net2, prim, shape in self._corner_active_segment(
                net=net, bottom=segment.bottom, top=segment.top,
                active=active, implant=nimplant, well=nwell, extra=spec.iovdd_ntap_extra,
                small45=True,
            ):
                layout.add_shape(net=net2, layer=prim, shape=shape)
            shape, _, _ = self._corner_segment(
                bottom=segment.bottom, top=segment.top, pin_width=pin_width, small45=True,
            )
            layouter.add_wire(net=net, wire=metal1, shape=shape)
        if len(tracksegs) > 1:
            # Fill up nimplant and nwell
            bottom = min(seg.bottom for seg in tracksegs)
            top = max(seg.top for seg in tracksegs)
            if nimplant is not None:
                idx = active.implant.index(nimplant)
                enc = active.min_implant_enclosure[idx]
                shape, _, _, = self._corner_segment(
                    bottom=bottom, top=top, pin_width=pin_width, ext=enc.first, small45=False,
                )
                layouter.add_portless(prim=nimplant, shape=shape)
            if nwell is not None:
                idx = active.well.index(nwell)
                enc = active.min_well_enclosure[idx]
                shape, _, _, = self._corner_segment(
                    bottom=bottom, top=top, pin_width=pin_width, ext=enc.first, small45=False,
                )
                layouter.add_wire(net=net, wire=nwell, shape=shape)

        # vss
        net = nets.vss
        y = self.cells_y + spec.iorow_height
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=pimplant, well=None,
            small45=False,
        ):
            l = layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
            small45=False,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        # vdd
        net= nets.vdd
        y = self.cells_y + spec.cells_height
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=nimplant, well=nwell,
            small45=False,
        ):
            l = layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
            small45=False,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

    def _corner_segment(self, *,
        bottom: float, top: float, pin_width: float,
        ext: float=0.0, small45: bool,
    ) -> Tuple[_geo.Polygon, _geo.Polygon, _geo.Polygon]:
        fab = self.fab
        tech = fab.tech

        cell_height = self.cell_height

        d_top = tech.on_grid((cell_height - top)/_hlp._sqrt2)
        if not small45:
            # Don't violate minimum space between two neighboring segments.
            d_bottom = tech.on_grid(d_top + (top - bottom)/_hlp._sqrt2, rounding="floor")
        else:
            # Make 45 deg part smaller in width than manhattan parts
            d_bottom = tech.on_grid(d_top + (top - bottom)/2.5, rounding="floor")

        if (d_top - _geo.epsilon) < pin_width:
            pin_width = d_top - tech.grid

        if d_top < _geo.epsilon:
            shape = _geo.Polygon.from_floats(points=(
                (ext, bottom),
                (-d_bottom, bottom),
                (-(cell_height - bottom), cell_height - d_bottom),
                (-(cell_height - bottom), cell_height + ext),
                (ext, cell_height + ext),
                (ext, bottom),
            ))
        else:
            shape = _geo.Polygon.from_floats(points=(
                (ext, bottom),
                (-d_bottom, bottom),
                (-(cell_height - bottom), cell_height - d_bottom),
                (-(cell_height - bottom), cell_height + ext),
                (-(cell_height - top), cell_height + ext),
                (-(cell_height - top), cell_height - d_top),
                (-d_top, top),
                (ext, top),
                (ext, bottom),
            ))

        pin1 = _geo.Rect(left=(ext - pin_width), bottom=bottom, right=ext, top=top)
        pin2 = _geo.Rect(
            left=(-cell_height + bottom), bottom=(cell_height + ext - pin_width),
            right=(-cell_height + top), top=(cell_height + ext),
        )

        return shape, pin1, pin2

    def _corner_active_segment(self, *,
        net: _ckt.CircuitNetT, bottom: float, top: float,
        active: _prm.WaferWire, implant: Optional[_prm.Implant], well: Optional[_prm.Well],
        extra: Iterable[_prm.DesignMaskPrimitiveT]=frozenset(), small45: bool,
    ) -> Iterable[Tuple[Optional[_ckt.CircuitNetT], _prm.DesignMaskPrimitiveT, _geo.Polygon]]:
        fab = self.fab
        tech = fab.tech

        pin_width = tech.grid

        polygon, _, _ = self._corner_segment(
            bottom=bottom, top=top, pin_width=pin_width, small45=small45,
        )
        yield net, active, polygon

        if implant is not None:
            idx = active.implant.index(implant)
            enc = active.min_implant_enclosure[idx]
            # Ensure min enclosure also for the 45 deg part
            d = enc.second if not small45 else 2*enc.second
            polygon, _, _ = self._corner_segment(
                bottom=(bottom - d), top=(top + d), ext=enc.first,
                pin_width=pin_width, small45=small45,
            )
            yield None, implant, polygon

        if well is not None:
            idx = active.well.index(well)
            enc = active.min_well_enclosure[idx]
            ext = enc.second if not small45 else 2*enc.second
            if (top - bottom + 2*ext + _geo.epsilon) > well.min_width:
                bottom2 = bottom - ext
                top2 = top + ext
            else:
                y = 0.5*(bottom + top)
                bottom2 = y - 0.5*well.min_width
                top2 = y + 0.5*well.min_width
            polygon, _, _ = self._corner_segment(
                bottom=bottom2, top=top2, ext=enc.first, pin_width=pin_width, small45=small45,
            )
            yield net, well, polygon

        for prim in extra:
            yield None, prim, polygon

    def _duotrack_iter(self, *,
        net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        track_segments: Tuple["_spec._SegmentSpecification", ...],
    ) -> Iterable[Tuple[
        _ckt._CircuitNet, _ckt._CircuitNet, _prm.MetalWire, _prm.Via, float,
        float, float, float, float,
    ]]:
        fab = self.fab
        tech = fab.tech
        comp = fab.computed

        assert len(track_segments) == 2, "Internal error"
        bottom_segment = track_segments[0]
        top_segment = track_segments[1]

        prev_metal: Optional[_prm.MetalWire] = None
        for n_metal, mspec in enumerate(comp.track_metalspecs[:-1]):
            metal = mspec.prim
            top_via = mspec.top_via
            space = mspec.tracksegment_space

            # From second layer we exchange the nets
            bottom_net = net1 if (n_metal == 0) else net2
            top_net = net2 if (n_metal == 0) else net1

            bottom_bottom = bottom_segment.bottom + 0.5*space
            bottom_top = bottom_segment.top - 0.5*space

            top_bottom = top_segment.bottom + 0.5*space
            top_top = top_segment.top - 0.5*space

            # Smaller segments for second metal
            if n_metal == 1:
                assert prev_metal is not None

                prevmetal_width = tech.computed.min_width(
                    prev_metal, up=True, down=False, min_enclosure=True,
                )
                metal_width = tech.computed.min_width(
                    metal, up=False, down=True, min_enclosure=True,
                )
                dy = 0.5*prevmetal_width + 0.5*metal_width + space
                bottom_top -= dy
                top_bottom += dy

            yield (
                bottom_net, top_net, metal, top_via, space,
                bottom_bottom, bottom_top, top_bottom, top_top,
            )

            prev_metal = metal

    #
    # Pad support
    #

    @property
    def pad(self) -> "_FactoryCell":
        if not self.has_pad:
            raise AttributeError("No pad attribute as pad_height was not given")
        if self._pad is None:
            fab = self.fab
            self._pad = fab.pad(width=self.pad_width, height=self.pad_height)
        return self._pad
    @property
    def has_pad(self) -> bool:
        return hasattr(self, "pad_height")

    def pad_bb(self, *, prim: _prm.DesignMaskPrimitiveT) -> _geo.RectangularT:
        try:
            bb = self._pad_bb[prim]
        except KeyError:
            if self.has_pad:
                bb = self.pad.layout.bounds(mask=prim.mask).moved(
                    dxy=_geo.Point(x=0.5*self.monocell_width, y=self.pad_y),
                )
            else:
                bb = self._padpin_shape
            self._pad_bb[prim] = bb

        return bb

    def add_pad_inst(self, *, ckt: _ckt._Circuit, net: _ckt._CircuitNet):
        try:
            pad = self.pad
        except AttributeError:
            pass
        else:
            i_pad = ckt.instantiate(pad, name="pad")
            net.childports += i_pad.ports.pad

    def place_pad(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet,
    ) -> _lay.LayoutT:
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        ckt = layouter.circuit
        insts = ckt.instances

        if self.has_pad:
            i_pad = insts.pad
            topmetal = comp.metal[len(comp.vias)].prim

            x = 0.5*spec.monocell_width
            l_pad = layouter.place(i_pad, x=x, y=self.pad_y)
            pad_bounds = self.pad_bb(prim=topmetal)
            layouter.add_wire(net=net, wire=topmetal, pin=topmetal.pin, shape=pad_bounds)

            return l_pad
        else:
            # draw pin at the bottom
            l = layouter.fab.new_layout()

            pin_shape = self._padpin_shape

            for metalspec in (comp.metal[2], *comp.track_metalspecs):
                metal = metalspec.prim
                l += layouter.add_wire(
                    net=net, wire=metal, pin=metal.pin, shape=pin_shape,
                )
            for i, via in enumerate(comp.vias[2:]):
                if i == 0:
                    space = self.trackconn_viaspace
                else:
                    space = self.tracksegment_viapitch - via.width
                l += layouter.add_wire(
                    net=net, space=space, wire=via, bottom_shape=pin_shape, top_shape=pin_shape,
                )

            return l

    def connect_pad2track(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT, track: str,
        pclamp_lay: Optional[_lay.LayoutT],
        ndio_lay: Optional[_lay.LayoutT], pdio_lay: Optional[_lay.LayoutT],
    ) -> _lay.LayoutT:
        fab = self.fab
        tech = fab.tech
        comp = fab.computed

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        metal3spec = comp.metal[3]
        via1 = comp.vias[1]
        via2 = comp.vias[2]

        layout = fab.layoutfab.new_layout()

        pad_m2bb = self.pad_bb(prim=metal2)
        pad_at_bottom = (pad_m2bb.bottom - _geo.epsilon) < 0.0
        if pad_at_bottom:
            assert pclamp_lay is None, "Unsupported configuration"

        if (track == "iovdd") and not pad_at_bottom:
            iovdd_trackspec = self.track_specs["iovdd"]

            max_pitch = self.tracksegment_maxpitch
            fingers = floor((self.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(self.pad_width/fingers, mult=2, rounding="floor")
            track_top = iovdd_trackspec.top
            for metal_spec in comp.track_metalspecs:
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = self.pad_bb(prim=metal)
                width = pitch - space
                top = track_top - 0.5*space
                bottom = pad_bb.top
                for n in range(fingers):
                    if n < fingers - 1:
                        left = pad_bb.left + n*pitch + 0.5*space
                        right = left + width
                    else:
                        right = pad_bb.right - 0.5*space
                        left = right - width
                    shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                    layout += layouter.add_wire(net=pad, wire=metal, shape=shape)

        if (track == "iovss") and not pad_at_bottom:
            iovss_trackspec = self.track_specs["iovss"]

            max_pitch = self.tracksegment_maxpitch
            fingers = floor((self.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(self.pad_width/fingers, mult=2, rounding="floor")
            track_bottom = iovss_trackspec.bottom
            track_top = iovss_trackspec.top
            for metal_spec in comp.track_metalspecs:
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = self.pad_bb(prim=metal)
                width = pitch - space
                bottom = min(track_bottom + 0.5*space, pad_bb.top)
                top = max(track_top - 0.5*space, pad_bb.bottom)
                for n in range(fingers):
                    if n < fingers - 1:
                        left = pad_bb.left + n*pitch + 0.5*space
                        right = left + width
                    else:
                        right = pad_bb.right - 0.5*space
                        left = right - width
                    shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                    layout += layouter.add_wire(net=pad, wire=metal, shape=shape)

        if pclamp_lay is not None:
            if track == "iovss":
                m1_top = self._track_segments["actiovss"][-1].top
                clm1_bounds = pclamp_lay.bounds(mask=metal1.mask)
                m1_bottom = clm1_bounds.top

                for polygon in pclamp_lay.filter_polygons(
                    net=pad, mask=metal2.mask, split=True,
                ):
                    bounds = polygon.bounds
                    layout += layouter.add_wire(
                        wire=via1, net=pad,
                        top_left=bounds.left, top_right=bounds.right,
                        bottom_bottom=m1_bottom, bottom_top=m1_top,
                        top_bottom=m1_bottom, top_top=m1_top,
                    )

            if track in ("vss", "vdd"):
                # connect_trackspec = self.track_spec["vddvss"]
                connect_tracksegs = self._track_segments["vddvss"]
                assert len(connect_tracksegs) == 2
                trackseg = connect_tracksegs[0 if track == "vss" else 1]
                m3connect_bottom = trackseg.bottom + 0.5*metal3spec.tracksegment_space
                m3connect_top = trackseg.top - 0.5*metal3spec.tracksegment_space

                for polygon in pclamp_lay.filter_polygons(
                    net=pad, mask=metal2.mask, split=True,
                ):
                    bounds = polygon.bounds
                    via2_lay = layouter.add_wire(
                        wire=via2, net=pad,
                        bottom_left=bounds.left, bottom_right=bounds.right,
                        top_bottom=m3connect_bottom, top_top=m3connect_top,
                    )
                    layout += via2_lay
                    via2_m2bb = via2_lay.bounds(mask=metal2.mask)

                    shape = _geo.Rect.from_rect(rect=via2_m2bb, bottom=bounds.bottom)
                    layout += layouter.add_wire(net=pad, wire=metal2, shape=shape)
        else:
            assert (ndio_lay is not None) or (pdio_lay is not None), "Unsupported configuration"
            diom2_left = None
            if ndio_lay is not None:
                ndio_m1bb = ndio_lay.bounds(mask=metal1.mask)
                diom2_left = ndio_m1bb.right
            if pdio_lay is not None:
                pdio_m1bb = pdio_lay.bounds(mask=metal1.mask)
                diom2_left = (
                    pdio_m1bb.right
                    if diom2_left is None
                    else max(diom2_left, pdio_m1bb.right)
                )
            assert diom2_left is not None

            if track == "iovdd":
                tracksegs = self._track_segments["iovdd"]
            elif track == "iovss":
                if self.has_secondiovss:
                    tracksegs = (
                        *self._track_segments["iovss"],
                        *self._track_segments["secondiovss"],
                    )
                else:
                    tracksegs = self._track_segments["iovss"]
            elif track in ("vss", "vdd"):
                connect_tracksegs = self._track_segments["vddvss"]
                assert len(connect_tracksegs) == 2
                tracksegs = (connect_tracksegs[0 if track == "vss" else 1],)
            else:
                raise RuntimeError("Internal error")

            max_pitch = self.tracksegment_maxpitch
            w = pad_m2bb.right - diom2_left
            fingers = floor((w + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(w/fingers, mult=2, rounding="floor")
            metal_spec = comp.track_metalspecs[0]
            metal = metal_spec.prim
            space = metal_spec.tracksegment_space

            pad_bb = self.pad_bb(prim=metal)
            width = pitch - space
            for n in range(fingers):
                if n < fingers - 1:
                    left = diom2_left + n*pitch + space
                    right = left + width
                else:
                    right = pad_bb.right
                    left = right - width
                top2 = 0.0
                for trackseg in tracksegs:
                    bottom = trackseg.bottom + 0.5*space
                    top = trackseg.top - 0.5*space
                    shape = _geo.Rect(
                        left=left, bottom=bottom, right=right, top=top,
                    )
                    layout += layouter.add_wire(
                        net=pad, wire=via2, space=self.trackconn_viaspace, top_shape=shape,
                    )
                    top2 = max(top2, top)
                shape = _geo.Rect(
                    left=left, bottom=pad_m2bb.bottom, right=right, top=top2,
                )
                layout += layouter.add_wire(net=pad, wire=metal2, shape=shape)

        return layout

    @property
    def _padpin_shape(self) -> _geo.Rect:
        if self.__padpin_shape is None:
            comp = self.fab.computed
            space = max(metalspec.tracksegment_space for metalspec in comp.track_metalspecs)
            self.__padpin_shape = _geo.Rect(
                left=space, bottom=0.0,
                right=(self.monocell_width - space), top=self.padpin_height,
            )
        return self.__padpin_shape

    #
    # clamp support
    #

    def add_clamp_nets(self, *,
        ckt: _ckt.CircuitT, add_n: bool=True, add_p: bool=True,
    ):
        if add_n:
            ckt.new_net(name="ngate", external=False)
        if add_p:
            ckt.new_net(name="pgate", external=False)

    def add_nclamp_inst(self, *,
        ckt: _ckt.CircuitT, n_trans: int, n_drive: int, rows: Optional[int]=None,
        pad: _ckt.CircuitNetT,
    ) -> None:
        fab = self.fab
        nets = ckt.nets

        if (n_trans != 0) or (n_drive != 0):
            c_clamp = fab.clamp(
                type_="n", n_trans=max(n_trans, n_drive), n_drive=n_drive, rows=rows,
            )
            i_clamp = ckt.instantiate(c_clamp, name="nclamp")
            nets.iovdd.childports += i_clamp.ports.iovdd
            nets.iovss.childports += i_clamp.ports.iovss
            pad.childports += i_clamp.ports.pad
            if n_drive > 0:
                nets.ngate.childports += i_clamp.ports.gate

    def add_pclamp_inst(self, *,
        ckt: _ckt.CircuitT, n_trans: int, n_drive: int,
        pad: _ckt.CircuitNetT,
    ) -> None:
        fab = self.fab
        nets = ckt.nets

        if (n_trans != 0) or  (n_drive != 0):
            c_clamp = fab.clamp(type_="p", n_trans=max(n_trans, n_drive), n_drive=n_drive)
            i_clamp = ckt.instantiate(c_clamp, name="pclamp")
            nets.iovdd.childports += i_clamp.ports.iovdd
            nets.iovss.childports += i_clamp.ports.iovss
            pad.childports += i_clamp.ports.pad
            if n_drive > 0:
                nets.pgate.childports += i_clamp.ports.gate

    def place_nclamp(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
    ) -> Optional[_lay.LayoutT]:
        fab = self.fab
        comp = fab.computed

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        try:
            inst = insts["nclamp"]
        except:
            # No nclamp was added
            return

        layout = layouter.layout

        metal2 = comp.metal[2].prim

        iovss_trackspec = self.track_specs["iovss"]

        l_nclamp = layouter.place(inst, x=0.0, y=iovss_trackspec.bottom)
        for polygon in self._pinpolygons(polygons=l_nclamp.polygons):
            layout.add_shape(net=nets.iovss, shape=polygon)

        pad_m2bb = self.pad_bb(prim=metal2)
        for polygon in l_nclamp.filter_polygons(net=pad, mask=metal2.pin.mask):
            # Iterate over bounds of individual shapes
            for bounds in _hlp._iterate_polygonbounds(polygon=polygon):
                shape = _geo.Rect.from_rect(
                    rect=bounds,
                    top=max(bounds.top, pad_m2bb.bottom),
                    bottom=min(bounds.bottom, pad_m2bb.top),
                )
                layouter.add_wire(wire=metal2, net=pad, shape=shape)

        return l_nclamp

    def place_pclamp(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
    ) -> Optional[_lay.LayoutT]:
        fab = self.fab
        comp = fab.computed

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        try:
            inst = insts["pclamp"]
        except:
            # No pclamp was added
            return

        layout = layouter.layout

        metal2 = comp.metal[2].prim

        iovdd_trackspec = self.track_specs["iovdd"]

        l_pclamp = layouter.place(inst, x=0.0, y=iovdd_trackspec.bottom)
        for polygon in self._pinpolygons(polygons=l_pclamp.polygons):
            layout.add_shape(net=nets.iovdd, shape=polygon)

        pad_m2bb = self.pad_bb(prim=metal2)
        for polygon in l_pclamp.filter_polygons(net=pad, mask=metal2.mask):
            # Iterate over bounds of individual shapes
            for bounds in _hlp._iterate_polygonbounds(polygon=polygon):
                shape = _geo.Rect.from_rect(rect=bounds, bottom=pad_m2bb.top)
                layouter.add_wire(wire=metal2, net=pad, shape=shape)

        return l_pclamp

    def add_rcclamp_insts(self, *,
        ckt: _ckt.CircuitT, pad: _ckt.CircuitNetT,
    ):
        fab = self.fab
        spec = fab.spec

        nets = ckt.nets
        iovss = nets["iovss"]

        self.add_clamp_nets(ckt=ckt, add_p=False)
        self.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.rcclampdrive, rows=spec.rcclamp_rows,
            pad=pad,
        )
        ngate = nets["ngate"]

        c_res = fab.get_cell("RCClampResistor")
        i_res = ckt.instantiate(c_res, name="rcres")
        pad.childports += i_res.ports.pin1

        c_inv = fab.get_cell("RCClampInverter")
        i_inv = ckt.instantiate(c_inv, name="rcinv")
        iovss.childports += i_inv.ports.ground
        pad.childports += i_inv.ports.supply
        ngate.childports += i_inv.ports.out

        ckt.new_net(name="res_cap", external=False, childports=(
            i_res.ports.pin2, i_inv.ports["in"],
        ))

    def layout_rcclamp(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
    ) -> _lay.LayoutT:
        fab = self.fab
        comp = fab.computed
        spec = fab.spec
        tech = fab.tech

        ckt = layouter.circuit

        nets = ckt.nets
        insts = ckt.instances

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        metal3 = metal[3].prim
        via1 = comp.vias[1]
        via2 = comp.vias[2]

        iovss_trackspec = self.track_specs["iovss"]
        iovdd_trackspec = self.track_specs["iovdd"]

        padm2_bounds = self.pad_bb(prim=metal2)

        # Place nclamp + connect to pad + pad guard ring
        l_nclamp = layouter.place(insts.nclamp, x=0.0, y=iovss_trackspec.bottom)
        for polygon in l_nclamp.filter_polygons(
            net=pad, mask=metal2pin.mask, split=True,
        ):
            bb = polygon.bounds
            shape = _geo.Rect.from_rect(
                rect=bb,
                top=max(bb.top, padm2_bounds.bottom),
                bottom=min(bb.bottom, padm2_bounds.top),
            )
            layouter.add_wire(wire=metal2, net=pad, shape=shape)

            if pad == nets["iovdd"]:
                y = bb.top
                layouter.add_wire(
                    net=pad, wire=via1, y=y,
                    bottom_left=shape.left, bottom_right=shape.right, bottom_enclosure="tall",
                    top_left=shape.left, top_right=shape.right, top_enclosure="tall",
                )

        # Draw guardring around pad and connect to iovdd track
        bottom = cast(_geo._Rectangular, l_nclamp.boundary).top
        top = iovdd_trackspec.bottom - comp.guardring_space
        c_guard = fab.guardring(
            type_="n", width=spec.monocell_width, height=(top - bottom),
        )
        inst_guard = ckt.instantiate(c_guard, name="pad_guard")
        nets["iovss"].childports += inst_guard.ports["conn"]
        l = layouter.place(inst_guard, x=0.5*spec.monocell_width, y=0.5*(bottom + top))
        padguardring_m1bb = l.bounds(mask=metal1.mask)

        # Place the RC clamp subblocks
        l_rcinv = layouter.place(
            insts.rcinv, x=spec.monocell_width, y=iovdd_trackspec.bottom,
            rotation=_geo.Rotation.MY,
        )
        _l = layouter.inst_layout(inst=insts.rcres, rotation=_geo.Rotation.MX)
        _bb = _l.boundary
        assert _bb is not None
        if self.has_pad:
            o = padm2_bounds.center - _bb.center
        else:
            nclamp_m1bb = l_nclamp.bounds(mask=metal1.mask)
            o = _geo.Point(
                x=(0.5*self.monocell_width - _bb.center.x),
                y=(
                    tech.on_grid(0.5*(nclamp_m1bb.top + iovdd_trackspec.bottom))
                    - _bb.center.y
                ),
            )
        l_rcres = layouter.place(_l, origin=o)

        # Connect supply of inv to track with same net as pad
        net = pad
        m1pinbb = l_rcinv.bounds(mask=metal1pin.mask, net=net, depth=1)

        if net == nets["iovdd"]:
            w = m1pinbb.width
            _l = layouter.wire_layout(
                net=net, wire=via1,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
            _m1bb = _l.bounds(mask=metal1.mask)
            x = m1pinbb.center.x
            y = m1pinbb.bottom - _m1bb.bottom
            layouter.place(_l, x=x, y=y)

            layouter.add_wire(
                net=net, wire=via2, x=x, y=y,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
        elif net == nets["vdd"]:
            w = m1pinbb.width
            _l = layouter.wire_layout(
                net=net, wire=via1,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
            _m1bb = _l.bounds(mask=metal1.mask)
            x = m1pinbb.center.x
            y = m1pinbb.bottom - _m1bb.bottom
            l = layouter.place(_l, x=x, y=y)
            m2bb1 = l.bounds(mask=metal2.mask)

            metal3spec = comp.metal[3]
            trackseg = self._track_segments["vddvss"][1]
            m3connect_bottom = trackseg.bottom + 0.5*metal3spec.tracksegment_space

            _l = layouter.wire_layout(
                net=net, wire=via2, rows=2,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
            _m3bb = _l.bounds(mask=metal3.mask)
            # x = x
            y = m3connect_bottom - _m3bb.bottom
            l = layouter.place(_l, x=x, y=y)
            m2bb2 = l.bounds(mask=metal2.mask)

            w = m2bb1.width
            max_pitch = self.tracksegment_maxpitch
            # Take space from M3
            space = comp.track_metalspecs[0].tracksegment_space
            fingers = floor((w + space + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(w/fingers, mult=2, rounding="floor")
            w_finger = pitch - space
            bottom = m2bb1.bottom
            top = m2bb2.top
            for n in range(fingers):
                if n < fingers - 1:
                    left = m2bb1.left + n*pitch
                    right = left + w_finger
                else:
                    right = m2bb1.right
                    left = right - w_finger
                shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                layouter.add_wire(
                    net=net, wire=metal2, shape=shape,
                )
        else: # pragma: no cover
            raise NotImplementedError(f"net '{net.name} for RCClampInverter supply")

        # Connect res output to inv input
        net = nets.res_cap
        res_m1pinbb = l_rcres.bounds(mask=metal1pin.mask, net=net, depth=1)
        inv_m2pinbb = l_rcinv.bounds(mask=metal2pin.mask, net=net, depth=1)

        w = inv_m2pinbb.right - res_m1pinbb.left
        _l = layouter.wire_layout(
            net=net, wire=via1,
            bottom_width=w, bottom_enclosure="tall",
            top_width=w, top_enclosure="tall",
        )
        _via1_m1bb = _l.bounds(mask=metal1.mask)
        x = res_m1pinbb.left - _via1_m1bb.left
        y = (
            padguardring_m1bb.top - comp.guardring_width - 2*metal1.min_space
            - _via1_m1bb.top
        )
        l = layouter.place(_l, x=x, y=y)
        via1_m1bb = l.bounds(mask=metal1.mask)
        via1_m2bb = l.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=res_m1pinbb, top=via1_m1bb.top)
        layouter.add_wire(net=net, wire=metal1, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=inv_m2pinbb,
            bottom=via1_m2bb.bottom, left=max(inv_m2pinbb.left, via1_m2bb.left),
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # Connect inv output to gate of nclamp
        net = nets.ngate
        inv_m2pinbb = l_rcinv.bounds(mask=metal2pin.mask, net=net, depth=1)
        nclamp_m2pinbb = l_nclamp.bounds(mask=metal2pin.mask, net=net, depth=1)

        left = 2*metal2.min_space
        shape = _geo.Rect.from_rect(rect=inv_m2pinbb, left=left)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=nclamp_m2pinbb, left=left)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=nclamp_m2pinbb.bottom,
            right=(left + 2*metal2.min_width), top=inv_m2pinbb.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # Connect pin1 of rcres to pad
        m1pinbb = l_rcres.bounds(mask=metal1pin.mask, net=pad, depth=1)

        _l = layouter.wire_layout(
            net=pad, wire=via1, columns=2,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bb = _l.bounds(mask=metal1.mask)
        x = m1pinbb.right - _m1bb.right
        y = m1pinbb.center.y
        l = layouter.place(_l, x=x, y=y)
        m2bb = l.bounds(mask=metal2.mask)
        if self.has_pad:
            _l = layouter.wire_layout(
                net=pad, wire=via2, columns=2,
                bottom_enclosure="tall", top_enclosure="tall",
            )
            _m2bb = _l.bounds(mask=metal2.mask)
            x = m2bb.right - _m2bb.right
            layouter.place(_l, x=x, y=y)
        else:
            w = m2bb.height
            x1 = m2bb.center.x
            y1 = m2bb.center.y
            x2 = nclamp_m2pinbb.right + metal2.min_space + w
            y2 = padm2_bounds.top
            shape = _geo.MultiPath(
                _geo.Start(point=m2bb.center, width=w),
                _geo.GoLeft(dist=(x1 - x2)),
                _geo.GoDown(dist=(y1 - y2)),
            )
            layouter.add_wire(net=pad, wire=metal2, shape=shape)

        return l_nclamp

    def _pinpolygons(self, *, polygons: Iterable[_geo.MaskShape]) -> Iterable[_geo.MaskShape]:
        trackmetalspecs = self.fab.computed.track_metalspecs
        trackpinmasks = tuple(spec.prim.pin.mask for spec in trackmetalspecs)

        return filter(lambda p: p.mask in trackpinmasks, polygons)

    def connect_clamp_wells(self, *,
        ckt: _ckt.CircuitT, layouter: _lay.CircuitLayouterT,
        nclamp_lay: Optional[_lay.LayoutT], pclamp_lay: Optional[_lay.LayoutT],
    ):
        if (nclamp_lay is None) or (pclamp_lay is None) or not self.has_pad:
            return

        nets = ckt.nets
        fab = self.fab
        comp = fab.computed

        width = self.monocell_width

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]

        bottom = cast(_geo._Rectangular, nclamp_lay.boundary).top
        top = cast(_geo._Rectangular, pclamp_lay.boundary).bottom - comp.guardring_space
        c_guardring = fab.guardring(
            type_="n", width=width, height=(top - bottom),
        )
        inst_guardring = ckt.instantiate(c_guardring, name="pad_guardring")
        nets["iovss"].childports += inst_guardring.ports["conn"]
        l_guardring = layouter.place(
            inst_guardring, x=0.5*width, y=0.5*(bottom + top),
        )
        guardringm1_bounds = l_guardring.bounds(mask=metal1.mask)
        viatop = guardringm1_bounds.top
        viay = viatop - 0.5*comp.metal[2].minwidth4ext_updown
        for polygon in pclamp_lay.filter_polygons(net=nets.iovdd, mask=metal2.mask):
            for bounds in _hlp._iterate_polygonbounds(polygon=polygon):
                l_via = layouter.add_wire(
                    net=nets.iovdd, wire=via1, y=viay,
                    top_left=bounds.left, top_right=bounds.right,
                )
                viam2_bounds = l_via.bounds(mask=metal2.mask)
                layouter.add_wire(net=nets.iovdd, wire=metal2, shape=_geo.Rect.from_rect(
                    rect=bounds, bottom=viam2_bounds.bottom,
                ))

    #
    # DCDiodes support
    #

    def add_dcdiodes_inst(self, *, ckt: _ckt.CircuitT, pad: _ckt.CircuitNetT) -> None:
        fab = self.fab
        spec = fab.spec

        if not spec.add_dcdiodes:
            return None
        else:
            if self.has_pad:
                raise NotImplementedError("DCDiodes with a pad")

        nets = ckt.nets

        iovdd = nets["iovdd"]
        iovss = nets["iovss"]

        ndio_cell = fab.dcdiode(type_="n")
        pdio_cell = fab.dcdiode(type_="p")

        ndio_inst = ckt.instantiate(ndio_cell, name="dcndiode")
        pdio_inst = ckt.instantiate(pdio_cell, name="dcpdiode")

        pad.childports += (ndio_inst.ports["cathode"], pdio_inst.ports["anode"])
        iovss.childports += (ndio_inst.ports["anode"], pdio_inst.ports["guard"])
        iovdd.childports += (ndio_inst.ports["guard"], pdio_inst.ports["cathode"])

    def place_dcdiodes(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
        nclamp_lay: Optional[_lay.LayoutT], pclamp_lay: Optional[_lay.LayoutT],
    ) -> Tuple[Optional[_lay.LayoutT], Optional[_lay.LayoutT]]:
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        if not spec.add_dcdiodes:
            return None, None

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]
        via2 = comp.vias[2]

        iovdd = nets["iovdd"]
        iovss = nets["iovss"]

        ndio_inst = insts["dcndiode"]
        _ndio_lay = layouter.inst_layout(inst=ndio_inst)
        _ndio_m1bb = _ndio_lay.bounds(mask=metal1.mask)
        assert _ndio_m1bb is not None

        pdio_inst = insts["dcpdiode"]
        _pdio_lay = layouter.inst_layout(inst=pdio_inst)
        _pdio_m1bb = _pdio_lay.bounds(mask=metal1.mask)
        assert _pdio_m1bb is not None

        if nclamp_lay is not None:
            assert pclamp_lay is not None, "Internal error"

            # Place ndiode
            nclamp_m1bb = nclamp_lay.bounds(mask=metal1.mask)
            x = 0.5*self.monocell_width - _ndio_m1bb.center.x
            y = nclamp_m1bb.top - _ndio_m1bb.bottom
            ndio_lay = layouter.place(_ndio_lay, x=x, y=y)

            pclamp_m1bb = pclamp_lay.bounds(mask=metal1.mask)
            x = 0.5*self.monocell_width - _pdio_m1bb.center.x
            y = pclamp_m1bb.bottom - _pdio_m1bb.top
            pdio_lay = layouter.place(_pdio_lay, x=x, y=y)

            m2left = None
            m2right = None

            # connect pad
            for pad_nclamp_m2poly in nclamp_lay.filter_polygons(
                net=pad, mask=metal2.pin.mask, depth=1, split=True,
            ):
                bb = pad_nclamp_m2poly.shape.bounds
                for pad_ndio_m1poly in ndio_lay.filter_polygons(
                    net=pad, mask=metal1.pin.mask, depth=1, split=True,
                ):
                    bb2 = pad_ndio_m1poly.shape.bounds
                    if (bb2.left < bb.left) and (bb2.right > bb.right):
                        shape = _geo.Rect(
                            left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                        )
                        layouter.add_wire(net=pad, wire=via1, bottom_shape=shape, top_shape=shape)
                m2left = bb.left if m2left is None else min(m2left, bb.left)
                m2right = bb.right if m2right is None else max(m2right, bb.right)

            for pad_pclamp_m2poly in pclamp_lay.filter_polygons(
                net=pad, mask=metal2.pin.mask, depth=1, split=True,
            ):
                bb = pad_pclamp_m2poly.shape.bounds
                for pad_pdio_m1poly in pdio_lay.filter_polygons(
                    net=pad, mask=metal1.pin.mask, depth=1, split=True,
                ):
                    bb2 = pad_pdio_m1poly.shape.bounds
                    if (bb2.left < bb.left) and (bb2.right > bb.right):
                        shape = _geo.Rect(
                            left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                        )
                        layouter.add_wire(net=pad, wire=via1, bottom_shape=shape, top_shape=shape)
                m2left = bb.left if m2left is None else min(m2left, bb.left)
                m2right = bb.right if m2right is None else max(m2right, bb.right)

            # Connect iovss
            pclamp_botbb = None # get bottom bb pin of pclamp
            for iovss_pdio_m1poly in pdio_lay.filter_polygons(
                net=iovss, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb = iovss_pdio_m1poly.shape.bounds
                if (pclamp_botbb is None) or (bb.bottom < pclamp_botbb.bottom):
                    pclamp_botbb = bb
            assert pclamp_botbb is not None

            for iovss_nclamp_m2poly in nclamp_lay.filter_polygons(
                net=iovss, mask=metal2.mask, depth=1, split=True,
            ):
                bb = iovss_nclamp_m2poly.shape.bounds
                for iovss_ndio_m1poly in ndio_lay.filter_polygons(
                    net=iovss, mask=metal1.pin.mask, depth=1, split=True,
                ):
                    bb2 = iovss_ndio_m1poly.shape.bounds
                    if (bb2.left < bb.left) and (bb2.right > bb.right):
                        shape = _geo.Rect(
                            left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                        )
                        layouter.add_wire(net=iovss, wire=via1, bottom_shape=shape, top_shape=shape)

                    if (pclamp_botbb.left < bb.left) and (pclamp_botbb.right > bb.right):
                        shape = _geo.Rect(
                            left=bb.left, bottom=pclamp_botbb.bottom, right=bb.right, top=pclamp_botbb.top,
                        )
                        layouter.add_wire(net=iovss, wire=via1, bottom_shape=shape, top_shape=shape)

                        shape = _geo.Rect.from_rect(rect=shape, bottom=bb.top)
                        layouter.add_wire(net=iovss, wire=metal2, shape=shape)
                m2left = bb.left if m2left is None else min(m2left, bb.left)
                m2right = bb.right if m2right is None else max(m2right, bb.right)

            # connect iovdd
            for iovdd_pclamp_m2poly in pclamp_lay.filter_polygons(
                net=iovdd, mask=metal2.mask, depth=1, split=True,
            ):
                bb = iovdd_pclamp_m2poly.shape.bounds
                for iovdd_pdio_m1poly in pdio_lay.filter_polygons(
                    net=iovdd, mask=metal1.pin.mask, depth=1, split=True,
                ):
                    bb2 = iovdd_pdio_m1poly.shape.bounds
                    if (bb2.left < bb.left) and (bb2.right > bb.right):
                        shape = _geo.Rect(
                            left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                        )
                        layouter.add_wire(net=iovdd, wire=via1, bottom_shape=shape, top_shape=shape)

                        shape = _geo.Rect.from_rect(rect=shape, top=bb.bottom)
                        layouter.add_wire(net=iovdd, wire=metal2, shape=shape)
                m2left = bb.left if m2left is None else min(m2left, bb.left)
                m2right = bb.right if m2right is None else max(m2right, bb.right)

            # Extra pad/iovss/iovdd connections if there is room
            min_w = 3*(metal2.min_width + metal2.min_space)
            assert m2left is not None
            assert m2right is not None
            m2right += comp.track_metalspecs[0].tracksegment_space

            for pad_ndio_m1poly in ndio_lay.filter_polygons(
                net=pad, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_ndio_m1poly.shape.bounds
                if (bb2.right - m2right) > min_w:
                    shape = _geo.Rect(
                        left=m2right, bottom=bb2.bottom, right=bb2.right, top=bb2.top,
                    )
                    layouter.add_wire(net=pad, wire=via1, bottom_shape=shape, top_shape=shape)

            top = None
            bottom = None
            left = None
            for pad_ndio_m1poly in ndio_lay.filter_polygons(
                net=nets.iovss, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_ndio_m1poly.shape.bounds
                if (m2left - bb2.left) > min_w:
                    shape = _geo.Rect(
                        left=bb2.left, bottom=bb2.bottom,
                        right=(m2left- metal2.min_space), top=bb2.top,
                    )
                    layouter.add_wire(
                        net=nets.iovss, wire=via1, bottom_shape=shape, top_shape=shape,
                    )
                    top = bb2.top if top is None else max(top, bb2.top)
                    bottom = bb2.bottom if bottom is None else min(bottom, bb2.bottom)
                    left = bb2.left
            if ((top is not None) and (bottom is not None) and (left is not None)):
                shape = _geo.Rect(
                    left=left, bottom=bottom, right=m2left, top=top,
                )
                layouter.add_wire(net=nets.iovss, wire=metal2, shape=shape)

            top_padm2bb = None
            for pad_pdio_m1poly in pdio_lay.filter_polygons(
                net=pad, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_pdio_m1poly.shape.bounds
                if (bb2.right - m2right) > min_w:
                    shape = _geo.Rect(
                        left=m2right, bottom=bb2.bottom, right=bb2.right, top=bb2.top,
                    )
                    l_via1 = layouter.add_wire(
                        net=pad, wire=via1, bottom_shape=shape, top_shape=shape,
                    )
                    via1_m2bb = l_via1.bounds(mask=metal2.mask)
                    if (top_padm2bb is None) or (via1_m2bb.top > top_padm2bb.top):
                        top_padm2bb = via1_m2bb
            if top_padm2bb is not None:
                shape = _geo.Rect.from_rect(
                    rect=top_padm2bb, bottom=self.pad_bb(prim=metal2).bottom,
                )
                layouter.add_wire(net=pad, wire=metal2, shape=shape)

            top = None
            bottom = None
            left = None
            for pad_pdio_m1poly in pdio_lay.filter_polygons(
                net=nets.iovdd, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_pdio_m1poly.shape.bounds
                if (m2left - bb2.left) > min_w:
                    shape = _geo.Rect(
                        left=bb2.left, bottom=bb2.bottom,
                        right=(m2left - metal2.min_space), top=bb2.top,
                    )
                    layouter.add_wire(
                        net=nets.iovdd, wire=via1, bottom_shape=shape, top_shape=shape,
                    )
                    top = bb2.top if top is None else max(top, bb2.top)
                    bottom = bb2.bottom if bottom is None else min(bottom, bb2.bottom)
                    left = bb2.left
            if ((top is not None) and (bottom is not None) and (left is not None)):
                shape = _geo.Rect(
                    left=left, bottom=bottom, right=m2left, top=top,
                )
                layouter.add_wire(net=nets.iovdd, wire=metal2, shape=shape)
        else:
            pad_m2bb = self.pad_bb(prim=metal2)

            ts = self.track_specs["iovss"]
            assert (_ndio_m1bb.width - _geo.epsilon) < ts.width
            # Rotate diode with 90 degrees
            x = _ndio_m1bb.top
            y = ts.bottom - _ndio_m1bb.bottom
            ndio_lay = layouter.place(_ndio_lay, x=x, y=y, rotation=_geo.Rotation.R90)
            ndio_m1bb = ndio_lay.bounds(mask=metal1.mask)

            # We assume pad connection is done by the pad connection of the pdiode
            assert pclamp_lay is None

            ts = self.track_specs["iovdd"]
            assert (_pdio_m1bb.width - _geo.epsilon) < ts.width
            # Rotate diode with 90 degrees
            x = _pdio_m1bb.top
            y = ts.bottom - _pdio_m1bb.left
            pdio_lay = layouter.place(_pdio_lay, x=x, y=y, rotation=_geo.Rotation.R90)
            pdio_m1bb = pdio_lay.bounds(mask=metal1.mask)

            # connect pad
            # if pad net is iovss connection will be done below
            if pad != iovss:
                for pad_ndio_m1ms in ndio_lay.filter_polygons(
                    net=pad, mask=metal1.pin.mask, depth=1, split=True,
                ):
                    pad_ndio_m1poly = pad_ndio_m1ms.shape.bounds

                    # Don't connect the guard ring; e.g. when they are touching the sides
                    if (
                        ((pad_ndio_m1poly.left - _geo.epsilon) < ndio_m1bb.left)
                        or ((pad_ndio_m1poly.right + _geo.epsilon) > ndio_m1bb.right)
                    ):
                        continue

                    layouter.add_wire(
                        net=pad, wire=via1, space=self.trackconn_viaspace,
                        bottom_shape=pad_ndio_m1poly, top_shape=pad_ndio_m1poly,
                    )

            # we assume that connecting the m2 to the pad for pdio will also connect it for
            # the ndio
            if ndio_m1bb.top < pad_m2bb.bottom: # pragma: no cover
                raise NotImplementedError("DCNDiode below pad")

            for pad_pdio_m1ms in pdio_lay.filter_polygons(
                net=pad, mask=metal1.pin.mask, depth=1, split=True,
            ):
                pad_pdio_m1poly = pad_pdio_m1ms.shape.bounds

                # Don't connect the guard ring; e.g. when they are touching the sides
                if (
                    ((pad_pdio_m1poly.left - _geo.epsilon) < ndio_m1bb.left)
                    or ((pad_pdio_m1poly.right + _geo.epsilon) > ndio_m1bb.right)
                ):
                    continue

                layouter.add_wire(
                    net=pad, wire=via1,
                    bottom_shape=pad_pdio_m1poly, top_shape=pad_pdio_m1poly,
                )

                shape = _geo.Rect.from_rect(rect=pad_pdio_m1poly, bottom=pad_m2bb.bottom)
                layouter.add_wire(net=pad, wire=metal2, shape=shape)

                if (pad_m2bb.left - _geo.epsilon) > pad_pdio_m1poly.right:
                    shape = _geo.Rect.from_rect(rect=pad_m2bb, left=pad_pdio_m1poly.left)
                    layouter.add_wire(net=pad, wire=metal2, shape=shape)

            # connect iovss
            for iovss_ndio_m1ms in ndio_lay.filter_polygons(
                net=iovss, mask=metal1.pin.mask, depth=1, split=True,
            ):
                iovss_ndio_m1poly = iovss_ndio_m1ms.shape.bounds

                layouter.add_wire(
                    net=iovss, wire=via1, space=self.trackconn_viaspace,
                    bottom_shape=iovss_ndio_m1poly, top_shape=iovss_ndio_m1poly,
                )
                layouter.add_wire(
                    net=iovss, wire=via2, space=self.trackconn_viaspace,
                    bottom_shape=iovss_ndio_m1poly, top_shape=iovss_ndio_m1poly,
                )

            # connect iovdd
            for iovdd_pdio_m1ms in pdio_lay.filter_polygons(
                net=iovdd, mask=metal1.pin.mask, depth=1, split=True,
            ):
                iovdd_pdio_m1poly = iovdd_pdio_m1ms.shape.bounds

                layouter.add_wire(
                    net=iovdd, wire=via1, space=self.trackconn_viaspace,
                    bottom_shape=iovdd_pdio_m1poly, top_shape=iovdd_pdio_m1poly,
                )
                layouter.add_wire(
                    net=iovdd, wire=via2, space=self.trackconn_viaspace,
                    bottom_shape=iovdd_pdio_m1poly, top_shape=iovdd_pdio_m1poly,
                )

        return ndio_lay, pdio_lay

    def connect_dcdiodes(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
        nclamp_lay: Optional[_lay.LayoutT], pclamp_lay: Optional[_lay.LayoutT],
        ndio_lay: Optional[_lay.LayoutT], pdio_lay: Optional[_lay.LayoutT],
        padconn_lay: Optional[_lay.LayoutT],
    ):
        fab = self.fab
        comp = fab.computed

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        space = comp.track_metalspecs[0].tracksegment_space

        if (
            (not self.has_pad)
            and (padconn_lay is not None)
            and (ndio_lay is not None)
            and (pdio_lay is not None)
        ):
            pc_m2bb = padconn_lay.bounds(mask=metal2.mask)
            ndio_m1bb = ndio_lay.bounds(mask=metal1.mask)
            ndio_m1padbb = ndio_lay.bounds(mask=metal1.mask, net=pad)
            pdio_m1bb = pdio_lay.bounds(mask=metal1.mask)
            pdio_m1padbb = pdio_lay.bounds(mask=metal1.mask, net=pad)

            left = min(ndio_m1padbb.left, pdio_m1padbb.left)
            bottom = ndio_m1bb.top + space
            top = pdio_m1bb.bottom - space
            right = pc_m2bb.right
            assert (top - bottom) < (self.tracksegment_maxpitch - space)
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(net=pad, wire=metal2, shape=shape)

    #
    # boundary
    #

    def set_boundary(self, *, layouter: _lay.CircuitLayouterT):
        layout = layouter.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=self.monocell_width, top=self.cell_height,
        )


class _FactoryCell(_fab.FactoryCell["_iofab.IOFactory"]):
    pass
FactoryCellT = _FactoryCell
class _FactoryOnDemandCell(_FactoryCell, _fab.FactoryOnDemandCell["_iofab.IOFactory"]):
    pass
