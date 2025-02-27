# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from math import floor
from typing import List, Dict, Optional, Callable, Type, Any, cast

from pdkmaster.technology import (
    property_ as _prp, primitive as _prm, geometry as _geo,
)
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, library as _lbry, factory as _fab,
)

from . import _helpers as _hlp, cell as _cell, specification as _spec


__all__ = [
    # Following subblock types are exported so user code can use them when overriding
    # the method that create them.
    "GuardRingT", "ClampT", "DCDiodeT",
    "PadT", "FillerT", "CornerT",
    "PadInT", "PadOutT", "PadTriOutT", "PadInOutT", "PadAnalogT",
    "PadVssT", "PadVddT", "PadIOVssT", "PadIOVddT",
    "GalleryT",
    "IOFactory",
]


class _GuardRing(_cell._FactoryCell):
    def __init__(self, *,
        name: str, fab: "IOFactory", type_: str,
        width: float, height: float, fill_well: bool, fill_implant:bool,
    ):
        super().__init__(fab=fab, name=name)
        self._type = type_
        self._width = width
        self._height = height
        self._fill_well = fill_well
        self._fill_implant = fill_implant
        assert not ((type_ == "p") and fill_well)

        spec = fab.spec
        comp = fab.computed

        ckt = self.new_circuit()
        conn = ckt.new_net(name="conn", external=True)
        layouter = self.new_circuitlayouter()
        layout = self.layout

        active = comp.active
        ionimplant = comp.ionimplant
        iopimplant = comp.iopimplant
        cont = comp.contact
        metal1 = comp.metal[1].prim

        left = -0.5*width
        right = 0.5*width
        bottom = -0.5*height
        top = 0.5*height

        ring_width = comp.guardring_width

        idx = cont.bottom.index(active)
        enc = cont.min_bottom_enclosure[idx].tall()
        side_enc = _prp.Enclosure((enc.first, cont.min_space))

        if type_ == "n":
            extra = spec.iovdd_ntap_extra
            implant = ionimplant
            inner_implant = iopimplant
            min_impl_space = comp.min_space_ionimplant_active
            nwell = spec.clamppmos.well
            cont_well_args = {"well_net": conn, "bottom_well": nwell}
        elif type_ == "p":
            extra = spec.iovss_ptap_extra
            implant = iopimplant
            inner_implant = ionimplant
            min_impl_space = comp.min_space_iopimplant_active
            cont_well_args = {}
            nwell = None
        else:
            raise AssertionError("Internal error")

        _l_ch = layouter.wire_layout(
            wire=cont, net=conn, **cont_well_args,
            bottom=active, bottom_implant=implant, bottom_extra=extra,
            bottom_enclosure="wide", bottom_width=width, bottom_height=ring_width
        )
        _actbounds = _l_ch.bounds(mask=active.mask)
        x = left - _actbounds.left
        y = bottom - _actbounds.bottom
        layouter.place(_l_ch, x=x, y=y)
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=(bottom + ring_width))
        layouter.add_wire(net=conn, wire=metal1, shape=shape)

        _l_ch = layouter.wire_layout(
            wire=cont, net=conn, **cont_well_args,
            bottom=active, bottom_implant=implant, bottom_extra=extra,
            bottom_enclosure="wide", bottom_width=width, bottom_height=ring_width
        )
        _actbounds = _l_ch.bounds(mask=active.mask)
        x = left - _actbounds.left
        y = top - _actbounds.top
        layouter.place(_l_ch, x=x, y=y)
        shape = _geo.Rect(left=left, bottom=(top - ring_width), right=right, top=top)
        layouter.add_wire(net=conn, wire=metal1, shape=shape)

        _l_ch = layouter.wire_layout(
            wire=cont, net=conn, **cont_well_args,
            bottom=active, bottom_implant=implant, bottom_extra=extra,
            bottom_enclosure=side_enc, bottom_width=ring_width, bottom_height=(height - 2*ring_width)
        )
        _actbounds = _l_ch.bounds(mask=active.mask)
        x = left - _actbounds.left
        y = bottom + ring_width - _actbounds.bottom
        layouter.place(_l_ch, x=x, y=y)
        shape = _geo.Rect(left=left, bottom=bottom, right=(left + ring_width), top=top)
        layouter.add_wire(net=conn, wire=metal1, shape=shape)

        _l_ch = layouter.wire_layout(
            wire=cont, net=conn, **cont_well_args,
            bottom=active, bottom_implant=implant, bottom_extra=extra,
            bottom_enclosure=side_enc, bottom_width=ring_width, bottom_height=(height - 2*ring_width)
        )
        _actbounds = _l_ch.bounds(mask=active.mask)
        x = right - _actbounds.right
        y = bottom + ring_width - _actbounds.bottom
        layouter.place(_l_ch, x=x, y=y)
        shape = _geo.Rect(left=(right - ring_width), bottom=bottom, right=right, top=top)
        layouter.add_wire(net=conn, wire=metal1, shape=shape)

        if fill_well:
            assert nwell is not None
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(net=conn, wire=nwell, shape=shape)
        if (inner_implant is not None) and fill_implant:
            layouter.add_portless(
                prim=inner_implant,
                x=0.0, width=(width - 2*ring_width - 2*min_impl_space),
                y=0.0, height=(height - 2*ring_width - 2*min_impl_space),
            )

        layout.boundary = _geo.Rect(left=left, bottom=bottom, right=right, top=top)

    @property
    def type_(self) -> str:
        return self._type
    @property
    def width(self) -> float:
        return self._width
    @property
    def ringwidth(self) -> float:
        return self.fab.computed.guardring_width
    @property
    def height(self) -> float:
        return self._height
    @property
    def fill_well(self) -> bool:
        return self._fill_well
    @property
    def fill_implant(self) -> bool:
        return self._fill_implant
GuardRingT = _GuardRing


class _Clamp(_cell._FactoryCell):
    def __init__(self, *,
        name: str, fab: "IOFactory", type_: str, n_trans: int, n_drive: int,
        rows: int,
    ):
        assert (
            (type_ in ("n", "p")) and (n_trans > 0) and (0 <= n_drive <= n_trans)
        ), "Internal error"

        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        nwell = comp.nwell
        active = comp.active
        poly = comp.poly
        cont = comp.contact
        metal1 = comp.metal[1].prim
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        via2 = comp.vias[2]

        iomos = comp.ionmos if type_ == "n" else comp.iopmos
        ox = iomos.gate.oxide

        super().__init__(fab=fab, name=name)
        self._type = type_
        self._n_trans = n_trans
        self._n_drive = n_drive

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layoutfab = layouter.fab

        iovss = ckt.new_net(name="iovss", external=True)
        iovdd = ckt.new_net(name="iovdd", external=True)
        source = iovss if type_ == "n" else iovdd
        notsource = iovdd if type_ == "n" else iovss
        pad = ckt.new_net(name="pad", external=True)

        gate_nets = tuple()
        gate: Optional[_ckt._CircuitNet] = None
        off: Optional[_ckt._CircuitNet] = None
        if n_drive > 0:
            gate = ckt.new_net(name="gate", external=True)
            gate_nets += n_drive*(gate,)
        if n_drive < n_trans:
            off = ckt.new_net(name="off", external=False)
            gate_nets += (n_trans - n_drive)*(off,)

        _l_clamp = _hlp.clamp(
            fab=fab, ckt=ckt, type_=type_, rows=rows,
            source_net=source, drain_net=pad, gate_nets=gate_nets,
        )
        clampact_bounds = _l_clamp.bounds(mask=active.mask)
        clamppoly_bounds = _l_clamp.bounds(mask=poly.mask)
        clampm1_bounds = _l_clamp.bounds(mask=metal1.mask)

        min_space_active_poly = tech.computed.min_space(comp.poly, active)
        # account for two touching guard bands
        min_space_metal1_guard = tech.computed.min_space(
            primitive1=metal1, width=2*comp.metal[1].minwidth4ext_down,
        )

        innerguardring_height = max(
            clamppoly_bounds.height + 2*min_space_active_poly,
            clampm1_bounds.height + 2*min_space_metal1_guard,
        ) + 2*comp.guardring_width
        if ox is not None:
            try:
                s = tech.computed.min_space(active, ox)
            except:
                pass
            else:
                clampox_bounds = _l_clamp.bounds(mask=ox.mask)
                innerguardring_height = max(
                    innerguardring_height,
                    clampox_bounds.height + 2*s + 2*comp.guardring_width,
                )

        innerguardring_width = (spec.monocell_width - 2*comp.guardring_pitch)
        outerguardring_height = innerguardring_height + 2*comp.guardring_pitch

        c_outerring = fab.guardring(
            type_=type_, width=spec.monocell_width, height=outerguardring_height,
        )
        i_outerring = ckt.instantiate(c_outerring, name="OuterRing")
        notsource.childports += i_outerring.ports.conn
        c_innerring = fab.guardring(
            type_="p" if (type_ == "n") else "n",
            width=innerguardring_width, height=innerguardring_height,
            fill_well=(type_ == "p"),
        )
        i_innerring = ckt.instantiate(c_innerring, name="InnerRing")
        source.childports += i_innerring.ports.conn

        # Place clamp, guard rings
        x = 0.5*spec.monocell_width
        y = 0.5*outerguardring_height
        layouter.place(i_outerring, x=x, y=y)
        layouter.place(i_innerring, x=x, y=y)
        l_clamp = layouter.place(_l_clamp, x=x, y=y)

        # Draw drain metal2 connections
        for ms in l_clamp.filter_polygons(net=pad, mask=metal1.mask, split=True):
            bounds = ms.shape.bounds
            l_via = layouter.add_wire(
                net=pad, wire=via1, x=bounds.center.x, columns=spec.clampdrain_via1columns,
                bottom_bottom=bounds.bottom, bottom_top=bounds.top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)

            shape = _geo.Rect.from_rect(
                rect=viam2_bounds, top=outerguardring_height,
            )
            layouter.add_wire(net=pad, wire=metal2, pin=metal2.pin, shape=shape)

        # Connect source to ring
        # Cache as polygons will be added during parsing
        for ms in l_clamp.filter_polygons(net=source, mask=metal1.mask, split=True):
            bounds = ms.shape.bounds
            x = bounds.center.x

            l_via = layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bounds.bottom, bottom_top=bounds.top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)

            bottom = 0.5*outerguardring_height - 0.5*innerguardring_height
            top = bottom + comp.guardring_width
            layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            top = 0.5*outerguardring_height + 0.5*innerguardring_height
            bottom = top - comp.guardring_width
            layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            shape = _geo.Rect.from_rect(
                rect=viam2_bounds,
                bottom=0.0, top=outerguardring_height,
            )
            layouter.add_wire(net=source, wire=metal2, shape=shape)
            layouter.add_wire(
                net=source, wire=via2, x=x,
                bottom_bottom=0.0, bottom_top=outerguardring_height,
            )

        # Draw gate diode and connect the gates
        if n_drive > 0:
            assert gate is not None
            diode = spec.ndiode if type_ == "n" else spec.pdiode
            well_args = {} if type_ == "n" else {"well_net": iovdd, "bottom_well": nwell}
            l_ch = layoutfab.layout_primitive(
                prim=cont, portnets={"conn": gate}, **well_args, rows=2,
                bottom=diode.wire, bottom_implant=diode.implant,
            )
            chact_bounds = l_ch.bounds(mask=diode.wire.mask)
            dgate = ckt.instantiate(diode, name="DGATE",
                width=max(chact_bounds.right - chact_bounds.left, diode.min_width),
                height=max(chact_bounds.top - chact_bounds.bottom, diode.min_width),
            )
            an = dgate.ports.anode
            cath = dgate.ports.cathode
            gate.childports += an if type_ == "p" else cath
            source.childports += an if type_ == "n" else cath

            x = tech.on_grid(0.5*spec.monocell_width + 0.5*(
                clampact_bounds.left - 0.5*innerguardring_width + comp.guardring_width
            ))
            y = 0.5*outerguardring_height + clampact_bounds.top - chact_bounds.top
            l_ch = layouter.place(l_ch, x=x, y=y)
            layouter.place(dgate, x=x, y=y)

            chm1_bounds = l_ch.bounds(mask=metal1.mask)
            clampm1gate_bounds = l_clamp.bounds(mask=metal1.mask, net=gate)

            rect = _geo.Rect.from_rect(
                rect=chm1_bounds, top=clampm1gate_bounds.top,
            )
            layouter.add_wire(wire=metal1, net=gate, shape=rect)
            rect = _geo.Rect.from_rect(
                rect=clampm1gate_bounds, left=chm1_bounds.left,
                bottom=(clampm1gate_bounds.top - metal1.min_width),
            )
            layouter.add_wire(wire=metal1, net=gate, shape=rect)

            bottom = chm1_bounds.bottom
            top = clampm1gate_bounds.top
            l_via = layouter.add_wire(
                wire=via1, net=gate, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)
            shape = _geo.Rect.from_rect(rect=viam2_bounds, top=outerguardring_height)
            layouter.add_wire(wire=metal2, net=gate, pin=metal2.pin, shape=shape)

        # Draw power off resistor and connect the gates
        if n_drive < n_trans:
            assert off is not None
            res = spec.nres if type_ == "n" else spec.pres
            w = max(res.min_width, comp.minwidth4ext_polywithcontact)
            # Make resistor poly as high as the active of the clamp transistor
            assert res.min_contact_space is not None
            h = (
                (clampact_bounds.top - clampact_bounds.bottom)
                - comp.minwidth_polywithcontact - cont.width - 2*res.min_contact_space
            )
            roff = ckt.instantiate(res, name="Roff", width=w, length=h)
            source.childports += roff.ports.port1
            off.childports += roff.ports.port2

            x = tech.on_grid(0.5*spec.monocell_width + 0.5*(
                clampact_bounds.right + 0.5*innerguardring_width - comp.guardring_width
            ))
            y = 0.5*outerguardring_height
            l_roff = layouter.place(roff, x=x, y=y)
            roffm1source_bounds = l_roff.bounds(mask=metal1.mask, net=source)
            roffm1off_bounds = l_roff.bounds(mask=metal1.mask, net=off)

            # Possibly extend implant if it is the same implant as the guard ring
            guard_impl = comp.pimplant if type_ == "n" else comp.nimplant
            if (guard_impl is not None) and (guard_impl in res.implant):
                roffimpl_bounds = l_roff.bounds(mask=guard_impl.mask)
                shape = _geo.Rect.from_rect(
                    rect=roffimpl_bounds,
                    bottom=(0.5*outerguardring_height - 0.5*innerguardring_height),
                    top=(0.5*outerguardring_height + 0.5*innerguardring_height),
                )
                layouter.add_portless(prim=guard_impl, shape=shape)

            x = roffm1source_bounds.center.x
            y = roffm1source_bounds.center.y
            l_via = layouter.add_wire(
                wire=via1, net=source, x=x, y=y, columns=2,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)
            y = comp.guardring_pitch + 0.5*comp.guardring_width
            l_via = layouter.add_wire(
                wire=via1, net=source, x=x, y=y, columns=2,
            )
            viam2_bounds2 = l_via.bounds(mask=metal2.mask)
            shape = _geo.Rect.from_rect(rect=viam2_bounds, bottom=viam2_bounds2.bottom)
            layouter.add_wire(wire=metal2, net=source, shape=shape)

            clampm1off_bounds = l_clamp.bounds(mask=metal1.mask, net=off)
            roffm1off_bounds = l_roff.bounds(mask=metal1.mask, net=off)

            rect = _geo.Rect.from_rect(
                rect=roffm1off_bounds, top=clampm1off_bounds.top,
            )
            layouter.add_wire(wire=metal1, net=off, shape=rect)
            shape = _geo.Rect.from_rect(
                rect=clampm1off_bounds,
                bottom=(clampm1off_bounds.top - metal1.min_width),
                right=roffm1off_bounds.right,
            )
            layouter.add_wire(wire=metal1, net=off, shape=shape)

        self.layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0,
            right=spec.monocell_width, top=outerguardring_height,
        )

    @property
    def type_(self) -> str:
        return self._type
    @property
    def n_trans(self) -> int:
        return self._n_trans
    @property
    def n_drive(self) -> int:
        return self._n_drive
ClampT = _Clamp


class _DCDiode(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory", type_: str):
        # This diode is rotated to make it larger in the X direction
        spec = fab.spec
        assert spec.add_dcdiodes, "Internal error"

        assert type_ in ("n", "p"), "Internal error"
        self._type = type_

        self._dio = spec.ndiode if type_ == "n" else spec.pdiode

        super().__init__(fab=fab, name=name)

    @property
    def type_(self) -> str:
        return self._type
    @property
    def innerwidth(self) -> float:
        return self.fab.spec.dcdiode_inneractheight
    @property
    def active_width(self) -> float:
        return self.fab.spec.dcdiode_actwidth
    @property
    def active_space(self) -> float:
        return self.fab.spec.dcdiode_actspace
    @property
    def activeend_space(self) -> float:
        return self.fab.spec.dcdiode_actspace_end
    @property
    def fingers(self) -> int:
        return self.fab.spec.dcdiode_fingers
    @property
    def active_pitch(self) -> float:
        return self.active_width + self.active_space
    @property
    def outerwidth(self) -> float:
        return self.innerwidth + 2*(self.activeend_space + self.active_width)
    @property
    def outerheight(self) -> float:
        return self.active_width + 2*self.fingers*self.active_pitch

    def _create_circuit(self) -> None:
        fab = self.fab
        spec = fab.spec

        ckt = self.new_circuit()
        type_ = self.type_
        fingers = spec.dcdiode_fingers
        dio = self._dio

        anode = ckt.new_net(name="anode", external=True)
        cathode = ckt.new_net(name="cathode", external=True)
        ckt.new_net(name="guard", external=True)

        width = spec.dcdiode_inneractheight
        height = spec.dcdiode_actwidth
        for i in range(fingers):
            dio_inst = ckt.instantiate(dio,
                name=self._diode_name(n=i), width=width, height=height,
            )
            anode.childports += dio_inst.ports.anode
            cathode.childports += dio_inst.ports.cathode

    def _create_layout(self) -> None:
        # We rotate the diode
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        type_ = self.type_
        active = comp.active
        cont = comp.contact
        metal1 = comp.metal[1].prim

        ckt = self.circuit
        nets = ckt.nets
        insts = ckt.instances

        guard = nets["guard"]

        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        actwidth = self.active_width
        fingers = self.fingers
        actpitch = self.active_pitch
        outerwidth = self.outerwidth
        outerheight = self.outerheight

        d_guard = spec.dcdiode_diodeguardspace + comp.guardring_width
        guardwidth = outerwidth + 2*d_guard
        guardheight = outerheight + 2*d_guard

        if type_ == "n":
            dio_net = nets["cathode"]
            outer_net = nets["anode"]
            outer_impl = comp.pimplant
            outer_extra = spec.iovss_ptap_extra
            well = None
            well_net = None
        else:
            dio_net = nets["anode"]
            outer_net = nets["cathode"]
            outer_impl = comp.nimplant
            outer_extra = spec.iovdd_ntap_extra
            well = comp.nwell
            well_net = outer_net
        outer_impl_enc = None if outer_impl is None else spec.dcdiode_implant_enclosure

        for i in range(fingers):
            dio_inst = insts[self._diode_name(n=i)]
            x = 0.5*outerwidth
            y = actpitch + 2*i*actpitch + 0.5*actwidth
            impl_args: Dict[str, Any] = (
                dict(implant_enclosure=spec.dcdiode_implant_enclosure)
                if self._dio.implant
                else {}
            )
            dio_lay = layouter.place(dio_inst, x=x, y=y, **impl_args)
            dio_actbb = dio_lay.bounds(mask=active.mask)

            layouter.add_wire(
                net=dio_net, wire=cont, bottom=active, bottom_shape=dio_actbb,
                top_shape=dio_actbb,
            )
            layouter.add_wire(net=dio_net, wire=metal1, pin=metal1.pin, shape=dio_actbb)

        # Make sure that min_space between contacts is not violated on the fingers
        idx = cont.bottom.index(active)
        enc = cont.min_bottom_enclosure[idx]
        hor_enc = _prp.Enclosure((max(enc.max(), cont.min_space), enc.min()))

        # guard contacts
        # left
        bottom = 0.0
        top = outerheight
        left = 0.0
        right = left + actwidth
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(
            net=outer_net, wire=cont, well_net=well_net,
            bottom=active, bottom_shape=shape,
            bottom_implant=outer_impl, bottom_implant_enclosure=outer_impl_enc,
            bottom_extra=outer_extra, bottom_well=well,
            top_shape=shape,
        )
        # right
        right = outerwidth
        left = right - actwidth
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(
            net=outer_net, wire=cont, well_net=well_net,
            bottom=active, bottom_shape=shape,
            bottom_implant=outer_impl, bottom_implant_enclosure=outer_impl_enc,
            bottom_extra=outer_extra, bottom_well=well,
            top_shape=shape,
        )
        # fingers
        left = actwidth
        right = outerwidth - actwidth
        for i in range(fingers + 1):
            bottom = 2*i*actpitch
            top = bottom + actwidth
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(
                net=outer_net, wire=cont, well_net=well_net,
                bottom=active, bottom_shape=shape,
                bottom_implant=outer_impl, bottom_implant_enclosure=outer_impl_enc,
                bottom_extra=outer_extra, bottom_enclosure=hor_enc, bottom_well=well,
                top_shape=shape,
            )
            shape = _geo.Rect.from_rect(rect=shape, left=0.0, right=outerwidth)
            layouter.add_wire(net=outer_net, wire=metal1, pin=metal1.pin, shape=shape)

        if well is not None:
            assert well_net is not None
            bb = layout.bounds(mask=well.mask)
            layouter.add_wire(net=well_net, wire=well, shape=bb)

        guard_cell = fab.guardring(type_=type_, width=guardwidth, height=guardheight)
        guard_inst = ckt.instantiate(guard_cell, name="guard")
        guard.childports += guard_inst.ports["conn"]
        x = -d_guard + 0.5*guardwidth
        y = -d_guard + 0.5*guardheight
        guard_lay = layouter.place(guard_inst, x=x, y=y)

        bnd = guard_lay.boundary
        assert bnd is not None
        if spec.dcdiode_indicator is not None:
            layouter.add_portless(prim=spec.dcdiode_indicator, shape=bnd)
        layout.boundary = bnd

        shape = _geo.Rect.from_rect(rect=bnd, top=(bnd.bottom + comp.guardring_width))
        layouter.add_wire(net=guard, wire=metal1, pin=metal1.pin, shape=shape)
        shape = _geo.Rect.from_rect(rect=bnd, bottom=(bnd.top - comp.guardring_width))
        layouter.add_wire(net=guard, wire=metal1, pin=metal1.pin, shape=shape)

    def _diode_name(self, *, n: int) -> str:
        # Get diode name
        fingers = self.fab.spec.dcdiode_fingers

        assert 0 <= n < fingers, "Internal error"

        return "dcdiode" if fingers == 1 else f"dcdiode[{n}]"
DCDiodeT = _DCDiode


class _Secondary(_cell._FactoryCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        spec = fab.spec
        comp = fab.computed

        cont = comp.contact
        pimplant = comp.pimplant
        metal1 = comp.metal[1].prim
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        super().__init__(fab=fab, name=name)

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        iovdd = ckt.new_net(name="iovdd", external=True)
        iovss = ckt.new_net(name="iovss", external=True)
        pad = ckt.new_net(name="pad", external=True)
        core = ckt.new_net(name="core", external=True)

        # Resistance
        r = ckt.instantiate(
            spec.nres, name="R",
            width=spec.secondres_width, length=spec.secondres_length,
        )
        pad.childports += r.ports.port1
        core.childports += r.ports.port2

        l_res = layouter.inst_layout(inst=r)
        respoly_bounds = l_res.bounds(mask=comp.poly.mask)
        res_width = respoly_bounds.right - respoly_bounds.left
        res_height = respoly_bounds.top - respoly_bounds.bottom

        guard_width = (
            res_width + 2*spec.secondres_active_space + 2*comp.guardring_width
        )
        guard_height = (
            res_height + 2*spec.secondres_active_space + 2*comp.guardring_width
        )
        c_guard1 = fab.guardring(
            type_="p", width=guard_width, height=guard_height,
        )
        inst_guard1 = ckt.instantiate(c_guard1, name="guard1")
        iovss.childports += inst_guard1.ports["conn"]

        l_res = layouter.place(l_res, x=0.5*guard_width, y=0.5*guard_height)
        resm1pad_bounds = l_res.bounds(mask=metal1.mask, net=pad)
        resm1core_bounds = l_res.bounds(mask=metal1.mask, net=core)
        l_guard1 = layouter.place(inst_guard1, x=0.5*guard_width, y=0.5*guard_height)
        resm1guard1_bounds = l_guard1.bounds(mask=metal1.mask)

        # if resistor has p implant draw pimplant over whole inner area
        # In this case we want to fill it with the same implant as the guard ring
        # and not the opposite as it would be if we ask for a guard band with the
        # fill_implant
        if (pimplant is not None) and (pimplant in spec.nres.implant):
            shape = _geo.Rect(left=0.0, bottom=0.0, right=guard_width, top=guard_height)
            layouter.add_portless(prim=pimplant, shape=shape)

        # N diode
        dn_prim = spec.ndiode
        diode_height = (
            guard_height - 2*comp.guardring_width - 2*comp.min_space_nmos_active
        )
        l_ch = layouter.fab.layout_primitive(
            cont, portnets={"conn": core}, columns=2,
            bottom=dn_prim.wire, bottom_implant=dn_prim.implant,
            bottom_height=diode_height,
        )
        dnchact_bounds = l_ch.bounds(mask=comp.active.mask)
        diode_width = dnchact_bounds.right - dnchact_bounds.left
        assert diode_width > (dn_prim.min_width - _geo.epsilon)
        dn = ckt.instantiate(
            dn_prim, name="DN", width=diode_width, height=diode_height,
        )
        core.childports += dn.ports.cathode
        iovss.childports += dn.ports.anode

        guard2_width = (
            diode_width + 2*comp.min_space_nmos_active + 2*comp.guardring_width
        )
        c_guard2 = fab.guardring(
            type_="p", width=guard2_width, height=guard_height,
        )
        inst_guard2 = ckt.instantiate(c_guard2, name="guard2")
        iovss.childports += inst_guard2.ports["conn"]

        x = guard_width + comp.guardring_space + 0.5*guard2_width
        y = 0.5*guard_height
        l_dn_ch = layouter.place(l_ch, x=x, y=y)
        layouter.place(dn, x=x, y=y)
        l_guard2 = layouter.place(inst_guard2, x=x, y=y)
        ndiom1guard_bounds = l_guard2.bounds(mask=metal1.mask)

        cell_right = guard_width + comp.guardring_space + guard2_width

        # connect guard rings
        # currently can't be done in metal1 as no shapes with two or more holes
        # in it are supported.
        _l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": iovss}, rows=3,
        )
        _m1_bounds = _l_via.bounds(mask=metal1.mask)
        y = (
            max(resm1guard1_bounds.bottom, ndiom1guard_bounds.bottom)
            - _m1_bounds.bottom + 2*metal2.min_space
        )
        l = layouter.place(
            _l_via, x=(resm1guard1_bounds.right - _m1_bounds.right), y=y,
        )
        m2_bounds1 = l.bounds(mask=metal2.mask)
        l = layouter.place(
            _l_via, x=(ndiom1guard_bounds.left - _m1_bounds.left), y=y,
        )
        m2_bounds2 = l.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(
            rect=m2_bounds1, right=m2_bounds2.right, top=m2_bounds2.top,
        )
        layouter.add_wire(net=iovss, wire=metal2, pin=metal2pin, shape=shape)

        # P diode
        dp_prim = spec.pdiode
        guard3_width = (
            guard_width + comp.guardring_space + guard2_width
        )
        diode2_width = (
            guard3_width - 2*comp.guardring_width - 2*comp.min_space_pmos_active
        )
        l_ch = layouter.fab.layout_primitive(
            cont, portnets={"conn": core}, rows=2,
            bottom=dp_prim.wire, bottom_implant=dp_prim.implant,
            bottom_width=diode2_width,
        )
        dpchact_bounds = l_ch.bounds(mask=comp.active.mask)
        diode2_height = dpchact_bounds.top - dpchact_bounds.bottom
        assert diode2_height > (dn_prim.min_width - _geo.epsilon)
        dp = ckt.instantiate(
            dp_prim, name="DP", width=diode2_width, height=diode2_height,
        )
        core.childports += dp.ports.anode
        iovdd.childports += dp.ports.cathode

        guard3_height = (
            diode2_height + 2*comp.min_space_pmos_active + 2*comp.guardring_width
        )
        c_guard3 = fab.guardring(
            type_="n", width=guard3_width, height=guard3_height, fill_well=True,
        )
        inst_guard3 = ckt.instantiate(c_guard3, name="guard3")
        iovdd.childports += inst_guard3.ports["conn"]

        x = 0.5*guard3_width
        y = guard_height + comp.guardring_space + 0.5*guard3_height
        l_dp_ch = layouter.place(l_ch, x=x, y=y)
        layouter.place(dp, x=x, y=y)
        layouter.place(inst_guard3, x=x, y=y)

        cell_top = guard_height + comp.guardring_space + guard3_height

        shape = _geo.Rect(
            left=0.0, bottom=(cell_top - comp.guardring_width),
            right=cell_right, top=cell_top,
        )
        layouter.add_wire(
            net=iovdd, wire=metal1, shape=shape, pin=metal1.pin,
        )

        # Draw interconnects
        w = resm1pad_bounds.right - resm1pad_bounds.left
        x = 0.5*(resm1pad_bounds.left + resm1pad_bounds.right)
        _l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": pad}, bottom_width=w,
        )
        _viam1_bounds = _l_via.bounds(mask=metal1.mask)
        y = -_viam1_bounds.top + resm1pad_bounds.top
        l_via = layouter.place(_l_via, x=x, y=y)
        shape = _geo.Rect.from_rect(rect=resm1pad_bounds, bottom=0.0)
        layouter.add_wire(wire=metal2, net=pad, pin=metal2.pin, shape=shape)

        dnm1_bounds = l_dn_ch.bounds(mask=metal1.mask)
        dpm1_bounds = l_dp_ch.bounds(mask=metal1.mask)

        w = resm1core_bounds.right - resm1core_bounds.left
        x = 0.5*(resm1core_bounds.left + resm1core_bounds.right)
        _l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": core}, bottom_width=w
        )
        _viam1_bounds = _l_via.bounds(mask=metal1.mask)
        y = -_viam1_bounds.bottom + resm1core_bounds.bottom
        l_via = layouter.place(_l_via, x=x, y=y)
        rescoreviam2_bounds = l_via.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=resm1core_bounds, top=dpm1_bounds.top)
        layouter.add_wire(wire=metal2, net=core, shape=shape)

        layouter.add_wire(
            wire=via1, net=core, bottom_shape=dnm1_bounds, top_shape=dnm1_bounds,
        )
        layouter.add_wire(wire=metal2, net=core, shape=dpm1_bounds)

        shape = _geo.Rect(
            left=rescoreviam2_bounds.left,
            bottom=min(rescoreviam2_bounds.bottom, dnm1_bounds.top),
            right=dnm1_bounds.right,
            top = max(rescoreviam2_bounds.top, dnm1_bounds.top),
        )
        layouter.add_wire(wire=metal2, net=core, shape=shape)

        layouter.add_wire(wire=via1, net=core, bottom_shape=dpm1_bounds)
        shape = _geo.Rect.from_rect(rect=dpm1_bounds, top=cell_top)
        layouter.add_wire(wire=metal2, net=core, pin=metal2.pin, shape=shape)

        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cell_right, top=cell_top,
        )


class _RCClampResistor(_cell._FactoryCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        # TODO: make3 more general; current only Sky130 compatibility
        super().__init__(fab=fab, name=name)

        spec = fab.spec
        tech = fab.tech

        res_prim = spec.resvdd_prim
        w = spec.resvdd_w
        l_finger = spec.resvdd_lfinger
        fingers = spec.resvdd_fingers
        space = spec.resvdd_space

        assert (
            (res_prim is not None) and (w is not None)
            and (l_finger is not None) and (fingers is not None)
            and (space is not None)
        )

        pitch = w + space

        wire = res_prim.wire
        contact = res_prim.contact
        contact_space = res_prim.min_contact_space
        assert (contact is not None) and (contact_space is not None)
        assert len(contact.top) == 1
        metal = contact.top[0]
        assert isinstance(metal, _prm.MetalWire)
        metalpin = metal.pin

        ckt = self.new_circuit()

        res = ckt.new_net(name="res", external=False)
        pin1 = ckt.new_net(name="pin1", external=True)
        pin2 = ckt.new_net(name="pin2", external=True)

        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        x = 0.0
        prev_conn_net = pin1
        prev_conn_mbb = None
        for i in range(fingers):
            if i == (fingers - 1):
                conn_net = pin2
            else:
                conn_net = ckt.new_net(name=f"conn_{i}_{i+1}", external=False)
            res_inst = ckt.instantiate(
                res_prim, name=f"res_fing[{i}]",
                width=spec.resvdd_w, length=spec.resvdd_lfinger,
            )
            prev_conn_net.childports += res_inst.ports["port1"]
            conn_net.childports += res_inst.ports["port2"]

            rot = _geo.Rotation.No if (i%2) == 0 else _geo.Rotation.MX
            _res_lay = layouter.inst_layout(inst=res_inst, rotation=rot)
            _res_polybb = _res_lay.bounds(mask=wire.mask)

            res_lay = layouter.place(_res_lay, x=(x - _res_polybb.left), y=(-_res_polybb.bottom))
            res_lay_prevconn_mbb = res_lay.bounds(mask=metal.mask, net=prev_conn_net)
            res_lay_conn_mbb = res_lay.bounds(mask=metal.mask, net=conn_net)

            if prev_conn_mbb is not None:
                shape = _geo.Rect.from_rect(rect=prev_conn_mbb, right=res_lay_prevconn_mbb.right)
                layouter.add_wire(net=prev_conn_net, wire=metal, shape=shape)

            x += pitch
            prev_conn_net = conn_net
            prev_conn_mbb = res_lay_conn_mbb

        # Join implant and indicator layers
        for prim in (*res_prim.indicator, *res_prim.implant):
            layouter.add_portless(prim=prim, shape=layout.bounds(mask=prim.mask))

        pin1_mbb = layout.bounds(mask=metal.mask, net=pin1)
        layouter.add_wire(net=pin1, wire=metal, pin=metalpin, shape=pin1_mbb)
        pin2_mbb = layout.bounds(mask=metal.mask, net=pin2)
        layouter.add_wire(net=pin2, wire=metal, pin=metalpin, shape=pin2_mbb)

        layout.boundary = layout.bounds(mask=wire.mask)


class _RCClampInverter(_cell._FactoryCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

        spec = fab.spec
        tech = fab.tech
        comp = fab.computed
        layoutfab = fab.layoutfab

        ninv_l = spec.invvdd_n_l
        ninv_w = spec.invvdd_n_w
        inv_nmos = spec.invvdd_n_mosfet
        n_fingers = spec.invvdd_n_fingers
        assert (
            (ninv_l is not None) and (ninv_w is not None)
            and (inv_nmos is not None) and (n_fingers is not None)
        )

        pinv_l = spec.invvdd_p_l
        pinv_w = spec.invvdd_p_w
        inv_pmos = spec.invvdd_p_mosfet
        p_fingers = spec.invvdd_p_fingers
        assert (
            (pinv_l is not None) and (pinv_w is not None)
            and (inv_pmos is not None) and (p_fingers is not None)
        )

        cap_l = spec.capvdd_l
        cap_w = spec.capvdd_w
        cap_mos = spec.capvdd_mosfet
        cap_fingers = spec.capvdd_fingers
        assert (
            (cap_l is not None) and (cap_w is not None)
            and (cap_mos is not None) and (cap_fingers is not None)
        )
        if cap_mos != inv_nmos:
            raise NotImplemented("Cap MOSFET != inverter nmos MOSFET")

        active = comp.active
        poly = comp.poly
        contact = comp.contact
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        ckt = self.new_circuit()
        supply = ckt.new_net(name="supply", external=True)
        ground = ckt.new_net(name="ground", external=True)
        in_ = ckt.new_net(name="in", external=True)
        out = ckt.new_net(name="out", external=True)

        layouter = self.new_circuitlayouter()

        actpitch = tech.computed.min_pitch(active, up=True)
        actrow_space = (
            active.min_space if spec.rcmosfet_row_minspace is None
            else spec.rcmosfet_row_minspace
        )

        min_actpoly_space = tech.computed.min_space(active, poly)

        min_actch_space = None
        try:
            min_actch_space = tech.computed.min_space(active, contact)
        except ValueError:
            pass # Keep value at None

        assert spec.invvdd_n_rows == spec.capvdd_rows
        rows = spec.capvdd_rows

        act_bottom = 0
        _l_nmos = layoutfab.new_layout()
        for row in range(rows):
            # Specs for cap mos and inverter nmos combined
            specs = []

            # inverter cap fingers
            for i in range(cap_fingers):
                inst_name = f"capmos{i}"
                if rows > 1:
                    inst_name += f"_r{row}"
                inst = ckt.instantiate(cap_mos, name=inst_name, l=cap_l, w=cap_w)
                in_.childports += inst.ports.gate
                ground.childports += (
                    inst.ports.sourcedrain1, inst.ports.sourcedrain2, inst.ports.bulk,
                )
                specs.append(_lay.MOSFETInstSpec(
                    inst=inst, contact_left=contact, contact_right=contact,
                ))

            # inverter nmos fingers
            for i in range(n_fingers):
                inst_name = f"nmos{i}"
                if rows >1:
                    inst_name += f"_r{row}"
                inst = ckt.instantiate(inv_nmos, name=inst_name, l=ninv_l, w=ninv_w)
                in_.childports += inst.ports.gate
                ground.childports += inst.ports.bulk
                if i%2 == 0:
                    ground.childports += inst.ports.sourcedrain1
                    out.childports += inst.ports.sourcedrain2
                else:
                    out.childports += inst.ports.sourcedrain1
                    ground.childports += inst.ports.sourcedrain2
                specs.append(_lay.MOSFETInstSpec(
                    inst=inst, contact_left=contact, contact_right=contact,
                ))

            _l = layouter.transistors_layout(trans_specs=specs)
            _actbb = _l.bounds(mask=active.mask)
            x = tech.on_grid(0.5*spec.monocell_width - _actbb.center.x)
            y = act_bottom + _actbb.center.y
            _l.move(dxy=_geo.Point(x=x, y=y))
            _l_nmos += _l

            act_bottom += _actbb.height + actrow_space
        _nmos_actbb = _l_nmos.bounds(mask=active.mask)
        l_nmos = layouter.place(_l_nmos, x=0.0, y=(4*actpitch - _nmos_actbb.bottom))
        nmos_actbb = l_nmos.bounds(mask=active.mask)
        nmos_polybb = l_nmos.bounds(mask=poly.mask)
        nmos_m1bb = l_nmos.bounds(mask=metal1.mask)

        nmosguardring_height = tech.on_grid(nmos_actbb.height + 8*actpitch, mult=2, rounding="ceiling")
        nmosguardring_width = spec.monocell_width

        nmosguardring_cell = fab.guardring(
            type_="p", width=nmosguardring_width, height=nmosguardring_height,
            fill_implant=True,
        )
        inst = ckt.instantiate(nmosguardring_cell, name="nmosguardring")
        ground.childports += inst.ports.conn
        x = 0.5*spec.monocell_width
        l = layouter.place(inst, x=x, y=nmos_actbb.center.y)
        nmosguardring_actbb = l.bounds(mask=active.mask)
        nmosguardring_m1bb = l.bounds(mask=metal1.mask)

        # nmos ground connection
        for ms in l_nmos.filter_polygons(
            net=ground, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            shape = _geo.Rect.from_rect(rect=bb, top=nmosguardring_m1bb.top)
            layouter.add_wire(net=ground, wire=metal1, shape=shape)

        # nmos in connection
        w = nmos_polybb.width
        _l = layouter.wire_layout(
            net=in_, wire=contact, bottom=poly,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _ch_polybb = _l.bounds(mask=poly.mask)
        _ch_chbb = _l.bounds(mask=contact.mask)
        _ch_m1bb = _l.bounds(mask=metal1.mask)

        x = nmos_polybb.center.x
        y = min(
            nmos_actbb.bottom - min_actpoly_space - _ch_polybb.top,
            nmos_m1bb.bottom - metal1.min_space - _ch_m1bb.top,
        )
        if min_actch_space is not None:
            y = min(y, nmos_actbb.bottom - min_actch_space - _ch_chbb.top)
        l = layouter.place(_l, x=x, y=y)
        ch_polybb = l.bounds(mask=poly.mask)
        nmosinch_m1bb = l.bounds(mask=metal1.mask)

        for ms in l_nmos.filter_polygons(net=in_, mask=poly.mask, split=True, depth=1):
            bb = ms.shape.bounds
            if bb.bottom - _geo.epsilon > ch_polybb.top:
                shape = _geo.Rect.from_rect(rect=bb, bottom=ch_polybb.bottom)
                layouter.add_wire(net=in_, wire=poly, shape=shape)

        _l = layouter.wire_layout(
            net=in_, wire=via1,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide"
        )
        _via1_m1bb = _l.bounds(mask=metal1.mask)
        _via1_m2bb = _l.bounds(mask=metal2.mask)
        y = min(
            nmosinch_m1bb.top - _via1_m1bb.top,
            nmos_m1bb.bottom - metal1.min_space - _via1_m1bb.top,
            nmos_m1bb.bottom - 2*metal2.min_space - _via1_m2bb.top,
        )
        l = layouter.place(_l, x=x, y=y)
        nmosinvia1_m1bb = l.bounds(mask=metal1.mask)
        nmosinvia1_m2bb = l.bounds(mask=metal2.mask)

        if (nmosinvia1_m1bb.top + _geo.epsilon) < nmosinch_m1bb.bottom:
            shape = _geo.Rect.from_rect(rect=nmosinvia1_m1bb, top=nmosinch_m1bb.bottom)
            layouter.add_wire(net=in_, wire=metal1, shape=shape)

        # nmos out connection
        nmosout_m2left = spec.monocell_width
        nmosout_m2right = 0.0
        for ms in l_nmos.filter_polygons(
            net=out, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            l = layouter.add_wire(
                net=out, wire=via1, x=bb.center.x,
                bottom_bottom=bb.bottom, bottom_top=bb.top, bottom_enclosure="tall",
                top_bottom=bb.bottom, top_top=bb.top, top_enclosure="tall",
            )
            m2bb = l.bounds(mask=metal2.mask)
            nmosout_m2left = min(nmosout_m2left, m2bb.left)
            nmosout_m2right = max(nmosout_m2right, m2bb.right)

        _l_pmos = layoutfab.new_layout()
        act_bottom = 0.0
        for row in range(spec.invvdd_p_rows):
            # inverter pmos fingers
            specs = []
            for i in range(p_fingers):
                inst_name = f"pmos{i}"
                if rows > 1:
                    inst_name += f"_r{row}"
                inst = ckt.instantiate(inv_pmos, name=inst_name, l=pinv_l, w=pinv_w)
                in_.childports += inst.ports.gate
                supply.childports += inst.ports.bulk
                if i%2 == 0:
                    supply.childports += inst.ports.sourcedrain1
                    out.childports += inst.ports.sourcedrain2
                else:
                    out.childports += inst.ports.sourcedrain1
                    supply.childports += inst.ports.sourcedrain2
                specs.append(_lay.MOSFETInstSpec(
                    inst=inst, contact_left=contact, contact_right=contact,
                ))

            _l = layouter.transistors_layout(trans_specs=specs)
            _actbb = _l.bounds(mask=active.mask)
            x = 0.5*spec.monocell_width - _actbb.center.x
            y = act_bottom - _actbb.bottom
            _l.move(dxy=_geo.Point(x=x, y=y))
            _l_pmos += _l

            act_bottom += _actbb.height + actrow_space
        _pmos_actbb = _l_pmos.bounds(mask=active.mask)
        y = nmosguardring_actbb.top + 8*actpitch - _pmos_actbb.bottom
        l_pmos = layouter.place(_l_pmos, x=0.0, y=y)
        pmos_actbb = l_pmos.bounds(mask=active.mask)
        pmosguardring_height = tech.on_grid(
            pmos_actbb.height + 8*actpitch, mult=2, rounding="ceiling",
        )
        pmosguardring_width = tech.on_grid(
            pmos_actbb.width + 6*actpitch, mult=2, rounding="ceiling",
        )
        pmos_polybb = l_pmos.bounds(mask=poly.mask)
        pmos_m1bb = l_pmos.bounds(mask=metal1.mask)

        # pmos guardring
        pmosguardring_cell = fab.guardring(
            type_="n", width=pmosguardring_width, height=pmosguardring_height,
            fill_well=True, fill_implant=True,
        )
        inst = ckt.instantiate(pmosguardring_cell, name="pmosguardring")
        supply.childports += inst.ports.conn
        x = 0.5*spec.monocell_width
        l = layouter.place(inst, x=x, y=pmos_actbb.center.y)
        pmosguardring_m1bb = l.bounds(mask=metal1.mask)

        for ms in l_pmos.filter_polygons(
            net=supply, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            shape = _geo.Rect.from_rect(rect=bb, bottom=pmosguardring_m1bb.bottom)
            layouter.add_wire(net=supply, wire=metal1, shape=shape)

        shape = _geo.Rect.from_rect(
            rect=pmosguardring_m1bb,
            bottom=(pmosguardring_m1bb.top - comp.guardring_width),
        )
        layouter.add_wire(net=supply, wire=metal1, pin=metal1pin, shape=shape)

        # pmos in connection
        w = pmos_polybb.width
        _l = layouter.wire_layout(
            net=in_, wire=contact, bottom=poly,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _ch_polybb = _l.bounds(mask=poly.mask)
        _ch_chbb = _l.bounds(mask=contact.mask)
        _ch_m1bb = _l.bounds(mask=metal1.mask)

        x = pmos_polybb.center.x
        y = max(
            pmos_actbb.top + min_actpoly_space - _ch_polybb.bottom,
            pmos_m1bb.top + metal1.min_space - _ch_m1bb.bottom,
        )
        if min_actch_space is not None:
            y = max(y, pmos_actbb.top + min_actch_space - _ch_chbb.bottom)
        l = layouter.place(_l, x=x, y=y)
        ch_polybb = l.bounds(mask=poly.mask)
        pmosinch_m1bb = l.bounds(mask=metal1.mask)

        for ms in l_pmos.filter_polygons(net=in_, mask=poly.mask, split=True, depth=1):
            bb = ms.shape.bounds
            if bb.top + _geo.epsilon < ch_polybb.bottom:
                shape = _geo.Rect.from_rect(rect=bb, top=ch_polybb.top)
                layouter.add_wire(net=in_, wire=poly, shape=shape)

        _l = layouter.wire_layout(
            net=in_, wire=via1,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _via1_m1bb = _l.bounds(mask=metal1.mask)
        _via1_m2bb = _l.bounds(mask=metal2.mask)
        y = max(
            pmosinch_m1bb.bottom - _via1_m1bb.bottom,
            pmos_m1bb.top + metal1.min_space - _via1_m1bb.bottom,
            pmos_m1bb.top + 2*metal2.min_space - _via1_m2bb.bottom,
        )
        l = layouter.place(_l, x=x, y=y)
        pmosinvia1_m1bb = l.bounds(mask=metal1.mask)
        pmosinvia1_m2bb = l.bounds(mask=metal2.mask)

        if (pmosinvia1_m1bb.bottom - _geo.epsilon) > pmosinch_m1bb.top:
            shape = _geo.Rect.from_rect(rect=pmosinvia1_m1bb, bottom=pmosinch_m1bb.top)
            layouter.add_wire(net=in_, wire=metal1, shape=shape)

        # pmos out connection
        pmosout_m2left = spec.monocell_width
        pmosout_m2right = 0.0
        for ms in l_pmos.filter_polygons(
            net=out, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            l = layouter.add_wire(
                net=out, wire=via1, x=bb.center.x,
                bottom_bottom=bb.bottom, bottom_top=bb.top, bottom_enclosure="tall",
                top_bottom=bb.bottom, top_top=bb.top, top_enclosure="tall",
            )
            m2bb = l.bounds(mask=metal2.mask)
            pmosout_m2left = min(pmosout_m2left, m2bb.left)
            pmosout_m2right = max(pmosout_m2right, m2bb.right)

        assert nmosout_m2left > pmosout_m2left
        shape = _geo.Rect(
            left=pmosout_m2left, bottom=pmos_m1bb.bottom,
            right=max(nmosout_m2right, pmosout_m2right), top=pmos_m1bb.top,
        )
        layouter.add_wire(net=out, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=nmosout_m2left, bottom=nmos_m1bb.bottom,
            right=nmosout_m2right, top=pmos_m1bb.top,
        )
        layouter.add_wire(net=out, wire=metal2, pin=metal2pin, shape=shape)

        # in pin
        assert pmosinvia1_m2bb.left > nmosinvia1_m2bb.left
        shape = _geo.Rect.from_rect(rect=pmosinvia1_m2bb, left=nmosinvia1_m2bb.left)
        layouter.add_wire(net=in_, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=nmosinvia1_m2bb.left, bottom=nmosinvia1_m2bb.bottom,
            right=(pmosout_m2left - 3*metal2.min_space), top=pmosinvia1_m2bb.top,
        )
        layouter.add_wire(net=in_, wire=metal2, pin=metal2pin, shape=shape)

        # boundary
        layouter.layout.boundary = layouter.layout.bounds(mask=metal1.mask)


class _Pad(_cell._FactoryOnDemandCell):
    def __init__(self, *,
        name: str, fab: "IOFactory", width: float, height: float, start_via: int,
    ):
        super().__init__(fab=fab, name=name)

        self._width = width
        self._height = height
        self._start_via = start_via

    @property
    def width(self) -> float:
        return self._width
    @property
    def height(self) -> float:
        return self._height
    @property
    def start_via(self) -> int:
        return self._start_via

    def _create_circuit(self):
        ckt = self.new_circuit()
        ckt.new_net(name="pad", external=True)

    def _create_layout(self):
        fab = self.fab
        width = self.width
        height = self.height
        start_via = self.start_via
        framespec = fab.frame.framespec

        comp = fab.computed
        pad = comp.pad
        topmetal = pad.bottom
        topmetalpin = topmetal.pin

        pad_net = self.circuit.nets.pad
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        enc = comp.pad.min_bottom_enclosure.max()
        metal_width = width + 2*enc
        metal_height = height + 2*enc

        metal_bounds = _geo.Rect.from_size(width=metal_width, height=metal_height)
        pad_bounds = _geo.Rect.from_size(width=width, height=height)

        # TODO: add support in layouter.add_wire for PadOpening
        layouter.add_wire(net=pad_net, wire=topmetal, pin=topmetalpin, shape=metal_bounds)
        layout.add_shape(layer=comp.pad, net=pad_net, shape=pad_bounds)

        if framespec.pad_viapitch is None:
            top_via = comp.vias[-1]
            via_pitch = top_via.width + top_via.min_space
        else:
            via_pitch = framespec.pad_viapitch

        for i, via in enumerate(comp.vias[start_via:]):
            l_via = _hlp.diamondvia(
                fab=fab, net=pad_net, via=via,
                width=metal_width, height=metal_height,
                space=(via_pitch - via.width),
                enclosure=_prp.Enclosure(framespec.pad_viametal_enclosure),
                center_via=((i%2) == 0), corner_distance=framespec.pad_viacorner_distance,
            )
            layouter.place(l_via, x=0.0, y=0.0)

        layout.boundary = metal_bounds
PadT = _Pad


class _LevelUp(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        circuit = self.new_circuit()

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, fab.computed.minwidth4ext_activewithcontact,
        )

        # Input inverter
        n_i_inv = circuit.instantiate(spec.nmos, name="n_i_inv", w=comp.maxnmos_w)
        p_i_inv = circuit.instantiate(spec.pmos, name="p_i_inv", w=comp.maxpmos_w)

        # Level shifter
        n_lvld_n = circuit.instantiate(
            spec.ionmos, name="n_lvld_n", w=comp.maxionmos_w,
        )
        n_lvld = circuit.instantiate(
            spec.ionmos, name="n_lvld", w=comp.maxionmos_w,
        )
        p_lvld_n = circuit.instantiate(
            spec.iopmos, name="p_lvld_n", w=iopmos_lvlshift_w,
        )
        p_lvld = circuit.instantiate(
            spec.iopmos, name="p_lvld", w=iopmos_lvlshift_w,
        )

        # Output inverter/driver
        n_lvld_n_inv = circuit.instantiate(
            spec.ionmos, name="n_lvld_n_inv", w=comp.maxionmos_w,
        )
        p_lvld_n_inv = circuit.instantiate(
            spec.iopmos, name="p_lvld_n_inv", w=comp.maxiopmos_w,
        )

        # Create the nets
        circuit.new_net(name="vdd", external=True, childports=(
            p_i_inv.ports.sourcedrain2, p_i_inv.ports.bulk,
        ))
        circuit.new_net(name="iovdd", external=True, childports=(
            p_lvld_n.ports.sourcedrain1, p_lvld_n.ports.bulk,
            p_lvld.ports.sourcedrain2, p_lvld.ports.bulk,
            p_lvld_n_inv.ports.sourcedrain1, p_lvld_n_inv.ports.bulk,
        ))
        circuit.new_net(name="vss", external=True, childports=(
            n_i_inv.ports.sourcedrain2, n_i_inv.ports.bulk,
            n_lvld_n.ports.sourcedrain1, n_lvld_n.ports.bulk,
            n_lvld.ports.sourcedrain2, n_lvld.ports.bulk,
            n_lvld_n_inv.ports.sourcedrain1, n_lvld_n_inv.ports.bulk,
        ))

        circuit.new_net(name="i", external=True, childports=(
            n_i_inv.ports.gate, p_i_inv.ports.gate,
            n_lvld_n.ports.gate,
        ))
        circuit.new_net(name="i_n", external=False, childports=(
            n_i_inv.ports.sourcedrain1, p_i_inv.ports.sourcedrain1,
            n_lvld.ports.gate,
        ))
        circuit.new_net(name="lvld", external=False, childports=(
            p_lvld_n.ports.gate,
            n_lvld.ports.sourcedrain1, p_lvld.ports.sourcedrain1,
        ))
        circuit.new_net(name="lvld_n", external=False, childports=(
            n_lvld_n.ports.sourcedrain2, p_lvld_n.ports.sourcedrain2,
            p_lvld.ports.gate,
            n_lvld_n_inv.ports.gate, p_lvld_n_inv.ports.gate,
        ))
        circuit.new_net(name="o", external=True, childports=(
            n_lvld_n_inv.ports.sourcedrain2, p_lvld_n_inv.ports.sourcedrain2,
        ))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        circuit = self.circuit
        insts = circuit.instances
        nets = circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        ionimplant = comp.ionimplant
        iopimplant = comp.iopimplant
        assert pimplant == iopimplant
        nwell = comp.nwell
        poly = comp.poly
        contact = comp.contact
        metal1 = contact.top[0]
        assert isinstance(metal1, _prm.MetalWire)
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = via1.top[0]
        assert isinstance(metal2, _prm.MetalWire)

        chm1_enc = contact.min_top_enclosure[0]
        chm1_wideenc = _prp.Enclosure((chm1_enc.max(), chm1_enc.min()))

        actox_enc = (
            comp.activeoxide_enclosure.max() if comp.activeoxide_enclosure is not None
            else comp.iogateoxide_enclosure.max()
        )

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, comp.minwidth4ext_activewithcontact,
        )

        layouter = self.new_circuitlayouter()
        layout = self.layout
        active_left = 0.5*active.min_space

        if metal2.pin is not None:
            pin_args = {"pin": metal2.pin}
        else:
            pin_args = {}

        min_actpoly_space = tech.computed.min_space(active, poly)
        try:
            min_actch_space = tech.computed.min_space(active, contact)
        except AttributeError:
            min_actch_space = None

        #
        # Core row
        #

        x = active_left + 0.5*comp.minwidth_activewithcontact
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        chvss_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            bottom_height=(top - bottom),
        )
        chvdd_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=chvss_m1bounds.top, top=chvdd_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i_n, wire=metal1, shape=shape)
        bottom_shape = _geo.Rect(
            bottom=chvss_m1bounds.bottom, top=chvdd_m1bounds.top,
            right=chvss_m1bounds.right, left=(chvss_m1bounds.right - comp.metal[1].minwidth_up),
        )
        m2bounds = layouter.add_wire(
            net=nets.i_n, wire=via1, bottom_shape=bottom_shape,
        ).bounds(mask=metal2.mask)
        i_n_m2bounds = _geo.Rect.from_rect(rect=m2bounds, bottom=spec.iorow_height)
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=i_n_m2bounds)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        n_i_inv_lay = l = layouter.place(insts.n_i_inv, x=x, y=comp.maxnmos_y)
        gatebounds_n = l.bounds(mask=poly.mask)
        p_i_inv_lay = l = layouter.place(insts.p_i_inv, x=x, y=comp.maxpmos_y)
        gatebounds_p = l.bounds(mask=poly.mask)

        shape = _geo.Rect(
            left=min(gatebounds_n.left, gatebounds_p.left), bottom=gatebounds_n.top,
            right=max(gatebounds_n.right, gatebounds_p.right), top=gatebounds_p.bottom,
        )
        polybounds = layouter.add_wire(
            net=nets.i, wire=poly, shape=shape,
        ).bounds(mask=poly.mask)
        x_pad = max(
            polybounds.left + 0.5*comp.minwidth4ext_polywithcontact,
            chvss_m1bounds.right + metal1.min_space
            + 0.5*comp.metal[1].minwidth4ext_down,
        )
        l = layouter.add_wire(
            net=nets.i, wire=contact, bottom=poly, x=x_pad,
            y=tech.on_grid(0.5*(polybounds.bottom + polybounds.top)),
        )
        ppad_m1bounds = l.bounds(mask=metal1.mask)
        ppad_polybounds = l.bounds(mask=poly.mask)
        if ppad_polybounds.left > polybounds.right:
            shape = _geo.Rect.from_rect(rect=ppad_polybounds, left=polybounds.left)
            layouter.add_wire(net=nets.i, wire=poly, shape=shape)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        bottom = comp.maxnmos_activebottom
        top = min(comp.maxnmos_activetop, ppad_m1bounds.bottom - metal1.min_width)
        chvss_m1bounds = layouter.add_wire(
            net=nets.vss, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space)
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = max(comp.maxpmos_activebottom, ppad_m1bounds.top + metal1.min_width)
        top = comp.maxpmos_activetop
        chvdd_m1bounds = layouter.add_wire(
            net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space),
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )

        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=spec.iorow_height, top=chvss_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.vss, wire=metal1, shape=shape)
        shape = _geo.Rect.from_rect(rect=chvdd_m1bounds, top=spec.cells_height)
        layouter.add_wire(net=nets.vdd, wire=metal1, shape=shape)

        x += comp.minwidth_activewithcontact + active.min_space
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        i_nactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        ndio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        i_pactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom),
        )
        pdio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=ndio_m1bounds, bottom=ndio_m1bounds.top, top=pdio_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        shape = _geo.Rect(
            left=ppad_m1bounds.left, bottom=(chvss_m1bounds.top + metal1.min_space),
            right=ndio_m1bounds.right, top=(chvdd_m1bounds.bottom - metal1.min_space),
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        bottom = ndio_m1bounds.bottom
        top = pdio_m1bounds.top
        i_m2bounds = layouter.add_wire(
            net=nets.i, wire=via1, x=x, bottom_bottom=bottom, bottom_top=top,
        ).bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i, wire=metal2, **pin_args, shape=i_m2bounds) # pyright: ignore

        # Fill implants
        if nimplant is not None:
            bb = i_nactcont_lay.bounds(mask=nimplant.mask)
            bb2 = n_i_inv_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(prim=nimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))
        if pimplant is not None:
            bb = i_pactcont_lay.bounds(mask=pimplant.mask)
            bb2 = p_i_inv_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(prim=pimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))

        #
        # IO row
        #
        active_left = 0.5*comp.min_oxactive_space
        y_iopmos_lvlshift = comp.maxiopmos_y

        # Place left source-drain contacts
        _nch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _nch_lvld_actbounds = _nch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _nch_lvld_actbounds.left
        y = comp.maxionmos_y
        nch_lvld_lay = layouter.place(object_=_nch_lvld_lay, x=x, y=y)
        nch_lvld_chbounds = nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_m1bounds = nch_lvld_lay.bounds(mask=metal1.mask)
        _pch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_actbounds = _pch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _pch_lvld_actbounds.left
        y = y_iopmos_lvlshift
        pch_lvld_lay = layouter.place(object_=_pch_lvld_lay, x=x, y=y)
        pch_lvld_chbounds = pch_lvld_lay.bounds(mask=contact.mask)
        pch_lvld_m1bounds = pch_lvld_lay.bounds(mask=metal1.mask)
        lvld_m1_lay = layouter.add_wire(
            net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_m1bounds, bottom=pch_lvld_m1bounds.bottom,
            ),
        )
        lvld_m1_bounds = lvld_m1_lay.bounds()

        poly_left = max(
            nch_lvld_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            pch_lvld_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld and p_lvld, and compute pad y placements
        _n_lvld_lay = layouter.inst_layout(
            inst=insts.n_lvld, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_polybounds = _n_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_polybounds.left
        y = comp.maxionmos_y
        n_lvld_lay = layouter.place(_n_lvld_lay, x=x, y=y)
        n_lvld_actbounds = n_lvld_lay.bounds(mask=active.mask)
        n_lvld_polybounds = n_lvld_lay.bounds(mask=poly.mask)
        _p_lvld_lay = layouter.inst_layout(
            inst=insts.p_lvld, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_polybounds = _p_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_lay = layouter.place(_p_lvld_lay, x=x, y=y)
        p_lvld_actbounds = p_lvld_lay.bounds(mask=active.mask)
        p_lvld_polybounds = p_lvld_lay.bounds(mask=poly.mask)
        w = cast(_ckt._PrimitiveInstance, insts.p_lvld).params["w"]
        p_lvld_pad_bottom = (
            y_iopmos_lvlshift + 0.5*w
            + tech.computed.min_space(active, poly)
        )
        p_lvld_pad_top = (
            p_lvld_pad_bottom + comp.minwidth4ext_polywithcontact
        )
        p_lvld_n_pad_bottom = p_lvld_pad_top + poly.min_space

        # Place mid source-drain contacts
        _lvlshift_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _lvlshift_chvss_chbounds = _lvlshift_chiovss_lay.bounds(mask=contact.mask)
        x = (
            n_lvld_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _lvlshift_chvss_chbounds.left
        )
        y = comp.maxionmos_y
        lvlshit_chiovss_lay = layouter.place(object_=_lvlshift_chiovss_lay, x=x, y=y)
        lvlshift_chiovss_chbounds = lvlshit_chiovss_lay.bounds(mask=contact.mask)
        lvlshift_chiovss_m1bounds = lvlshit_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovss_m1bounds, top=spec.iorow_height,
            ),
        )
        _lvlshift_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact, bottom_height=iopmos_lvlshift_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            top_enclosure=chm1_wideenc,
        )
        _lvlshift_chiovdd_chbounds = _lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        x = (
            p_lvld_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _lvlshift_chiovdd_chbounds.left
        )
        y = y_iopmos_lvlshift
        lvlshift_chiovdd_lay = layouter.place(object_=_lvlshift_chiovdd_lay, x=x, y=y)
        lvlshift_chiovdd_chbounds = lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        lvlshift_chiovdd_m1bounds = lvlshift_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovdd_m1bounds, bottom=0.0,
            ),
        )

        poly_left = max(
            lvlshift_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            lvlshift_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld_n and p_lvld_n
        _n_lvld_n_lay = layouter.inst_layout(
            inst=insts.n_lvld_n, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_n_polybounds = _n_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_n_polybounds.left
        y = comp.maxionmos_y
        n_lvld_n_lay = layouter.place(object_=_n_lvld_lay, x=x, y=y)
        n_lvld_n_actbounds = n_lvld_n_lay.bounds(mask=active.mask)
        n_lvld_n_polybounds = n_lvld_n_lay.bounds(mask=poly.mask)
        _p_lvld_n_lay = layouter.inst_layout(
            inst=insts.p_lvld_n, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_n_polybounds = _p_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_n_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_n_lay = layouter.place(object_=_p_lvld_n_lay, x=x, y=y)
        p_lvld_n_polybounds = p_lvld_n_lay.bounds(mask=poly.mask)

        # Place right source-drain contacts
        _nch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
        )
        _nch_lvld_n_chbounds = _nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_n_x = (
            n_lvld_n_polybounds.right + spec.nmos.computed.min_contactgate_space
            - _nch_lvld_n_chbounds.left
        )
        nch_lvld_n_y = comp.maxionmos_y
        nch_lvld_n_lay = layouter.place(
            object_=_nch_lvld_n_lay, x=nch_lvld_n_x, y=nch_lvld_n_y,
        )
        nch_lvld_n_actbounds = nch_lvld_n_lay.bounds(mask=active.mask)
        nch_lvld_n_m1bounds = nch_lvld_n_lay.bounds(mask=metal1.mask)
        _pch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_n_chbounds = _pch_lvld_n_lay.bounds(mask=contact.mask)
        pch_lvld_n_x = (
            p_lvld_n_polybounds.right + spec.pmos.computed.min_contactgate_space
            - _pch_lvld_n_chbounds.left
        )
        pch_lvld_n_y = y_iopmos_lvlshift
        pch_lvld_n_lay = layouter.place(
            object_=_pch_lvld_n_lay, x=pch_lvld_n_x, y=pch_lvld_n_y
        )
        pch_lvld_n_actbounds = pch_lvld_n_lay.bounds(mask=active.mask)
        pch_lvld_n_m1bounds = pch_lvld_n_lay.bounds(mask=metal1.mask)
        lvld_n_m1_lay = layouter.add_wire(
            net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_n_m1bounds, bottom=pch_lvld_n_m1bounds.bottom,
            ),
        )
        lvld_n_m1_bounds = lvld_n_m1_lay.bounds()
        # Add manual implant rectangle
        if iopimplant is not None:
            bb1 = pch_lvld_lay.bounds(mask=iopimplant.mask)
            bb2 = pch_lvld_n_lay.bounds(mask=iopimplant.mask)
            if iopimplant is not None:
                layouter.add_portless(prim=iopimplant, shape=_geo.Rect(
                    left=bb1.left, bottom=bb1.bottom,
                    right=bb2.right, top=bb1.top,
                ))

        # Poly pads for nmoses of the level shifter
        _n_lvld_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_ppad_polybounds = _n_lvld_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_ppad_chbounds = _n_lvld_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_ppad_m1bounds = _n_lvld_ppad_lay.bounds(mask=metal1.mask)
        _n_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_n_ppad_polybounds = _n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_n_ppad_chbounds = _n_lvld_n_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_n_ppad_m1bounds = _n_lvld_n_ppad_lay.bounds(mask=metal1.mask)

        n_lvld_ppad_x = max(
            n_lvld_polybounds.left - _n_lvld_ppad_polybounds.left,
            n_lvld_polybounds.right - _n_lvld_ppad_polybounds.right,
            lvld_m1_bounds.right + metal1.min_space - _n_lvld_ppad_m1bounds.left,
        )
        n_lvld_ppad_y = min(
            n_lvld_actbounds.bottom - min_actpoly_space - _n_lvld_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_ppad_y = min(
                n_lvld_ppad_y,
                n_lvld_actbounds.bottom - min_actch_space - _n_lvld_ppad_chbounds.top,
            )
        n_lvld_n_ppad_x = min(
            n_lvld_n_polybounds.left - _n_lvld_n_ppad_polybounds.left,
            n_lvld_n_polybounds.right - _n_lvld_n_ppad_polybounds.right,
            lvld_n_m1_bounds.left - metal1.min_space - _n_lvld_n_ppad_m1bounds.right,
        )
        n_lvld_n_ppad_y = min(
            n_lvld_n_actbounds.bottom - min_actpoly_space - _n_lvld_n_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_n_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_n_ppad_y = min(
                n_lvld_n_ppad_y,
                n_lvld_n_actbounds.bottom - min_actch_space - _n_lvld_n_ppad_chbounds.top,
            )

        n_lvld_ppad_lay = layouter.place(
            object_=_n_lvld_ppad_lay, x=n_lvld_ppad_x, y=n_lvld_ppad_y,
        )
        n_lvld_ppad_polybounds = n_lvld_ppad_lay.bounds(mask=poly.mask)
        n_lvld_ppad_m1bounds = n_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_polybounds, bottom=n_lvld_ppad_polybounds.bottom,
        ))
        n_lvld_n_ppad_lay = layouter.place(
            object_=_n_lvld_n_ppad_lay, x=n_lvld_n_ppad_x, y=n_lvld_n_ppad_y,
        )
        n_lvld_n_ppad_polybounds = n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        n_lvld_n_ppad_m1bounds = n_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_polybounds, bottom=n_lvld_n_ppad_polybounds.bottom,
        ))

        # via1 pads on the poly pads
        # draw two vias to make sure metal1 area is big enough
        _n_lvld_via_lay = layouter.wire_layout(net=nets.i_n, wire=via1, rows=2)
        _n_lvld_via_m1bounds = _n_lvld_via_lay.bounds(mask=metal1.mask)
        n_lvld_via_x = n_lvld_ppad_m1bounds.left - _n_lvld_via_m1bounds.left
        n_lvld_via_y = n_lvld_ppad_m1bounds.top - _n_lvld_via_m1bounds.top
        n_lvld_via_lay = layouter.place(
            object_=_n_lvld_via_lay, x=n_lvld_via_x, y=n_lvld_via_y,
        )
        n_lvld_n_via_m2bounds = n_lvld_via_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=_geo.Rect.from_rect(
            rect=i_n_m2bounds, bottom=n_lvld_n_via_m2bounds.bottom,
        ))
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_via_m2bounds, left=i_n_m2bounds.left,
        ))
        _n_lvld_n_via_lay = layouter.wire_layout(net=nets.i, wire=via1, rows=2)
        _n_lvld_n_via_m1bounds = _n_lvld_n_via_lay.bounds(mask=metal1.mask)
        n_lvld_n_via_x = n_lvld_n_ppad_m1bounds.right - _n_lvld_n_via_m1bounds.right
        n_lvld_n_via_y = n_lvld_n_ppad_m1bounds.top - _n_lvld_n_via_m1bounds.top
        n_lvld_n_via_lay = layouter.place(
            object_=_n_lvld_n_via_lay, x=n_lvld_n_via_x, y=n_lvld_n_via_y,
        )
        n_lvld_n_via_m2bounds = n_lvld_n_via_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i, wire=metal2, shape=_geo.Rect.from_rect(
            rect=i_m2bounds, bottom=n_lvld_n_via_m2bounds.bottom,
        ))
        assert i_m2bounds.left <= n_lvld_n_via_m2bounds.right
        layouter.add_wire(net=nets.i, wire=metal2, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_via_m2bounds, left=i_m2bounds.left,
        ))

        # Poly pads for the pmoses of the level shifter
        _p_lvld_ppad_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_ppad_polybounds = _p_lvld_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_ppad_chbounds = _p_lvld_ppad_lay.bounds(mask=contact.mask)
        _p_lvld_ppad_m1bounds = _p_lvld_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_ppad_x = max(
            lvld_m1_bounds.right + metal1.min_space - _p_lvld_ppad_m1bounds.left,
            p_lvld_polybounds.left - _p_lvld_ppad_polybounds.left,
            p_lvld_polybounds.right - _p_lvld_ppad_polybounds.right,
        )
        p_lvld_ppad_y = max(
            p_lvld_actbounds.top + min_actpoly_space - _p_lvld_ppad_polybounds.bottom,
            lvlshift_chiovdd_m1bounds.top + metal1.min_space - _p_lvld_ppad_m1bounds.bottom,
        )
        if min_actch_space is not None:
            p_lvld_ppad_y = max(
                p_lvld_ppad_y,
                p_lvld_actbounds.top + min_actch_space - _p_lvld_ppad_chbounds.bottom
            )
        p_lvld_ppad_lay = layouter.place(
            object_=_p_lvld_ppad_lay, x=p_lvld_ppad_x, y=p_lvld_ppad_y,
        )
        p_lvld_ppad_polybounds = p_lvld_ppad_lay.bounds(mask=poly.mask)
        p_lvld_ppad_m1bounds = p_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_polybounds, top=p_lvld_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_ppad_m1bounds, right=lvld_n_m1_bounds.right,
        ))

        _p_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_n_ppad_polybounds = _p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_n_ppad_m1bounds = _p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_n_ppad_x = min(
            lvld_n_m1_bounds.left - metal1.min_space - _p_lvld_n_ppad_m1bounds.right,
            p_lvld_n_polybounds.left - _p_lvld_n_ppad_polybounds.left,
            p_lvld_n_polybounds.right - _p_lvld_n_ppad_polybounds.right,
        )
        p_lvld_n_ppad_y = (
            p_lvld_ppad_m1bounds.top + metal1.min_space - _p_lvld_n_ppad_m1bounds.bottom
        )
        p_lvld_n_ppad_lay = layouter.place(
            object_=_p_lvld_n_ppad_lay, x=p_lvld_n_ppad_x, y=p_lvld_n_ppad_y,
        )
        p_lvld_n_ppad_polybounds = p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        p_lvld_n_ppad_m1bounds = p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_polybounds, top=p_lvld_n_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_ppad_m1bounds, left=lvld_m1_bounds.left,
        ))

        # Output buffer
        active_left = (
            max(nch_lvld_n_actbounds.right, pch_lvld_n_actbounds.right)
            + comp.min_oxactive_space
        )

        # Place left source-drain contacts
        _obuf_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _obuf_chiovss_actbounds = _obuf_chiovss_lay.bounds(mask=active.mask)
        obuf_chiovss_x = active_left - _obuf_chiovss_actbounds.left
        obuf_chiovss_y = comp.maxionmos_y
        obuf_chiovss_lay = layouter.place(
            object_=_obuf_chiovss_lay, x=obuf_chiovss_x, y=obuf_chiovss_y,
        )
        obuf_chiovss_chbounds = obuf_chiovss_lay.bounds(mask=contact.mask)
        obuf_chiovss_m1bounds = obuf_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovss_m1bounds, top=spec.iorow_height,
        ))
        _obuf_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact,
            bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
        )
        _obuf_chiovdd_actbounds = _obuf_chiovdd_lay.bounds(mask=active.mask)
        obuf_chiovdd_x = active_left - _obuf_chiovdd_actbounds.left
        obuf_chiovdd_y = comp.maxiopmos_y
        obuf_chiovdd_lay = layouter.place(
            object_=_obuf_chiovdd_lay, x=obuf_chiovdd_x, y=obuf_chiovdd_y,
        )
        obuf_chiovdd_chbounds = obuf_chiovdd_lay.bounds(mask=contact.mask)
        obuf_chiovdd_m1bounds = obuf_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovdd_m1bounds, bottom=0.0,
        ))

        poly_left = max(
            obuf_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            obuf_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Output buffer ionmos+iopmos
        x = obuf_chiovss_m1bounds.center.x + max(
            comp.minionmos_contactgatepitch,
            comp.miniopmos_contactgatepitch,
        )
        _n_obuf_lay = layouter.inst_layout(inst=insts.n_lvld_n_inv)
        _n_obuf_polybounds = _n_obuf_lay.bounds(mask=poly.mask)
        n_obuf_x = poly_left - _n_obuf_polybounds.left
        n_obuf_y = comp.maxionmos_y
        n_obuf_lay = layouter.place(
            object_=_n_obuf_lay, x=n_obuf_x, y=n_obuf_y
        )
        n_obuf_polybounds = n_obuf_lay.bounds(mask=poly.mask)
        _p_obuf_lay = layouter.inst_layout(inst=insts.p_lvld_n_inv)
        _p_obuf_polybounds = _p_obuf_lay.bounds(mask=poly.mask)
        p_obuf_x = poly_left - _p_obuf_polybounds.left
        p_obuf_y = comp.maxiopmos_y
        p_obuf_lay = layouter.place(object_=_p_obuf_lay, x=p_obuf_x, y=p_obuf_y)
        p_obuf_polybounds = p_obuf_lay.bounds(mask=poly.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_obuf_polybounds, bottom=p_obuf_polybounds.top,
        ))

        # poly pad
        _obuf_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _obuf_ppad_polybounds = _obuf_ppad_lay.bounds(mask=poly.mask)
        obuf_ppad_x = min(
            n_obuf_polybounds.left - _obuf_ppad_polybounds.left,
            n_obuf_polybounds.right - _obuf_ppad_polybounds.right,
        )
        obuf_ppad_y = tech.on_grid(0.5*(n_obuf_polybounds.bottom + p_obuf_polybounds.top))
        obuf_ppad_lay = layouter.place(object_=_obuf_ppad_lay, x=obuf_ppad_x, y=obuf_ppad_y)
        obuf_ppad_m1bounds = obuf_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_ppad_m1bounds, left=nch_lvld_n_m1bounds.left,
        ))

        # Place right source-drain contacts
        _nch_o_lay = layouter.wire_layout(
            net=nets.o, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _nch_o_chbounds = _nch_o_lay.bounds(mask=contact.mask)
        nch_o_x = (
            n_obuf_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _nch_o_chbounds.left
        )
        nch_o_y = comp.maxionmos_y
        nch_o_lay = layouter.place(object_=_nch_o_lay, x=nch_o_x, y=nch_o_y)
        nch_o_m1bounds = nch_o_lay.bounds(mask=metal1.mask)
        _pch_o_lay = layouter.wire_layout(
            net=nets.o, well_net=nets.iovdd, wire=contact, bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _pch_o_chbounds = _pch_o_lay.bounds(mask=contact.mask)
        pch_o_x = (
            p_obuf_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _pch_o_chbounds.left
        )
        pch_o_y = comp.maxiopmos_y
        pch_o_lay = layouter.place(object_=_pch_o_lay, x=pch_o_x, y=pch_o_y)
        pch_o_m1bounds = pch_o_lay.bounds(mask=metal1.mask)
        m1_o_lay = layouter.add_wire(net=nets.o, wire=metal1, shape=_geo.Rect.from_rect(
            rect=nch_o_m1bounds, bottom=pch_o_m1bounds.bottom,
        ))
        m1_o_bounds = m1_o_lay.bounds()
        _via1_o_lay = layouter.wire_layout(
            net=nets.o, wire=via1, bottom_height=m1_o_bounds.height
        )
        _via1_o_m1bounds = _via1_o_lay.bounds(mask=metal1.mask)
        via1_o_x = m1_o_bounds.left - _via1_o_m1bounds.left
        via1_o_y = m1_o_bounds.bottom - _via1_o_m1bounds.bottom
        via1_o_lay = layouter.place(object_=_via1_o_lay, x=via1_o_x, y=via1_o_y)
        via1_o_m2bounds = via1_o_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.o, wire=metal2, **pin_args, shape=via1_o_m2bounds) # pyright: ignore

        cells_right = layout.bounds(mask=active.mask).right + 0.5*comp.min_oxactive_space

        # fill implants
        if nimplant is not None:
            bb = n_obuf_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(
                prim=nimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )
        if pimplant is not None:
            bb = p_obuf_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(
                prim=pimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )

        #
        # Set boundary
        #

        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cells_right, top=spec.cells_height,
        )

        #
        # Well/bulk contacts
        #

        l1 = layouter.add_wire(
            net=nets.iovdd, wire=contact, well_net=nets.iovdd,
            bottom=active, bottom_implant=ionimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=0, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.iovdd, wire=active, implant=ionimplant,
            well_net=nets.iovdd, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        nw_enc = spec.iopmos.computed.min_active_well_enclosure.max()
        shape = _geo.Rect(
            left=-nw_enc,
            bottom=min(bb1.bottom, bb2.bottom),
            right=(cells_right + nw_enc),
            top=spec.iorow_nwell_height,
        )
        layouter.add_wire(net=nets.iovdd, wire=nwell, shape=shape)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.metal[1].minwidth_updown,
        )

        layouter.add_wire(
            net=nets.vss, wire=contact, bottom=active,
            bottom_implant=pimplant, top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.iorow_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        layouter.add_wire(
            net=nets.vss, wire=active, implant=pimplant,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=nets.vss, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.metal[1].minwidth_updown,
        )

        l1 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=contact, bottom=active,
            bottom_implant=nimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.cells_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active,
            implant=nimplant, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        layouter.add_wire(
            net=nets.vdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.metal[1].minwidth_updown,
        )
        shape = _geo.Rect(
            left=min(bb1.left, bb2.left),
            bottom=(spec.cells_height - spec.corerow_nwell_height),
            right=max(bb1.right, bb2.right),
            top=max(bb1.top, bb2.top),
        )
        layouter.add_wire(net=nets.vdd, wire=nwell, shape=shape)

        # Thick oxide
        assert comp.ionmos.gate.oxide is not None
        layouter.add_portless(prim=comp.ionmos.gate.oxide, shape=_geo.Rect(
            left=-actox_enc, bottom=comp.io_oxidebottom,
            right=(cells_right + actox_enc), top=comp.io_oxidetop,
        ))


class _LevelUpInv(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        circuit = self.new_circuit()

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, fab.computed.minwidth4ext_activewithcontact,
        )

        # Input inverter
        n_i_inv = circuit.instantiate(spec.nmos, name="n_i_inv", w=comp.maxnmos_w)
        p_i_inv = circuit.instantiate(spec.pmos, name="p_i_inv", w=comp.maxpmos_w)

        # Level shifter
        n_lvld_n = circuit.instantiate(
            spec.ionmos, name="n_lvld_n", w=comp.maxionmos_w,
        )
        n_lvld = circuit.instantiate(
            spec.ionmos, name="n_lvld", w=comp.maxionmos_w,
        )
        p_lvld_n = circuit.instantiate(
            spec.iopmos, name="p_lvld_n", w=iopmos_lvlshift_w,
        )
        p_lvld = circuit.instantiate(
            spec.iopmos, name="p_lvld", w=iopmos_lvlshift_w,
        )

        # Output inverter/driver
        n_lvld_n_inv = circuit.instantiate(
            spec.ionmos, name="n_lvld_n_inv", w=comp.maxionmos_w,
        )
        p_lvld_n_inv = circuit.instantiate(
            spec.iopmos, name="p_lvld_n_inv", w=comp.maxiopmos_w,
        )

        # Create the nets
        circuit.new_net(name="vdd", external=True, childports=(
            p_i_inv.ports.sourcedrain2, p_i_inv.ports.bulk,
        ))
        circuit.new_net(name="iovdd", external=True, childports=(
            p_lvld_n.ports.sourcedrain1, p_lvld_n.ports.bulk,
            p_lvld.ports.sourcedrain2, p_lvld.ports.bulk,
            p_lvld_n_inv.ports.sourcedrain1, p_lvld_n_inv.ports.bulk,
        ))
        circuit.new_net(name="vss", external=True, childports=(
            n_i_inv.ports.sourcedrain2, n_i_inv.ports.bulk,
            n_lvld_n.ports.sourcedrain1, n_lvld_n.ports.bulk,
            n_lvld.ports.sourcedrain2, n_lvld.ports.bulk,
            n_lvld_n_inv.ports.sourcedrain1, n_lvld_n_inv.ports.bulk,
        ))

        circuit.new_net(name="i", external=True, childports=(
            n_i_inv.ports.gate, p_i_inv.ports.gate,
            n_lvld.ports.gate,
        ))
        circuit.new_net(name="i_n", external=False, childports=(
            n_i_inv.ports.sourcedrain1, p_i_inv.ports.sourcedrain1,
            n_lvld_n.ports.gate,
        ))
        circuit.new_net(name="lvld", external=False, childports=(
            p_lvld_n.ports.gate,
            n_lvld.ports.sourcedrain1, p_lvld.ports.sourcedrain1,
        ))
        circuit.new_net(name="lvld_n", external=False, childports=(
            n_lvld_n.ports.sourcedrain2, p_lvld_n.ports.sourcedrain2,
            p_lvld.ports.gate,
            n_lvld_n_inv.ports.gate, p_lvld_n_inv.ports.gate,
        ))
        circuit.new_net(name="o", external=True, childports=(
            n_lvld_n_inv.ports.sourcedrain2, p_lvld_n_inv.ports.sourcedrain2,
        ))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        circuit = self.circuit
        insts = circuit.instances
        nets = circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        ionimplant = comp.ionimplant
        iopimplant = comp.iopimplant
        assert pimplant == iopimplant
        nwell = comp.nwell
        poly = comp.poly
        contact = comp.contact
        metal1 = contact.top[0]
        assert isinstance(metal1, _prm.MetalWire)
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = via1.top[0]
        assert isinstance(metal2, _prm.MetalWire)

        chm1_enc = contact.min_top_enclosure[0]
        chm1_wideenc = _prp.Enclosure((chm1_enc.max(), chm1_enc.min()))

        actox_enc = (
            comp.activeoxide_enclosure.max() if comp.activeoxide_enclosure is not None
            else comp.iogateoxide_enclosure.max()
        )

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, comp.minwidth4ext_activewithcontact,
        )

        layouter = self.new_circuitlayouter()
        layout = self.layout
        active_left = 0.5*active.min_space

        if metal2.pin is not None:
            pin_args = {"pin": metal2.pin}
        else:
            pin_args = {}

        min_actpoly_space = tech.computed.min_space(active, poly)
        try:
            min_actch_space = tech.computed.min_space(active, contact)
        except AttributeError:
            min_actch_space = None

        #
        # Core row
        #

        x = active_left + 0.5*comp.minwidth_activewithcontact
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        chvss_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            bottom_height=(top - bottom),
        )
        chvdd_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=chvss_m1bounds.top, top=chvdd_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i_n, wire=metal1, shape=shape)
        bottom_shape = _geo.Rect(
            bottom=chvss_m1bounds.bottom, top=chvdd_m1bounds.top,
            right=chvss_m1bounds.right, left=(chvss_m1bounds.right - comp.metal[1].minwidth_up),
        )
        m2bounds = layouter.add_wire(
            net=nets.i_n, wire=via1, bottom_shape=bottom_shape,
        ).bounds(mask=metal2.mask)
        i_n_m2bounds = _geo.Rect.from_rect(rect=m2bounds, bottom=spec.iorow_height)
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=i_n_m2bounds)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        n_i_inv_lay = l = layouter.place(insts.n_i_inv, x=x, y=comp.maxnmos_y)
        gatebounds_n = l.bounds(mask=poly.mask)
        p_i_inv_lay = l = layouter.place(insts.p_i_inv, x=x, y=comp.maxpmos_y)
        gatebounds_p = l.bounds(mask=poly.mask)

        shape = _geo.Rect(
            left=min(gatebounds_n.left, gatebounds_p.left), bottom=gatebounds_n.top,
            right=max(gatebounds_n.right, gatebounds_p.right), top=gatebounds_p.bottom,
        )
        polybounds = layouter.add_wire(
            net=nets.i, wire=poly, shape=shape,
        ).bounds(mask=poly.mask)
        x_pad = max(
            polybounds.left + 0.5*comp.minwidth4ext_polywithcontact,
            chvss_m1bounds.right + metal1.min_space
            + 0.5*comp.metal[1].minwidth4ext_down,
        )
        l = layouter.add_wire(
            net=nets.i, wire=contact, bottom=poly, x=x_pad,
            y=tech.on_grid(0.5*(polybounds.bottom + polybounds.top)),
        )
        ppad_m1bounds = l.bounds(mask=metal1.mask)
        ppad_polybounds = l.bounds(mask=poly.mask)
        if ppad_polybounds.left > polybounds.right:
            shape = _geo.Rect.from_rect(rect=ppad_polybounds, left=polybounds.left)
            layouter.add_wire(net=nets.i, wire=poly, shape=shape)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        bottom = comp.maxnmos_activebottom
        top = min(comp.maxnmos_activetop, ppad_m1bounds.bottom - metal1.min_width)
        chvss_m1bounds = layouter.add_wire(
            net=nets.vss, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space)
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = max(comp.maxpmos_activebottom, ppad_m1bounds.top + metal1.min_width)
        top = comp.maxpmos_activetop
        chvdd_m1bounds = layouter.add_wire(
            net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space),
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )

        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=spec.iorow_height, top=chvss_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.vss, wire=metal1, shape=shape)
        shape = _geo.Rect.from_rect(rect=chvdd_m1bounds, top=spec.cells_height)
        layouter.add_wire(net=nets.vdd, wire=metal1, shape=shape)

        x += comp.minwidth_activewithcontact + active.min_space
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        i_nactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        ndio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        i_pactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom),
        )
        pdio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=ndio_m1bounds, bottom=ndio_m1bounds.top, top=pdio_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        shape = _geo.Rect(
            left=ppad_m1bounds.left, bottom=(chvss_m1bounds.top + metal1.min_space),
            right=ndio_m1bounds.right, top=(chvdd_m1bounds.bottom - metal1.min_space),
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        bottom = ndio_m1bounds.bottom
        top = pdio_m1bounds.top
        i_m2bounds = layouter.add_wire(
            net=nets.i, wire=via1, x=x, bottom_bottom=bottom, bottom_top=top,
        ).bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i, wire=metal2, **pin_args, shape=i_m2bounds) # pyright: ignore

        # Fill implants
        if nimplant is not None:
            bb = i_nactcont_lay.bounds(mask=nimplant.mask)
            bb2 = n_i_inv_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(prim=nimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))
        if pimplant is not None:
            bb = i_pactcont_lay.bounds(mask=pimplant.mask)
            bb2 = p_i_inv_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(prim=pimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))

        #
        # IO row
        #
        active_left = 0.5*comp.min_oxactive_space
        y_iopmos_lvlshift = comp.maxiopmos_y

        # Place left source-drain contacts
        _nch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _nch_lvld_actbounds = _nch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _nch_lvld_actbounds.left
        y = comp.maxionmos_y
        nch_lvld_lay = layouter.place(object_=_nch_lvld_lay, x=x, y=y)
        nch_lvld_chbounds = nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_m1bounds = nch_lvld_lay.bounds(mask=metal1.mask)
        _pch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_actbounds = _pch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _pch_lvld_actbounds.left
        y = y_iopmos_lvlshift
        pch_lvld_lay = layouter.place(object_=_pch_lvld_lay, x=x, y=y)
        pch_lvld_chbounds = pch_lvld_lay.bounds(mask=contact.mask)
        pch_lvld_m1bounds = pch_lvld_lay.bounds(mask=metal1.mask)
        lvld_m1_lay = layouter.add_wire(
            net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_m1bounds, bottom=pch_lvld_m1bounds.bottom,
            ),
        )
        lvld_m1_bounds = lvld_m1_lay.bounds()

        poly_left = max(
            nch_lvld_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            pch_lvld_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld and p_lvld, and compute pad y placements
        _n_lvld_lay = layouter.inst_layout(
            inst=insts.n_lvld, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_polybounds = _n_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_polybounds.left
        y = comp.maxionmos_y
        n_lvld_lay = layouter.place(_n_lvld_lay, x=x, y=y)
        n_lvld_actbounds = n_lvld_lay.bounds(mask=active.mask)
        n_lvld_polybounds = n_lvld_lay.bounds(mask=poly.mask)
        _p_lvld_lay = layouter.inst_layout(
            inst=insts.p_lvld, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_polybounds = _p_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_lay = layouter.place(_p_lvld_lay, x=x, y=y)
        p_lvld_actbounds = p_lvld_lay.bounds(mask=active.mask)
        p_lvld_polybounds = p_lvld_lay.bounds(mask=poly.mask)
        w = cast(_ckt._PrimitiveInstance, insts.p_lvld).params["w"]
        p_lvld_pad_bottom = (
            y_iopmos_lvlshift + 0.5*w
            + tech.computed.min_space(active, poly)
        )
        p_lvld_pad_top = (
            p_lvld_pad_bottom + comp.minwidth4ext_polywithcontact
        )
        p_lvld_n_pad_bottom = p_lvld_pad_top + poly.min_space

        # Place mid source-drain contacts
        _lvlshift_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _lvlshift_chvss_chbounds = _lvlshift_chiovss_lay.bounds(mask=contact.mask)
        x = (
            n_lvld_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _lvlshift_chvss_chbounds.left
        )
        y = comp.maxionmos_y
        lvlshit_chiovss_lay = layouter.place(object_=_lvlshift_chiovss_lay, x=x, y=y)
        lvlshift_chiovss_chbounds = lvlshit_chiovss_lay.bounds(mask=contact.mask)
        lvlshift_chiovss_m1bounds = lvlshit_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovss_m1bounds, top=spec.iorow_height,
            ),
        )
        _lvlshift_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact, bottom_height=iopmos_lvlshift_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            top_enclosure=chm1_wideenc,
        )
        _lvlshift_chiovdd_chbounds = _lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        x = (
            p_lvld_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _lvlshift_chiovdd_chbounds.left
        )
        y = y_iopmos_lvlshift
        lvlshift_chiovdd_lay = layouter.place(object_=_lvlshift_chiovdd_lay, x=x, y=y)
        lvlshift_chiovdd_chbounds = lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        lvlshift_chiovdd_m1bounds = lvlshift_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovdd_m1bounds, bottom=0.0,
            ),
        )

        poly_left = max(
            lvlshift_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            lvlshift_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld_n and p_lvld_n
        _n_lvld_n_lay = layouter.inst_layout(
            inst=insts.n_lvld_n, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_n_polybounds = _n_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_n_polybounds.left
        y = comp.maxionmos_y
        n_lvld_n_lay = layouter.place(object_=_n_lvld_lay, x=x, y=y)
        n_lvld_n_actbounds = n_lvld_n_lay.bounds(mask=active.mask)
        n_lvld_n_polybounds = n_lvld_n_lay.bounds(mask=poly.mask)
        _p_lvld_n_lay = layouter.inst_layout(
            inst=insts.p_lvld_n, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_n_polybounds = _p_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_n_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_n_lay = layouter.place(object_=_p_lvld_n_lay, x=x, y=y)
        p_lvld_n_polybounds = p_lvld_n_lay.bounds(mask=poly.mask)

        # Place right source-drain contacts
        _nch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
        )
        _nch_lvld_n_chbounds = _nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_n_x = (
            n_lvld_n_polybounds.right + spec.nmos.computed.min_contactgate_space
            - _nch_lvld_n_chbounds.left
        )
        nch_lvld_n_y = comp.maxionmos_y
        nch_lvld_n_lay = layouter.place(
            object_=_nch_lvld_n_lay, x=nch_lvld_n_x, y=nch_lvld_n_y,
        )
        nch_lvld_n_actbounds = nch_lvld_n_lay.bounds(mask=active.mask)
        nch_lvld_n_m1bounds = nch_lvld_n_lay.bounds(mask=metal1.mask)
        _pch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_n_chbounds = _pch_lvld_n_lay.bounds(mask=contact.mask)
        pch_lvld_n_x = (
            p_lvld_n_polybounds.right + spec.pmos.computed.min_contactgate_space
            - _pch_lvld_n_chbounds.left
        )
        pch_lvld_n_y = y_iopmos_lvlshift
        pch_lvld_n_lay = layouter.place(
            object_=_pch_lvld_n_lay, x=pch_lvld_n_x, y=pch_lvld_n_y
        )
        pch_lvld_n_actbounds = pch_lvld_n_lay.bounds(mask=active.mask)
        pch_lvld_n_m1bounds = pch_lvld_n_lay.bounds(mask=metal1.mask)
        lvld_n_m1_lay = layouter.add_wire(
            net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_n_m1bounds, bottom=pch_lvld_n_m1bounds.bottom,
            ),
        )
        lvld_n_m1_bounds = lvld_n_m1_lay.bounds()
        # Add manual implant rectangle
        if iopimplant is not None:
            bb1 = pch_lvld_lay.bounds(mask=iopimplant.mask)
            bb2 = pch_lvld_n_lay.bounds(mask=iopimplant.mask)
            if iopimplant is not None:
                layouter.add_portless(prim=iopimplant, shape=_geo.Rect(
                    left=bb1.left, bottom=bb1.bottom,
                    right=bb2.right, top=bb1.top,
                ))

        # Poly pads for nmoses of the level shifter
        _n_lvld_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_ppad_polybounds = _n_lvld_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_ppad_chbounds = _n_lvld_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_ppad_m1bounds = _n_lvld_ppad_lay.bounds(mask=metal1.mask)
        _n_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_n_ppad_polybounds = _n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_n_ppad_chbounds = _n_lvld_n_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_n_ppad_m1bounds = _n_lvld_n_ppad_lay.bounds(mask=metal1.mask)

        n_lvld_ppad_x = max(
            n_lvld_polybounds.left - _n_lvld_ppad_polybounds.left,
            n_lvld_polybounds.right - _n_lvld_ppad_polybounds.right,
            lvld_m1_bounds.right + metal1.min_space - _n_lvld_ppad_m1bounds.left,
        )
        n_lvld_ppad_y = min(
            n_lvld_actbounds.bottom - min_actpoly_space - _n_lvld_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_ppad_y = min(
                n_lvld_ppad_y,
                n_lvld_actbounds.bottom - min_actch_space - _n_lvld_ppad_chbounds.top,
            )
        n_lvld_n_ppad_x = min(
            n_lvld_n_polybounds.left - _n_lvld_n_ppad_polybounds.left,
            n_lvld_n_polybounds.right - _n_lvld_n_ppad_polybounds.right,
            lvld_n_m1_bounds.left - metal1.min_space - _n_lvld_n_ppad_m1bounds.right,
        )
        n_lvld_n_ppad_y = min(
            n_lvld_n_actbounds.bottom - min_actpoly_space - _n_lvld_n_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_n_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_n_ppad_y = min(
                n_lvld_n_ppad_y,
                n_lvld_n_actbounds.bottom - min_actch_space - _n_lvld_n_ppad_chbounds.top,
            )

        n_lvld_ppad_lay = layouter.place(
            object_=_n_lvld_ppad_lay, x=n_lvld_ppad_x, y=n_lvld_ppad_y,
        )
        n_lvld_ppad_polybounds = n_lvld_ppad_lay.bounds(mask=poly.mask)
        n_lvld_ppad_m1bounds = n_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_polybounds, bottom=n_lvld_ppad_polybounds.bottom,
        ))
        n_lvld_n_ppad_lay = layouter.place(
            object_=_n_lvld_n_ppad_lay, x=n_lvld_n_ppad_x, y=n_lvld_n_ppad_y,
        )
        n_lvld_n_ppad_polybounds = n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        n_lvld_n_ppad_m1bounds = n_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_polybounds, bottom=n_lvld_n_ppad_polybounds.bottom,
        ))

        # via1 pads on the poly pads
        # draw two vias to make sure metal1 area is big enough
        _n_lvld_via_lay = layouter.wire_layout(net=nets.i, wire=via1, rows=2)
        _n_lvld_via_m1bounds = _n_lvld_via_lay.bounds(mask=metal1.mask)
        n_lvld_via_x = n_lvld_ppad_m1bounds.left - _n_lvld_via_m1bounds.left
        n_lvld_via_y = n_lvld_ppad_m1bounds.top - _n_lvld_via_m1bounds.top
        n_lvld_via_lay = layouter.place(
            object_=_n_lvld_via_lay, x=n_lvld_via_x, y=n_lvld_via_y,
        )
        n_lvld_via_m2bounds = n_lvld_via_lay.bounds(mask=metal2.mask)
        o = _geo.Point(
            x=n_lvld_via_m2bounds.center.x,
            y=n_lvld_via_m2bounds.top,
        )
        shape = _geo.MultiPath(
            _geo.Start(point=o, width=n_lvld_via_m2bounds.width),
            _geo.GoUp(dist=(i_m2bounds.bottom - o.y)),
            _geo.GoRight(dist=(i_m2bounds.right - o.x)),
        )
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=shape)
        _n_lvld_n_via_lay = layouter.wire_layout(net=nets.i, wire=via1, rows=2)
        _n_lvld_n_via_m1bounds = _n_lvld_n_via_lay.bounds(mask=metal1.mask)
        n_lvld_n_via_x = n_lvld_n_ppad_m1bounds.right - _n_lvld_n_via_m1bounds.right
        n_lvld_n_via_y = n_lvld_n_ppad_m1bounds.top - _n_lvld_n_via_m1bounds.top
        n_lvld_n_via_lay = layouter.place(
            object_=_n_lvld_n_via_lay, x=n_lvld_n_via_x, y=n_lvld_n_via_y,
        )
        n_lvld_n_via_m2bounds = n_lvld_n_via_lay.bounds(mask=metal2.mask)
        o = _geo.Point(
            x=n_lvld_n_via_m2bounds.center.x,
            y=n_lvld_n_via_m2bounds.bottom,
        )
        shape = _geo.MultiPath(
            _geo.Start(point=o, width=n_lvld_n_via_m2bounds.width),
            _geo.GoDown(dist=n_lvld_n_via_m2bounds.height),
            _geo.GoLeft(dist=(o.x - i_n_m2bounds.center.x)),
            _geo.GoUp(dist=(
                i_n_m2bounds.bottom - n_lvld_n_via_m2bounds.bottom + n_lvld_n_via_m2bounds.height
            )),
        )
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=shape)

        # Poly pads for the pmoses of the level shifter
        _p_lvld_ppad_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_ppad_polybounds = _p_lvld_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_ppad_chbounds = _p_lvld_ppad_lay.bounds(mask=contact.mask)
        _p_lvld_ppad_m1bounds = _p_lvld_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_ppad_x = max(
            lvld_m1_bounds.right + metal1.min_space - _p_lvld_ppad_m1bounds.left,
            p_lvld_polybounds.left - _p_lvld_ppad_polybounds.left,
            p_lvld_polybounds.right - _p_lvld_ppad_polybounds.right,
        )
        p_lvld_ppad_y = max(
            p_lvld_actbounds.top + min_actpoly_space - _p_lvld_ppad_polybounds.bottom,
            lvlshift_chiovdd_m1bounds.top + metal1.min_space - _p_lvld_ppad_m1bounds.bottom,
        )
        if min_actch_space is not None:
            p_lvld_ppad_y = max(
                p_lvld_ppad_y,
                p_lvld_actbounds.top + min_actch_space - _p_lvld_ppad_chbounds.bottom
            )
        p_lvld_ppad_lay = layouter.place(
            object_=_p_lvld_ppad_lay, x=p_lvld_ppad_x, y=p_lvld_ppad_y,
        )
        p_lvld_ppad_polybounds = p_lvld_ppad_lay.bounds(mask=poly.mask)
        p_lvld_ppad_m1bounds = p_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_polybounds, top=p_lvld_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_ppad_m1bounds, right=lvld_n_m1_bounds.right,
        ))

        _p_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_n_ppad_polybounds = _p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_n_ppad_m1bounds = _p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_n_ppad_x = min(
            lvld_n_m1_bounds.left - metal1.min_space - _p_lvld_n_ppad_m1bounds.right,
            p_lvld_n_polybounds.left - _p_lvld_n_ppad_polybounds.left,
            p_lvld_n_polybounds.right - _p_lvld_n_ppad_polybounds.right,
        )
        p_lvld_n_ppad_y = (
            p_lvld_ppad_m1bounds.top + metal1.min_space - _p_lvld_n_ppad_m1bounds.bottom
        )
        p_lvld_n_ppad_lay = layouter.place(
            object_=_p_lvld_n_ppad_lay, x=p_lvld_n_ppad_x, y=p_lvld_n_ppad_y,
        )
        p_lvld_n_ppad_polybounds = p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        p_lvld_n_ppad_m1bounds = p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_polybounds, top=p_lvld_n_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_ppad_m1bounds, left=lvld_m1_bounds.left,
        ))

        # Output buffer
        active_left = (
            max(nch_lvld_n_actbounds.right, pch_lvld_n_actbounds.right)
            + comp.min_oxactive_space
        )

        # Place left source-drain contacts
        _obuf_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _obuf_chiovss_actbounds = _obuf_chiovss_lay.bounds(mask=active.mask)
        obuf_chiovss_x = active_left - _obuf_chiovss_actbounds.left
        obuf_chiovss_y = comp.maxionmos_y
        obuf_chiovss_lay = layouter.place(
            object_=_obuf_chiovss_lay, x=obuf_chiovss_x, y=obuf_chiovss_y,
        )
        obuf_chiovss_chbounds = obuf_chiovss_lay.bounds(mask=contact.mask)
        obuf_chiovss_m1bounds = obuf_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovss_m1bounds, top=spec.iorow_height,
        ))
        _obuf_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact,
            bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
        )
        _obuf_chiovdd_actbounds = _obuf_chiovdd_lay.bounds(mask=active.mask)
        obuf_chiovdd_x = active_left - _obuf_chiovdd_actbounds.left
        obuf_chiovdd_y = comp.maxiopmos_y
        obuf_chiovdd_lay = layouter.place(
            object_=_obuf_chiovdd_lay, x=obuf_chiovdd_x, y=obuf_chiovdd_y,
        )
        obuf_chiovdd_chbounds = obuf_chiovdd_lay.bounds(mask=contact.mask)
        obuf_chiovdd_m1bounds = obuf_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovdd_m1bounds, bottom=0.0,
        ))

        poly_left = max(
            obuf_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            obuf_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Output buffer ionmos+iopmos
        x = obuf_chiovss_m1bounds.center.x + max(
            comp.minionmos_contactgatepitch,
            comp.miniopmos_contactgatepitch,
        )
        _n_obuf_lay = layouter.inst_layout(inst=insts.n_lvld_n_inv)
        _n_obuf_polybounds = _n_obuf_lay.bounds(mask=poly.mask)
        n_obuf_x = poly_left - _n_obuf_polybounds.left
        n_obuf_y = comp.maxionmos_y
        n_obuf_lay = layouter.place(
            object_=_n_obuf_lay, x=n_obuf_x, y=n_obuf_y
        )
        n_obuf_polybounds = n_obuf_lay.bounds(mask=poly.mask)
        _p_obuf_lay = layouter.inst_layout(inst=insts.p_lvld_n_inv)
        _p_obuf_polybounds = _p_obuf_lay.bounds(mask=poly.mask)
        p_obuf_x = poly_left - _p_obuf_polybounds.left
        p_obuf_y = comp.maxiopmos_y
        p_obuf_lay = layouter.place(object_=_p_obuf_lay, x=p_obuf_x, y=p_obuf_y)
        p_obuf_polybounds = p_obuf_lay.bounds(mask=poly.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_obuf_polybounds, bottom=p_obuf_polybounds.top,
        ))

        # poly pad
        _obuf_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _obuf_ppad_polybounds = _obuf_ppad_lay.bounds(mask=poly.mask)
        obuf_ppad_x = min(
            n_obuf_polybounds.left - _obuf_ppad_polybounds.left,
            n_obuf_polybounds.right - _obuf_ppad_polybounds.right,
        )
        obuf_ppad_y = tech.on_grid(0.5*(n_obuf_polybounds.bottom + p_obuf_polybounds.top))
        obuf_ppad_lay = layouter.place(object_=_obuf_ppad_lay, x=obuf_ppad_x, y=obuf_ppad_y)
        obuf_ppad_m1bounds = obuf_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_ppad_m1bounds, left=nch_lvld_n_m1bounds.left,
        ))

        # Place right source-drain contacts
        _nch_o_lay = layouter.wire_layout(
            net=nets.o, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _nch_o_chbounds = _nch_o_lay.bounds(mask=contact.mask)
        nch_o_x = (
            n_obuf_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _nch_o_chbounds.left
        )
        nch_o_y = comp.maxionmos_y
        nch_o_lay = layouter.place(object_=_nch_o_lay, x=nch_o_x, y=nch_o_y)
        nch_o_m1bounds = nch_o_lay.bounds(mask=metal1.mask)
        _pch_o_lay = layouter.wire_layout(
            net=nets.o, well_net=nets.iovdd, wire=contact, bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _pch_o_chbounds = _pch_o_lay.bounds(mask=contact.mask)
        pch_o_x = (
            p_obuf_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _pch_o_chbounds.left
        )
        pch_o_y = comp.maxiopmos_y
        pch_o_lay = layouter.place(object_=_pch_o_lay, x=pch_o_x, y=pch_o_y)
        pch_o_m1bounds = pch_o_lay.bounds(mask=metal1.mask)
        m1_o_lay = layouter.add_wire(net=nets.o, wire=metal1, shape=_geo.Rect.from_rect(
            rect=nch_o_m1bounds, bottom=pch_o_m1bounds.bottom,
        ))
        m1_o_bounds = m1_o_lay.bounds()
        _via1_o_lay = layouter.wire_layout(
            net=nets.o, wire=via1, bottom_height=m1_o_bounds.height
        )
        _via1_o_m1bounds = _via1_o_lay.bounds(mask=metal1.mask)
        via1_o_x = m1_o_bounds.left - _via1_o_m1bounds.left
        via1_o_y = m1_o_bounds.bottom - _via1_o_m1bounds.bottom
        via1_o_lay = layouter.place(object_=_via1_o_lay, x=via1_o_x, y=via1_o_y)
        via1_o_m2bounds = via1_o_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.o, wire=metal2, **pin_args, shape=via1_o_m2bounds) # pyright: ignore

        cells_right = layout.bounds(mask=active.mask).right + 0.5*comp.min_oxactive_space

        # fill implants
        if nimplant is not None:
            bb = n_obuf_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(
                prim=nimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )
        if pimplant is not None:
            bb = p_obuf_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(
                prim=pimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )

        #
        # Set boundary
        #

        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cells_right, top=spec.cells_height,
        )

        #
        # Well/bulk contacts
        #

        l1 = layouter.add_wire(
            net=nets.iovdd, wire=contact, well_net=nets.iovdd,
            bottom=active, bottom_implant=ionimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=0, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.iovdd, wire=active, implant=ionimplant,
            well_net=nets.iovdd, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        nw_enc = spec.iopmos.computed.min_active_well_enclosure.max()
        shape = _geo.Rect(
            left=-nw_enc,
            bottom=min(bb1.bottom, bb2.bottom),
            right=(cells_right + nw_enc),
            top=spec.iorow_nwell_height,
        )
        layouter.add_wire(net=nets.iovdd, wire=nwell, shape=shape)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.metal[1].minwidth_updown,
        )

        layouter.add_wire(
            net=nets.vss, wire=contact, bottom=active,
            bottom_implant=pimplant, top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.iorow_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        layouter.add_wire(
            net=nets.vss, wire=active, implant=pimplant,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=nets.vss, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.metal[1].minwidth_updown,
        )

        l1 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=contact, bottom=active,
            bottom_implant=nimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.cells_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active,
            implant=nimplant, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        layouter.add_wire(
            net=nets.vdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.metal[1].minwidth_updown,
        )
        shape = _geo.Rect(
            left=min(bb1.left, bb2.left),
            bottom=(spec.cells_height - spec.corerow_nwell_height),
            right=max(bb1.right, bb2.right),
            top=max(bb1.top, bb2.top),
        )
        layouter.add_wire(net=nets.vdd, wire=nwell, shape=shape)

        # Thick oxide
        assert comp.ionmos.gate.oxide is not None
        layouter.add_portless(prim=comp.ionmos.gate.oxide, shape=_geo.Rect(
            left=-actox_enc, bottom=comp.io_oxidebottom,
            right=(cells_right + actox_enc), top=comp.io_oxidetop,
        ))


class _LevelDown(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        circuit = self.new_circuit()

        # inverter with 5V gates
        n_hvinv = circuit.instantiate(
            spec.ionmos, name="n_hvinv", w=comp.maxionmoscore_w,
        )
        p_hvinv = circuit.instantiate(
            spec.iopmos, name="p_hvinv", w=comp.maxiopmoscore_w,
        )

        # second inverter, keep same w
        n_lvinv = circuit.instantiate(
            spec.nmos, name="n_lvinv", w=comp.maxnmos_w,
        )
        p_lvinv = circuit.instantiate(
            spec.pmos, name="p_lvinv", w=comp.maxpmos_w,
        )

        prot = circuit.instantiate(fab.get_cell("SecondaryProtection"), name="secondprot")

        # Create the nets
        circuit.new_net(name="vdd", external=True, childports=(
            p_hvinv.ports.sourcedrain1, p_hvinv.ports.bulk,
            p_lvinv.ports.sourcedrain2, p_lvinv.ports.bulk,
        ))
        circuit.new_net(name="vss", external=True, childports=(
            n_hvinv.ports.sourcedrain1, n_hvinv.ports.bulk,
            n_lvinv.ports.sourcedrain2, n_lvinv.ports.bulk,
        ))
        circuit.new_net(name="iovdd", external=True, childports=(
            prot.ports.iovdd,
        ))
        circuit.new_net(name="iovss", external=True, childports=(
            prot.ports.iovss,
        ))
        circuit.new_net(name="pad", external=True, childports=(
            prot.ports.pad,
        ))
        circuit.new_net(name="padres", external=False, childports=(
            prot.ports.core,
            n_hvinv.ports.gate, p_hvinv.ports.gate,
        ))
        circuit.new_net(name="padres_n", external=False, childports=(
            n_hvinv.ports.sourcedrain2, p_hvinv.ports.sourcedrain2,
            n_lvinv.ports.gate, p_lvinv.ports.gate,
        ))
        circuit.new_net(name="core", external=True, childports=(
            n_lvinv.ports.sourcedrain1, p_lvinv.ports.sourcedrain1,
        ))

    def _create_layout(self):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        circuit = self.circuit
        insts = circuit.instances
        nets = circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        oxide = comp.oxide
        nwell = comp.nwell
        poly = comp.poly
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        contact = comp.contact
        chm1_enclosure = contact.min_top_enclosure[0]
        via1 = comp.vias[1]

        layouter = self.new_circuitlayouter()
        layout = self.layout

        left = 0.5*comp.active.min_space

        # Place instances
        #

        # transistors + contacts
        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.n_lvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        act_left = l.bounds(mask=active.mask).left
        l_n_lvinv = layouter.place(l, x=(left - act_left), y=comp.maxnmos_y)

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.p_lvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        act_left = l.bounds(mask=active.mask).left
        l_p_lvinv = layouter.place(l, x=(left - act_left), y=comp.maxpmos_y)

        rect1 = l_n_lvinv.bounds(mask=active.mask)
        rect2 = l_p_lvinv.bounds(mask=active.mask)
        ox_left = (
            max(rect1.right, rect2.right)
            + tech.computed.min_space(oxide, active)
        )

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.n_hvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        ox_left2 = l.bounds(mask=oxide.mask).left
        l_n_hvinv = layouter.place(l, x=(ox_left - ox_left2), y=comp.maxionmoscore_y)

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.p_hvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        ox_left2 = l.bounds(mask=oxide.mask).left
        l_p_hvinv = layouter.place(l, x=(ox_left - ox_left2), y=comp.maxiopmoscore_y)

        # secondary protection
        l = layouter.inst_layout(inst=insts.secondprot)
        _actvdd_bounds = l.bounds(net=nets.iovdd, mask=active.mask)
        l_prot = layouter.place(
            l, x=0,
            y=(-_actvdd_bounds.top + 0.5*comp.minwidth_activewithcontact),
        )

        # Cell boundary
        #
        secprot = fab.get_cell("SecondaryProtection")
        assert secprot.layout.boundary is not None
        cell_width = tech.on_grid(
            max(
                layout.bounds(mask=active.mask).right + 0.5*active.min_space,
                secprot.layout.boundary.right,
            ),
            mult=2, rounding="ceiling",
        )
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cell_width, top=spec.cells_height,
        )
        x_mid = 0.5*cell_width

        # Connect nets
        #

        # core
        net = nets.core # Output of lv inverter
        rect1 = l_n_lvinv.bounds(mask=metal1.mask, net=net)
        rect2 = l_p_lvinv.bounds(mask=metal1.mask, net=net)
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.bottom,
            right=max(rect1.right, rect2.right), top=rect2.top,
        ))

        # pad
        net = nets.pad
        rect = l_prot.bounds(net=net, mask=metal2pin.mask)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=rect)

        # padres
        net = nets.padres
        rect1 = l_n_hvinv.bounds(mask=poly.mask)
        rect2 = l_p_hvinv.bounds(mask=poly.mask)
        assert rect1.top < rect2.bottom
        layouter.add_wire(wire=poly, net=nets.padres, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.top,
            right=max(rect1.right, rect2.right), top=rect2.bottom,
        ))
        l = layouter.wire_layout(
            net=net, wire=contact, bottom=poly, top_enclosure=chm1_enclosure.wide(),
        )
        rect3 = l.bounds(mask=poly.mask)
        x = max(rect1.right, rect2.right) - rect3.right
        y = tech.on_grid(0.5*(rect1.top + rect2.bottom))
        l_hv_ch = layouter.place(l, x=x, y=y)

        # y = y
        l = layouter.wire_layout(net=net, wire=via1, bottom_enclosure="wide")
        rect1 = l_hv_ch.bounds(mask=metal1.mask)
        rect2 = l.bounds(mask=metal1.mask)
        x = rect1.right - rect2.right
        l_hv_via1 = layouter.place(l, x=x, y=y)

        rect1 = l_hv_via1.bounds(mask=metal2.mask)
        rect2 = l_prot.bounds(net=net, mask=metal2pin.mask)
        assert rect1.left >= rect2.left
        l_m2_padres = layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=rect1, bottom=rect2.top,
        ))

        # padres_n
        net = nets.padres_n # Output of hv inverter
        rect1 = l_n_lvinv.bounds(mask=poly.mask)
        rect2 = l_p_lvinv.bounds(mask=poly.mask)
        assert rect1.top < rect2.bottom
        layouter.add_wire(wire=poly, net=nets.padres_n, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.top,
            right=max(rect1.right, rect2.right), top=rect2.bottom,
        ))
        l = layouter.wire_layout(
            net=net, wire=contact, bottom=poly, top_enclosure=chm1_enclosure.wide(),
        )
        rect3 = l.bounds(mask=poly.mask)
        x = max(rect1.right, rect2.right) - rect3.left
        y = tech.on_grid(0.5*(rect1.top + rect2.bottom))
        l_lv_ch = layouter.place(object_=l, x=x, y=y)

        rect1 = l_lv_ch.bounds(mask=metal1.mask)
        l = layouter.wire_layout(net=net, wire=via1, bottom_enclosure="wide")
        rect2 = l.bounds(mask=metal1.mask)
        x = rect1.right - rect2.right
        # y = y
        l_lv_via1 = layouter.place(l, x=x, y=y)

        rect1 = l_n_hvinv.bounds(mask=metal1.mask, net=net)
        rect2 = l_p_hvinv.bounds(mask=metal1.mask, net=net)
        left = min(rect1.right, rect2.right)
        right = left + metal1.min_space
        bottom = rect1.bottom
        top = rect2.top
        l_hv_m1 = layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))

        m1rect1 = l_hv_m1.bounds(mask=metal1.mask)
        m2rect1 = l_lv_via1.bounds(mask=metal2.mask)
        m2rect2 = l_m2_padres.bounds(mask=metal2.mask)
        l = layouter.wire_layout(net=net, wire=via1)
        m1rect2 = l.bounds(mask=metal1.mask)
        m2rect3 = l.bounds(mask=metal2.mask)
        x = m1rect1.left - m1rect2.left
        y = (m2rect2.top + metal2.min_space) - m2rect3.bottom
        l_via1 = layouter.place(l, x=x, y=y)
        m2rect3 = l_via1.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=m2rect1, top=m2rect3.top,
        ))
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=m2rect3, left=m2rect1.left,
        ))

        # Increase metal1 area for padres & padres_n poly pad connections
        rect1 = l_lv_via1.bounds(mask=metal1.mask)
        rect2 = l_hv_via1.bounds(mask=metal1.mask)
        mid = 0.5*(rect1.right + rect2.left)
        right = tech.on_grid(mid - 0.5*metal1.min_space, rounding="floor")
        shape = _geo.Rect.from_rect(rect=rect1, right=right)
        layouter.add_wire(net=nets.padres_n, wire=metal1, shape=shape)
        left = tech.on_grid(mid + 0.5*metal1.min_space, rounding="ceiling")
        shape = _geo.Rect.from_rect(rect=rect2, left=left)
        layouter.add_wire(net=nets.padres, wire=metal1, shape=shape)

        # vss
        net = nets.vss
        layouter.add_wire(
            net=net, wire=contact, bottom=active,
            bottom_implant=pimplant, top_enclosure=comp.chm1_enclosure.wide(),
            x=x_mid, bottom_width=(cell_width - contact.min_space),
            y=spec.iorow_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        layouter.add_wire(
            net=net, wire=active, implant=pimplant,
            x=x_mid, width=cell_width,
            y=spec.iorow_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=net, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=spec.iorow_height, height=comp.metal[1].minwidth_updown,
        )

        rect1 = l_n_lvinv.bounds(net=net, mask=metal1.mask)
        rect2 = l_n_hvinv.bounds(net=net, mask=metal1.mask)
        layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=rect1.left, bottom=spec.iorow_height,
            right=rect2.right, top=min(rect1.top, rect2.top),
        ))

        # vdd
        net = nets.vdd
        l = layouter.add_wire(
            net=net, well_net=net, wire=contact, bottom=active,
            bottom_implant=nimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=x_mid, bottom_width=(cell_width - contact.min_space),
            y=spec.cells_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        l = layouter.add_wire(
            net=net, well_net=net, wire=active,
            implant=nimplant, well=nwell,
            x=x_mid, width=cell_width,
            y=spec.cells_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=net, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=spec.cells_height, height=comp.metal[1].minwidth_updown,
        )
        strap_vdd_nwellbounds = l.bounds(mask=nwell.mask)
        shape = _geo.Rect.from_rect(
            rect=strap_vdd_nwellbounds,
            bottom=(spec.cells_height - spec.corerow_nwell_height),
        )
        layouter.add_wire(net=net, wire=nwell, shape=shape)

        rect1 = l_p_lvinv.bounds(net=net, mask=metal1.mask)
        rect2 = l_p_hvinv.bounds(net=net, mask=metal1.mask)
        layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=rect1.left, bottom=max(rect1.bottom, rect2.bottom),
            right=rect2.right, top=spec.cells_height,
        ))

        # iovss
        net = nets.iovss
        rect = l_prot.bounds(net=net, mask=metal2pin.mask)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=rect)

        # iovdd
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=0, height=comp.metal[1].minwidth_updown,
        )

        # Netless polygons
        #

        # Join transistor implant layers
        if nimplant is not None:
            n_lvinv_implbounds = l_n_lvinv.bounds(mask=nimplant.mask)
            n_hvinv_implbounds = l_n_hvinv.bounds(mask=nimplant.mask)
            shape = _geo.Rect.from_rect(rect=n_lvinv_implbounds, right=n_hvinv_implbounds.right)
            layouter.add_portless(prim=nimplant, shape=shape)

        if pimplant is not None:
            p_lvinv_implbounds = l_p_lvinv.bounds(mask=pimplant.mask)
            p_hvinv_implbounds = l_p_hvinv.bounds(mask=pimplant.mask)
            shape = _geo.Rect.from_rect(rect=p_lvinv_implbounds, right=p_hvinv_implbounds.right)
            layouter.add_portless(prim=pimplant, shape=shape)

        # Join transistor oxide layer
        bounds = layout.bounds(mask=oxide.mask)
        layouter.add_portless(prim=oxide, shape=bounds)


class _GateLevelUp(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec

        levelup = fab.get_cell("LevelUp")

        ckt = self.new_circuit()

        ngatelu = ckt.instantiate(levelup, name="ngate_levelup")
        pgatelu = ckt.instantiate(levelup, name="pgate_levelup")

        ckt.new_net(name="vdd", external=True, childports=(
            ngatelu.ports.vdd, pgatelu.ports.vdd,
        ))
        ckt.new_net(name="vss", external=True, childports=(
            ngatelu.ports.vss, pgatelu.ports.vss,
        ))
        ckt.new_net(name="iovdd", external=True, childports=(
            ngatelu.ports.iovdd, pgatelu.ports.iovdd,
        ))

        ckt.new_net(name="core", external=True, childports=(
            ngatelu.ports.i, pgatelu.ports.i,
        ))
        ckt.new_net(name="ngate", external=True, childports=(ngatelu.ports.o))
        ckt.new_net(name="pgate", external=True, childports=(pgatelu.ports.o))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        insts = self.circuit.instances
        nets = self.circuit.nets

        levelup = fab.get_cell("LevelUp")
        assert levelup.layout.boundary is not None

        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        layouter = self.new_circuitlayouter()
        fab = layouter.fab
        layout = self.layout

        # Place the cells
        x_lu = 0.0
        y_lu = -levelup.layout.boundary.top - spec.levelup_core_space
        l_ngatelu = layouter.place(insts.ngate_levelup, x=x_lu, y=y_lu)
        ngatelu_d_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.core)
        ngatelu_ngate_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate)
        ngatelu_bb = l_ngatelu.boundary
        assert ngatelu_bb is not None

        x_lu = ngatelu_bb.right
        l_pgatelu = layouter.place(insts.pgate_levelup, x=x_lu, y=y_lu)
        pgatelu_d_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.core)
        pgatelu_pgate_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate)
        pgatelu_bb = l_pgatelu.boundary
        assert pgatelu_bb is not None

        # Set the boundary
        cell_bb = _geo.Rect.from_rect(rect=ngatelu_bb, right=pgatelu_bb.right)
        layout.boundary = cell_bb

        # Connect the nets
        # core
        net = nets.core

        shape = _geo.Rect.from_rect(rect=ngatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=pgatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=ngatelu_d_m2pinbounds.left, bottom=cell_bb.top,
            right=pgatelu_d_m2pinbounds.right, top=(cell_bb.top + 2*metal2.min_width),
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=shape)

        # ngate
        net = nets.ngate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=ngatelu_ngate_m2pinbounds,
        )

        # pgate
        net = nets.pgate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=pgatelu_pgate_m2pinbounds,
        )

        # vss
        net = nets.vss
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # vdd
        net = nets.vdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # iovdd
        net = nets.iovdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)


class _GateLevelUpInv(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec

        levelupinv = fab.get_cell("LevelUpInv")

        ckt = self.new_circuit()

        ngatelu = ckt.instantiate(levelupinv, name="ngate_levelup")
        pgatelu = ckt.instantiate(levelupinv, name="pgate_levelup")

        ckt.new_net(name="vdd", external=True, childports=(
            ngatelu.ports.vdd, pgatelu.ports.vdd,
        ))
        ckt.new_net(name="vss", external=True, childports=(
            ngatelu.ports.vss, pgatelu.ports.vss,
        ))
        ckt.new_net(name="iovdd", external=True, childports=(
            ngatelu.ports.iovdd, pgatelu.ports.iovdd,
        ))

        ckt.new_net(name="core", external=True, childports=(
            ngatelu.ports.i, pgatelu.ports.i,
        ))
        ckt.new_net(name="ngate", external=True, childports=(ngatelu.ports.o))
        ckt.new_net(name="pgate", external=True, childports=(pgatelu.ports.o))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        insts = self.circuit.instances
        nets = self.circuit.nets

        levelup = fab.get_cell("LevelUp")
        assert levelup.layout.boundary is not None

        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        layouter = self.new_circuitlayouter()
        fab = layouter.fab
        layout = self.layout

        # Place the cells
        x_lu = 0.0
        y_lu = -levelup.layout.boundary.top - spec.levelup_core_space
        l_ngatelu = layouter.place(insts.ngate_levelup, x=x_lu, y=y_lu)
        ngatelu_d_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.core)
        ngatelu_ngate_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate)
        ngatelu_bb = l_ngatelu.boundary
        assert ngatelu_bb is not None

        x_lu = ngatelu_bb.right
        l_pgatelu = layouter.place(insts.pgate_levelup, x=x_lu, y=y_lu)
        pgatelu_d_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.core)
        pgatelu_pgate_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate)
        pgatelu_bb = l_pgatelu.boundary
        assert pgatelu_bb is not None

        # Set the boundary
        cell_bb = _geo.Rect.from_rect(rect=ngatelu_bb, right=pgatelu_bb.right)
        layout.boundary = cell_bb

        # Connect the nets
        # core
        net = nets.core

        shape = _geo.Rect.from_rect(rect=ngatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=pgatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=ngatelu_d_m2pinbounds.left, bottom=cell_bb.top,
            right=pgatelu_d_m2pinbounds.right, top=(cell_bb.top + 2*metal2.min_width),
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=shape)

        # ngate
        net = nets.ngate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=ngatelu_ngate_m2pinbounds,
        )

        # pgate
        net = nets.pgate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=pgatelu_pgate_m2pinbounds,
        )

        # vss
        net = nets.vss
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # vdd
        net = nets.vdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # iovdd
        net = nets.iovdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)


class _GateDecode(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        stdfab = spec.stdcellfab

        tie = stdfab.getcreate_cell(name="tie")
        inv = stdfab.getcreate_cell(name="inv_x1")
        nand = stdfab.getcreate_cell(name="nand2_x1")
        nor = stdfab.getcreate_cell(name="nor2_x1")
        levelup = fab.get_cell(name="LevelUp")

        ckt = self.new_circuit()

        tieinst = ckt.instantiate(tie, name="tieinst")
        eninv = ckt.instantiate(inv, name="en_inv")
        ngatenor = ckt.instantiate(nor, name="ngate_nor")
        ngatelu = ckt.instantiate(levelup, name="ngate_levelup")
        pgatenand = ckt.instantiate(nand, name="pgate_nand")
        pgatelu = ckt.instantiate(levelup, name="pgate_levelup")

        ckt.new_net(name="vdd", external=True, childports=(
            tieinst.ports.vdd, eninv.ports.vdd, ngatenor.ports.vdd, ngatelu.ports.vdd,
            pgatenand.ports.vdd, pgatelu.ports.vdd,
        ))
        ckt.new_net(name="vss", external=True, childports=(
            tieinst.ports.vss, eninv.ports.vss, ngatenor.ports.vss, ngatelu.ports.vss,
            pgatenand.ports.vss, pgatelu.ports.vss,
        ))
        ckt.new_net(name="iovdd", external=True, childports=(
            ngatelu.ports.iovdd, pgatelu.ports.iovdd,
        ))

        ckt.new_net(name="core", external=True, childports=(
            ngatenor.ports.i0, pgatenand.ports.i0,
        ))
        ckt.new_net(name="en", external=True, childports=(
            eninv.ports.i, pgatenand.ports.i1,
        ))
        ckt.new_net(name="en_n", external=False, childports=(
            eninv.ports.nq, ngatenor.ports.i1,
        ))
        ckt.new_net(name="ngate_core", external=False, childports=(
            ngatenor.ports.nq, ngatelu.ports.i,
        ))
        ckt.new_net(name="ngate", external=True, childports=(ngatelu.ports.o))
        ckt.new_net(name="pgate_core", external=False, childports=(
            pgatenand.ports.nq, pgatelu.ports.i,
        ))
        ckt.new_net(name="pgate", external=True, childports=(pgatelu.ports.o))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        stdfab = spec.stdcellfab
        comp = fab.computed

        insts = self.circuit.instances
        nets = self.circuit.nets

        tie = stdfab.getcreate_cell(name="tie")
        assert tie.layout.boundary is not None
        levelup = fab.get_cell("LevelUp")
        assert levelup.layout.boundary is not None
        via1 = comp.vias[1]
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        layouter = self.new_circuitlayouter()
        fab = layouter.fab
        layout = self.layout

        # Place the cells
        l_tie = layouter.place(insts.tieinst, x=0.0, y=0.0)
        assert l_tie.boundary is not None

        l_ngatenor = layouter.place(insts.ngate_nor, x=l_tie.boundary.right, y=0.0)
        assert l_ngatenor.boundary is not None
        ngatenor_d_m1pinbounds = l_ngatenor.bounds(mask=metal1pin.mask, net=nets.core)
        ngatenor_ngatecore_m1pinbounds = l_ngatenor.bounds(
            mask=metal1pin.mask, net=nets.ngate_core,
        )
        ngatenor_den_m1pinbounds = l_ngatenor.bounds(mask=metal1pin.mask, net=nets.en_n)
        l_pgatenand = layouter.place(
            insts.pgate_nand, x=l_ngatenor.boundary.right, y=0.0,
        )
        assert l_pgatenand.boundary is not None
        pgatenand_d_m1pinbounds = l_pgatenand.bounds(mask=metal1pin.mask, net=nets.core)
        pgatenand_pgatecore_m1pinbounds = l_pgatenand.bounds(
            mask=metal1pin.mask, net=nets.pgate_core,
        )
        pgatenand_de_m1pinbounds = l_pgatenand.bounds(mask=metal1pin.mask, net=nets.en)
        l_eninv = layouter.place(
            insts.en_inv, x=l_pgatenand.boundary.right, y=0.0,
        )
        assert l_eninv.boundary is not None
        eninv_de_m1pinbounds = l_eninv.bounds(mask=metal1pin.mask, net=nets.en)
        eninv_den_m1pinbounds = l_eninv.bounds(mask=metal1pin.mask, net=nets.en_n)

        y_lu = -levelup.layout.boundary.top - spec.levelup_core_space
        l_ngatelu = layouter.place(
            insts.ngate_levelup,
            x=tie.layout.boundary.right, y=y_lu,
        )
        ngatelu_ngatecore_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate_core)
        ngatelu_ngate_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate)
        assert l_ngatelu.boundary is not None
        l_pgatelu = layouter.place(
            insts.pgate_levelup, x=l_ngatelu.boundary.right, y=y_lu
        )
        pgatelu_pgatecore_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate_core)
        pgatelu_pgate_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate)
        assert l_pgatelu.boundary is not None

        # Set the boundary
        cell_left = 0.0
        cell_bottom = l_pgatelu.boundary.bottom
        cell_right = max(l_eninv.boundary.right, l_pgatelu.boundary.right)
        cell_top = l_eninv.boundary.top
        layout.boundary = _geo.Rect(
            left=cell_left, bottom=cell_bottom, right=cell_right, top=cell_top,
        )

        # Connect the nets
        # en
        net = nets.en
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        y = (
            min(pgatenand_de_m1pinbounds.top, eninv_de_m1pinbounds.top)
            - _m1bounds.top
        )
        l_via_pgatenand_de = layouter.place(
            object_=_l_via, x=pgatenand_de_m1pinbounds.center.x, y=y,
        )
        via_pgatenand_de_m2bounds = l_via_pgatenand_de.bounds(mask=metal2.mask)
        l_via_eninv_de = layouter.place(
            object_=_l_via, x=eninv_de_m1pinbounds.center.x, y=y,
        )
        via_eninv_de_m2bounds = l_via_eninv_de.bounds(mask=metal2.mask)

        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=via_pgatenand_de_m2bounds, right=via_eninv_de_m2bounds.right,
        ))
        shape = _geo.Rect(
            left=via_pgatenand_de_m2bounds.left,
            bottom=via_pgatenand_de_m2bounds.bottom,
            right=via_pgatenand_de_m2bounds.left + comp.metal[2].minwidth4ext_updown,
            top=l_eninv.boundary.top,
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2.pin, shape=shape)

        # core
        net = nets.core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        y = (min(ngatenor_d_m1pinbounds.top, pgatenand_d_m1pinbounds.top) - _m1bounds.top)
        if pgatenand_d_m1pinbounds.center.x > pgatenand_de_m1pinbounds.center.x:
            y = min(
                y,
                (
                    min(via_pgatenand_de_m2bounds.bottom, via_eninv_de_m2bounds.bottom)
                    - metal2.min_space
                    - _m2bounds.top
                ),
            )
        l_via_ngatenor_d = layouter.place(
            object_=_l_via, x=ngatenor_d_m1pinbounds.center.x, y=y,
        )
        via_ngatenor_d_m2bounds = l_via_ngatenor_d.bounds(mask=metal2.mask)
        l_via_pgatenand_d = layouter.place(
            object_=_l_via, x=pgatenand_d_m1pinbounds.center.x, y=y,
        )
        via_pgatenand_d_m2bounds = l_via_pgatenand_d.bounds(mask=metal2.mask)

        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=via_ngatenor_d_m2bounds, right=via_pgatenand_d_m2bounds.right,
        ))
        shape = _geo.Rect(
            left=via_ngatenor_d_m2bounds.left,
            bottom=via_pgatenand_d_m2bounds.bottom,
            right=via_ngatenor_d_m2bounds.left + comp.metal[2].minwidth4ext_updown,
            top=l_eninv.boundary.top,
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2.pin, shape=shape)

        # en_n
        net = nets.en_n
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        y = min(
            (
                min(
                    via_ngatenor_d_m2bounds.bottom,
                    via_pgatenand_d_m2bounds.bottom,
                    via_pgatenand_de_m2bounds.bottom,
                )
                - metal2.min_space
                - _m2bounds.top
            ),
            (
                min(ngatenor_den_m1pinbounds.top, eninv_den_m1pinbounds.top)
                - _m1bounds.top
            ),
        )
        l_via_eninv_den = layouter.place(
            object_=_l_via, x=eninv_den_m1pinbounds.center.x, y=y,
        )
        via_eninv_den_m2bounds = l_via_eninv_den.bounds(mask=metal2.mask)
        if (y + _m1bounds.bottom + _geo.epsilon) > ngatenor_den_m1pinbounds.bottom:
            l_via_ngatenor_den = layouter.place(
                object_=_l_via, x=ngatenor_den_m1pinbounds.center.x, y=y,
            )
            via_ngatenor_den_m2bounds = l_via_ngatenor_den.bounds(mask=metal2.mask)

            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_ngatenor_den_m2bounds, right=via_eninv_den_m2bounds.right,
            ))
        else:
            y2 = ngatenor_den_m1pinbounds.bottom - _m1bounds.bottom

            l_via_ngatenor_den = layouter.place(
                object_=_l_via, x=ngatenor_den_m1pinbounds.center.x, y=y2,
            )
            via_ngatenor_den_m2bounds = l_via_ngatenor_den.bounds(mask=metal2.mask)

            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_ngatenor_den_m2bounds, bottom=via_eninv_den_m2bounds.bottom,
            ))
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_eninv_den_m2bounds, left=via_ngatenor_den_m2bounds.left,
            ))

        # ngate_core
        net = nets.ngate_core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        x = ngatenor_ngatecore_m1pinbounds.left - _m1bounds.left
        y = ngatenor_ngatecore_m1pinbounds.bottom - _m1bounds.bottom
        l_via = layouter.place(object_=_l_via, x=x, y=y)
        m2bounds = l_via.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=ngatelu_ngatecore_m2pinbounds, top=m2bounds.top,
        ))
        if m2bounds.left < ngatelu_ngatecore_m2pinbounds.left:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, right=ngatelu_ngatecore_m2pinbounds.right,
            ))
        else:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, left=ngatelu_ngatecore_m2pinbounds.left,
            ))

        # pgate_core
        net = nets.pgate_core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        x = pgatenand_pgatecore_m1pinbounds.left - _m1bounds.left
        y = pgatenand_pgatecore_m1pinbounds.bottom - _m1bounds.bottom
        l_via = layouter.place(object_=_l_via, x=x, y=y)
        m2bounds = l_via.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=pgatelu_pgatecore_m2pinbounds, top=m2bounds.top,
        ))
        if m2bounds.left < pgatelu_pgatecore_m2pinbounds.left:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, right=pgatelu_pgatecore_m2pinbounds.right,
            ))
        else:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, left=pgatelu_pgatecore_m2pinbounds.left,
            ))

        # ngate
        net = nets.ngate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=ngatelu_ngate_m2pinbounds,
        )

        # pgate
        net = nets.pgate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=pgatelu_pgate_m2pinbounds,
        )

        # vss
        net = nets.vss
        lum1pin_bounds = l_pgatelu.bounds(mask=metal1pin.mask, net=net)
        invm1pin_bounds = l_eninv.bounds(mask=metal1pin.mask, net=net)
        x = lum1pin_bounds.right - 0.5*comp.metal[1].minwidth4ext_up
        y = lum1pin_bounds.top
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds1 = l_via.bounds(mask=metal2.mask)
        y = invm1pin_bounds.bottom + 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds2 = l_via.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=viam2_bounds1, top=viam2_bounds2.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=invm1pin_bounds, left=cell_left, right=cell_right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # vdd
        net = nets.vdd
        m1pin_bounds = l_eninv.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_left, right=cell_right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)
        x = cell_left + 0.5*comp.metal[1].minwidth4ext_up
        y = m1pin_bounds.bottom + 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds1 = l_via.bounds(mask=metal2.mask)
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        y = m1pin_bounds.top - 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds2 = l_via.bounds(mask=metal2.mask)
        viam1_bounds = l_via.bounds(mask=metal1.mask)
        shape = _geo.Rect.from_rect(rect=viam2_bounds1, bottom=viam2_bounds2.bottom)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=m1pin_bounds, left=viam1_bounds.left)
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        # iovdd
        net = nets.iovdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(rect=m1pin_bounds, left=cell_left, right=cell_right)
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)


class _PadOut(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory", drive: int):
        super().__init__(fab=fab, name=name)
        self.drive = drive

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        c2p = ckt.new_net(name="c2p", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatelu = ckt.instantiate(fab.get_cell("GateLevelUpInv"), name="gatelu")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatelu.ports[name]
        c2p.childports += i_gatelu.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        assert l_nclamp is not None # output IO cell has drivers
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)
        assert l_pclamp is not None # output IO cell has drivers

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # Gate levelup + interconnect
        _l_gatelu = layouter.inst_layout(inst=insts.gatelu)
        _gatelu_bb = _l_gatelu.boundary
        assert _gatelu_bb is not None
        dm2pin_bounds = _l_gatelu.bounds(net=nets.c2p, mask=metal2pin.mask)
        x = tech.on_grid(
            0.5*spec.monocell_width - 0.5*(dm2pin_bounds.left + dm2pin_bounds.right)
        )
        l_gatelu = layouter.place(
            _l_gatelu, x=x,
            y=(frame.cells_y - _gatelu_bb.bottom),
        )

        # c2p
        net = nets.c2p
        frame.promote_m2instpin_to_corepin(layouter=layouter, net=net, inst_layout=l_gatelu)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatelu.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatelu.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.pad,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=None,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadOutT = _PadOut


class _PadTriOut(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory", drive: int):
        super().__init__(fab=fab, name=name)
        self.drive = drive

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        c2p = ckt.new_net(name="c2p", external=True)
        c2p_en = ckt.new_net(name="c2p_en", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatedec = ckt.instantiate(fab.get_cell("GateDecode"), name="gatedec")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatedec.ports[name]
        c2p.childports += i_gatedec.ports.core
        c2p_en.childports += i_gatedec.ports.en

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        assert l_nclamp is not None # output IO cell has drivers
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)
        assert l_pclamp is not None # output IO cell has drivers

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # Gate decoder + interconnect
        _l_gatedec = layouter.inst_layout(inst=insts.gatedec)
        dm2pin_bounds = _l_gatedec.bounds(net=nets.c2p, mask=metal2pin.mask)
        dem2pin_bounds = _l_gatedec.bounds(net=nets.c2p_en, mask=metal2pin.mask)
        x = tech.on_grid(
            0.5*spec.monocell_width - 0.5*(dm2pin_bounds.left + dem2pin_bounds.right)
        )
        l_gatedec = layouter.place(
            _l_gatedec, x=x,
            y=(frame.cells_y - cast(_geo._Rectangular, _l_gatedec.boundary).bottom),
        )

        # c2p & c2p_en
        # bring pins to top
        for name in ("c2p", "c2p_en"):
            frame.promote_m2instpin_to_corepin(layouter=layouter, net=nets[name], inst_layout=l_gatedec)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.pad,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=None,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadTriOutT = _PadTriOut


class _PadIn(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)

        p2c = ckt.new_net(name="p2c", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=pad,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_leveldown = ckt.instantiate(fab.get_cell("LevelDown"), name="leveldown")
        for name in ("vss", "vdd", "iovss", "iovdd", "pad"):
            ckt.nets[name].childports += i_leveldown.ports[name]
        p2c.childports += i_leveldown.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        via1 = comp.vias[1]

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # LevelDown + interconnect
        _l_ld = layouter.inst_layout(inst=insts.leveldown)

        # p2c
        net = nets.p2c
        _m1pin_bounds = _l_ld.bounds(net=net, mask=metal1pin.mask)
        x = 0.5*spec.monocell_width - 0.5*(_m1pin_bounds.left + _m1pin_bounds.right)
        l_ld = layouter.place(_l_ld, x=x, y=frame.cells_y)
        frame.promote_m1instpin_to_corepin(
            layouter=layouter, net=net, inst_layout=l_ld, align="left",
        )

        # pad
        net = nets.pad
        m2pin_bounds = l_ld.bounds(net=net, mask=metal2pin.mask)
        clamp_bounds = None
        if l_pclamp is not None:
            for polygon in l_pclamp.filter_polygons(
                net=nets.pad, mask=metal2.mask, split=True,
            ):
                bounds = polygon.bounds
                if clamp_bounds is None:
                    if bounds.left >= m2pin_bounds.left:
                        clamp_bounds = bounds
                else:
                    if (
                        (bounds.left >= m2pin_bounds.left)
                        and (bounds.left < clamp_bounds.left)
                    ):
                        clamp_bounds = bounds
            assert clamp_bounds is not None, "Internal error"
            m2_width = comp.metal[2].minwidth4ext_updown
            shape = _geo.Rect(
                left=m2pin_bounds.left, bottom=(m2pin_bounds.bottom - m2_width),
                right=(clamp_bounds.left + m2_width), top=m2pin_bounds.bottom,
            )
            layouter.add_wire(net=net, wire=metal2, shape=shape)
            if (clamp_bounds.top + _geo.epsilon) < m2pin_bounds.bottom:
                shape = _geo.Rect.from_rect(
                    rect=clamp_bounds, bottom=clamp_bounds.top, top=m2pin_bounds.bottom,
                )
                layouter.add_wire(net=net, wire=metal2, shape=shape)

            l_padconn = None
        else:
            assert not frame.has_pad
            pad_m2bb = frame.pad_bb(prim=metal2)
            shape = _geo.Rect.from_rect(rect=m2pin_bounds, bottom=pad_m2bb.top)
            l_padconn = layouter.add_wire(net=net, wire=metal2, shape=shape)

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.pad,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=l_padconn,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadInT = _PadIn


class _PadInOut(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory", drive: int):
        super().__init__(fab=fab, name=name)
        self.drive = drive

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        p2c = ckt.new_net(name="p2c", external=True)
        c2p = ckt.new_net(name="c2p", external=True)
        c2p_en = ckt.new_net(name="c2p_en", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=self.drive, pad=pad,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatedec = ckt.instantiate(fab.get_cell("GateDecode"), name="gatedec")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatedec.ports[name]
        c2p.childports += i_gatedec.ports.core
        c2p_en.childports += i_gatedec.ports.en

        i_leveldown = ckt.instantiate(fab.get_cell("LevelDown"), name="leveldown")
        for name in ("vss", "vdd", "iovss", "iovdd", "pad"):
            ckt.nets[name].childports += i_leveldown.ports[name]
        p2c.childports += i_leveldown.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        via1 = comp.vias[1]

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        assert l_nclamp is not None # output IO cell has drivers
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)
        assert l_pclamp is not None # output IO cell has drivers

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # Gate decoder + interconnect
        _l_gatedec = layouter.inst_layout(inst=insts.gatedec)
        dm2pin_bounds = _l_gatedec.bounds(net=nets.c2p, mask=metal2pin.mask)
        dem2pin_bounds = _l_gatedec.bounds(net=nets.c2p_en, mask=metal2pin.mask)
        x = tech.on_grid(
            0.25*spec.monocell_width - 0.5*(dm2pin_bounds.left + dem2pin_bounds.right),
        )
        l_gatedec = layouter.place(
            _l_gatedec, x=x,
            y=(frame.cells_y - cast(_geo._Rectangular, _l_gatedec.boundary).bottom),
        )

        # c2p & c2p_en
        # bring pins to top
        for name in ("c2p", "c2p_en"):
            frame.promote_m2instpin_to_corepin(layouter=layouter, net=nets[name], inst_layout=l_gatedec)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # LevelDown + interconnect
        _l_ld = layouter.inst_layout(inst=insts.leveldown)

        # p2c
        net = nets.p2c
        _m1pin_bounds = _l_ld.bounds(net=net, mask=metal1pin.mask)
        x = tech.on_grid(
            0.75*spec.monocell_width - 0.5*(_m1pin_bounds.left + _m1pin_bounds.right),
        )
        l_ld = layouter.place(_l_ld, x=x, y=frame.cells_y)
        frame.promote_m1instpin_to_corepin(
            layouter=layouter, net=net, inst_layout=l_ld, align="left",
        )

        # pad
        net = nets.pad
        m2pin_bounds = l_ld.bounds(net=net, mask=metal2pin.mask)
        clamp_bounds = None
        for polygon in l_pclamp.filter_polygons(
            net=nets.pad, mask=metal2.mask, split=True,
        ):
            bounds = polygon.bounds
            if clamp_bounds is None:
                if bounds.right <= m2pin_bounds.right:
                    clamp_bounds = bounds
            else:
                if (
                    (bounds.right <= m2pin_bounds.right)
                    and (bounds.right > clamp_bounds.right)
                ):
                    clamp_bounds = bounds
        assert clamp_bounds is not None, "Internal error"
        m2_width = comp.metal[2].minwidth4ext_updown
        shape = _geo.Rect(
            left=(clamp_bounds.right - m2_width), bottom=(m2pin_bounds.bottom - m2_width),
            right=m2pin_bounds.right, top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=clamp_bounds, bottom=clamp_bounds.top, top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.pad,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=None,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadInOutT = _PadInOut


class _PadAnalog(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovss = nets.iovss
        iovdd = nets.iovdd

        pad = ckt.new_net(name="pad", external=True)
        padres = ckt.new_net(name="padres", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount_analog, n_drive=0, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount_analog, n_drive=0, pad=pad,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        c_secondprot = fab.get_cell("SecondaryProtection")
        i_secondprot = ckt.instantiate(c_secondprot, name="secondprot")
        iovss.childports += i_secondprot.ports.iovss
        iovdd.childports += i_secondprot.ports.iovdd
        pad.childports += i_secondprot.ports.pad
        padres.childports += i_secondprot.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed
        frame = fab.frame

        active = comp.active
        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # Place the secondary protection
        # Search for pad pin closest to the middle of the cell
        x_clamppin = None
        pinmask = metal2pin.mask
        clamppinm2_bounds: Optional[_geo.Rect] = None
        if l_pclamp is not None:
            for polygon in l_pclamp.filter_polygons(net=nets.pad, mask=pinmask):
                for bounds in _hlp._iterate_polygonbounds(polygon=polygon):
                    x_p = bounds.center.x
                    if (x_clamppin is None) or (x_p > x_clamppin):
                        x_clamppin = x_p
                        assert isinstance(bounds, _geo.Rect)
                        clamppinm2_bounds = bounds
        else:
            assert False
        assert x_clamppin is not None
        assert clamppinm2_bounds is not None
        _l_secondprot = layouter.inst_layout(inst=insts.secondprot)
        _actvdd_bounds = _l_secondprot.bounds(net=nets.iovdd, mask=active.mask)
        y = frame.cells_y - _actvdd_bounds.top + 0.5*comp.minwidth_activewithcontact
        _protpadpin_bounds = _l_secondprot.bounds(mask=pinmask, net=nets.pad)
        x_protpadpin = 0.5*(_protpadpin_bounds.left + _protpadpin_bounds.right)
        # Center pins
        x = tech.on_grid(x_clamppin - x_protpadpin)
        l_secondprot = layouter.place(_l_secondprot, x=x, y=y)
        protpadpin_bounds = l_secondprot.bounds(mask=pinmask, net=nets.pad)
        protpadrespin_bounds = l_secondprot.bounds(mask=pinmask, net=nets.padres)

        # Connect pins of secondary protection
        shape = _geo.Rect.from_rect(
            rect=protpadpin_bounds, bottom=clamppinm2_bounds.top,
        )
        layouter.add_wire(wire=metal2, net=nets.pad, shape=shape)

        shape = _geo.Rect.from_rect(
            rect=protpadrespin_bounds,
            left=(protpadrespin_bounds.right - comp.metal[2].minwidth4ext_updown),
        )
        frame.add_corepin(layouter=layouter, net=nets.padres, m2_shape=shape)

        # Connect pad pins
        left = spec.monocell_width
        right = 0.0
        for polygon in l_pclamp.filter_polygons(net=nets.pad, mask=pinmask):
            for bounds in _hlp._iterate_polygonbounds(polygon=polygon):
                if bounds.right < x_clamppin:
                    shape = _geo.Rect.from_rect(rect=bounds, top=frame.cell_height)
                    layouter.add_wire(net=nets.pad, wire=metal2, shape=shape)

                    left = min(left, bounds.left)
                    right = max(right, bounds.right)
        top = frame.cell_height
        bottom = top - 5*metal2.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        frame.add_corepin(layouter=layouter, net=nets.pad, m2_shape=shape)

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.pad,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=None,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadAnalogT = _PadAnalog


class _PadIOVss(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovss = nets.iovss

        frame.add_pad_inst(ckt=ckt, net=iovss)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovss,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovss,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=iovss)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.iovss)

        # iovss & iovdd
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.iovss)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.iovss)

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["iovss"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        l_padconn = frame.connect_pad2track(
            layouter=layouter, pad=nets.iovss, track="iovss",
            pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.iovss,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=l_padconn,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadIOVssT = _PadIOVss


class _PadIOVdd(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovdd = nets.iovdd

        frame.add_pad_inst(ckt=ckt, net=iovdd)

        if spec.invvdd_n_mosfet is None:
            # Just put a n&p clamp without drive
            frame.add_nclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovdd,
            )
            frame.add_pclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovdd,
            )
        else:
            frame.add_rcclamp_insts(ckt=ckt, pad=iovdd)

        # Also generate the layout as it will change the circuit
        self.layout

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame
        tech = self.tech
        comp = fab.computed

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(
            ckt=ckt, layouter=layouter,
            skip_top=() if frame.has_pad else ("iovss",),
        )
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.iovdd)

        if spec.invvdd_n_mosfet is None:
            # Place nclamp/pclamp + connect to iovdd track
            l_nclamp = frame.place_nclamp(
                layouter=layouter, pad=nets.iovdd,
            )
            pclamp_lay = frame.place_pclamp(
                layouter=layouter, pad=nets.iovdd,
            )
            frame.connect_pad2track(
                layouter=layouter, pad=nets.iovdd, track="iovdd",
                pclamp_lay=pclamp_lay, ndio_lay=None, pdio_lay=None
            )
        else:
            l_nclamp = frame.layout_rcclamp(layouter=layouter, pad=nets.iovdd)

            # Connect pad to iovdd track
            specs = comp.track_metalspecs
            net = nets["iovdd"]
            max_pitch = frame.tracksegment_maxpitch
            fingers = floor((frame.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(frame.pad_width/fingers, mult=2, rounding="floor")
            track_top = frame.track_specs["iovdd"].top
            for metal_spec in (specs if frame.has_pad else specs[-1:]):
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = frame.pad_bb(prim=metal)
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
                    layouter.add_wire(net=net, wire=metal, shape=shape)

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=None, ndio_lay=None, pdio_lay=None,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadIOVddT = _PadIOVdd


class _PadVss(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        vss = nets.vss

        frame.add_pad_inst(ckt=ckt, net=vss)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vss,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vss,
        )

        frame.add_dcdiodes_inst(ckt=ckt, pad=vss)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        metal = comp.metal
        metal2 = metal[2].prim

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.vss)

        # iovss & iovdd
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.vss)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.vss)

        # DC Diodes
        l_ndio, l_pdio = frame.place_dcdiodes(
            layouter=layouter, pad=nets["vss"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        l_padconn = frame.connect_pad2track(
            layouter=layouter, pad=nets.vss, track="vss",
            pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # connect DCDiodes
        frame.connect_dcdiodes(
            layouter=layouter, pad=nets.vss,
            nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
            ndio_lay=l_ndio, pdio_lay=l_pdio,
            padconn_lay=l_padconn,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadVssT = _PadVss


class _PadVdd(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        vdd = nets.vdd

        frame.add_pad_inst(ckt=ckt, net=vdd)

        if frame.has_pad or (spec.invvdd_n_mosfet is None):
            frame.add_nclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vdd,
            )
            frame.add_pclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vdd,
            )

            frame.add_dcdiodes_inst(ckt=ckt, pad=vdd)
        else:
            frame.add_rcclamp_insts(ckt=ckt, pad=vdd)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame
        tech = self.tech
        comp = fab.computed

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(
            ckt=ckt, layouter=layouter,
            skip_top=() if frame.has_pad else ("iovss", "iovdd", "secondiovss"),
        )
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.vdd)

        if frame.has_pad or (spec.invvdd_n_mosfet is None):
            # iovss & iovdd
            l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.vdd)
            l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.vdd)

            # DC Diodes
            l_ndio, l_pdio = frame.place_dcdiodes(
                layouter=layouter, pad=nets["vdd"],
                nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
            )

            # Bulk/well connection clamps
            frame.connect_clamp_wells(
                ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
            )

            l_padconn = frame.connect_pad2track(
                layouter=layouter, pad=nets.vdd, track="vdd",
                pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
            )

            # connect DCDiodes
            frame.connect_dcdiodes(
                layouter=layouter, pad=nets.vdd,
                nclamp_lay = l_nclamp, pclamp_lay=l_pclamp,
                ndio_lay=l_ndio, pdio_lay=l_pdio,
                padconn_lay=l_padconn,
            )
        else:
            l_nclamp = frame.layout_rcclamp(layouter=layouter, pad=nets.vdd)
            l_pclamp = None
            l_ndio = None
            l_pdio = None

            # Connect pad to vdd track
            specs = comp.track_metalspecs
            net = nets["vdd"]
            max_pitch = frame.tracksegment_maxpitch
            fingers = floor((frame.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(frame.pad_width/fingers, mult=2, rounding="floor")
            track_seg = frame._track_segments["vddvss"][0]
            track_top = track_seg.top
            track_bottom = track_seg.bottom
            metal_spec = specs[-1]
            metal = metal_spec.prim
            space = metal_spec.tracksegment_space

            pad_bb = frame.pad_bb(prim=metal)
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
                layouter.add_wire(net=net, wire=metal, shape=shape)

            metal_spec2 = specs[-2]
            via = metal_spec2.top_via
            via_space = frame.tracksegment_viapitch - via.width
            shape = _geo.Rect(
                left=(pad_bb.left + 0.5*space), bottom=(track_bottom + 0.5*space),
                right=(pad_bb.right - 0.5*space), top=(track_top - 0.5*space),
            )
            layouter.add_wire(
                net=net, wire=via, space=via_space,
                bottom_shape=shape, top_shape=shape,
            )
            layouter.add_wire(net=net, wire=metal, pin=metal.pin, shape=shape)

        # Bulk/well connection cell
        frame.draw_trackconn(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp, ndio_lay=l_ndio, pdio_lay=l_pdio,
        )

        # Set boundary
        frame.set_boundary(layouter=layouter)
PadVddT = _PadVdd


class _Filler(_cell._FactoryCell):
    def __init__(self, *,
        fab: "IOFactory", name: str, cell_width: float,
    ):
        super().__init__(fab=fab, name=name)
        self._cell_width = cell_width

        frame = fab.frame

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        frame.add_track_nets(ckt=ckt)

        frame.draw_tracks(ckt=ckt, layouter=layouter, cell_width=cell_width)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=cell_width, cells_only=False,
        )

        # Boundary
        bb = _geo.Rect(
            left=0.0, bottom=0.0, right=cell_width, top=frame.cell_height,
        )
        layout.boundary = bb

    @property
    def cell_width(self) -> float:
        return self._cell_width
FillerT = _Filler


class _Corner(_cell._FactoryCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        super().__init__(fab=fab, name=name)

        frame = fab.frame
        spec = fab.spec

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        frame.add_track_nets(ckt=ckt)
        frame.draw_corner_tracks(ckt=ckt, layouter=layouter)

        # Boundary
        bb = _geo.Rect(
            left=-frame.cell_height, bottom=0.0, right=0.0, top=frame.cell_height,
        )
        layout.boundary = bb
CornerT = _Corner


class _Gallery(_cell._FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory"):
        spec = fab.spec
        super().__init__(fab=fab, name=name)

        self.outs = outs = (
            ("IOPadOut",) if isinstance(spec.clampdrive, int)
            else tuple(f"IOPadOut{strength}" for strength in spec.clampdrive.keys())
        )
        self.outs_l = tuple(out.lower() for out in outs)
        self.triouts = triouts = (
            ("IOPadTriOut",) if isinstance(spec.clampdrive, int)
            else tuple(f"IOPadTriOut{strength}" for strength in spec.clampdrive.keys())
        )
        self.triouts_l = tuple(triout.lower() for triout in triouts)
        self.inouts = inouts = (
            ("IOPadInOut",) if isinstance(spec.clampdrive, int)
            else tuple(f"IOPadInOut{strength}" for strength in spec.clampdrive.keys())
        )
        self.inouts_l = tuple(inout.lower() for inout in inouts)
        self.cells = cells = (
            "Corner",
            "Filler200", "Filler400", "Filler1000", "Filler2000", "Filler4000", "Filler10000",
            "IOPadVss", "IOPadVdd", "IOPadIn", *outs, *triouts, *inouts,
            "IOPadIOVss", "IOPadIOVdd", "IOPadAnalog",
        )
        self.cells_l = tuple(cell.lower() for cell in cells)

    def _create_circuit(self):
        fab = self.fab
        tech = self.tech
        ckt = self.new_circuit()
        insts = ckt.instances

        for cell_name in self.cells:
            if cell_name.startswith("Filler"):
                w = float(cell_name[6:])*tech.grid
                cell = fab.filler(cell_width=w)
            else:
                cell = fab.get_cell(cell_name)
            ckt.instantiate(cell, name=cell_name.lower())

        # Add second corner cell
        ckt.instantiate(fab.get_cell("Corner"), name="corner2")
        cells_l = (*self.cells_l, "corner2")

        # vss and iovss are connected by the substrate
        # make only vss in Gallery so it is LVS clean.
        for net in ("vdd", "vss", "iovdd"):
            ports = tuple(insts[cell].ports[net] for cell in cells_l)
            if net == "vss":
                ports += tuple(insts[cell].ports["iovss"] for cell in cells_l)
            ckt.new_net(name=net, external=True, childports=ports)

        for inst_name in ("iopadin", *self.outs_l, *self.triouts_l, *self.inouts_l):
            ckt.new_net(
                name=f"{inst_name}_pad", external=True,
                childports=insts[inst_name].ports.pad,
            )
        for inst_name in ("iopadin", *self.inouts_l):
            ckt.new_net(
                name=f"{inst_name}_p2c", external=True,
                childports=insts[inst_name].ports.p2c,
            )
        for inst_name in (*self.outs_l, *self.triouts_l, *self.inouts_l):
            ckt.new_net(
                name=f"{inst_name}_c2p", external=True,
                childports=insts[inst_name].ports.c2p,
            )
        for inst_name in (*self.triouts_l, *self.inouts_l):
            ckt.new_net(
                name=f"{inst_name}_c2p_en", external=True,
                childports=insts[inst_name].ports.c2p_en,
            )
        ckt.new_net(name="ana_out", external=True, childports=(
            insts.iopadanalog.ports.pad,
        ))
        ckt.new_net(name="ana_outres", external=True, childports=(
            insts.iopadanalog.ports.padres,
        ))

    def _create_layout(self):
        fab = self.fab
        frame = fab.frame
        comp = fab.computed

        ckt = self.circuit
        nets = ckt.nets
        insts = ckt.instances
        layouter = self.new_circuitlayouter()

        padpin_metal = comp.track_metalspecs[-1].prim
        padpin_bb = frame.pad_bb(prim=padpin_metal)
        metal3 = comp.metal[3].prim

        x = 0.0
        y = 0.0

        pad_nets = {
            "iopadvss": nets["vss"],
            "iopadiovss": nets["vss"],
            "iopadvdd": nets["vdd"],
            "iopadiovdd": nets["iovdd"],
            **{
                cell_name: nets[f"{cell_name}_pad"]
                for cell_name in ("iopadin", *self.outs_l, *self.triouts_l, *self.inouts_l)
            },
            "iopadanalog": nets["ana_out"],
        }
        core_nets = {
            "iopadin": (nets["iopadin_p2c"],),
            **{
                out: (nets[f"{out}_c2p"],)
                for out in self.outs_l
            },
            **{
                out: (nets[f"{out}_c2p"], nets[f"{out}_c2p_en"])
                for out in self.triouts_l
            },
            **{
                io: (nets[f"{io}_p2c"], nets[f"{io}_c2p"], nets[f"{io}_c2p_en"])
                for io in self.inouts_l
            },
            "iopadanalog": (nets["ana_out"], nets["ana_outres"]),
        }
        bnd: Optional[_geo._Rectangular] = None
        for cell in self.cells_l:
            inst = insts[cell]
            l = layouter.place(inst, x=x, y=y)

            net =  pad_nets.get(cell, None)
            if net is not None:
                layouter.add_wire(
                    net=net, wire=padpin_metal, pin=padpin_metal.pin,
                    shape=padpin_bb.moved(dxy=_geo.Point(x=x, y=y)),
                )
            for net in core_nets.get(cell, ()):
                for ms in l.filter_polygons(net=net, mask=metal3.pin.mask, split=True, depth=1):
                    shape = cast(_geo.RectangularT, ms.shape)
                    if shape.bottom > _geo.epsilon:
                        layouter.add_wire(net=net, wire=metal3, pin=metal3.pin, shape=shape)

            bnd = l.boundary
            assert bnd is not None
            x = bnd.right
        assert bnd is not None

        # Add second corner cell
        l = layouter.place(insts["corner2"], x=x, y=y, rotation=_geo.Rotation.MY)
        bnd = l.boundary
        assert bnd is not None

        self.layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=bnd.right, top=bnd.top,
        )
GalleryT = _Gallery


class IOFactory(_fab.CellFactory[_cell._FactoryCell]):
    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
        spec: "_spec.IOSpecification", framespec: "_spec.IOFrameSpecification",
        name_prefix: str="", name_suffix: str="",
    ):
        if lib.tech != spec.stdcellfab.lib.tech:
            raise ValueError(
                f"Library technology '{lib.tech.name}' differs from standard cell technology"
                f" '{spec.stdcellfab.lib.name}'"
            )
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab, cell_class=_cell._FactoryCell,
            name_prefix=name_prefix, name_suffix=name_suffix,
        )
        self.spec = spec

        self.computed = _spec._ComputedSpecs(
            fab=self, framespec=framespec,
            nmos=spec.nmos, pmos=spec.pmos, ionmos=spec.ionmos, iopmos=spec.iopmos,
        )
        self.frame = _cell._IOCellFrame(fab=self, framespec=framespec)

    def guardring(self, *,
        type_: str, width: float, height: float,
        fill_well: bool=False, fill_implant: bool=False,
        create_cb: Optional[Callable[[GuardRingT], None]]=None,
    ) -> GuardRingT:
        s = "GuardRing_{}{}W{}H{}{}".format(
            type_.upper(),
            round(width/self.tech.grid),
            round(height/self.tech.grid),
            "T" if fill_well else "F",
            "T" if fill_implant else "F",
        )

        return self.getcreate_cell(
            name=s, cell_class=_GuardRing, create_cb=create_cb,
            type_=type_, width=width, height=height,
            fill_well=fill_well, fill_implant=fill_implant,
        )

    def pad(self, *,
        width: float, height: float, create_cb: Optional[Callable[[PadT], None]]=None,
    ) -> PadT:
        s = "Pad_{}W{}H".format(
            round(width/self.tech.grid),
            round(height/self.tech.grid),
        )

        return self.getcreate_cell(
            name=s, cell_class=_Pad, create_cb=create_cb,
            width=width, height=height, start_via=2,
        )

    def clamp(self, *,
        type_: str, n_trans: int, n_drive: int, rows: Optional[int]=None,
        create_cb: Optional[Callable[[ClampT], None]]=None,
    ) -> ClampT:
        s = "Clamp_{}{}N{}D".format(
            type_.upper(),
            n_trans,
            n_drive,
        )
        if rows is None:
            rows = self.spec.clampnmos_rows if type_ == "n" else self.spec.clamppmos_rows
        else:
            s += f"{rows}R"

        return self.getcreate_cell(
            name=s, cell_class=_Clamp, create_cb=create_cb,
            type_=type_, n_trans=n_trans, n_drive=n_drive, rows=rows,
        )

    def filler(self, *,
        cell_width: float, create_cb: Optional[Callable[[FillerT], None]]=None,
    ) -> FillerT:
        tech = self.tech
        s = f"Filler{round(cell_width/tech.grid)}"

        return self.getcreate_cell(
            name=s, cell_class=_Filler, create_cb=create_cb,
            cell_width=cell_width,
        )

    def dcdiode(self, *,
        type_: str, create_cb: Optional[Callable[[DCDiodeT], None]]=None,
    ) -> DCDiodeT:
        if not self.spec.add_dcdiodes:
            raise TypeError("Can't generate DCDiode for Factory without DC diodes")

        if type_ not in ("n", "p"):
            raise ValueError(f"DCDiode type has to be 'n' or 'p' not '{type_}'")
        s = f"DC{type_.upper()}Diode"

        return self.getcreate_cell(
            name=s, cell_class=_DCDiode, create_cb=create_cb,
            type_=type_,
        )

    def out(self, *,
        drivestrength: Optional[str]=None,
        create_cb: Optional[Callable[[PadOutT], None]]=None,
        cell_class: Type[PadOutT]=_PadOut,
    ) -> PadOutT:
        spec = self.spec

        if drivestrength is None:
            if not isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength has to be a string if clampdrive spec is not an int"
                )
            name = "IOPadOut"
            drive = spec.clampdrive
        else:
            if isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength must be None if clampdrive spec is an int"
                )
            name = f"IOPadOut{drivestrength}"
            drive = spec.clampdrive[drivestrength]

        return self.getcreate_cell(
            name=name, cell_class=cell_class, create_cb=create_cb,
            drive=drive,
        )

    def triout(self, *,
        drivestrength: Optional[str]=None,
        create_cb: Optional[Callable[[PadTriOutT], None]]=None,
        cell_class: Type[PadTriOutT]=_PadTriOut,
    ) -> PadTriOutT:
        spec = self.spec

        if drivestrength is None:
            if not isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength has to be a string if clampdrive spec is not an int"
                )
            name = "IOPadTriOut"
            drive = spec.clampdrive
        else:
            if isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength must be None if clampdrive spec is an int"
                )
            name = f"IOPadTriOut{drivestrength}"
            drive = spec.clampdrive[drivestrength]

        return self.getcreate_cell(
            name=name, cell_class=cell_class, create_cb=create_cb,
            drive=drive,
        )

    def inout(self, *,
        drivestrength: Optional[str]=None,
        create_cb: Optional[Callable[[PadInOutT], None]]=None,
        cell_class: Type[PadInOutT]=_PadInOut,
    ) -> PadInOutT:
        spec = self.spec

        if drivestrength is None:
            if not isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength has to be a string if clampdrive spec is not an int"
                )
            name = "IOPadInOut"
            drive = spec.clampdrive
        else:
            if isinstance(spec.clampdrive, int):
                raise TypeError(
                    "drivestrength must be None if clampdrive spec is an int"
                )
            name = f"IOPadInOut{drivestrength}"
            drive = spec.clampdrive[drivestrength]

        return self.getcreate_cell(
            name=name, cell_class=cell_class, create_cb=create_cb,
            drive=drive,
        )

    def get_cell(self, name: str, *,
        create_cb: Optional[Callable[[_cell.FactoryCellT], None]]=None,
    ) -> _cell.FactoryCellT:
        if name.startswith("IOPadOut"):
            drive = name[8:]
            if not drive:
                return self.out()
            else:
                return self.out(drivestrength=drive)
        if name.startswith("IOPadTriOut"):
            drive = name[11:]
            if not drive:
                return self.triout()
            else:
                return self.triout(drivestrength=drive)
        if name.startswith("IOPadInOut"):
            drive = name[10:]
            if not drive:
                return self.inout()
            else:
                return self.inout(drivestrength=drive)
        if name.startswith("Filler"):
            w = int(name[6:])
            return self.filler(cell_width=(w*self.tech.grid))

        cls = {
            "SecondaryProtection": _Secondary,
            "RCClampResistor": _RCClampResistor,
            "RCClampInverter": _RCClampInverter,
            "LevelUp": _LevelUp,
            "LevelUpInv": _LevelUpInv,
            "LevelDown": _LevelDown,
            "GateLevelUp": _GateLevelUp,
            "GateLevelUpInv": _GateLevelUpInv,
            "GateDecode": _GateDecode,
            "IOPadIn": _PadIn,
            "IOPadVdd": _PadVdd,
            "IOPadVss": _PadVss,
            "IOPadIOVdd": _PadIOVdd,
            "IOPadIOVss": _PadIOVss,
            "IOPadAnalog": _PadAnalog,
            "Corner": _Corner,
            "Gallery": _Gallery,
        }[name]

        return self.getcreate_cell(name=name, cell_class=cls, create_cb=create_cb)
