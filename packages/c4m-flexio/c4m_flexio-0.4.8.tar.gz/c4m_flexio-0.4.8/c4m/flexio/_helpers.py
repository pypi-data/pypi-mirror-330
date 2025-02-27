# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from itertools import product
from typing import Collection, List, Generator, Optional, Callable, cast

from pdkmaster.technology import (
    property_ as _prp, geometry as _geo, mask as _msk, primitive as _prm,
)
from pdkmaster.design import circuit as _ckt, layout as _lay
# TODO: Remove use of PDKMaster internal classes
# see [#1](https://gitlab.com/Chips4Makers/c4m-flexio/-/issues/1)
from pdkmaster.design.layout import layout_ as _laylay

from . import factory as _fab


_sqrt2 = 2**0.5


def _iterate_polygonbounds(*, polygon: _geo.MaskShape) -> Generator[
    _geo._Rectangular, None, None,
]:
    for shape in polygon.shape.pointsshapes:
        yield shape.bounds


def clamp(*,
    name: str="clamp", fab: "_fab.IOFactory", ckt: _ckt._Circuit, type_: str,
    rows: int, source_net: _ckt._CircuitNet, drain_net: _ckt._CircuitNet,
    gate_nets: Collection[_ckt._CircuitNet], bulk_net: Optional[_ckt._CircuitNet]=None,
):
    spec = fab.spec
    comp = fab.computed
    layoutfab = fab.layoutfab
    tech = fab.tech

    active = comp.active
    poly = comp.poly
    ionimplant = comp.ionimplant
    iopimplant = comp.iopimplant
    cont = comp.contact
    metal1 = comp.metal[1].prim

    layout = layoutfab.new_layout()
    if type_ == "n":
        mos = spec.clampnmos
        w = spec.clampnmos_w
        l = spec.clampnmos_l
        implant = ionimplant
        tapimplant = spec.clamppmos.implant[0] if spec.clamppmos.implant else None
        sd_enc = comp.min_ionsd_enc
        well = None
        ch_well_args = {}
    elif type_ == "p":
        mos = spec.clamppmos
        w = spec.clamppmos_w
        l = spec.clamppmos_l
        implant = iopimplant
        tapimplant = spec.clampnmos.implant[0] if spec.clampnmos.implant else None
        sd_enc = comp.min_iopsd_enc
        well = mos.well
        ch_well_args = {"bottom_well": well, "well_net": source_net}
    else:
        raise AssertionError("Internal error: clamp mos type")
    if bulk_net is None:
        bulk_net = source_net

    # Compupte row placement for the transistor
    polypad_width = max(tech.computed.min_width(poly, up=True, min_enclosure=False), l)
    polypad_height = tech.computed.min_width(poly, up=True, min_enclosure=True)

    row_pitch = w + 2*spec.clampgate_gatecont_space + cont.width
    trans_height = rows*row_pitch

    # Create cont shapes to add
    if not spec.add_clampsourcetap:
        _l_srcch_left = _l_srcch_mid = _l_srcch_right = layoutfab.layout_primitive(
            portnets={"conn": source_net}, prim=cont, **ch_well_args,
            bottom=active, bottom_implant=implant, bottom_implant_enclosure=sd_enc,
            bottom_height=w, columns=1,
        )
    else:
        impl_masks: List[_msk.DesignMask] = []
        if implant is not None:
            impl_masks.append(implant.mask)
        if tapimplant is not None:
            impl_masks.append(tapimplant.mask)
        assert impl_masks, "Internal error"

        # Reduce size of the implant
        def reduce_ms_left(ms: _geo.MaskShape, shape: _geo.Rect) -> _geo.MaskShape:
            if ms.mask not in impl_masks:
                return ms
            else:
                assert isinstance(ms.shape, _geo.Rect)
                rect = _geo.Rect.from_rect(rect=ms.shape, left=shape.left)
                return _geo.MaskShape(mask=ms.mask, shape=rect)
        def reduce_ms_right(ms: _geo.MaskShape, shape: _geo.Rect) -> _geo.MaskShape:
            if ms.mask not in impl_masks:
                return ms
            else:
                assert isinstance(ms.shape, _geo.Rect)
                rect = _geo.Rect.from_rect(rect=ms.shape, right=shape.right)
                return _geo.MaskShape(mask=ms.mask, shape=rect)
        def reduce_ms_both(ms: _geo.MaskShape, shape: _geo.Rect) -> _geo.MaskShape:
            if ms.mask not in impl_masks:
                return ms
            else:
                assert isinstance(ms.shape, _geo.Rect)
                rect = _geo.Rect.from_rect(rect=ms.shape, left=shape.left, right=shape.right)
                return _geo.MaskShape(mask=ms.mask, shape=rect)
        def reduce_implant(*,
            lay: _lay.LayoutT, shape: _geo.Rect,
            reduce_ms: Callable[[_geo.MaskShape, _geo.Rect], _geo.MaskShape],
        ) -> None:
            def reduce_sl(sl: _laylay._SubLayout):
                if not isinstance(sl, _laylay._MaskShapesSubLayout):
                    return sl
                else:
                    return _laylay._MaskShapesSubLayout(
                        net=sl.net,
                        shapes=_geo.MaskShapes(reduce_ms(ms, shape) for ms in sl.shapes),
                    )

            lay._sublayouts = _laylay._SubLayouts(reduce_sl(sl) for sl in lay._sublayouts)

        def merge_mask(*, lay: _lay.LayoutT, mask: _msk._Mask) -> None:
            def merge_sl(sl: _laylay._SubLayout) -> _laylay._SubLayout:
                if not isinstance(sl, _laylay._MaskShapesSubLayout):
                    return sl
                else:
                    def merge_ms(ms: _geo.MaskShape) -> _geo.MaskShape:
                        if ms.mask != mask:
                            return ms
                        else:
                            rect = ms.shape.bounds
                            return _geo.MaskShape(mask=ms.mask, shape=rect)

                    shapes = _geo.MaskShapes(merge_ms(ms) for ms in sl.shapes)
                    return _laylay._MaskShapesSubLayout(net=sl.net, shapes=shapes)

            lay._sublayouts = _laylay._SubLayouts(merge_sl(sl) for sl in lay._sublayouts)

        _l_tapch = layoutfab.layout_primitive(
            prim=cont, portnets={"conn": source_net}, **ch_well_args,
            bottom=active, bottom_implant=tapimplant,
            bottom_height=w, bottom_enclosure=spec.clampsource_cont_tap_enclosure,
            columns=1,
        )
        _tapact_bounds = _l_tapch.bounds(mask=active.mask)

        assert isinstance(spec.clampsource_cont_tap_space, float)
        width = cont.width + 2*spec.clampsource_cont_tap_space
        _l_actch = layoutfab.layout_primitive(
            portnets={"conn": source_net}, prim=cont, **ch_well_args,
            bottom=active, bottom_implant=implant, bottom_implant_enclosure=sd_enc,
            bottom_height=w, bottom_width=width,
        )
        _srcact_bounds = _l_actch.bounds(mask=active.mask)

        _l_actch_left = _l_actch.dup()
        reduce_implant(lay=_l_actch_left, shape=_srcact_bounds, reduce_ms=reduce_ms_right)
        x = _tapact_bounds.left - _srcact_bounds.right
        _l_actch_left.move(dxy=_geo.Point(x=x, y=0.0))
        _l_actch_right = _l_actch.dup()
        reduce_implant(lay=_l_actch_right, shape=_srcact_bounds, reduce_ms=reduce_ms_left)
        x = _tapact_bounds.right - _srcact_bounds.left
        _l_actch_right.move(dxy=_geo.Point(x=x, y=0.0))

        _l_srcch_left = _l_tapch.dup()
        reduce_implant(lay=_l_srcch_left, shape=_tapact_bounds, reduce_ms=reduce_ms_right)
        _l_srcch_left += _l_actch_right
        merge_mask(lay=_l_srcch_left, mask=metal1.mask)

        _l_srcch_mid = _l_tapch.dup()
        reduce_implant(lay=_l_srcch_mid, shape=_tapact_bounds, reduce_ms=reduce_ms_both)
        _l_srcch_mid += _l_actch_left
        _l_srcch_mid += _l_actch_right
        merge_mask(lay=_l_srcch_mid, mask=metal1.mask)

        _l_srcch_right = _l_tapch.dup()
        reduce_implant(lay=_l_srcch_right, shape=_tapact_bounds, reduce_ms=reduce_ms_left)
        _l_srcch_right += _l_actch_left
        merge_mask(lay=_l_srcch_right, mask=metal1.mask)
    srcchch_bounds = _l_srcch_mid.bounds(mask=cont.mask)

    _l_drnch = layoutfab.layout_primitive(
        portnets={"conn": drain_net}, prim=cont, **ch_well_args,
        bottom=active, bottom_implant=implant, bottom_implant_enclosure=sd_enc,
        bottom_height=w, columns=spec.clampdrain_contcolumns,
    )
    drnchch_bounds = _l_drnch.bounds(mask=cont.mask)

    # Compute dimensions
    ngates = len(gate_nets)
    ch_pitch = cont.width + cont.min_space
    gate_pitch = ( # Average gate patch; actually pitch of middle of source/drain area
        0.5*srcchch_bounds.width + spec.clampgate_sourcecont_space
        + l + spec.clampgate_draincont_space
        + 0.5*drnchch_bounds.width
    )

    x_ch0 = -0.5*ngates*gate_pitch
    y_ch0 = -0.5*trans_height
    y_trans0 = -0.5*(rows - 1)*row_pitch
    active_bottom = y_trans0 - 0.5*w
    active_top = y_trans0 + (rows - 1)*row_pitch + 0.5*w

    clampdrain_left = clampdrain_bottom = clampdrain_right = clampdrain_top = None

    if spec.clampdrain_active_ext is not None:
        clampdrain_bottom = active_bottom - spec.clampdrain_active_ext
        clampdrain_top = active_top + spec.clampdrain_active_ext

    # Draw/place subblocks
    actmos_boundss: List[Optional[_geo.RectangularT]] = rows*[cast(Optional[_geo.RectangularT], None)]
    active_left = None
    for i, gate_net in enumerate(gate_nets):
        x_ch = x_ch0 + i*gate_pitch
        if (i % 2) == 0: # source
            ch_net = sd1_net = source_net
            sd2_net = drain_net
            x_trans = x_ch + 0.5*srcchch_bounds.width + spec.clampgate_sourcecont_space + 0.5*l
            if spec.clampgate_clampdrain_overlap is not None:
                assert spec.clampdrain_gatecont_space is not None
                clampdrain_left = x_trans + 0.5*l - spec.clampgate_clampdrain_overlap
                clampdrain_right = (
                    x_trans + 0.5*l + spec.clampgate_draincont_space - spec.clampdrain_gatecont_space
                )
            _l_actch = _l_srcch_left if i == 0 else _l_srcch_mid
        else: # drain
            ch_net = sd1_net = drain_net
            sd2_net = source_net
            x_trans = x_ch + 0.5*drnchch_bounds.width + spec.clampgate_draincont_space + 0.5*l
            if spec.clampgate_clampdrain_overlap is not None:
                assert spec.clampdrain_gatecont_space is not None
                clampdrain_left = (
                    x_trans - 0.5*l - spec.clampgate_draincont_space + spec.clampdrain_gatecont_space
                )
                clampdrain_right = x_trans - 0.5*l + spec.clampgate_clampdrain_overlap
            _l_actch = _l_drnch

        polymos_bounds = None
        for row in range(rows):
            transname = f"{name}_g{i}"
            if rows > 1:
                transname += f"_r{row}"

            y_trans = y_trans0 + row*row_pitch

            # Draw source-drain contact column
            l_actch = _l_actch.moved(dxy=_geo.Point(x=x_ch, y=y_trans))
            layout += l_actch
            actch_bounds = l_actch.bounds(mask=active.mask)
            if i == 0:
                active_left = actch_bounds.left
            # If not first connect with active of last drawn transistor
            actmos_bounds = actmos_boundss[row]
            if actmos_bounds is not None:
                rect = _geo.Rect(
                    left=actmos_bounds.right, bottom=actmos_bounds.bottom,
                    right=actch_bounds.right, top=actmos_bounds.top,
                )
                # Only add shape for active, implant may clash with tap implant
                layout.add_shape(net=ch_net, layer=active, shape=rect)

            # Draw the gate
            inst = ckt.instantiate(mos, name=transname, l=l, w=w)
            sd1_net.childports += inst.ports.sourcedrain1
            sd2_net.childports += inst.ports.sourcedrain2
            gate_net.childports += inst.ports.gate
            bulk_net.childports += inst.ports.bulk
            l_mos = layout.add_primitive(
                portnets={
                    "sourcedrain1": sd1_net, "sourcedrain2": sd2_net,
                    "gate": gate_net, "bulk": bulk_net,
                },
                prim=mos, x=x_trans, y=y_trans, l=l, w=w,
            )
            actmos_bounds = actmos_boundss[row] = l_mos.bounds(mask=active.mask)
            polymos_bounds = l_mos.bounds(mask=poly.mask)
            # Connect to active of source-drain contact column
            rect = _geo.Rect(
                left=actch_bounds.left, bottom=actmos_bounds.bottom,
                right=actmos_bounds.left, top=actmos_bounds.top,
            )
            layout.add_shape(net=ch_net, layer=active, shape=rect)
            if spec.clamp_clampdrain is not None:
                assert clampdrain_left is not None
                assert clampdrain_bottom is not None
                assert clampdrain_right is not None
                assert clampdrain_top is not None
                # Draw the extra drain layer
                layout.add_shape(layer=spec.clamp_clampdrain, net=None, shape=_geo.Rect(
                    left=clampdrain_left, bottom=clampdrain_bottom,
                    right=clampdrain_right, top=clampdrain_top,
                ))
        assert polymos_bounds is not None

        polych_bounds1 = None
        m1ch_bounds1 = None
        polych_bounds2 = None
        m1ch_bounds2 = None
        for row in range(rows + 1):
            y_ch = y_ch0 + row*row_pitch

            l_polych = layout.add_primitive(
                prim=cont, portnets={"conn": gate_net}, bottom=poly,
                x=x_trans, y=y_ch,
                bottom_width=polypad_width, bottom_height=polypad_height,
                bottom_enclosure="wide",
            )
            polych_bounds = l_polych.bounds(mask=poly.mask)
            if row == 0:
                polych_bounds1 = l_polych.bounds(mask=poly.mask)
                m1ch_bounds1 = l_polych.bounds(mask=metal1.mask)
            polych_bounds2 = l_polych.bounds(mask=poly.mask)
            m1ch_bounds2 = l_polych.bounds(mask=comp.metal[1].prim.mask)
        assert polych_bounds1 is not None
        assert m1ch_bounds1 is not None
        assert polych_bounds2 is not None
        assert m1ch_bounds2 is not None
        # Connect both contact with poly and M1
        shape = _geo.Rect(
            left=polymos_bounds.left, bottom=polych_bounds1.bottom,
            right=polymos_bounds.right, top=polych_bounds2.top,
        )
        layout.add_shape(net=gate_net, layer=poly, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m1ch_bounds1, bottom=m1ch_bounds1.top, top=m1ch_bounds2.bottom,
        )
        layout.add_shape(net=gate_net, layer=comp.metal[1].prim, shape=shape)

    # Draw rightmost source-drain contact column
    active_right = None
    for row in range(rows):
        y_trans = y_trans0 + row*row_pitch

        x_ch = x_ch0 + ngates*gate_pitch
        if (ngates % 2) == 0:
            ch_net = source_net
            _l_actch = _l_srcch_right
        else:
            ch_net = drain_net
            _l_actch = _l_drnch

        l_actch = _l_actch.moved(dxy=_geo.Point(x=x_ch, y=y_trans))
        layout += l_actch
        actch_bounds = l_actch.bounds(mask=active.mask)
        active_right = actch_bounds.right
        actmos_bounds = actmos_boundss[row]
        assert actmos_bounds is not None
        rect = _geo.Rect(
            left=actmos_bounds.right, bottom=actmos_bounds.bottom,
            right=actch_bounds.right, top=actmos_bounds.top,
        )
        # Only add shape, implants may clash with tap implant.
        layout.add_shape(net=ch_net, layer=active, shape=rect)
    assert active_right is not None

    # Draw gate marker layer around the whole clamp
    l_extra: List[_prm.DesignMaskPrimitiveT] = []
    encs: List[float] = []
    if spec.clampdrain_active_ext is not None:
        encs.append(spec.clampdrain_active_ext)
    if mos.gate.oxide is not None:
        l_extra.append(mos.gate.oxide)
        if mos.gate.min_gateoxide_enclosure is not None:
            encs.append(mos.gate.min_gateoxide_enclosure.max())
    if mos.gate.inside is not None:
        l_extra.extend(mos.gate.inside)
        if mos.gate.min_gateinside_enclosure is not None:
            encs.extend(enc.max() for enc in mos.gate.min_gateinside_enclosure)
    if l_extra:
        enc = max(encs)
        assert active_left is not None
        r = _geo.Rect(
            left=(active_left - enc), bottom=(active_bottom - enc),
            right=(active_right + enc), top=(active_top + enc),
        )

        for extra in l_extra:
            layout.add_shape(layer=extra, net=None, shape=r)

    return layout


def diamondvia(*,
    fab, net, via, width, height, space, enclosure, center_via, corner_distance,
):
    assert all((
        (len(via.bottom) == 1) or isinstance(via.bottom[0], _prm.MetalWire),
        (len(via.top) == 1) or isinstance(via.top[0], _prm.MetalWire),
    )), "Unhandled configuration"
    metal_down = via.bottom[0]
    metal_up = via.top[0]

    layout = fab.layoutfab.new_layout()

    enc = enclosure.max()
    mbounds = _geo.Rect.from_size(width=width, height=height)
    vbounds = _geo.Rect.from_rect(rect=mbounds, bias=-enc)

    def away_from_corner(xy):
        x = xy[0]
        y = xy[1]
        via_left = x - via.width//2
        via_bottom = y - via.width//2
        via_right = via_left + via.width
        via_top = via_bottom + via.width

        d_left = via_left - vbounds.left
        d_bottom = via_bottom - vbounds.bottom
        d_right = vbounds.right - via_right
        d_top = vbounds.top - via_top

        return not any((
            corner_distance - d_left > d_bottom, # In bottom-left corner
            corner_distance - d_right > d_bottom, # In bottom-right corner
            corner_distance - d_left > d_top, # In top-left corner
            corner_distance - d_right > d_top, # In bottom-left corner
        ))

    via_pitch = via.width + space
    vwidth = vbounds.right - vbounds.left
    vheight = vbounds.top - vbounds.bottom
    if center_via:
        # Odd number of vias in horizontal and vertical direction
        nx = int(((vwidth - via.width)/via_pitch)//2)*2 + 1
        ny = int(((vheight - via.width)/via_pitch)//2)*2 + 1
    else:
        # Even number of vias in horizontal and vertical direction
        nx = int(((vwidth + space)/via_pitch)//2)*2
        ny = int(((vheight + space)/via_pitch)//2)*2


    real_width = nx*via_pitch - space
    real_height = ny*via_pitch - space
    real_left = vbounds.left + 0.5*(vwidth - real_width) + 0.5*via.width
    real_bottom = vbounds.bottom + 0.5*(vheight - real_height) + 0.5*via.width

    via_xy = (
        (real_left + i*via_pitch, real_bottom + j*via_pitch)
        for i, j in product(range(nx), range(ny))
    )

    layout.add_shape(layer=via, net=net, shape=_geo.MultiShape(shapes=(
        _geo.Rect.from_size(
            center=_geo.Point(x=x, y=y), width=via.width, height=via.width,
        )
        for x, y in filter(away_from_corner, via_xy)
    )))
    layout.add_shape(layer=metal_down, net=None, shape=mbounds)
    layout.add_shape(layer=metal_up, net=None, shape=mbounds)

    layout.boundary = mbounds

    return layout
