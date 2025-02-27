# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from itertools import product
from typing import List, Tuple, Dict, Iterable, Optional, Any, cast

from pdkmaster.technology import property_ as _prp,  geometry as _geo
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, cell as _cell, library as _lbry, factory as _fab,
)
from pdkmaster.io.coriolis import CoriolisExportSpec

from .canvas import StdCellCanvas
from .cell import _Cell
from . import activecolumnscell as _acc


__all__ = ["coriolis_export_spec", "StdCellFactory"]


def _direction_cb(net_name: str) -> str:
    if net_name == "vdd":
        return "supply"
    elif net_name == "vss":
        return "ground"
    elif net_name in ("ck", "clk"):
        return "clock"
    elif net_name in ("nq", "q", "one", "zero"):
        return "out"
    else:
        return "in"
coriolis_export_spec = CoriolisExportSpec(
    globalnets=("vdd", "vss"), net_direction_cb=_direction_cb,
)


class NotEnoughRoom(Exception):
    """Exception to indicate there is not enough room in a cell"""
    pass


class _Fill(_Cell):
    def __init__(self, *, fab: "StdCellFactory", name: str, width: int=1):
        super().__init__(fab=fab, name=name)

        canvas = fab.canvas

        nimplant = canvas._nimplant
        pimplant = canvas._pimplant

        self.set_width(width=width*canvas._cell_horplacement_grid)

        layouter = self.layouter

        if pimplant is not None:
            shape = _geo.Rect(
                left=0.0, right=self.width,
                bottom=0.0, top=pimplant.min_width,
            )
            layouter.add_portless(prim=pimplant, shape=shape)

        if nimplant is not None:
            shape = _geo.Rect(
                left=0.0, right=self.width,
                bottom=(canvas._cell_height - nimplant.min_width),
                top=canvas._cell_height,
            )
            layouter.add_portless(prim=nimplant, shape=shape)


class _Tie(_acc.ActiveColumnsCellFrame):
    def __init__(self, *,
        fab: "StdCellFactory", name: str, max_diff: bool=False, max_poly: bool=False, width: int=1,
    ):
        if max_diff and max_poly:
            raise ValueError("only one of max_diff and max_poly can be 'True'")

        super().__init__(fab=fab, name=name, draw_implants=(not max_diff))

        canvas = fab.canvas
        ac_canvas = self.ac_canvas
        tech = fab.tech

        cell_width = width*canvas._cell_horplacement_grid
        self.set_width(width=cell_width)

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        nwell_net = self.nwell_net
        pwell = canvas._pwell
        pwell_net = self.pwell_net
        poly = canvas._poly
        contact = canvas._contact
        metal1 = canvas._metal1

        ckt = self.circuit
        layouter = self._layouter

        vdd = ckt.nets.vdd
        vss = ckt.nets.vss

        min_actpoly_space = tech.computed.min_space(primitive1=active, primitive2=poly)

        if not max_diff:
            if max_poly:
                # Add big poly
                vss_dio_tap_bb = self.vsstap_lay.bounds(mask=active.mask)
                vdd_dio_tap_bb = self.vddtap_lay.bounds(mask=active.mask)
                left = 0.5*poly.min_space
                try:
                    s = min_actpoly_space
                except:
                    pass
                else:
                    left = max(left, -0.5*canvas._min_active_space + s)
                right = cell_width - left
                bottom = vss_dio_tap_bb.top + min_actpoly_space
                top = vdd_dio_tap_bb.bottom - min_actpoly_space
                layouter.add_wire(net=vss, wire=poly, shape=_geo.Rect(
                    left=left, bottom=bottom, right=right, top=top,
                ))

                l_ch = layouter.wire_layout(net=vss, wire=contact, bottom=poly)
                poly_bb = l_ch.bounds(mask=poly.mask)
                ch_bb = l_ch.bounds(mask=contact.mask)
                x = 0.5*cell_width
                y = bottom - poly_bb.bottom
                if canvas._min_contact_active_space is not None:
                    y = max(
                        y,
                        vss_dio_tap_bb.top + canvas._min_contact_active_space - ch_bb.bottom
                    )
                vss_polych_lay = layouter.place(object_=l_ch, x=x, y=y)
                vss_polych_m1_bb = vss_polych_lay.bounds(mask=metal1.mask)
                if vss_polych_m1_bb.bottom > canvas._m1_vssrail_width:
                    layouter.add_wire(net=vss, wire=metal1, shape=_geo.Rect.from_rect(
                        rect=vss_polych_m1_bb, bottom=0.0,
                    ))
        else: # max_diff == True
            args: Dict[str, Any]

            act_w = cell_width + canvas._min_active_space - 2*canvas._min_nactive_pactive_space
            if act_w + _geo.epsilon < active.min_width:
                raise NotEnoughRoom(f"maximum Tie with w == {width}")

            # extend vss tap
            top = canvas._well_edge_height - ac_canvas._min_nact_nwell_space
            if pimplant is not None:
                idx = active.implant.index(pimplant)
                enc = active.min_implant_enclosure[idx].tall()
                args = {"implant_enclosure": enc}
                top = min(top, canvas._well_edge_height - pimplant.min_space - enc.second)
            else:
                assert nimplant is not None
                args = {}
            bottom = 0.5*canvas._min_active_space
            shape = _geo.Rect(
                left=0.5*(cell_width - act_w), bottom=bottom,
                right=0.5*(cell_width + act_w), top=top,
            )
            layouter.add_wire(
                net=vss, wire=active, shape=shape, implant=pimplant,
                well=pwell, well_net=pwell_net,
                **args,
            )

            # extend vdd tap
            bottom = canvas._well_edge_height + ac_canvas._min_pact_nwell_enclosure
            if nimplant is not None:
                idx = active.implant.index(nimplant)
                enc = active.min_implant_enclosure[idx].tall()
                args = {"implant_enclosure": enc}
                bottom = max(bottom, canvas._well_edge_height + nimplant.min_space + enc.second)
            else:
                assert pimplant is not None
                enc = None
                args = {}
            top = canvas._cell_height - 0.5*canvas._min_active_space
            shape = _geo.Rect(
                left=0.5*(cell_width - act_w), bottom=bottom,
                right=0.5*(cell_width + act_w), top=top,
            )
            layouter.add_wire(
                net=vdd, wire=active, shape=shape, implant=nimplant,
                well=nwell, well_net=nwell_net,
                **args,
            )


class _Diode(_acc.ActiveColumnsCellFrame):
    def __init__(self, *,
        fab: "StdCellFactory", name: str,
    ):
        super().__init__(fab=fab, name=name)

        canvas = fab.canvas
        tech = fab.tech
        ac_canvas = self.ac_canvas

        cell_width = canvas._cell_horplacement_grid
        self.set_width(width=cell_width)

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        nwell_net = self.nwell_net
        pwell = canvas._pwell
        pwell_net = self.pwell_net
        contact = canvas._contact
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin

        ckt = self.circuit
        layouter = self._layouter

        i_ = ckt.new_net(name="i", external=True)

        # Min active space without implants overlapping
        vss_tap_act_bb = self.vsstap_lay.bounds(mask=active.mask)
        vdd_tap_act_bb = self.vddtap_lay.bounds(mask=active.mask)

        bottom_width = max(
            tech.computed.min_width(active, up=True, down=False, min_enclosure=True),
            canvas._min_active_width,
        )

        # ndiode
        bottom = max(
            vss_tap_act_bb.top + canvas._min_nactive_pactive_space_maxenc,
            canvas._m1_vssrail_width + canvas.min_m1_space,
        )
        top = canvas._well_edge_height - canvas._min_active_nwell_space
        h = tech.on_grid(top - bottom, mult=2, rounding="floor")
        vss_dio_x = 0.5*cell_width
        vss_dio_y = bottom + 0.5*h
        vss_dio_lay = layouter.add_wire(
            net=i_, well_net=pwell_net, wire=contact,
            bottom=active, bottom_implant=nimplant, bottom_well=pwell,
            x=vss_dio_x, y=vss_dio_y,
            bottom_width=bottom_width, bottom_height=h, bottom_enclosure="tall",
            top_height=h,
        )
        vss_dio_m1_bb = vss_dio_lay.bounds(mask=metal1.mask)

        # pdiode
        bottom = canvas._well_edge_height + canvas._min_active_nwell_enclosure
        top = min(
            vdd_tap_act_bb.bottom - canvas._min_nactive_pactive_space_maxenc,
            canvas._cell_height - canvas._m1_vddrail_width - canvas.min_m1_space,
        )
        h = tech.on_grid(top - bottom, mult=2, rounding="floor")
        vdd_dio_x = 0.5*cell_width
        vdd_dio_y = top - 0.5*h
        vdd_dio_lay = layouter.add_wire(
            net=i_, well_net=nwell_net, wire=contact,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            x=vdd_dio_x, y=vdd_dio_y,
            bottom_width=bottom_width, bottom_height=h, bottom_enclosure="tall",
            top_height=h,
        )
        vdd_dio_m1_bb = vdd_dio_lay.bounds(mask=metal1.mask)

        # input pin
        left = 0.5*cell_width - 0.5*canvas._pin_width
        right = left + canvas._pin_width
        bottom = vss_dio_m1_bb.bottom
        top = vdd_dio_m1_bb.top
        layouter.add_wire(
            net=i_, wire=metal1, pin=metal1pin, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            )
        )


class _ZeroOneDecap(_acc.ActiveColumnsCell):
    """A cell that can represent a logic zero and/or one; it can be used as decap
    cell with optional extra mos capacitance.
    """
    # TODO: optional extra moscap
    def __init__(self, *,
        name: str, fab: "StdCellFactory",
        zero_pin: bool, one_pin: bool,
    ):
        self._zero_pin = zero_pin
        self._one_pin = one_pin

        super().__init__(name=name, fab=fab)

    @property
    def zero_pin(self) -> bool:
        return self._zero_pin
    @property
    def one_pin(self) -> bool:
        return self._one_pin

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        ### nets

        one = ckt.new_net(name="one", external=self.one_pin)
        zero = ckt.new_net(name="zero", external=self.zero_pin)

        ### columns and rows

        # active columns, poly rows
        vss_sd = self.vss_sd(name="vss_sd")
        one_sd = self.signal_psd(name="one_sd", net=one, with_contact=True)
        sdcol0 = self.activecolumn(name="sdcol0", connect=False, elements=(vss_sd, one_sd))

        npass = self.nmos(name="npass", net=one, w_size="max")
        npasspad = self.polypad(name="npasspad", net=one)
        ppass = self.pmos(name="ppass", net=zero, w_size="max")
        ppasspad = self.polypad(name="ppasspad", net=zero)

        npassrow = self.polyrow(name="npassrow", elements=(npasspad, npass))
        ppassrow = self.polyrow(name="ppassrow", elements=(ppass, ppasspad))
        transcol = self.activecolumn(
            name="transcol", connect=False, elements=(npass, ppass),
        )

        zero_sd = self.signal_nsd(name="zero_sd", net=zero, with_contact=True)
        vdd_sd = self.vdd_sd(name="vdd_sd")
        sdcol1 = self.activecolumn(name="sdcol1", connect=False, elements=(zero_sd, vdd_sd))

        # m1 columns
        m1col_one = (self.m1pin if self.one_pin else self.m1column)(
            name="m1col_one", elements=(npasspad, one_sd),
        )
        m1col_zero = (self.m1pin if self.zero_pin else self.m1column)(
            name="m1col_zero", elements=(zero_sd, ppasspad),
        )

        ### Constraints

        return self.constraints(
            activecolumns=(sdcol0, transcol, sdcol1),
            polyrows=(npassrow.multipolyrow, ppassrow.multipolyrow),
            m1rows=(),
            m1columns=(m1col_one.multim1column, m1col_zero.multim1column),
        )


class _Inv(_acc.ActiveColumnsCell):
    def __init__(self, *,
        name: str, fab: "StdCellFactory",
        drive: int,
    ):
        assert drive >= 0
        # This needs to be set before calling __init__ of super class
        # as that will call build_generator method
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        ### nets

        i = ckt.new_net(name="i", external=True)
        nq = ckt.new_net(name="nq", external=True)

        ### columns and rows

        actcols: List[_acc.ActiveColumnT] = []
        polyknots: List[_acc.PolyKnotT] = []
        m1knots: List[_acc.M1KnotT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []

        # active columns
        w_size = "min" if self.drive == 0 else "max"

        def add_sdcol(*, n: int):
            col_name = f"sdcol[{n}]"
            if (n%2) == 0:
                # even columns => vss/vdd connections
                if self.drive <= 1:
                    vss_sd_name = "vss_sd"
                    vdd_sd_name = "vdd_sd"
                else:
                    vss_sd_name = f"vss_sd[{n//2}]"
                    vdd_sd_name = f"vdd_sd[{n//2}]"
                nsd = self.vss_sd(name=vss_sd_name)
                psd = self.vdd_sd(name=vdd_sd_name)
            else:
                # odd columns => nq outputs
                if self.drive <= 2:
                    nsd_name = "nq_nsd"
                    psd_name = "nq_psd"
                else:
                    nsd_name = f"nq_nsd[{n//2}]"
                    psd_name = f"nq_psd[{n//2}]"
                nsd = self.signal_nsd(name=nsd_name, net=nq, with_contact=True)
                psd = self.signal_psd(name=psd_name, net=nq, with_contact=True)

                if self.drive <= 2:
                    m1col_name = "nq_m1col"
                    m1col_elems = (nsd, psd)
                else:
                    m1col_name = f"nq_m1col[{n//2}]"
                    m1knot = self.m1knot(name=f"nq_m1knot[{n//2}]", net=nq)
                    m1col_elems = (nsd, m1knot, psd)
                    m1knots.append(m1knot)
                m1col = (self.m1pin if (n == 1) else self.m1column)(
                    name=m1col_name, elements=m1col_elems,
                )
                m1cols.append(m1col.multim1column)
            actcols.append(self.activecolumn(name=col_name, connect=False, elements=(nsd, psd)))

        def add_transcol(*, n: int):
            if self.drive <= 1:
                col_name = "transcol"
                nmos_name = "nmos"
                knot_name = "polyknot"
                pmos_name = "pmos"
            else:
                col_name = f"transcol[{n}]"
                nmos_name = f"nmos[{n}]"
                knot_name = f"polyknot[{n}]"
                pmos_name = f"pmos[{n}]"

            nmos = self.nmos(name=nmos_name, net=i, w_size=w_size)
            knot = self.polyknot(name=knot_name, net=i)
            pmos = self.pmos(name=pmos_name, net=i, w_size=w_size)

            actcols.append(self.activecolumn(
                name=col_name, connect=True,
                elements=(nmos, knot, pmos),
            ))
            polyknots.append(knot)

        n_fingers = max(1, self.drive) # also 1 finger if drive == 0
        for n in range(n_fingers):
            add_sdcol(n=n)
            add_transcol(n=n)
        add_sdcol(n=n_fingers)

        # polypad
        polypad = self.polypad(name="polypad", net=i)
        polyrow = self.polyrow(name="polyrow", elements=(polypad, *polyknots)).multipolyrow
        m1col = self.m1pin(name="i_m1col", elements=polypad)
        m1cols.insert(0, m1col.multim1column)

        return self.constraints(
            activecolumns=actcols,
            polyrows=polyrow,
            m1rows=(
                () if len(m1knots) == 0
                else self.m1row(name="m1_row", elements=m1knots).multim1row
            ),
            m1columns=m1cols,
        )


class _Buf(_acc.ActiveColumnsCell):
    def __init__(self, *,
        name: str, fab: "StdCellFactory",
        drive_first: int, drive_second: int,
    ):
        if drive_first > 1:
            raise NotImplementedError(
                "_Buf with more than one finger for first stage"
            )

        self._drive_first = drive_first
        self._drive_second = drive_second

        super().__init__(name=name, fab=fab)

    @property
    def drive_first(self) -> int:
        return self._drive_first
    @property
    def drive_second(self) -> int:
        return self._drive_second

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size_stage0: str = "min" if self.drive_first == 0 else "max"
        w_size_stage1: str = "min" if self.drive_second == 0 else "max"

        ### nets

        i = ckt.new_net(name="i", external=True)
        _i_n = ckt.new_net(name="_i_n", external=False)
        q = ckt.new_net(name="q", external=True)

        ### columns and rows

        actcols: List[_acc.ActiveColumnT] = []
        m1rows: List[_acc.MultiM1RowT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []
        in_polyrow_elems: List[_acc.PolyRowElementT] = []
        q_m1row_elems: List[_acc.M1RowElementT] = []

        # first stage

        # SDs
        nsd = self.signal_nsd(name="in_nsd", net=_i_n, with_contact=True)
        psd = self.signal_psd(name="in_psd", net=_i_n, with_contact=True)
        in_polypad = self.polypad(name="in_pad", net=_i_n)

        actcols.append(self.activecolumn(name="stage0_sd", connect=False, elements=(nsd, psd)))
        m1col = self.m1column(name="in_m1col", elements=(nsd, in_polypad, psd))
        m1cols.append(m1col.multim1column)
        in_polyrow_elems.append(in_polypad)

        # trans
        nmos = self.nmos(name="stage0_nmos", net=i, w_size=w_size_stage0)
        pmos = self.pmos(name="stage0_pmos", net=i, w_size=w_size_stage0)
        nmospad = self.polypad(name="stage0_nmospad", net=i)
        pmospad = self.polypad(name="stage0_pmospad", net=i)

        actcols.append(
            self.activecolumn(name="stage0_strans", connect=False, elements=(nmos, pmos)),
        )

        stage0_nmospolyrow = self.polyrow(
            name="stage0_nmospolyrow", elements=(nmos, nmospad)
        ).multipolyrow
        stage0_pmospolyrow = self.polyrow(
            name="stage0_pmospolyrow", elements=(pmos, pmospad)
        ).multipolyrow

        # vss/vdd sd

        if self.drive_second <= 1:
            actcols.append(self.activecolumn(name="dc_sd", connect=False, elements=(
                self.vss_sd(name="vss_sd"), self.vdd_sd(name="vdd_sd"),
            )))
        else:
            actcols.append(self.activecolumn(name="dc_sd", connect=False, elements=(
                self.vss_sd(name="vss_sd[0]"), self.vdd_sd(name="vdd_sd[0]"),
            )))

        m1col = self.m1pin(name="i_m1col", elements=(nmospad, pmospad))
        m1cols.append(m1col.multim1column)

        # second stage

        # SDs & transistors
        def add_sdcol(*, n: int):
            col_name = f"sdcol[{n}]"
            if (n%2) == 1:
                # odd columns => vss/vdd connections
                vss_sd_name = f"vss_sd[{n//2 + 1}]"
                vdd_sd_name = f"vdd_sd[{n//2 + 1}]"
                nsd = self.vss_sd(name=vss_sd_name)
                psd = self.vdd_sd(name=vdd_sd_name)
            else:
                # even columns => nq outputs
                if self.drive_second <= 2:
                    nsd_name = "q_nsd"
                    psd_name = "q_psd"
                else:
                    nsd_name = f"q_nsd[{n//2}]"
                    psd_name = f"q_psd[{n//2}]"
                nsd = self.signal_nsd(name=nsd_name, net=q, with_contact=True)
                psd = self.signal_psd(name=psd_name, net=q, with_contact=True)

                if self.drive_second <= 2:
                    m1col_name = "q_m1col"
                    m1col_elems = (nsd, psd)
                else:
                    m1col_name = f"nq_m1col[{n//2}]"
                    m1knot = self.m1knot(name=f"q_m1knot[{n//2}]", net=q)
                    m1col_elems = (nsd, m1knot, psd)
                    q_m1row_elems.append(m1knot)
                m1col = (self.m1pin if (n == 0) else self.m1column)(
                    name=m1col_name, elements=m1col_elems,
                )
                m1cols.append(m1col.multim1column)
            actcols.append(self.activecolumn(name=col_name, connect=False, elements=(nsd, psd)))

        def add_transcol(*, n: int):
            if self.drive_second <= 1:
                col_name = "transcol"
                nmos_name = "nmos"
                knot_name = "polyknot"
                pmos_name = "pmos"
            else:
                col_name = f"transcol[{n}]"
                nmos_name = f"nmos[{n}]"
                knot_name = f"polyknot[{n}]"
                pmos_name = f"pmos[{n}]"

            nmos = self.nmos(name=nmos_name, net=_i_n, w_size=w_size_stage1)
            knot = self.polyknot(name=knot_name, net=_i_n)
            pmos = self.pmos(name=pmos_name, net=_i_n, w_size=w_size_stage1)

            if n == 0:
                actcol = self.activecolumn(
                    name=col_name, connect=True,
                    elements=(nmos, knot, pmos),
                    left=(nmospad, pmospad),
                )
            else:
                actcol = self.activecolumn(
                    name=col_name, connect=True,
                    elements=(nmos, knot, pmos),
                )
            actcols.append(actcol)
            in_polyrow_elems.append(knot)

        for n in range(max(self.drive_second, 1)):
            add_transcol(n=n)
            add_sdcol(n=n)

        assert len(q_m1row_elems) != 1, "Internal error"
        if len(q_m1row_elems) > 1:
            m1row = self.m1row(name="q_m1row", elements=q_m1row_elems)
            m1rows.append(m1row.multim1row)
        in_polyrow = self.polyrow(
            name="i_n_polyrow", elements=in_polyrow_elems,
        ).multipolyrow
        polyrows = (stage0_nmospolyrow, in_polyrow, stage0_pmospolyrow)
        return self.constraints(
            activecolumns=actcols, polyrows=polyrows, m1rows=m1rows, m1columns=m1cols,
        )


class _Nand(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int, inputs: int):
        if inputs < 2:
            raise ValueError(f"Nand '{name}' with inputs < 2")
        if drive > 1:
            raise NotImplementedError(f"Nand '{name}' with drive > 1")

        self._drive = drive
        self._inputs = inputs
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive
    @property
    def inputs(self) -> int:
        return self._inputs

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        nq = ckt.new_net(name="nq", external=True)

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        nq_psds: List[_acc.SignalPSDT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []

        w_size = "min" if self.drive == 0 else "max"

        prev_transcol = None
        prev_polypad = None
        signal_psd0 = None
        for n in range(self.inputs):
            # SDs
            if n == 0:
                nsd = self.vss_sd(name="vss_sd")
            else:
                net_name = f"_net{n -1}"
                sd_net = ckt.new_net(name=net_name, external=False)
                nsd = self.signal_nsd(name=f"{net_name}_nsd", net=sd_net, with_contact=False)

            if n%2 == 0:
                psd = self.vdd_sd(name="vdd_sd")
            else:
                psd = self.signal_psd(
                    name=("nq_psd" if self.inputs <= 2 else f"nq_psd[{n//2}]"),
                    net=nq, with_contact=True
                )
                nq_psds.append(psd)

                if n == 1:
                    signal_psd0 = psd

            actcols.append(
                self.activecolumn(name=f"sdcol[{n}]", connect=False, elements=(nsd, psd)),
            )

            # i{n} trans
            net_name = f"i{n}"
            net = ckt.new_net(name=net_name, external=True)

            nmos = self.nmos(name=f"{net_name}_nmos", net=net, w_size=w_size)
            pmos = self.pmos(name=f"{net_name}_pmos", net=net, w_size=w_size)
            poly_knot = self.polyknot(name=f"{net_name}_polyknot", net=net)
            lefts = []
            if prev_transcol is not None:
                lefts.append(prev_transcol)
            if prev_polypad is not None:
                lefts.append(prev_polypad)
            poly_pad = self.polypad(
                name=f"{net_name}_polypad", net=net, left=lefts,
            )

            actcols.append(self.activecolumn(
                name=f"{net_name}_actcol", connect=True, elements=(nmos, poly_knot, pmos),
                left=(() if prev_polypad is None else prev_polypad),
            ))
            if n == 0:
                m1col = self.m1pin(name=f"{net_name}_pin", elements=poly_pad)
            else:
                assert signal_psd0 is not None, "Internal error"
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad, top=signal_psd0,
                )
            m1cols.append(m1col.multim1column)
            polyrow = self.polyrow(
                name=f"{net_name}_polyrow", elements=(poly_pad, poly_knot),
            )
            polyrows.append(polyrow)

            prev_transcol = actcols[-1]
            prev_polypad = poly_pad

        # Last SD
        nsd = self.signal_nsd(name="nq_nsd", net=nq, with_contact=True)
        if self.inputs%2 == 0:
            psd = self.vdd_sd(name=f"vdd_sd[{self.drive//2}]")
            m1_elem = self.m1knot(name="nq_m1knot", net=nq)
        else:
            psd = self.signal_psd(name=f"nq_psd[{self.drive//2}]", net=nq, with_contact=True)
            m1_elem = psd
        actcols.append(self.activecolumn(
            name="nq_actcol", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))
        m1rows = self.m1row(name="nq_m1row", elements=(*nq_psds, m1_elem)).multim1row

        m1col = self.m1pin(name="nq_pin", elements=(nsd, m1_elem))
        m1cols.append(m1col.multim1column)

        return self.constraints(
            activecolumns=actcols, polyrows=(
                self.multipolyrow(name="polyrow_even", rows=polyrows),
            ),
            m1rows=m1rows, m1columns=m1cols,
        )


class _And(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int, inputs: int):
        if inputs < 2:
            raise ValueError(f"And '{name}' with inputs < 2")
        if drive > 1:
            raise NotImplementedError(f"And '{name}' with drive > 1")

        self._drive = drive
        self._inputs = inputs
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive
    @property
    def inputs(self) -> int:
        return self._inputs

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        q = ckt.new_net(name="q", external=True)
        nq = ckt.new_net(name="nq", external=False)

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        nq_psds: List[_acc.SignalPSDT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []

        w_size = "min" if self.drive == 0 else "max"

        prev_transcol = None
        prev_poly_pad = None
        signal_psd0 = None
        nq_nsd = None
        for n in range(self.inputs):
            # SDs
            if n == 0:
                nq_nsd = nsd = self.signal_nsd(name="nq_nsd", net=nq, with_contact=True)
            else:
                net_name = f"_net{n -1}"
                sd_net = ckt.new_net(name=net_name, external=False)
                nsd = self.signal_nsd(name=f"{net_name}_nsd", net=sd_net, with_contact=False)
            assert nq_nsd is not None

            if (self.inputs - n)%2 == 0:
                psd = self.vdd_sd(name="vdd_sd")
            else:
                psd = self.signal_psd(
                    name=("nq_psd" if self.inputs <= 2 else f"nq_psd[{n//2}]"),
                    net=nq, with_contact=True
                )
                nq_psds.append(psd)
                if signal_psd0 is None:
                    signal_psd0 = psd

            actcols.append(
                self.activecolumn(name=f"sdcol[{n}]", connect=False, elements=(nsd, psd)),
            )

            # i{n} trans
            net_name = f"i{n}"
            net = ckt.new_net(name=net_name, external=True)

            nmos = self.nmos(name=f"{net_name}_nmos", net=net, w_size="min")
            pmos = self.pmos(name=f"{net_name}_pmos", net=net, w_size="min")
            poly_knot = self.polyknot(name=f"{net_name}_polyknot", net=net)
            lefts = []
            if prev_transcol is not None:
                lefts.append(prev_transcol)
            if prev_poly_pad is not None:
                lefts.append(prev_poly_pad)
            poly_pad = self.polypad(
                name=f"{net_name}_polypad", net=net, left=lefts
            )

            actcols.append(self.activecolumn(
                name=f"{net_name}_actcol", connect=True, elements=(nmos, poly_knot, pmos),
                left=(() if prev_poly_pad is None else prev_poly_pad),
            ))
            if signal_psd0 is None:
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad, bottom=nq_nsd,
                )
            else:
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad,
                    bottom=nq_nsd, top=signal_psd0,
                )
            m1cols.append(m1col.multim1column)
            polyrow = self.polyrow(
                name=f"{net_name}_polyrow", elements=(poly_pad, poly_knot),
            )
            polyrows.append(polyrow)

            prev_transcol = actcols[-1]
            prev_poly_pad = poly_pad
        assert nq_nsd is not None
        assert prev_transcol is not None, "Internal error"
        assert prev_poly_pad is not None, "Internal error"

        # Last NAND2 SD
        nsd = self.vss_sd(name="vss_sd")
        psd = self.vdd_sd(name=f"vdd_sd[{self.drive//2}]")
        nq_m1knot0 = self.m1knot(name="nq_m1knot0", net=nq)
        nq_m1knot1 = self.m1knot(name="nq_m1knot1", net=nq)
        actcols.append(self.activecolumn(
            name="dc_actcol", connect=False, elements=(nsd, psd),
        ))
        m1rows = (
            self.m1row(name="nq_m1row0", elements=(nq_nsd, nq_m1knot0)).multim1row,
            self.m1row(name="nq_m1row1", elements=(*nq_psds, nq_m1knot1)).multim1row,
        )

        # nq inverter
        nmos = self.nmos(name="n_pd", net=nq, w_size=w_size)
        pmos = self.pmos(name="q_pu", net=nq, w_size=w_size)
        nq_polyknot = self.polyknot(name="nq_polyknot", net=nq)
        actcols.append(self.activecolumn(
            name="nq_inv", connect=True, elements=(nmos, nq_polyknot, pmos),
            left=prev_poly_pad,
        ))

        nq_polypad = self.polypad(name="nq_polypad", net=nq, left=(prev_transcol, prev_poly_pad))
        polyrow = self.polyrow(
            name=f"nq_polyrow", elements=(nq_polypad, nq_polyknot),
        )
        polyrows.append(polyrow)

        m1col = self.m1column(
            name="nq_pin", elements=(nq_m1knot0, nq_polypad, nq_m1knot1),
        )
        m1cols.append(m1col.multim1column)

        # q sds
        nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        psd = self.signal_psd(name="q_psd", net=q, with_contact=True)
        actcols.append(self.activecolumn(
            name="q_sds", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))
        m1col = self.m1pin(name="q_pin", elements=(nsd, psd))
        m1cols.append(m1col.multim1column)

        return self.constraints(
            activecolumns=actcols,
            polyrows=self.multipolyrow(name="polyrow", rows=polyrows),
            m1rows=m1rows, m1columns=m1cols,
        )


class _Nor(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int, inputs: int):
        if drive > 1:
            raise NotImplementedError(f"Nor '{name}' with drive > 1")
        if inputs < 2:
            raise ValueError(f"Nor '{name}' with inputs < 2")

        self._drive = drive
        self._inputs = inputs
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive
    @property
    def inputs(self) -> int:
        return self._inputs

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        nq = ckt.new_net(name="nq", external=True)

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        nq_nsds: List[_acc.SignalNSDT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []

        w_size = "min" if self.drive == 0 else "max"

        prev_transcol = None
        prev_polypad = None
        signal_nsd0 = None
        for n in range(self.inputs):
            # SDs
            if n%2 == 0:
                nsd = self.vss_sd(name=f"vss_sd[{n//2}]")
            else:
                nsd = self.signal_nsd(
                    name=("nq_psd" if self.inputs <= 2 else f"nq_psd[{n//2}]"),
                    net=nq, with_contact=True
                )
                nq_nsds.append(nsd)

                if n == 1:
                    signal_nsd0 = nsd

            if n == 0:
                psd = self.vdd_sd(name="vdd_sd")
            else:
                net_name = f"_net{n - 1}"
                sd_net = ckt.new_net(name=net_name, external=False)
                psd = self.signal_psd(name=f"{net_name}_psd", net=sd_net, with_contact=False)


            actcols.append(
                self.activecolumn(name=f"sdcol[{n}]", connect=False, elements=(nsd, psd)),
            )

            # i{n} trans
            net_name = f"i{n}"
            net = ckt.new_net(name=net_name, external=True)

            nmos = self.nmos(name=f"{net_name}_nmos", net=net, w_size=w_size)
            pmos = self.pmos(name=f"{net_name}_pmos", net=net, w_size=w_size)
            poly_knot = self.polyknot(name=f"{net_name}_polyknot", net=net)
            lefts = []
            if prev_transcol is not None:
                lefts.append(prev_transcol)
            if prev_polypad is not None:
                lefts.append(prev_polypad)
            poly_pad = self.polypad(
                name=f"{net_name}_polypad", net=net, left=lefts,
            )

            actcols.append(self.activecolumn(
                name=f"{net_name}_actcol", connect=True, elements=(nmos, poly_knot, pmos),
                left=(() if prev_polypad is None else prev_polypad),
            ))
            if n == 0:
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad,
                )
            else:
                assert signal_nsd0 is not None, "Internal error"
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad,
                    bottom=signal_nsd0,
                )
            m1cols.append(m1col.multim1column)
            polyrow = self.polyrow(
                name=f"{net_name}_polyrow", elements=(poly_pad, poly_knot),
            )
            polyrows.append(polyrow)

            prev_transcol = actcols[-1]
            prev_polypad = poly_pad

        # Last SD
        if self.inputs%2 == 0:
            nsd = self.vss_sd(name=f"vss_sd[{self.drive//2}]")
            m1_elem = self.m1knot(name="nq_m1knot", net=nq)
        else:
            nsd = self.signal_nsd(name=f"nq_nsd[{self.drive//2}]", net=nq, with_contact=True)
            m1_elem = nsd
        psd = self.signal_psd(name="nq_psd", net=nq, with_contact=True)
        actcols.append(self.activecolumn(
            name="nq_actcol", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))
        m1rows = self.m1row(name="nq_m1row", elements=(*nq_nsds, m1_elem)).multim1row

        m1col = self.m1pin(name="nq_pin", elements=(m1_elem, psd))
        m1cols.append(m1col.multim1column)

        return self.constraints(
            activecolumns=actcols, polyrows=(
                self.multipolyrow(name="polyrow_even", rows=polyrows),
            ),
            m1rows=m1rows, m1columns=m1cols,
        )


class _Or(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int, inputs: int):
        if inputs < 2:
            raise ValueError(f"Or '{name}' with inputs < 2")
        if drive > 1:
            raise NotImplementedError(f"Or '{name}' with drive > 1")

        self._drive = drive
        self._inputs = inputs
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive
    @property
    def inputs(self) -> int:
        return self._inputs

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        q = ckt.new_net(name="q", external=True)
        nq = ckt.new_net(name="nq", external=False)

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        nq_nsds: List[_acc.SignalNSDT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []

        w_size = "min" if self.drive == 0 else "max"

        prev_transcol = None
        prev_poly_pad = None
        signal_nsd0 = None
        nq_psd = None
        for n in range(self.inputs):
            # SDs
            if (self.inputs - n)%2 == 0:
                nsd = self.vss_sd(name="vss_sd")
            else:
                nsd = self.signal_nsd(
                    name=("nq_nsd" if self.inputs <= 2 else f"nq_nsd[{n//2}]"),
                    net=nq, with_contact=True
                )
                nq_nsds.append(nsd)
                if signal_nsd0 is None:
                    signal_nsd0 = nsd

            if n == 0:
                nq_psd = psd = self.signal_psd(name="nq_psd", net=nq, with_contact=True)
            else:
                net_name = f"_net{n -1}"
                sd_net = ckt.new_net(name=net_name, external=False)
                psd = self.signal_psd(name=f"{net_name}_nsd", net=sd_net, with_contact=False)
            assert nq_psd is not None

            actcols.append(
                self.activecolumn(name=f"sdcol[{n}]", connect=False, elements=(nsd, psd)),
            )

            # i{n} trans
            net_name = f"i{n}"
            net = ckt.new_net(name=net_name, external=True)

            nmos = self.nmos(name=f"{net_name}_nmos", net=net, w_size="min")
            pmos = self.pmos(name=f"{net_name}_pmos", net=net, w_size="min")
            poly_knot = self.polyknot(name=f"{net_name}_polyknot", net=net)
            lefts = []
            if prev_transcol is not None:
                lefts.append(prev_transcol)
            if prev_poly_pad is not None:
                lefts.append(prev_poly_pad)
            poly_pad = self.polypad(
                name=f"{net_name}_polypad", net=net, left=lefts,
            )

            actcols.append(self.activecolumn(
                name=f"{net_name}_actcol", connect=True, elements=(nmos, poly_knot, pmos),
                left=(() if prev_poly_pad is None else prev_poly_pad),
            ))
            if signal_nsd0 is None:
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad,
                    top=nq_psd
                )
            else:
                m1col = self.m1pin(
                    name=f"{net_name}_pin", elements=poly_pad,
                    bottom=signal_nsd0, top=nq_psd,
                )
            m1cols.append(m1col.multim1column)
            polyrow = self.polyrow(
                name=f"{net_name}_polyrow", elements=(poly_pad, poly_knot),
            )
            polyrows.append(polyrow)

            prev_transcol = actcols[-1]
            prev_poly_pad = poly_pad
        assert nq_psd is not None, "Internal error"
        assert prev_transcol is not None, "Internal error"
        assert prev_poly_pad is not None, "Internal error"

        # Last NAND2 SD
        nsd = self.vss_sd(name=f"vss_sd[{self.drive//2}]")
        psd = self.vdd_sd(name=f"vdd_sd")
        nq_m1knot0 = self.m1knot(name="nq_m1knot0", net=nq)
        nq_m1knot1 = self.m1knot(name="nq_m1knot1", net=nq)
        actcols.append(self.activecolumn(
            name="dc_actcol", connect=False, elements=(nsd, psd),
        ))
        m1rows = (
            self.m1row(name="nq_m1row0", elements=(*nq_nsds, nq_m1knot0)).multim1row,
            self.m1row(name="nq_m1row1", elements=(nq_psd, nq_m1knot1)).multim1row,
        )

        # nq inverter
        nmos = self.nmos(name="n_pd", net=nq, w_size=w_size)
        pmos = self.pmos(name="q_pu", net=nq, w_size=w_size)
        nq_polyknot = self.polyknot(name="nq_polyknot", net=nq)
        actcols.append(self.activecolumn(
            name="nq_inv", connect=True, elements=(nmos, nq_polyknot, pmos),
            left=prev_poly_pad,
        ))

        nq_polypad = self.polypad(name="nq_polypad", net=nq, left=(prev_transcol, prev_poly_pad))
        polyrow = self.polyrow(
            name=f"nq_polyrow", elements=(nq_polypad, nq_polyknot),
        )
        polyrows.append(polyrow)

        m1col = self.m1column(
            name="nq_pin", elements=(nq_m1knot0, nq_polypad, nq_m1knot1),
        )
        m1cols.append(m1col.multim1column)

        # q sds
        nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        psd = self.signal_psd(name="q_psd", net=q, with_contact=True)
        actcols.append(self.activecolumn(
            name="q_sds", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))
        m1col = self.m1pin(name="q_pin", elements=(nsd, psd))
        m1cols.append(m1col.multim1column)

        return self.constraints(
            activecolumns=actcols,
            polyrows=self.multipolyrow(name="polyrows", rows=polyrows),
            m1rows=m1rows, m1columns=m1cols,
        )


class _And21Nor(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int):
        if drive > 1:
            raise NotImplementedError(f"And21Nor cell '{name}' with drive > 1")
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size = "min" if self.drive == 0 else "max"

        ### nets

        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        nq = ckt.new_net(name="nq", external=True)

        ### elems

        vss_sd0 = self.vss_sd(name="vss_sd0")
        vss_sd1 = self.vss_sd(name="vss_sd1")

        vdd_sd = self.vdd_sd(name="vdd_sd")

        net0_psd0 = self.signal_psd(name="net0_psd0", net=_net0, with_contact=True)
        net0_psd1 = self.signal_psd(name="net0_psd0", net=_net0, with_contact=True)

        net1_nsd = self.signal_nsd(name="net1_nsd", net=_net1, with_contact=False)

        nq_nsd = self.signal_nsd(name="nq_nsd", net=nq, with_contact=True)
        nq_psd = self.signal_psd(name="nq_psd", net=nq, with_contact=True)
        nq_m1knot = self.m1knot(name="nq_m1knot", net=nq)

        nsds = (vss_sd0, net1_nsd, nq_nsd, vss_sd1)
        psds = (net0_psd0, vdd_sd, net0_psd1, nq_psd)

        ## columns and rows

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []
        prev_polypad: Optional[_acc.PolyContactT] = None
        for n in range(3):
            nsd = nsds[n]
            psd = psds[n]
            args = {
                "name": "sds[{n}]",
                "connect": False,
                "elements": (nsd, psd)
            }
            if n == 2:
                assert prev_polypad is not None
                args["left"] = prev_polypad
            actcols.append(self.activecolumn(**args))

            i = ckt.new_net(name=f"i{n}", external=True)

            nmos = self.nmos(name=f"i{n}_nmos", net=i, w_size=w_size)
            pmos = self.pmos(name=f"i{n}_pmos", net=i, w_size=w_size)
            polyknot = self.polyknot(name=f"i{0}_polyknot", net=i)
            actcols.append(self.activecolumn(
                name=f"i{n}_trans", connect=True, elements=(nmos, polyknot, pmos),
            ))

            args = {
                "name": f"i{n}_polypad",
                "net": i,
            }
            if n > 0:
                assert prev_polypad is not None
                args["left"] = (actcols[-3], prev_polypad)
            polypad = self.polypad(**args)
            polyrows.append(self.polyrow(name=f"i{n}_polyrow", elements=(polypad, polyknot)))

            args = {
                "name": f"i{n}_pin",
                "elements": polypad,
            }
            if n < 2:
                args["top"] = nq_psd
            else:
                assert n == 2
                args["bottom"] = nq_nsd
                args["left"] = actcols[-2]
            m1cols.append(self.m1pin(**args).multim1column)

            prev_polypad = polypad
        nsd = nsds[3]
        psd = psds[3]
        actcols.append(self.activecolumn(
            name=f"sds[{3}]", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))

        m1col = self.m1pin(name="nq_pin", elements=(nq_m1knot, nq_psd))
        m1cols.append(m1col.multim1column)

        m1rows = (
            self.m1row(name="nq_m1row", elements=(nq_nsd, nq_m1knot)).multim1row,
            self.m1row(name="net0_m1row", elements=(net0_psd0, net0_psd1)).multim1row,
        )

        ### Constraints

        return self.constraints(
            activecolumns=actcols,
            polyrows=(
                self.multipolyrow(name="mpolyrow0", rows=polyrows),
            ),
            m1rows=m1rows,
            m1columns=m1cols,
        )


class _Or21Nand(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int):
        if drive > 1:
            raise NotImplementedError(f"Or21Nand cell '{name}' with drive > 1")
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size = "min" if self.drive == 0 else "max"

        ### nets

        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        nq = ckt.new_net(name="nq", external=True)

        ### elems

        vdd_sd0 = self.vdd_sd(name="vdd_sd0")
        vdd_sd1 = self.vdd_sd(name="vdd_sd1")

        vss_sd = self.vss_sd(name="vss_sd")

        net0_nsd0 = self.signal_nsd(name="net0_nsd0", net=_net0, with_contact=True)
        net0_nsd1 = self.signal_nsd(name="net0_nsd0", net=_net0, with_contact=True)

        net1_psd = self.signal_psd(name="net1_psd", net=_net1, with_contact=False)

        nq_nsd = self.signal_nsd(name="nq_nsd", net=nq, with_contact=True)
        nq_psd = self.signal_psd(name="nq_psd", net=nq, with_contact=True)
        nq_m1knot = self.m1knot(name="nq_m1knot", net=nq)

        nsds = (net0_nsd0, vss_sd, net0_nsd1, nq_nsd)
        psds = (vdd_sd0, net1_psd, nq_psd, vdd_sd1)

        ## columns and rows

        actcols: List[_acc.ActiveColumnT] = []
        polyrows: List[_acc.PolyRowT] = []
        m1cols: List[_acc.MultiM1ColumnT] = []
        prev_polypad: Optional[_acc.PolyContactT] = None
        for n in range(3):
            nsd = nsds[n]
            psd = psds[n]
            args = {
                "name": f"sds[{n}]",
                "connect": False,
                "elements": (nsd, psd),
            }
            if n == 2:
                assert prev_polypad is not None
                args["left"] = prev_polypad
            actcols.append(self.activecolumn(**args))

            i = ckt.new_net(name=f"i{n}", external=True)

            nmos = self.nmos(name=f"i{n}_nmos", net=i, w_size=w_size)
            pmos = self.pmos(name=f"i{n}_pmos", net=i, w_size=w_size)
            polyknot = self.polyknot(name=f"i{0}_polyknot", net=i)
            actcols.append(self.activecolumn(
                name=f"i{n}_trans", connect=True, elements=(nmos, polyknot, pmos),
            ))

            args = {
                "name": f"i{n}_polypad",
                "net": i,
            }
            if n > 0:
                assert prev_polypad is not None
                args["left"] = (actcols[-3], prev_polypad)
            polypad = self.polypad(**args)
            polyrows.append(self.polyrow(name=f"i{n}_polyrow", elements=(polypad, polyknot)))

            args = {
                "name": f"i{n}_pin",
                "elements": polypad,
            }
            if n < 2:
                args["bottom"] = nq_nsd
            else:
                assert n == 2
                args["top"] = nq_psd
                args["left"] = actcols[-2]
            m1cols.append(self.m1pin(**args).multim1column)

            prev_polypad = polypad
        nsd = nsds[3]
        psd = psds[3]
        actcols.append(self.activecolumn(
            name=f"sds[{3}]", connect=False, elements=(nsd, psd), left=m1cols[-1],
        ))

        m1col = self.m1pin(name="nq_pin", elements=(nq_nsd, nq_m1knot))
        m1cols.append(m1col.multim1column)

        m1rows = (
            self.m1row(name="net0_m1row", elements=(net0_nsd0, net0_nsd1)).multim1row,
            self.m1row(name="nq_m1row", elements=(nq_psd, nq_m1knot)).multim1row,
        )

        ### Constraints

        return self.constraints(
            activecolumns=actcols,
            polyrows=(
                self.multipolyrow(name="mpolyrow0", rows=polyrows),
            ),
            m1rows=m1rows,
            m1columns=m1cols,
        )


class _Mux2(_acc.ActiveColumnsCell):
    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        ### nets

        i0 = ckt.new_net(name="i0", external=True)
        i1 = ckt.new_net(name="i1", external=True)
        cmd = ckt.new_net(name="cmd", external=True)
        q = ckt.new_net(name="q", external=True)

        _cmd_n = ckt.new_net(name="cmd_n", external=False)
        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        _net2 = ckt.new_net(name="_net2", external=False)
        _net3 = ckt.new_net(name="_net3", external=False)
        _q_n = ckt.new_net(name="_q_n", external=False)

        ### sd and mos elements and activecolumns

        actcols: List[_acc.ActiveColumnT] = []

        # cmd_n sds
        cmd_n_nsd = self.signal_nsd(name="cmd_n_nsd", net=_cmd_n, with_contact=True)
        cmd_n_psd = self.signal_psd(name="cmd_n_psd", net=_cmd_n, with_contact=True)
        actcols.append(self.activecolumn(
            name="cmd_n_sds", connect=False, elements=(cmd_n_nsd, cmd_n_psd),
        ))

        # cmd inverter
        cmd_inv_nmos = self.nmos(name="cmd_inv_nmos", net=cmd, w_size="min")
        cmd_inv_pmos = self.pmos(name="cmd_inv_pmos", net=cmd, w_size="min")
        cmd_inv_polyknot = self.polyknot(name="cmd_polyknot", net=cmd)
        cmd_inv = self.activecolumn(
            name="cmd_inv", connect=True, elements=(cmd_inv_nmos, cmd_inv_polyknot, cmd_inv_pmos),
        )
        actcols.append(cmd_inv)

        # vss/vdd sd0
        vss_sd0 = self.vss_sd(name="vss_sd0")
        vdd_sd0 = self.vdd_sd(name="vdd_sd0")
        actcols.append(self.activecolumn(
            name="dc_sd0", connect=False, elements=(vss_sd0, vdd_sd0),
        ))

        # i0 transistors
        i0_nmos = self.nmos(name="i0_nmos", net=i0, w_size="min")
        i0_pmos = self.pmos(name="i0_pmos", net=i0, w_size="min")
        i0_trans = self.activecolumn(
            name="i0_trans", connect=False, elements=(i0_nmos, i0_pmos),
        )
        actcols.append(i0_trans)

        # Connection sds0
        _net0_nsd = self.signal_nsd(name="_net0_nsd", net=_net0, with_contact=False)
        _net1_psd = self.signal_psd(name="_net1_psd", net=_net1, with_contact=False)
        actcols.append(self.activecolumn(
            name="conn_sd0", connect=False, elements=(_net0_nsd, _net1_psd)),
        )

        # cmd_n nmos & cmd pmos
        i0_nmospad = self.polypad(name="i0_nmospad", net=i0, left=cmd_inv)
        i0_pmospad = self.polypad(name="i0_pmospad", net=i0, left=cmd_inv)
        cmd_n_npasspad = self.polypad(
            name="cmd_n_npasspad", net=_cmd_n, left=(i0_trans, i0_nmospad),
        )
        cmd_n_npass=self.nmos(name="cmd_n_npass", net=_cmd_n, w_size="min")
        cmd_ppass=self.pmos(name="cmd_ppass", net=cmd, w_size="min")

        passtrans0 = self.activecolumn(
            name="passtrans0", connect=False, elements=(cmd_n_npass, cmd_ppass),
            left=(i0_nmospad, i0_pmospad),
        )
        actcols.append(passtrans0)

        # _q_n sds
        q_n_nsd = self.signal_nsd(name="q_n_nsd", net=_q_n, with_contact=True)
        q_n_psd = self.signal_psd(name="q_n_psd", net=_q_n, with_contact=True)
        actcols.append(self.activecolumn(
            name="_q_n_sd", connect=False, elements=(q_n_nsd, q_n_psd), left=cmd_n_npasspad,
        ))

        # cmd nmos & cmd_n pmos
        cmd_npass = self.nmos(name="cmd_npass", net=cmd, w_size="min")
        cmd_n_ppass = self.pmos(name="cmd_n_ppass", net=_cmd_n, w_size="min")
        passtrans1 = self.activecolumn(
            name="passtrans1", connect=False, elements=(cmd_npass, cmd_n_ppass),
        )
        actcols.append(passtrans1)

        # Connection sds1
        _net2_nsd = self.signal_nsd(name="_net2_nsd", net=_net2, with_contact=False)
        _net3_psd = self.signal_psd(name="_net3_psd", net=_net3, with_contact=False)
        actcols.append(self.activecolumn(
            name="conn_sd1", connect=False, elements=(_net2_nsd, _net3_psd)),
        )

        # i1 transistors
        i1_pad = self.polypad(name="i1_pad", net=i1, left=passtrans1)
        i1_polyknot = self.polyknot(name="i1_polyknot", net=i1)
        i1_nmos = self.nmos(name="i1_nmos", net=i1, w_size="min")
        i1_pmos = self.pmos(name="i1_pmos", net=i1, w_size="min")

        i1_trans = self.activecolumn(
            name="i1_trans", connect=True, elements=(i1_nmos, i1_polyknot, i1_pmos),
        )
        actcols.append(i1_trans)

        # vss/vdd sd1
        vss_sd1 = self.vss_sd(name="vss_sd1")
        vdd_sd1 = self.vdd_sd(name="vdd_sd1")
        actcols.append(self.activecolumn(
            name="dc_sd1", connect=False, elements=(vss_sd1, vdd_sd1),
        ))

        # q_n inverter
        q_n_inv_nmos = self.nmos(name="q_n_inv_nmos", net=_q_n, w_size="max")
        q_n_inv_pmos = self.pmos(name="q_n_inv_pmos", net=_q_n, w_size="max")
        q_n_polypad = self.polypad(name="q_n_polypad", net=_q_n, left=i1_trans)
        q_n_inv_polyknot = self.polyknot(name="cmd_polyknot", net=_q_n)
        q_n_inv = self.activecolumn(
            name="q_n_inv", connect=True,
            elements=(q_n_inv_nmos, q_n_inv_polyknot, q_n_inv_pmos),
        )
        actcols.append(q_n_inv)

        # q sds
        q_nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        q_psd = self.signal_psd(name="q_psd", net=q, with_contact=True)
        actcols.append(self.activecolumn(
            name="q_sd", connect=False, elements=(q_nsd, q_psd),
            left=q_n_polypad,
        ))

        ### poly rows

        # cmd_n polyrows
        cmd_n_ppasspad = self.polypad(name="cmd_n_ppasspad", net=_cmd_n, left=passtrans0)

        cmd_n_npasspolyrow = self.polyrow(
            name="cmd_n_npasspolyrow", elements=(cmd_n_npasspad, cmd_n_npass),
        )
        cmd_n_ppasspolyrow = self.polyrow(
            name="cmd_n_ppasspolyrow", elements=(cmd_n_ppass, cmd_n_ppasspad),
        )

        # cmd polyrow
        cmd_polypad = self.polypad(name="cmd_polypad", net=cmd)

        cmd_polyrow = self.polyrow(
            name="cmd_polyrow", elements=(cmd_inv_polyknot, cmd_polypad, cmd_ppass, cmd_npass),
        )

        # _q_n_polyrow
        q_n_polyrow = self.polyrow(
            name="q_n_polyrow", elements=(q_n_polypad, q_n_inv_polyknot),
        )

        # i0 polyrows
        i0_nmospolyrow = self.polyrow(name="i0_nmospolyrow", elements=(i0_nmospad, i0_nmos))
        i0_pmospolyrow = self.polyrow(name="i0_pmospolyrow", elements=(i0_pmospad, i0_pmos))

        # i1 polyrows
        i1_polyrow = self.polyrow(name="i1_polyrow", elements=(i1_polyknot, i1_pad))

        ### m1 rows and columns

        # cmd_n columns & rows
        cmd_n_m1knot0 = self.m1knot(name="cmd_n_m1knot0", net=_cmd_n)
        cmd_n_m1knot1 = self.m1knot(name="cmd_n_m1knot1", net=_cmd_n)

        cmd_n_m1col0 = self.m1column(
            name="cmd_n_m1col0", elements=(cmd_n_nsd, cmd_n_psd),
        )
        cmd_n_m1row0 = self.m1row(
            name="cmd_n_m1row0", elements=(cmd_n_nsd, cmd_n_m1knot0),
        )
        cmd_n_m1col1 = self.m1column(
            name="cmd_n_m1col1", elements=(cmd_n_m1knot0, cmd_n_npasspad, cmd_n_m1knot1),
        )
        cmd_n_m1row1 = self.m1row(
            name="cmd_n_m1row1", elements=(cmd_n_m1knot1, cmd_n_ppasspad),
        )

        # q_n columns & rows
        q_n_m1knot0 = self.m1knot(name="q_n_m1knot0", net=_q_n)
        q_n_m1knot1 = self.m1knot(name="q_n_m1knot1", net=_q_n)

        q_n_m1row0 = self.m1row(
            name="q_n_m1row0", elements=(q_n_nsd, q_n_m1knot0),
        )
        q_n_m1row1 = self.m1row(
            name="q_n_m1row1", elements=(q_n_psd, q_n_m1knot1),
        )
        q_n_m1col = self.m1column(
            name="q_n_m1col", elements=(q_n_m1knot0, q_n_polypad, q_n_m1knot1),
        )

        # cmd pin
        cmd_pin = self.m1pin(
            name="cmd_pin", elements=cmd_polypad, bottom=cmd_n_nsd,
        )

        # i0 pin
        i0_pin = self.m1pin(
            name="i0_pin", elements=(i0_nmospad, i0_pmospad), bottom=cmd_n_nsd,
        )

        # i1 pin
        i1_pin = self.m1pin(
            name="i1_pin", elements=i1_pad, bottom=q_n_nsd, top=q_n_psd,
        )

        # q pin
        q_pin = self.m1pin(name="q_pin", elements=(q_nsd, q_psd))

        ### constraints

        polyrows = (
            self.multipolyrow(
                name="polyrow1", rows=(i0_nmospolyrow, cmd_n_npasspolyrow, i1_polyrow),
            ),
            self.multipolyrow(
                name="polyrow2", rows=(cmd_polyrow, q_n_polyrow),
            ),
            self.multipolyrow(
                name="polyrow3", rows=(i0_pmospolyrow, cmd_n_ppasspolyrow),
            ),
        )

        m1rows = (
            self.multim1row(name="nsd_m1row", rows=(cmd_n_m1row0, q_n_m1row0)),
            cmd_n_m1row1.multim1row, q_n_m1row1.multim1row,
        )

        m1cols = (
            cmd_n_m1col0.multim1column,
            cmd_pin.multim1column,
            i0_pin.multim1column,
            cmd_n_m1col1.multim1column,
            i1_pin.multim1column,
            q_n_m1col.multim1column,
            q_pin.multim1column,
        )

        return self.constraints(
            activecolumns=actcols,
            polyrows=polyrows,
            m1rows=m1rows,
            m1columns=m1cols,
        )


class _Xor2(_acc.ActiveColumnsCell):
    """Cell vor xor or nexor gate."""
    def __init__(self, *,
        name: str, fab: "StdCellFactory",
        inverted: bool, drive: int,
    ):
        if drive > 0:
            raise NotImplementedError("_Xor with drive > 0")
        self._drive = drive
        self._inverted = inverted
        super().__init__(name=name, fab=fab)

    @property
    def inverted(self) -> bool:
        return self._inverted
    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        ### nets

        i0 = ckt.new_net(name="i0", external=True)
        i1 = ckt.new_net(name="i1", external=True)
        # Use always same variable but let real name depend on wether it is inverted
        q = ckt.new_net(name=("q" if not self.inverted else "nq"), external=True)

        _i0_n = ckt.new_net(name="i0_n", external=False)
        _i1_n = ckt.new_net(name="i1_n", external=False)

        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        _net2 = ckt.new_net(name="_net2", external=False)

        ### build up active columns from left to right
        ### create elements as needed

        i0_n_nsd = self.signal_nsd(name="i0_n_nsd", net=_i0_n, with_contact=True)
        i0_n_psd = self.signal_psd(name="i0_n_psd", net=_i0_n, with_contact=True)
        i0_n_pad = self.polypad(name="i0_n_pad", net=_i0_n)
        i0_n_sds = self.activecolumn(name="i0_n_sds", connect=False, elements=(i0_n_nsd, i0_n_psd))
        i0_n_m1col = self.m1column(
            name="i0_n_m1col", elements=(i0_n_nsd, i0_n_pad, i0_n_psd),
        )

        i0_nmos0 = self.nmos(name="i0_nmos0", net=i0, w_size="min")
        i0_pmos0 = self.pmos(name="i0_pmos0", net=i0, w_size="min")
        i0_inv = self.activecolumn(
            name="i0_inv", connect=False, elements=(i0_nmos0, i0_pmos0),
        )

        i0_nmospad = self.polypad(name="i0_nmospad", net=i0)
        i0_pmospad = self.polypad(name="i0_pmospad", net=i0)
        i0_pin = self.m1pin(name="i0_pin", elements=(i0_nmospad, i0_pmospad))

        vss_sd0 = self.vss_sd(name="vss_sd0")
        vdd_sd0 = self.vdd_sd(name="vdd_sd0")
        vssvdd_sds0 = self.activecolumn(
            name="vssvdd_sds0", connect=False, elements=(vss_sd0, vdd_sd0),
        )

        i0_nmos1 = self.nmos(name="i0_nmos1", net=i0, w_size="min")
        i0_pmos1 = self.pmos(name="i0_pmos1", net=i0, w_size="min")
        i0_pass0 = self.activecolumn(
            name="i0_pass0", connect=False, elements=(i0_nmos1, i0_pmos1),
        )
        i0_nmosrow = self.polyrow(
            name="i0_nmosrow", elements=(i0_nmos0, i0_nmospad, i0_nmos1),
        )
        i0_pmosrow = self.polyrow(
            name="i0_pmosrow", elements=(i0_pmos0, i0_pmospad, i0_pmos1),
        )

        net0_nsd = self.signal_nsd(name="net0_nsd", net=_net0, with_contact=False)
        net1_psd0 = self.signal_psd(name="net1_psd0", net=_net1, with_contact=True)
        net01_sds = self.activecolumn(
            name="net01_sds", connect=False, elements=(net0_nsd, net1_psd0),
        )

        q_m1knot0 = self.m1knot(name="q_m1knot0", net=q)
        q_m1knot1 = self.m1knot(name="q_m1knot1", net=q)
        q_pin = self.m1pin(
            name="q_pin", elements=(q_m1knot0, q_m1knot1), top=net1_psd0,
        )

        i1_nmos0: Optional[_acc.NMOST] = None
        i1_nmos0pad: Optional[_acc.PolyContactT] = None
        i1_nmospad: Optional[_acc.PolyContactT] = None
        i1_pmos0: Optional[_acc.PMOST] = None
        i1_pmos0pad: Optional[_acc.PolyContactT] = None
        i1_n_nmos: Optional[_acc.NMOST] = None
        i1_n_nmospad: Optional[_acc.PolyContactT] = None
        i1_n_pmos: Optional[_acc.PMOST] = None
        i1_n_pmospad: Optional[_acc.PolyContactT] = None
        i1_nmosrow0: Optional[_acc.PolyRowT] = None
        i1_nmosrow1: Optional[_acc.PolyRowT] = None
        i1_pmosrow0: Optional[_acc.PolyRowT] = None
        i1_pmosrow1: Optional[_acc.PolyRowT] = None

        if not self.inverted:
            i1_nmos0 = self.nmos(name="i1_nmos0", net=i1, w_size="min")
            i1_nmos0pad = self.polypad(
                name="i1_nmos0pad", net=i1, left=(i0_pass0, q_pin),
            )
            i1_nmosrow0 = self.polyrow(
                name="i1_nmos0row", elements=(i1_nmos0pad, i1_nmos0),
            )
            i1_n_pmos = self.pmos(name="i1_n_pmos", net=_i1_n, w_size="min")
            i1_n_pmospad = self.polypad(
                name="i1_n_pmospad", net=_i1_n, left=(i0_pass0, q_pin),
            )
            i1_pmosrow0 = self.polyrow(
                name="i1_n_pmosrow", elements=(i1_n_pmospad, i1_n_pmos),
            )
            i1_pass0 = self.activecolumn(
                name="i1_pass0", connect=False, elements=(i1_nmos0, i1_n_pmos),
            )
        else:
            i1_n_nmos = self.nmos(name="i1_n_nmos", net=_i1_n, w_size="min")
            i1_n_nmospad = self.polypad(
                name="i1_n_nmospad", net=_i1_n, left=(i0_pass0, q_pin),
            )
            i1_nmosrow0 = self.polyrow(
                name="i1_n_nmosrow", elements=(i1_n_nmospad, i1_n_nmos)
            )
            i1_pmos0 = self.pmos(name="i1_pmos0", net=i1, w_size="min")
            i1_pmos0pad = self.polypad(
                name="i1_pmos0pad", net=i1, left=(i0_pass0, q_pin),
            )
            i1_pmosrow0 = self.polyrow(
                name="i1_pmos0row", elements=(i1_pmos0pad, i1_pmos0),
            )
            i1_pass0 = self.activecolumn(
                name="i1_pass0", connect=False, elements=(i1_n_nmos, i1_pmos0),
            )
        q_nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        q_psd = self.signal_psd(name="q_psd", net=q, with_contact=False)
        q_nsdrow = self.m1row(name="q_nsdrow", elements=(q_m1knot0, q_nsd))
        q_psdrow = self.m1row(name="q_psdrow", elements=(q_m1knot1, q_psd.contact))
        q_sds = self.activecolumn(name="q_sds", connect=False, elements=(q_nsd, q_psd))

        i0_n_nmos = self.nmos(name="i0_n_nmos", net=_i0_n, w_size="min")
        i0_n_pmos = self.pmos(name="i0_n_pmos", net=_i0_n, w_size="min")
        i0_n_polyknot = self.polyknot(name="i0_n_polyknot", net=_i0_n)
        i0_n_polyrow = self.polyrow(
            name="i0_n_polyrow", elements=(i0_n_pad, i0_n_polyknot),
        )
        i0_n_pass = self.activecolumn(
            name="i0_n_pass", connect=True, elements=(i0_n_nmos, i0_n_polyknot, i0_n_pmos),
        )

        net2_nsd = self.signal_nsd(name="net2_nsd", net=_net2, with_contact=False)
        net1_psd1 = self.signal_psd(name="net1_psd1", net=_net1, with_contact=True)
        net1_psdrow = self.m1row(name="net1_psdrow", elements=(net1_psd0, net1_psd1))
        net12_sds = self.activecolumn(
            name="net12_sds", connect=False, elements=(net2_nsd, net1_psd1),
        )

        i1_n_pad0 = self.polypad(name="i1_n_pad0", net=_i1_n, left=i0_n_pass)
        i1_n_m1knot = self.m1knot(name="i1_n_m1knot", net=_i1_n)
        if not self.inverted:
            assert i1_n_pmospad is not None, "Internal error"

            i1_n_nmos = self.nmos(name="i1_n_nmos", net=_i1_n, w_size="min")
            i1_n_m1row = self.m1row(
                name="i1_n_m1row", elements=(i1_n_pmospad, i1_n_m1knot),
            )
            i1_n_m1col0 = self.m1column(
                name="i1_n_m1col0", elements=(i1_n_pad0, i1_n_m1knot),
            )
            i1_pmos0 = self.pmos(name="i1_pmos0", net=i1, w_size="min")
            i1_pass1 = self.activecolumn(
                name="i1_pass1", connect=False, elements=(i1_n_nmos, i1_pmos0),
            )
        else:
            assert i1_n_nmospad is not None, "Internal error"

            i1_nmos0 = self.nmos(name="i1_nmos0", net=i1, w_size="min")
            i1_nmospad = self.polypad(name="i1_nmospad", net=i1)
            i1_n_m1row = self.m1row(
                name="i1_n_m1row", elements=(i1_n_nmospad, i1_n_m1knot),
            )
            i1_n_m1col0 = self.m1column(
                name="i1_n_m1col0", elements=(i1_n_m1knot, i1_n_pad0),
            )
            i1_n_pmos = self.pmos(name="i1_n_pmos", net=_i1_n, w_size="min")
            i1_pass1 = self.activecolumn(
                name="i1_pass1", connect=False, elements=(i1_nmos0, i1_n_pmos),
            )

        vss_sd1 = self.vss_sd(name="vss_sd1")
        vdd_sd1 = self.vdd_sd(name="vdd_sd1")
        vssvdd_sds1 = self.activecolumn(
            name="vssvdd_sds1", connect=False, elements=(vss_sd1, vdd_sd1),
        )

        i1_nmos1 = self.nmos(name="i1_nmos1", net=i1, w_size="min")
        i1_pmos1 = self.pmos(name="i1_pmos1", net=i1, w_size="min")
        if not self.inverted:
            assert i1_pmos0 is not None
            assert i1_nmos0pad is not None

            i1_nmos1pad = self.polypad(name="i1_nmos1pad", net=i1, left=i1_pass1)
            i1_nmos1knot = self.m1knot(name="i1_nmos1knot", net=i1)
            i1_nmosrow1 = self.polyrow(name="i1_nmos1row", elements=(i1_nmos1pad, i1_nmos1))
            i1_m1row = self.m1row(
                name="i1_m1row", elements=(i1_nmos0pad, i1_nmos1knot),
            )
            i1_pmospad = self.polypad(name="i1_pmospad", net=i1)
            i1_pmosrow1 = self.polyrow(
                name="i1_pmosrow", elements=(i1_pmos0, i1_pmospad, i1_pmos1),
            )
            i1_pin = self.m1pin(name="i1_pin", elements=(i1_nmos1pad, i1_nmos1knot, i1_pmospad))
        else:
            assert i1_nmos0 is not None
            assert i1_nmospad is not None
            assert i1_pmos0pad is not None

            i1_nmosrow1 = self.polyrow(
                name="i1_nmosrow", elements=(i1_nmos0, i1_nmospad, i1_nmos1),
            )
            i1_pmos1pad = self.polypad(name="i1_pmos1pad", net=i1, left=i1_pass1)
            i1_pmos1knot = self.m1knot(name="i1_pmos1knot", net=i1)
            i1_pmosrow1 = self.polyrow(name="i1_pmos1row", elements=(i1_pmos1pad, i1_pmos1))
            i1_m1row = self.m1row(
                name="i1_m1row", elements=(i1_pmos0pad, i1_pmos1knot),
            )
            i1_pin = self.m1pin(name="i1_pin", elements=(i1_nmospad, i1_pmos1knot, i1_pmos1pad))

        i1_inv = self.activecolumn(
            name="i1_inv", connect=False, elements=(i1_nmos1, i1_pmos1),
        )


        i1_n_nsd = self.signal_nsd(name="i1_n_nsd", net=_i1_n, with_contact=True)
        i1_n_psd = self.signal_psd(name="i1_n_psd", net=_i1_n, with_contact=True)
        i1_n_pad = self.polypad(name="i1_n_pad", net=_i1_n)
        mos = i1_n_nmos if not self.inverted else i1_n_pmos
        assert mos is not None
        i1_n_polyrow = self.polyrow(
            name="i1_n_polyrow", elements=(i1_n_pad0, mos, i1_n_pad),
        )
        i1_n_m1col1 = self.m1column(
            name="i1_n_m1col1", elements=(i1_n_nsd, i1_n_pad, i1_n_psd),
        )
        i1_n_sds = self.activecolumn(
            name="i1_n_sds", connect=False, elements=(i1_n_nsd, i1_n_psd), left=i1_pin,
        )

        ### Constriants

        return self.constraints(
            activecolumns=(
                i0_n_sds, i0_inv, vssvdd_sds0, i0_pass0, net01_sds,
                i1_pass0, q_sds, i0_n_pass, net12_sds, i1_pass1, vssvdd_sds1,
                i1_inv, i1_n_sds,
            ),
            polyrows=(
                self.multipolyrow(
                    name="nmos_multirow", rows=(i0_nmosrow, i1_nmosrow0, i1_nmosrow1),
                ),
                self.multipolyrow(name="conn_multirow", rows=(
                    i0_n_polyrow, i1_n_polyrow,
                )),
                i1_pmosrow0.multipolyrow,
                self.multipolyrow(name="pmos_multirow", rows=(
                    i0_pmosrow, i1_pmosrow1,
                )),
            ),
            m1rows=(
                q_nsdrow.multim1row,
                *(
                    (
                        i1_m1row.multim1row,
                        i1_n_m1row.multim1row,
                    )
                    if not self.inverted
                    else
                    (
                        i1_n_m1row.multim1row,
                        i1_m1row.multim1row,
                    )
                ),
                q_psdrow.multim1row,
                net1_psdrow.multim1row,
            ),
            m1columns=(
                i0_n_m1col.multim1column,
                i0_pin.multim1column,
                q_pin.multim1column,
                i1_n_m1col0.multim1column,
                i1_pin.multim1column,
                i1_n_m1col1.multim1column,
            ),
        )


class _nRnSLatch(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int):
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size = "min" if (self.drive == 0) else "max"

        ### nets

        nset = ckt.new_net(name="nset", external=True)
        nrst = ckt.new_net(name="nrst", external=True)

        q = ckt.new_net(name="q", external=True)
        nq = ckt.new_net(name="nq", external=True)

        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)

        ### sd and trans elements, poly knots

        vss_sd = self.vss_sd(name="vss_sd")

        vdd_sd0 = self.vdd_sd(name="vdd_sd0")
        vdd_sd1 = self.vdd_sd(name="vdd_sd1")
        vdd_sd2 = self.vdd_sd(name="vdd_sd2")

        net0_nsd = self.signal_nsd(name="net0_nsd", net=_net0, with_contact=False)
        net1_nsd = self.signal_nsd(name="net1_nsd", net=_net1, with_contact=False)

        q_nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        q_psd = self.signal_psd(name="q_psd", net=q, with_contact=True)

        nq_nsd = self.signal_nsd(name="nq_nsd", net=nq, with_contact=True)
        nq_psd = self.signal_psd(name="nq_psd", net=nq, with_contact=True)

        q_nmos = self.nmos(name="q_nmos", net=q, w_size=w_size)
        q_pmos = self.pmos(name="q_pmos", net=q, w_size=w_size)

        nq_nmos = self.nmos(name="nq_nmos", net=nq, w_size=w_size)
        nq_pmos = self.pmos(name="nq_pmos", net=nq, w_size=w_size)

        nset_nmos = self.nmos(name="nset_nmos", net=nset, w_size=w_size)
        nset_pmos = self.pmos(name="nset_pmos", net=nset, w_size=w_size)

        nrst_nmos = self.nmos(name="nrst_nmos", net=nrst, w_size=w_size)
        nrst_pmos = self.pmos(name="nrst_pmos", net=nrst, w_size=w_size)

        ### poly knots

        q_polyknot = self.polyknot(name="q_polyknot", net=q)
        nq_polyknot = self.polyknot(name="nq_polyknot", net=q)
        nset_polyknot = self.polyknot(name="nset_polyknot", net=nset)
        nrst_polyknot = self.polyknot(name="nrst_polyknot", net=nset)

        ### active columns

        sds0 = self.activecolumn(
            name="sds0", connect=False, elements=(q_nsd, vdd_sd0),
        )

        nset_trans = self.activecolumn(
            name="nest_trans", connect=True, elements=(nset_nmos, nset_polyknot, nset_pmos),
        )

        sds1 = self.activecolumn(
            name="sds1", connect=False, elements=(net0_nsd, q_psd),
        )

        nq_trans = self.activecolumn(
            name="nq_trans", connect=True, elements=(nq_nmos, nq_polyknot, nq_pmos),
        )
        q_pad = self.polypad(name="q_pad", net=q, left=nq_trans)

        sds2 = self.activecolumn(
            name="sds2", connect=False, elements=(vss_sd, vdd_sd1),
        )

        # Early allocated elem needed as left specification
        q_m1knot1 = self.m1knot(name="q_m1knot1", net=q)
        nq_pad = self.polypad(name="nq_pad", net=nq, left=(nset_trans, q_m1knot1))

        q_trans = self.activecolumn(
            name="q_trans", connect=True, elements=(q_nmos, q_polyknot, q_pmos),
            left=nq_pad,
        )

        sds3 = self.activecolumn(
            name="sds3", connect=False, elements=(net1_nsd, nq_psd),
            left=q_pad,
        )

        nrst_trans = self.activecolumn(
            name="nrst_trans", connect=True, elements=(nrst_nmos, nrst_polyknot, nrst_pmos),
        )

        sds4 = self.activecolumn(
            name="sds4", connect=False, elements=(nq_nsd, vdd_sd2),
        )

        actcols: Tuple[_acc.ActiveColumnT, ...] = (
            sds0, nset_trans, sds1, nq_trans,
            sds2, q_trans, sds3, nrst_trans,
            sds4,
        )

        ### m1 knots, rows & columns

        nset_pad = self.polypad(name="nset_pad", net=nset)
        nset_pin = self.m1pin(
            name="nset_pin", elements=nset_pad, bottom=q_nsd,
        )

        q_m1knot0 = self.m1knot(name="q_m1knot0", net=q)
        q_m1knot2 = self.m1knot(name="q_m1knot2", net=q)
        q_m1row0 = self.m1row(name="q_m1row0", elements=(q_nsd, q_m1knot0))
        q_m1row1 = self.m1row(name="q_m1row1", elements=(q_m1knot1, q_pad))
        q_m1row2 = self.m1row(name="q_m1row2", elements=(q_m1knot2, q_psd))
        q_pin = self.m1pin(
            name="q_pin", elements=(q_m1knot0, q_m1knot1, q_m1knot2),
        )

        nq_m1knot0 = self.m1knot(name="nq_m1knot0", net=nq)
        nq_m1knot1 = self.m1knot(name="nq_m1knot1", net=nq)
        nq_m1row0 = self.m1row(name="nq_m1row0", elements=(nq_m1knot0, nq_nsd))
        nq_m1row1 = self.m1row(name="nq_m1row1", elements=(nq_pad, nq_m1knot1))
        nq_pin = self.m1pin(
            name="nq_pin", elements=(nq_m1knot0, nq_m1knot1, nq_psd),
        )

        nrst_pad = self.polypad(name="rst_pad", net=nrst)
        nrst_pin = self.m1pin(
            name="nrst_pin", elements=nrst_pad, bottom=nq_nsd,
        )

        m1rows: Tuple[_acc.MultiM1RowT, ...] = (
            self.multim1row(name="nsd_mm1row", rows=(q_m1row0, nq_m1row0)),
            nq_m1row1.multim1row, q_m1row1.multim1row, q_m1row2.multim1row,
        )
        m1cols: Tuple[_acc.MultiM1ColumnT, ...] = (
            nset_pin.multim1column, q_pin.multim1column, nq_pin.multim1column,
            nrst_pin.multim1column,
        )

        ### poly rows

        nset_polyrow = self.polyrow(name="nset_polyrow", elements=(nset_pad, nset_polyknot))
        q_polyrow = self.polyrow(name="q_polyrow", elements=(q_pad, q_polyknot))
        nq_polyrow = self.polyrow(name="nq_polyrow", elements=(nq_polyknot, nq_pad))
        nrst_polyrow = self.polyrow(name="nrst_polyrow", elements=(nrst_polyknot, nrst_pad))

        polyrows: Tuple[_acc.MultiPolyRowT, ...] = (
            self.multipolyrow(name="mpolyrow0", rows=(nq_polyrow, nrst_polyrow)),
            self.multipolyrow(name="mpolyrow1", rows=(nset_polyrow, q_polyrow)),
        )

        ### constraints

        return self.constraints(
            activecolumns=actcols,
            polyrows=polyrows,
            m1rows=m1rows,
            m1columns=m1cols,
        )


class _DFF(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int):
        if drive > 1:
            raise NotImplementedError(f"DFF drive '{drive}' > 1")
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size_q = "min" if self.drive == 0 else "max"

        ### nets

        i = ckt.new_net(name="i", external=True)
        clk = ckt.new_net(name="clk", external=True)
        q = ckt.new_net(name="q", external=True)

        _clk_n = ckt.new_net(name="_clk_n", external=False)
        _clk_buf = ckt.new_net(name="_clk_buf", external=False)
        _dff_m = ckt.new_net(name="_dff_m", external=False)
        _dff_s = ckt.new_net(name="_dff_s", external=False)
        _u = ckt.new_net(name="_u", external=False)
        _y = ckt.new_net(name="_y", external=False)

        ### elements

        i_nmos = self.nmos(name="i_nmos", net=i, w_size="min")
        i_pmos = self.pmos(name="i_pmos", net=i, w_size="min")

        clk_nmos = self.nmos(name="clk_nmos", net=clk, w_size="min")
        clk_pmos = self.pmos(name="clk_pmos", net=clk, w_size="min")

        q_nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        q_psd = self.signal_psd(name="q_psd", net=q, with_contact=True)
        q_nmos = self.nmos(name="q_nmos", net=q, w_size="min")
        q_pmos = self.pmos(name="q_pmos", net=q, w_size="min")

        clk_n_nsd = self.signal_nsd(name="clk_n_nsd", net=_clk_n, with_contact=True)
        clk_n_psd = self.signal_psd(name="clk_n_psd", net=_clk_n, with_contact=True)
        clk_n_nmos0 = self.nmos(name="clk_n_nmos0", net=_clk_n, w_size="min")
        clk_n_nmos1 = self.nmos(name="clk_n_nmos1", net=_clk_n, w_size="min")
        clk_n_nmos2 = self.nmos(name="clk_n_nmos2", net=_clk_n, w_size="min")
        clk_n_pmos0 = self.pmos(name="clk_n_pmos0", net=_clk_n, w_size="min")
        clk_n_pmos1 = self.pmos(name="clk_n_pmos1", net=_clk_n, w_size="min")
        clk_n_pmos2 = self.pmos(name="clk_n_pmos2", net=_clk_n, w_size="min")

        clk_buf_nsd = self.signal_nsd(name="clk_buf_nsd", net=_clk_buf, with_contact=True)
        clk_buf_psd = self.signal_psd(name="clk_buf_psd", net=_clk_buf, with_contact=True)
        clk_buf_nmos0 = self.nmos(name="clk_buf_nmos0", net=_clk_buf, w_size="min")
        clk_buf_nmos1 = self.nmos(name="clk_buf_nmos1", net=_clk_buf, w_size="min")
        clk_buf_pmos0 = self.pmos(name="clk_buf_pmos0", net=_clk_buf, w_size="min")
        clk_buf_pmos1 = self.pmos(name="clk_buf_pmos1", net=_clk_buf, w_size="min")

        dff_m_nsd = self.signal_nsd(name="dff_m_nsd", net=_dff_m, with_contact=True)
        dff_m_psd = self.signal_psd(name="dff_m_psd", net=_dff_m, with_contact=True)
        dff_m_nmos = self.nmos(name="dff_m_nmos", net=_dff_m, w_size="min")
        dff_m_pmos = self.pmos(name="dff_m_pmos", net=_dff_m, w_size="min")

        dff_s_nsd = self.signal_nsd(name="dff_s_nsd", net=_dff_s, with_contact=True)
        dff_s_psd = self.signal_psd(name="dff_s_psd", net=_dff_s, with_contact=True)
        dff_s_nmos = self.nmos(name="dff_s_nmos", net=_dff_s, w_size=w_size_q)
        dff_s_pmos = self.pmos(name="dff_s_pmos", net=_dff_s, w_size=w_size_q)

        u_nsd = self.signal_nsd(name="u_nsd", net=_u, with_contact=True)
        u_psd = self.signal_psd(name="u_psd", net=_u, with_contact=True)
        u_nmos = self.nmos(name="u_nmos", net=_u, w_size="min")
        u_pmos = self.pmos(name="u_pmos", net=_u, w_size="min")

        y_nsd = self.signal_nsd(name="y_nsd", net=_y, with_contact=True)
        y_psd = self.signal_psd(name="y_psd", net=_y, with_contact=True)
        y_nmos = self.nmos(name="y_nmos", net=_y, w_size="min")
        y_pmos = self.pmos(name="y_pmos", net=_y, w_size="min")

        ### columns and rows

        # clk
        clk_nmospad = self.polypad(name="clk_nmospad", net=clk)
        clk_pmospad = self.polypad(name="clk_pmospad", net=clk)

        clk_inv = self.activecolumn(
            name="clk_inv", connect=False, elements=(clk_nmos, clk_pmos),
        )
        clk_nmosrow = self.polyrow(name="clk_nmosrow", elements=(clk_nmos, clk_nmospad))
        clk_pmosrow = self.polyrow(name="clk_pmosrow", elements=(clk_pmos, clk_pmospad))
        clk_pin = self.m1pin(
            name="clk_pin", elements=(clk_nmospad, clk_pmospad),
        )

        # clk_n, pt. 1
        clk_n_polypad0 = self.polypad(name="clk_n_pad0", net=_clk_n)
        clk_n_polyknot = self.polyknot(name="clk_n_polyknot", net=_clk_n)
        clk_n_polypad1 = self.polypad(name="clk_n_pad1", net=_clk_n)

        clk_n_sds = self.activecolumn(
            name="clk_n_sds", connect=False, elements=(clk_n_nsd, clk_n_psd),
        )
        clk_n_inv = self.activecolumn(
            name="clk_n_inv", connect=True, elements=(clk_n_nmos0, clk_n_polyknot, clk_n_pmos0),
            left=(clk_nmospad, clk_pmospad),
        )
        clk_n_m1col0 = self.m1column(
            name="clk_n_m1col0", elements=(clk_n_nsd, clk_n_polypad0, clk_n_psd),
        )

        # clk_buf - pt. 1
        clk_buf_m1knot = self.m1knot(name="clk_buf_m1knot", net=_clk_buf)
        clk_buf_polypad0 = self.polypad(
            name="clk_buf_polypad0", net=_clk_buf, left=clk_n_inv,
        )

        clk_buf_sds = self.activecolumn(
            name="clk_buf_sds", connect=False, elements=(clk_buf_nsd, clk_buf_psd),
        )
        clk_buf_sdm1col = self.m1column(
            name="clk_buf_sdm1col", elements=(clk_buf_nsd, clk_buf_m1knot, clk_buf_psd),
        )
        clk_buf_m1row = self.m1row(
            name="clk_buf_m1row", elements=(clk_buf_m1knot, clk_buf_polypad0),
        )

        # clk_n/clk_buf transistor - pt. 1
        clk_trans0 = self.activecolumn(
            name="clk_trans0", connect=False, elements=(clk_n_nmos1, clk_buf_pmos0),
        )

        # sd interconnect
        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        _net2 = ckt.new_net(name="_net2", external=False)
        _net3 = ckt.new_net(name="_net3", external=False)
        _net4 = ckt.new_net(name="_net4", external=False)
        _net5 = ckt.new_net(name="_net5", external=False)

        net0_nsd = self.signal_nsd(name="net0_nsd", net=_net0, with_contact=False)
        net2_nsd = self.signal_nsd(name="net2_nsd", net=_net2, with_contact=False)
        net4_nsd = self.signal_nsd(name="net4_nsd", net=_net4, with_contact=False)
        net1_psd = self.signal_psd(name="net1_psd", net=_net1, with_contact=False)
        net3_psd = self.signal_psd(name="net3_psd", net=_net3, with_contact=False)
        net5_psd = self.signal_psd(name="net5_psd", net=_net5, with_contact=False)

        sdcon0 = self.activecolumn(
            name="sdcon0", connect=False, elements=(net0_nsd, net1_psd),
        )
        sdcon1 = self.activecolumn(
            name="sdcon1", connect=False, elements=(net2_nsd, net3_psd),
        )
        sdcon2 = self.activecolumn(
            name="sdcon2", connect=False, elements=(net4_nsd, net5_psd),
        )

        # i - pt.1
        i_trans = self.activecolumn(name="i_trans", connect=False, elements=(i_nmos, i_pmos))

        # u
        u_nmospad = self.polypad(name="u_nmospad", net=_u, left=i_trans)
        u_pmospad = self.polypad(name="u_pmospad", net=_u, left=i_trans)
        u_m1knot0 = self.m1knot(name="u_m1knot0", net=_u)
        u_m1knot1 = self.m1knot(name="u_m1knot1", net=_u)

        u_sds = self.activecolumn(
            name="u_sds", connect=False, elements=(u_nsd, u_psd),
        )
        u_nsdrow = self.m1row(name="u_nsdrow", elements=(u_nsd, u_m1knot0))
        u_psdrow = self.m1row(name="u_psdrow", elements=(u_psd, u_m1knot1))
        u_nmosrow = self.polyrow(name="u_nmosrow", elements=(u_nmospad, u_nmos))
        u_pmosrow = self.polyrow(name="u_pmosrow", elements=(u_pmospad, u_pmos))
        u_m1col = self.m1column(
            name="u_m1col", elements=(u_m1knot0, u_nmospad, u_pmospad, u_m1knot1),
        )
        u_trans = self.activecolumn(
            name="u_trans", connect=False, elements=(u_nmos, u_pmos),
        )

        # clk_n - pt. 2
        clk_n_nmos1pad = self.polypad(
            name="clk_n_nmos1pad", net=_clk_n, left=(u_trans, u_nmospad),
        )

        clk_n_nmos1row = self.polyrow(
            name="clk_n_nmos0row", elements=(clk_n_nmos1pad, clk_n_nmos1),
        )
        clk_n_m1col1 = self.m1column(
            name="clk_n_m1col1", elements=(clk_n_nmos1pad, clk_n_polypad1),
        )

        # clk_buf - pt. 2
        clk_buf_polypad1 = self.polypad(name="clk_buf_polypad1", net=_clk_buf)
        clk_buf_pmos0pad = self.polypad(
            name="clk_buf_pmos0pad", net=_clk_buf, left=(u_trans, u_pmospad),
        )
        clk_buf_pmos0m1knot = self.m1knot(name="clk_buf_pmos0m1knot", net=_clk_buf)

        clk_buf_pmos0polyrow = self.polyrow(
            name="clk_buf_pmos0polyrow", elements=(clk_buf_pmos0, clk_buf_pmos0pad)
        )
        clk_buf_pmos0m1row = self.m1row(
            name="clk_buf_pmos0m1row", elements=(clk_buf_pmos0pad, clk_buf_pmos0m1knot),
        )
        clk_buf_pmos0m1col = self.m1column(
            name="clk_buf_pmos0m1col", elements=(clk_buf_polypad1, clk_buf_pmos0m1knot),
        )

        # clk_n/clk_buf transistor - pt. 2
        clk_trans1 = self.activecolumn(
            name="clk_trans1", connect=False, elements=(clk_buf_nmos0, clk_n_pmos1),
            left=(clk_n_nmos1pad, clk_buf_pmos0pad),
        )
        clk_trans2 = self.activecolumn(
            name="clk_trans2", connect=False, elements=(clk_buf_nmos1, clk_n_pmos2),
        )

        # i - pt. 2
        i_nmospad = self.polypad(name="i_nmospad", net=i)
        i_pmospad = self.polypad(name="i_pmospad", net=i)

        i_pin = self.m1pin(
            name="i_pin", elements=(i_nmospad, i_pmospad),
            left=clk_buf_polypad0, bottom=u_nsd, top=u_psd,
        )
        i_nmosrow = self.polyrow(name="i_nmosrow", elements=(i_nmospad, i_nmos))
        i_pmosrow = self.polyrow(name="i_pmosrow", elements=(i_pmospad, i_pmos))

        # y - pt.1
        y_nmospad = self.polypad(name="y_nmospad", net=_y, left=clk_trans1)
        y_pmospad = self.polypad(name="y_pmospad", net=_y, left=clk_trans1)

        y_trans = self.activecolumn(
            name="y_trans", connect=False, elements=(y_nmos, y_pmos),
        )

        # dff_m
        dff_m_m1knot0 = self.m1knot(name="dff_m_m1knot0", net=_dff_m)
        dff_m_m1knot1 = self.m1knot(name="dff_m_m1knot1", net=_dff_m)
        dff_m_m1knot2 = self.m1knot(name="dff_m_m1knot2", net=_dff_m)
        dff_m_nmospad = self.polypad(
            name="dff_m_nmospad", net=_dff_m, left=(y_trans, y_nmospad),
        )
        dff_m_pmospad = self.polypad(
            name="dff_m_pmospad", net=_dff_m, left=(y_trans, y_pmospad),
        )

        dff_m_sds = self.activecolumn(
            name="dff_n_sds", connect=False, elements=(dff_m_nsd, dff_m_psd)
        )
        dff_m_nsdrow = self.m1row(name="dff_m_nsdrow", elements=(dff_m_nsd, dff_m_m1knot0))
        dff_m_psdrow = self.m1row(
            name="dff_m_psdrow", elements=(dff_m_psd, dff_m_m1knot1, dff_m_m1knot2),
        )
        dff_m_m1col0 = self.m1column(
            name="dff_m_m1col0", elements=(dff_m_m1knot0, dff_m_m1knot1),
        )
        dff_m_m1col1 = self.m1column(
            name="dff_m_m1col1", elements=(dff_m_nmospad, dff_m_pmospad, dff_m_m1knot2),
        )
        dff_m_nmospolyrow = self.polyrow(
            name="dff_m_nmospolyrow", elements=(dff_m_nmospad, dff_m_nmos),
        )
        dff_m_pmospolyrow = self.polyrow(
            name="dff_m_pmospolyrow", elements=(dff_m_pmospad, dff_m_pmos),
        )
        dff_m_trans = self.activecolumn(
            name="dff_m_trans", connect=False, elements=(dff_m_nmos, dff_m_pmos),
            left=(y_nmospad, y_pmospad),
        )

        # y - pt.2
        y_m1knot0 = self.m1knot(name="y_m1knot0", net=_y)

        y_nmospolyrow = self.polyrow(name="y_nmospolyrow", elements=(y_nmos, y_nmospad))
        y_pmospolyrow = self.polyrow(name="y_pmospolyrow", elements=(y_pmos, y_pmospad))
        y_sds = self.activecolumn(
            name="y_sds", connect=False, elements=(y_nsd, y_psd),
            left=(dff_m_nmospad, dff_m_pmospad),
        )
        y_nsdrow = self.m1row(
            name="y_nsdrow", elements=(y_m1knot0, y_nsd),
        )
        y_m1col0 = self.m1column(
            name="y_m1col0", elements=(y_m1knot0, y_nmospad, y_pmospad),
        )
        y_m1col1 = self.m1column(
            name="y_m1col1", elements=(y_nsd, y_psd),
        )

        # clk_buf - pt. 3
        clk_buf_polypad2 = self.polypad(
            name="clk_buf_polypad2", net=_clk_buf, left=y_m1col1,
        )
        clk_buf_pmos1pad = self.polypad(
            name="clk_buf_pmos1pad", net=_clk_buf, left=clk_trans2,
        )
        clk_buf_pmos1polyrow = self.polyrow(
            name="clk_buf_pmos1row", elements=(clk_buf_pmos1pad, clk_buf_pmos1),
        )
        clk_buf_pmos1m1knot = self.m1knot(name="clk_buf_pmos1m1knot", net=_clk_buf)
        clk_buf_pmos1m1row = self.m1row(
            name="clk_buf_pmos1m1row", elements=(clk_buf_pmos1m1knot, clk_buf_pmos1pad),
        )
        clk_buf_pmos1m1col = self.m1column(
            name="clk_buf_pmos1m1col", elements=(clk_buf_polypad2, clk_buf_pmos1m1knot),
        )
        clk_buf_polyrow = self.polyrow(
            name="clk_buf_polyrow", elements=(
                clk_buf_polypad0, clk_buf_polypad1, clk_buf_nmos0, clk_buf_nmos1,
                clk_buf_polypad2,
            ),
        )

        # clk_n, pt. 3
        clk_n_polypad2 = self.polypad(name="clk_n_polypad2", net=_clk_n)
        clk_n_nmos2pad = self.polypad(
            name="clk_n_nmos2pad", net=_clk_n, left=clk_trans2,
        )
        clk_n_nmos2polyrow = self.polyrow(
            name="clk_n_nmos2polyrow", elements=(clk_n_nmos2, clk_n_nmos2pad)
        )
        clk_n_nmos2m1col = self.m1column(
            name="clk_n_nmos2m1col", elements=(clk_n_nmos2pad, clk_n_polypad2)
        )
        clk_n_polyrow = self.polyrow(
            name="clk_n_polyrow", elements=(
                clk_n_polypad0, clk_n_polyknot, clk_n_polypad1, clk_n_pmos1, clk_n_pmos2,
                clk_n_polypad2,
            )
        )

        # clk_n/clk_buf transistor - pt. 3
        clk_trans3 = self.activecolumn(
            name="clk_trans3", connect=False, elements=(clk_n_nmos2, clk_buf_pmos1),
        )

        # q - pt. 1
        q_trans = self.activecolumn(
            name="q_trans", connect=False, elements=(q_nmos, q_pmos),
            left=clk_n_polypad2,
        )

        # dff_s - pt. 1
        dff_s_m1knot0 = self.m1knot(name="dff_s_m1knot0", net=_dff_s)
        dff_s_m1knot1 = self.m1knot(name="dff_s_m1knot1", net=_dff_s)
        dff_s_polyknot = self.polyknot(name="dff_s_polyknot", net=_dff_s)
        dff_s_polypad = self.polypad(
            name="dff_s_polypad", net=_dff_s, left=clk_buf_polypad2,
        )

        dff_s_sds = self.activecolumn(
            name="dff_s_sds", connect=False, elements=(dff_s_nsd, dff_s_psd),
        )
        dff_s_polyrow = self.polyrow(
            name="dff_s_polyrow", elements=(dff_s_polypad, dff_s_polyknot)
        )
        dff_s_nsdrow = self.m1row(
            name="dff_s_nsdrow", elements=(dff_s_nsd, dff_s_m1knot0),
        )
        dff_s_psdrow = self.m1row(
            name="dff_s_psdrow", elements=(dff_s_psd, dff_s_m1knot1),
        )
        dff_s_m1col = self.m1column(
            name="dff_s_m1col", elements=(dff_s_m1knot0, dff_s_polypad, dff_s_m1knot1),
        )

        # q - pt. 2
        q_nmospad = self.polypad(
            name="q_nmospad", net=q, left=(dff_s_m1col, clk_n_nmos2pad, clk_trans3),
        )
        q_pmospad = self.polypad(
            name="q_pmospad", net=q, left=(dff_s_m1col, clk_n_polypad2, clk_trans3),
        )
        q_m1knot0 = self.m1knot(name="q_m1knot0", net=q)
        q_m1knot1 = self.m1knot(name="q_m1knot1", net=q)

        q_nmospolyrow = self.polyrow(name="q_nmospolyrow", elements=(q_nmospad, q_nmos))
        q_pmospolyrow = self.polyrow(name="q_pmospolyrow", elements=(q_pmospad, q_pmos))
        q_sds = self.activecolumn(
            name="q_sds", connect=False, elements=(q_nsd, q_psd),
            left=dff_s_polypad
        )
        q_nsdrow = self.m1row(name="q_nsdrow", elements=(q_m1knot0, q_nsd))
        q_psdrow = self.m1row(name="q_psdrow", elements=(q_m1knot1, q_psd))
        q_pin = self.m1pin(
            name="q_pin", elements=(q_m1knot0, q_nmospad, q_pmospad, q_m1knot1),
        )

        # dff_s - pt. 2
        dff_s_inv = self.activecolumn(
            name="dff_s_inv", connect=True, elements=(
                dff_s_nmos, dff_s_polyknot, dff_s_pmos,
            ), left=(q_nmospad, q_pmospad),
        )

        # vss/vdd sd
        vssvdd_sds = tuple(
            self.activecolumn(name=f"vssvdd_sd{n}", connect=False, elements=(
                self.vss_sd(name=f"vss_sd{n}"), self.vdd_sd(name=f"vdd_sd{n}"),
            ))
            for n in range(4)
        )

        # gap
        actgap = self.activecolumn(name="actgap", connect=False, elements=())

        ### constraints

        return self.constraints(
            activecolumns=(
                clk_n_sds, clk_inv, vssvdd_sds[0], clk_n_inv, clk_buf_sds, actgap,
                u_sds, i_trans, vssvdd_sds[1], u_trans, sdcon0, clk_trans0, dff_m_sds,
                clk_trans1, sdcon1, y_trans, vssvdd_sds[2], dff_m_trans, y_sds, clk_trans2,
                dff_s_sds, clk_trans3, sdcon2, q_trans, vssvdd_sds[3], dff_s_inv, q_sds,
            ),
            polyrows=(
                self.multipolyrow(name="polyrow0", rows=(
                    i_nmosrow, u_nmosrow, clk_n_nmos1row, y_nmospolyrow, dff_m_nmospolyrow,
                    clk_n_nmos2polyrow, q_nmospolyrow,
                )),
                self.multipolyrow(name="polyrow1", rows=(
                    clk_nmosrow, clk_buf_polyrow, dff_s_polyrow,
                )),
                self.multipolyrow(name="polyrow2", rows=(
                    clk_n_polyrow, q_pmospolyrow,
                )),
                self.multipolyrow(name="polyrow3", rows=(
                    clk_pmosrow, i_pmosrow, u_pmosrow, clk_buf_pmos0polyrow, y_pmospolyrow,
                    dff_m_pmospolyrow, clk_buf_pmos1polyrow,
                )),
            ),
            m1rows=(
                self.multim1row(name="nsdmrow", rows=(
                    u_nsdrow, dff_m_nsdrow, y_nsdrow, dff_s_nsdrow,
                )),
                # q_nsdrow need separate multirow as they have different y
                self.multim1row(name="nsdmrowmax", rows=q_nsdrow),
                clk_buf_m1row.multim1row,
                self.multim1row(
                    name="pmosm1row", rows=(clk_buf_pmos0m1row, clk_buf_pmos1m1row),
                ),
                self.multim1row(name="psdmrow", rows=(
                    u_psdrow, dff_m_psdrow, dff_s_psdrow,
                )),
                # q_psdrow need separate multirow as they have different y
                self.multim1row(name="psdmrowmax", rows=q_psdrow),
            ),
            m1columns=(
                clk_n_m1col0.multim1column, clk_pin.multim1column,
                clk_buf_sdm1col.multim1column, i_pin.multim1column,
                u_m1col.multim1column, clk_n_m1col1.multim1column,
                clk_buf_pmos0m1col.multim1column, dff_m_m1col0.multim1column,
                y_m1col0.multim1column, dff_m_m1col1.multim1column,
                y_m1col1.multim1column, clk_buf_pmos1m1col.multim1column,
                clk_n_nmos2m1col.multim1column, dff_s_m1col.multim1column,
                q_pin.multim1column,
            ),
        )


class _DFFnR(_acc.ActiveColumnsCell):
    def __init__(self, *, name: str, fab: "StdCellFactory", drive: int):
        if drive > 1:
            raise NotImplementedError(f"DFF drive '{drive}' > 1")
        self._drive = drive
        super().__init__(name=name, fab=fab)

    @property
    def drive(self) -> int:
        return self._drive

    def build_generator(self) -> _acc.ConstraintsT:
        ckt = self.circuit

        w_size_q = "min" if self.drive == 0 else "max"

        ### nets

        i = ckt.new_net(name="i", external=True)
        clk = ckt.new_net(name="clk", external=True)
        q = ckt.new_net(name="q", external=True)
        nrst = ckt.new_net(name="nrst", external=True)

        _clk_n = ckt.new_net(name="_clk_n", external=False)
        _clk_buf = ckt.new_net(name="_clk_buf", external=False)
        _dff_m = ckt.new_net(name="_dff_m", external=False)
        _dff_s = ckt.new_net(name="_dff_s", external=False)
        _u = ckt.new_net(name="_u", external=False)
        _y = ckt.new_net(name="_y", external=False)

        ### elements

        i_nmos = self.nmos(name="i_nmos", net=i, w_size="min")
        i_pmos = self.pmos(name="i_pmos", net=i, w_size="min")

        nrst_nmos0 = self.nmos(name="nrst_nmos0", net=nrst, w_size="min")
        nrst_nmos1 = self.nmos(name="nrst_nmos1", net=nrst, w_size="min")
        nrst_pmos0 = self.pmos(name="nrst_pmos0", net=nrst, w_size="min")
        nrst_pmos1 = self.pmos(name="nrst_pmos1", net=nrst, w_size="min")

        clk_nmos = self.nmos(name="clk_nmos", net=clk, w_size="min")
        clk_pmos = self.pmos(name="clk_pmos", net=clk, w_size="min")

        q_nsd = self.signal_nsd(name="q_nsd", net=q, with_contact=True)
        q_psd = self.signal_psd(name="q_psd", net=q, with_contact=True)
        q_nmos = self.nmos(name="q_nmos", net=q, w_size="min")
        q_pmos = self.pmos(name="q_pmos", net=q, w_size="min")

        clk_n_nsd = self.signal_nsd(name="clk_n_nsd", net=_clk_n, with_contact=True)
        clk_n_psd = self.signal_psd(name="clk_n_psd", net=_clk_n, with_contact=True)
        clk_n_nmos0 = self.nmos(name="clk_n_nmos0", net=_clk_n, w_size="min")
        clk_n_nmos1 = self.nmos(name="clk_n_nmos1", net=_clk_n, w_size="min")
        clk_n_nmos2 = self.nmos(name="clk_n_nmos2", net=_clk_n, w_size="min")
        clk_n_pmos0 = self.pmos(name="clk_n_pmos0", net=_clk_n, w_size="min")
        clk_n_pmos1 = self.pmos(name="clk_n_pmos1", net=_clk_n, w_size="min")
        clk_n_pmos2 = self.pmos(name="clk_n_pmos2", net=_clk_n, w_size="min")

        clk_buf_nsd = self.signal_nsd(name="clk_buf_nsd", net=_clk_buf, with_contact=True)
        clk_buf_psd = self.signal_psd(name="clk_buf_psd", net=_clk_buf, with_contact=True)
        clk_buf_nmos0 = self.nmos(name="clk_buf_nmos0", net=_clk_buf, w_size="min")
        clk_buf_nmos1 = self.nmos(name="clk_buf_nmos1", net=_clk_buf, w_size="min")
        clk_buf_pmos0 = self.pmos(name="clk_buf_pmos0", net=_clk_buf, w_size="min")
        clk_buf_pmos1 = self.pmos(name="clk_buf_pmos1", net=_clk_buf, w_size="min")

        dff_m_nsd = self.signal_nsd(name="dff_m_nsd", net=_dff_m, with_contact=True)
        dff_m_psd = self.signal_psd(name="dff_m_psd", net=_dff_m, with_contact=True)
        dff_m_nmos = self.nmos(name="dff_m_nmos", net=_dff_m, w_size="min")
        dff_m_pmos = self.pmos(name="dff_m_pmos", net=_dff_m, w_size="min")

        dff_s_nsd = self.signal_nsd(name="dff_s_nsd", net=_dff_s, with_contact=True)
        dff_s_psd = self.signal_psd(name="dff_s_psd", net=_dff_s, with_contact=False)
        dff_s_nmos = self.nmos(name="dff_s_nmos", net=_dff_s, w_size=w_size_q)
        dff_s_pmos = self.pmos(name="dff_s_pmos", net=_dff_s, w_size=w_size_q)

        u_nsd = self.signal_nsd(name="u_nsd", net=_u, with_contact=True)
        u_psd = self.signal_psd(name="u_psd", net=_u, with_contact=True)
        u_nmos = self.nmos(name="u_nmos", net=_u, w_size="min")
        u_pmos = self.pmos(name="u_pmos", net=_u, w_size="min")

        y_nsd0 = self.signal_nsd(name="y_nsd0", net=_y, with_contact=True)
        y_nsd1 = self.signal_nsd(name="y_nsd1", net=_y, with_contact=False)
        y_nsd2 = self.signal_nsd(name="y_nsd2", net=_y, with_contact=False)
        y_psd0 = self.signal_psd(name="y_psd0", net=_y, with_contact=True)
        y_psd1 = self.signal_psd(name="y_psd1", net=_y, with_contact=False)
        y_nmos = self.nmos(name="y_nmos", net=_y, w_size="min")
        y_pmos = self.pmos(name="y_pmos", net=_y, w_size="min")

        ### columns and rows

        # clk
        clk_nmospad = self.polypad(name="clk_nmospad", net=clk)
        clk_pmospad = self.polypad(name="clk_pmospad", net=clk)

        clk_inv = self.activecolumn(
            name="clk_inv", connect=False, elements=(clk_nmos, clk_pmos),
        )
        clk_nmosrow = self.polyrow(name="clk_nmosrow", elements=(clk_nmos, clk_nmospad))
        clk_pmosrow = self.polyrow(name="clk_pmosrow", elements=(clk_pmos, clk_pmospad))
        clk_pin = self.m1pin(
            name="clk_pin", elements=(clk_nmospad, clk_pmospad),
        )

        # clk_n, pt. 1
        clk_n_polypad0 = self.polypad(name="clk_n_pad0", net=_clk_n)
        clk_n_polyknot = self.polyknot(name="clk_n_polyknot", net=_clk_n)
        clk_n_polypad1 = self.polypad(name="clk_n_pad1", net=_clk_n)

        clk_n_sds = self.activecolumn(
            name="clk_n_sds", connect=False, elements=(clk_n_nsd, clk_n_psd),
        )
        clk_n_inv = self.activecolumn(
            name="clk_n_inv", connect=True, elements=(clk_n_nmos0, clk_n_polyknot, clk_n_pmos0),
            left=(clk_nmospad, clk_pmospad),
        )
        clk_n_m1col0 = self.m1column(
            name="clk_n_m1col0", elements=(clk_n_nsd, clk_n_polypad0, clk_n_psd),
        )

        # clk_buf - pt. 1
        clk_buf_m1knot = self.m1knot(name="clk_buf_m1knot", net=_clk_buf)
        clk_buf_polypad0 = self.polypad(
            name="clk_buf_polypad0", net=_clk_buf, left=clk_n_inv,
        )

        clk_buf_sds = self.activecolumn(
            name="clk_buf_sds", connect=False, elements=(clk_buf_nsd, clk_buf_psd),
        )
        clk_buf_sdm1col = self.m1column(
            name="clk_buf_sdm1col", elements=(clk_buf_nsd, clk_buf_m1knot, clk_buf_psd),
        )
        clk_buf_m1row = self.m1row(
            name="clk_buf_m1row", elements=(clk_buf_m1knot, clk_buf_polypad0),
        )

        # clk_n/clk_buf transistor - pt. 1
        clk_trans0 = self.activecolumn(
            name="clk_trans0", connect=False, elements=(clk_n_nmos1, clk_buf_pmos0),
        )

        # sd interconnect
        _net0 = ckt.new_net(name="_net0", external=False)
        _net1 = ckt.new_net(name="_net1", external=False)
        _net2 = ckt.new_net(name="_net2", external=False)
        _net3 = ckt.new_net(name="_net3", external=False)
        _net4 = ckt.new_net(name="_net4", external=False)
        _net5 = ckt.new_net(name="_net5", external=False)
        _net6 = ckt.new_net(name="_net6", external=False)
        _net7 = ckt.new_net(name="_net7", external=False)

        net0_nsd = self.signal_nsd(name="net0_nsd", net=_net0, with_contact=False)
        net2_nsd = self.signal_nsd(name="net2_nsd", net=_net2, with_contact=False)
        net4_nsd = self.signal_nsd(name="net4_nsd", net=_net4, with_contact=False)
        net6_nsd = self.signal_nsd(name="net6_nsd", net=_net6, with_contact=False)
        net7_nsd = self.signal_nsd(name="net7_nsd", net=_net7, with_contact=False)

        net1_psd = self.signal_psd(name="net1_psd", net=_net1, with_contact=False)
        net3_psd = self.signal_psd(name="net3_psd", net=_net3, with_contact=False)
        net5_psd0 = self.signal_psd(name="net5_psd0", net=_net5, with_contact=True)
        net5_psd1 = self.signal_psd(name="net5_psd1", net=_net5, with_contact=True)

        sdcon0 = self.activecolumn(
            name="sdcon0", connect=False, elements=(net0_nsd, net1_psd),
        )
        sdcon1 = self.activecolumn(
            name="sdcon1", connect=False, elements=(net2_nsd, net3_psd),
        )
        sdcon2 = self.activecolumn(
            name="sdcon2", connect=False, elements=(net4_nsd, net5_psd1),
        )

        # i - pt.1
        i_nmospad = self.polypad(name="i_nmospad", net=i)
        i_pmospad = self.polypad(name="i_pmospad", net=i)

        i_trans = self.activecolumn(name="i_trans", connect=False, elements=(i_nmos, i_pmos))
        i_nmosrow = self.polyrow(name="i_nmosrow", elements=(i_nmospad, i_nmos))
        i_pmosrow = self.polyrow(name="i_pmosrow", elements=(i_pmospad, i_pmos))

        # u
        u_nmospad = self.polypad(
            name="u_nmospad", net=_u, left=(i_trans, i_nmospad),
            )
        u_pmospad = self.polypad(
            name="u_pmospad", net=_u, left=(i_trans, i_pmospad),
        )
        u_m1knot0 = self.m1knot(name="u_m1knot0", net=_u)
        u_m1knot1 = self.m1knot(name="u_m1knot1", net=_u)

        u_sds = self.activecolumn(
            name="u_sds", connect=False, elements=(u_nsd, u_psd),
        )
        u_nsdrow = self.m1row(name="u_nsdrow", elements=(u_nsd, u_m1knot0))
        u_psdrow = self.m1row(name="u_psdrow", elements=(u_psd, u_m1knot1))
        u_nmosrow = self.polyrow(name="u_nmosrow", elements=(u_nmospad, u_nmos))
        u_pmosrow = self.polyrow(name="u_pmosrow", elements=(u_pmospad, u_pmos))
        u_m1col = self.m1column(
            name="u_m1col", elements=(u_m1knot0, u_nmospad, u_pmospad, u_m1knot1),
        )
        u_trans = self.activecolumn(
            name="u_trans", connect=False, elements=(u_nmos, u_pmos),
        )

        # clk_n - pt. 2
        clk_n_nmos1pad = self.polypad(
            name="clk_n_nmos1pad", net=_clk_n, left=(u_trans, u_nmospad),
        )

        clk_n_nmos1row = self.polyrow(
            name="clk_n_nmos0row", elements=(clk_n_nmos1pad, clk_n_nmos1),
        )
        clk_n_m1col1 = self.m1column(
            name="clk_n_m1col1", elements=(clk_n_nmos1pad, clk_n_polypad1),
        )

        # clk_buf - pt. 2
        clk_buf_polypad1 = self.polypad(name="clk_buf_polypad1", net=_clk_buf)
        clk_buf_pmos0pad = self.polypad(
            name="clk_buf_pmos0pad", net=_clk_buf, left=(u_trans, u_pmospad),
        )
        clk_buf_pmos0m1knot = self.m1knot(name="clk_buf_pmos0m1knot", net=_clk_buf)

        clk_buf_pmos0polyrow = self.polyrow(
            name="clk_buf_pmos0polyrow", elements=(clk_buf_pmos0, clk_buf_pmos0pad)
        )
        clk_buf_pmos0m1row = self.m1row(
            name="clk_buf_pmos0m1row", elements=(clk_buf_pmos0pad, clk_buf_pmos0m1knot),
        )
        clk_buf_pmos0m1col = self.m1column(
            name="clk_buf_pmos0m1col", elements=(clk_buf_polypad1, clk_buf_pmos0m1knot),
        )

        # clk_n/clk_buf transistor - pt. 2
        clk_trans1 = self.activecolumn(
            name="clk_trans1", connect=False, elements=(clk_buf_nmos0, clk_n_pmos1),
            left=(clk_buf_pmos0pad, clk_n_nmos1pad),
        )
        clk_trans2 = self.activecolumn(
            name="clk_trans2", connect=False, elements=clk_buf_nmos1,
        )

        # i - pt. 2
        i_pin = self.m1pin(
            name="i_pin", elements=(i_nmospad, i_pmospad),
            left=clk_buf_polypad0, bottom=u_nsd, top=u_psd,
        )

        # y - pt.1
        y_nmospad = self.polypad(name="y_nmospad", net=_y, left=clk_trans1)
        y_pmospad = self.polypad(name="y_pmospad", net=_y, left=clk_trans1)

        y_trans = self.activecolumn(
            name="y_trans", connect=False, elements=(y_nmos, y_pmos),
        )

        # dff_m
        dff_m_m1knot0 = self.m1knot(name="dff_m_m1knot0", net=_dff_m)
        dff_m_m1knot1 = self.m1knot(name="dff_m_m1knot1", net=_dff_m)
        dff_m_m1knot2 = self.m1knot(name="dff_m_m1knot2", net=_dff_m)
        dff_m_nmospad = self.polypad(
            name="dff_m_nmospad", net=_dff_m, left=(y_trans, y_nmospad),
        )
        dff_m_pmospad = self.polypad(
            name="dff_m_pmospad", net=_dff_m, left=(y_trans, y_pmospad),
        )

        dff_m_sds = self.activecolumn(
            name="dff_n_sds", connect=False, elements=(dff_m_nsd, dff_m_psd)
        )
        dff_m_nsdrow = self.m1row(name="dff_m_nsdrow", elements=(dff_m_nsd, dff_m_m1knot0))
        dff_m_psdrow = self.m1row(
            name="dff_m_psdrow", elements=(dff_m_psd, dff_m_m1knot1, dff_m_m1knot2),
        )
        dff_m_m1col0 = self.m1column(
            name="dff_m_m1col0", elements=(dff_m_m1knot0, dff_m_m1knot1),
        )
        dff_m_m1col1 = self.m1column(
            name="dff_m_m1col1", elements=(dff_m_nmospad, dff_m_pmospad, dff_m_m1knot2),
        )
        dff_m_nmospolyrow = self.polyrow(
            name="dff_m_nmospolyrow", elements=(dff_m_nmospad, dff_m_nmos),
        )
        dff_m_pmospolyrow = self.polyrow(
            name="dff_m_pmospolyrow", elements=(dff_m_pmospad, dff_m_pmos),
        )
        dff_m_trans = self.activecolumn(
            name="dff_m_trans", connect=False, elements=(dff_m_nmos, dff_m_pmos),
            left=(y_nmospad, y_pmospad),
        )

        # y - pt.2
        y_m1knot0 = self.m1knot(name="y_m1knot0", net=_y)
        y_m1knot1 = self.m1knot(name="y_m1knot1", net=_y)
        y_m1knot2 = self.m1knot(name="y_m1knot2", net=_y)
        y_m1knot3 = self.m1knot(name="y_m1knot3", net=_y)

        y_nmospolyrow = self.polyrow(name="y_nmospolyrow", elements=(y_nmos, y_nmospad))
        y_pmospolyrow = self.polyrow(name="y_pmospolyrow", elements=(y_pmos, y_pmospad))
        net6_y_sds = self.activecolumn(
            name="net6_y_sds", connect=False, elements=(net6_nsd, y_psd0),
            left=(dff_m_nmospad, dff_m_pmospad),
        )
        y_vdd_sds = self.activecolumn(
            name="y_vdd_sds", connect=False, elements=(
                y_nsd0, self.vdd_sd(name="vdd_sd4")
            ),
        )
        y_nsdrow = self.m1row(
            name="y_nsdrow", elements=(y_m1knot0, y_m1knot1, y_nsd0),
        )
        y_m1col0 = self.m1column(
            name="y_m1col0", elements=(y_m1knot0, y_nmospad, y_pmospad),
        )
        y_m1col1 = self.m1column(
            name="y_m1col1", elements=(y_m1knot1, y_psd0),
        )
        y_m1col2 = self.m1column(
            name="y_m1col2", elements=(y_m1knot3, y_m1knot2)
        )
        y_psdrow = self.m1row(
            name="y_psdrow", elements=(y_psd0, y_m1knot2),
        )
        y_m1row1 = self.m1row(
            name="y_m1row1", elements=(y_m1knot3, y_psd1.contact),
        )
        y_net5_sds = self.activecolumn(
            name="y_net5_sds", connect=False, elements=(y_nsd2, net5_psd0),
            left=y_m1col2,
        )

        # nrst - pt. 1
        nrst_nmos0pad = self.polypad(name="nrst_nmos0pad", net=nrst)
        nrst_pmospad = self.polypad(name="nrst_pmospas", net=nrst)
        nrst_m1knot0 = self.m1knot(name="nrst_m1knot0", net=nrst)
        nrst_m1knot1 = self.m1knot(name="nrst_m1knot1", net=nrst)

        nrst_trans0 = self.activecolumn(
            name="nrst_trans0", connect=False, elements=(nrst_nmos0, nrst_pmos0),
        )
        y_nrst_actcol = self.activecolumn(
            name="y_nrst_actcol", connect=False, elements=(y_nsd1, nrst_pmos1),
        )
        nrst_nmos0polyrow = self.polyrow(
            name="nrst_nmos0polyrow", elements=(nrst_nmos0, nrst_nmos0pad)
        )
        nrst_pmospolyrow = self.polyrow(
            name="nrst_pmospolyrow", elements=(nrst_pmos0, nrst_pmospad, nrst_pmos1),
        )
        nrst_pin = self.m1pin(
            name="nrst_pin", elements=(nrst_m1knot0, nrst_nmos0pad, nrst_pmospad),
            bottom=y_nsd0, top=y_psdrow,
        )

        # clk_n - pt. 3
        clk_n_polyknot1 = self.polyknot(name="clk_n_polyknot1", net=_clk_n)
        clk_n_polyrow = self.polyrow(
            name="clk_n_polyrow", elements=(
                clk_n_polypad0, clk_n_polyknot, clk_n_polypad1, clk_n_pmos1, clk_n_polyknot1,
            )
        )

        # clk_n/clk_buf transistor - pt. 3
        clk_trans3 = self.activecolumn(
            name="clk_trans3", connect=True, elements=(
                clk_n_nmos2, clk_n_polyknot1, clk_n_pmos2,
            ),
        )
        nrst_clk_trans4 = self.activecolumn(
            name="clk_trans3", connect=False, elements=(nrst_nmos1, clk_buf_pmos1),
        )

        # clk_buf - pt. 3
        clk_buf_polypad2 = self.polypad(
            name="clk_buf_polypad2", net=_clk_buf, left=y_m1col1,
        )
        clk_buf_pmos1pad = self.polypad(
            name="clk_buf_pmos1pad", net=_clk_buf, left=clk_trans3,
        )
        clk_buf_pmos1polyrow = self.polyrow(
            name="clk_buf_pmos1row", elements=(clk_buf_pmos1pad, clk_buf_pmos1),
        )
        clk_buf_pmos1m1knot = self.m1knot(name="clk_buf_pmos1m1knot", net=_clk_buf)
        clk_buf_pmos1m1row = self.m1row(
            name="clk_buf_pmos1m1row", elements=(clk_buf_pmos1m1knot, clk_buf_pmos1pad),
        )
        clk_buf_pmos1m1col = self.m1column(
            name="clk_buf_pmos1m1col", elements=(clk_buf_polypad2, clk_buf_pmos1m1knot),
        )
        clk_buf_polyrow = self.polyrow(
            name="clk_buf_polyrow", elements=(
                clk_buf_polypad0, clk_buf_polypad1, clk_buf_nmos0, clk_buf_polypad2,
                clk_buf_nmos1,
            ),
        )

        # nrst - pt. 2
        nrst_nmos1pad = self.polypad(name="nrst_nmos1pad", net=nrst, left=clk_trans3)

        nrst_nmos1polyrow = self.polyrow(
            name="nrst_nmos1polyrow", elements=(nrst_nmos1pad, nrst_nmos1),
        )
        nrst_m1row = self.m1row(
            name="nrst_m1row", elements=(nrst_m1knot0, nrst_m1knot1),
        )
        nrst_m1col1 = self.m1column(
            name="nrst_m1col1", elements=(nrst_m1knot1, nrst_nmos1pad),
        )

        # net5
        net5_psdrow = self.m1row(
            name="net5_m1row", elements=(net5_psd0, net5_psd1),
        )
        # q - pt. 1
        q_trans = self.activecolumn(
            name="q_trans", connect=False, elements=(q_nmos, q_pmos),
        )

        # dff_s - pt. 1
        dff_s_m1knot0 = self.m1knot(name="dff_s_m1knot0", net=_dff_s)
        dff_s_m1knot1 = self.m1knot(name="dff_s_m1knot1", net=_dff_s)
        dff_s_polyknot = self.polyknot(name="dff_s_polyknot", net=_dff_s)
        dff_s_polypad = self.polypad(
            name="dff_s_polypad", net=_dff_s, left=clk_trans3,
        )

        dff_s_y_sds = self.activecolumn(
            name="dff_s_y_sds", connect=False, elements=(dff_s_nsd, y_psd1),
        )
        net7_dff_s_sds = self.activecolumn(
            name="net7_dff_s_sds", connect=False, elements=(net7_nsd, dff_s_psd),
        )
        dff_s_polyrow = self.polyrow(
            name="dff_s_polyrow", elements=(dff_s_polypad, dff_s_polyknot)
        )
        dff_s_nsdrow = self.m1row(
            name="dff_s_nsdrow", elements=(dff_s_nsd, dff_s_m1knot0),
        )
        dff_s_m1row = self.m1row(
            name="dff_s_m1row", elements=(dff_s_psd.contact, dff_s_m1knot1),
        )
        dff_s_m1col = self.m1column(
            name="dff_s_m1col", elements=(dff_s_m1knot0, dff_s_polypad, dff_s_m1knot1),
            left=clk_buf_pmos1pad,
        )

        # q - pt. 2
        q_nmospad = self.polypad(name="q_nmospad", net=q, left=dff_s_m1col)
        q_pmospad = self.polypad(name="q_pmospad", net=q, left=dff_s_m1col)
        q_m1knot0 = self.m1knot(name="q_m1knot0", net=q)
        q_m1knot1 = self.m1knot(name="q_m1knot1", net=q)

        q_nmospolyrow = self.polyrow(name="q_nmospolyrow", elements=(q_nmos, q_nmospad))
        q_pmospolyrow = self.polyrow(name="q_pmospolyrow", elements=(q_pmos, q_pmospad))
        q_sds = self.activecolumn(
            name="q_sds", connect=False, elements=(q_nsd, q_psd),
            left=dff_s_polypad
        )
        q_nsdrow = self.m1row(name="q_nsdrow", elements=(q_m1knot0, q_nsd))
        q_psdrow = self.m1row(name="q_psdrow", elements=(q_m1knot1, q_psd))
        q_pin = self.m1pin(
            name="q_pin", elements=(q_m1knot0, q_nmospad, q_pmospad, q_m1knot1),
            left=net5_psd1,
        )

        # dff_s - pt. 2
        dff_s_inv = self.activecolumn(
            name="dff_s_inv", connect=True, elements=(
                dff_s_nmos, dff_s_polyknot, dff_s_pmos,
            ), left=(q_nmospad, q_pmospad),
        )

        # vss/vdd sd
        vssvdd_sds = tuple(
            self.activecolumn(name=f"vssvdd_sd{n}", connect=False, elements=(
                self.vss_sd(name=f"vss_sd{n}"), self.vdd_sd(name=f"vdd_sd{n}"),
            ))
            for n in range(4)
        )

        # gap
        actgap = self.activecolumn(name="actgap", connect=False, elements=())

        ### constraints

        return self.constraints(
            activecolumns=(
                clk_n_sds, clk_inv, vssvdd_sds[0], clk_n_inv, clk_buf_sds, actgap,
                u_sds, i_trans, vssvdd_sds[1], u_trans, sdcon0, clk_trans0, dff_m_sds,
                clk_trans1, sdcon1, y_trans, vssvdd_sds[2], dff_m_trans,
                net6_y_sds, nrst_trans0, y_vdd_sds, y_nrst_actcol, y_net5_sds,
                clk_trans2, dff_s_y_sds, clk_trans3, net7_dff_s_sds, nrst_clk_trans4,
                sdcon2, q_trans, vssvdd_sds[3], dff_s_inv, q_sds,
            ),
            polyrows=(
                self.multipolyrow(name="polyrow1", rows=(
                    i_nmosrow, u_nmosrow, clk_n_nmos1row, y_nmospolyrow, dff_m_nmospolyrow,
                    nrst_nmos0polyrow, nrst_nmos1polyrow, q_nmospolyrow,
                )),
                self.multipolyrow(name="polyrow2", rows=(
                    clk_nmosrow, clk_buf_polyrow, dff_s_polyrow,
                )),
                self.multipolyrow(name="polyrow3", rows=(
                    clk_n_polyrow, clk_buf_pmos1polyrow, q_pmospolyrow,
                )),
                self.multipolyrow(name="polyrow4", rows=(
                    clk_pmosrow, i_pmosrow, u_pmosrow, clk_buf_pmos0polyrow, y_pmospolyrow,
                    dff_m_pmospolyrow, nrst_pmospolyrow,
                )),
            ),
            m1rows=(
                self.multim1row(name="nsdmrow", rows=(
                    u_nsdrow, dff_m_nsdrow, y_nsdrow, dff_s_nsdrow,
                )),
                # q_nsdrow need separate multirow as they have different y
                self.multim1row(name="nsdmrowmax", rows=q_nsdrow),
                nrst_m1row.multim1row,
                clk_buf_m1row.multim1row,
                clk_buf_pmos1m1row.multim1row,
                clk_buf_pmos0m1row.multim1row,
                # Put y_m1row1, dff_s_m1row on separate row to put them as high as possible
                # This is relying on internal fact that multirow without a poly contact
                # but with a SignalSDContactT should be separate row to them as high as possible.
                self.multim1row(
                    name="pmosm1row", rows=(y_m1row1, dff_s_m1row),
                ),
                self.multim1row(name="psdmrow", rows=(
                    u_psdrow, dff_m_psdrow, y_psdrow, net5_psdrow,
                )),
                # q_psdrow need separate multirow as they have different y
                self.multim1row(name="psdmrowmax", rows=q_psdrow),
            ),
            m1columns=(
                clk_n_m1col0.multim1column, clk_pin.multim1column,
                clk_buf_sdm1col.multim1column, i_pin.multim1column,
                u_m1col.multim1column, clk_n_m1col1.multim1column,
                clk_buf_pmos0m1col.multim1column, dff_m_m1col0.multim1column,
                y_m1col0.multim1column, dff_m_m1col1.multim1column,
                y_m1col1.multim1column, nrst_pin.multim1column,
                self.multim1column(name="clkbuf_y_m1col", columns=(
                    clk_buf_pmos1m1col, y_m1col2,
                )),
                nrst_m1col1.multim1column,
                dff_s_m1col.multim1column, q_pin.multim1column,
            ),
        )


class _Gallery(_fab.FactoryCell["StdCellFactory"]):
    def __init__(self, *, name: str, fab: "StdCellFactory", cells: Iterable[_cell.Cell]):
        cells = tuple(cells)

        canvas = fab.canvas

        m1 = canvas._metal1
        m1pin = canvas._metal1pin
        via = canvas._via1
        m2 = canvas._metal2

        super().__init__(name=name, fab=fab)

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()

        n_cells = len(cells)

        cells2 = tuple(reversed(cells))

        # Make a shuffled row of cells for more DRC checking
        def shuffled_i(i: int) -> int:
            is_odd = (i%2) == 1
            if not is_odd:
                return n_cells - (i//2) - 1
            else:
                return (i//2)
        cells3 = tuple(cells[shuffled_i(i)] for i in range(n_cells))

        vss_ports = []
        vdd_ports = []
        x0 = x1 = x2 = 0.0
        for i, cell in enumerate(cells):
            inst = ckt.instantiate(cell, name=f"{cell.name}[0]")

            for port in inst.ports:
                if port.name == "vss":
                    vss_ports.append(port)
                elif port.name == "vdd":
                    vdd_ports.append(port)
                else:
                    ckt.new_net(
                        name=f"{inst.name}.{port.name}", external=False, childports=port,
                    )

            layouter.place(inst, x=x0, y=0.0)
            x0 += cast(_Cell, cell).width

            cell2 = cells2[i]
            inst = ckt.instantiate(cell2, name=f"{cell2.name}[1]")

            for port in inst.ports:
                if port.name == "vss":
                    vss_ports.append(port)
                elif port.name == "vdd":
                    vdd_ports.append(port)
                else:
                    ckt.new_net(
                        name=f"{inst.name}.{port.name}", external=False, childports=port,
                    )

            layouter.place(inst, x=x1, y=0.0, rotation=_geo.Rotation.MX)
            x1 += cast(_Cell, cell2).width

            cell3 = cells3[i]
            inst = ckt.instantiate(cell3, name=f"{cell3.name}[2]")

            for port in inst.ports:
                if port.name == "vss":
                    vss_ports.append(port)
                elif port.name == "vdd":
                    vdd_ports.append(port)
                else:
                    ckt.new_net(
                        name=f"{inst.name}.{port.name}", external=False, childports=port,
                    )

            layouter.place(inst, x=x2, y=2*canvas._cell_height, rotation=_geo.Rotation.MX)
            x2 += cast(_Cell, cell3).width

        vss = ckt.new_net(name="vss", external=True, childports=vss_ports)
        vdd = ckt.new_net(name="vdd", external=True, childports=vdd_ports)

        # Put labels for vss pin
        bottom = -canvas._m1_vssrail_width
        top = canvas._m1_vssrail_width
        shape = _geo.Rect(left=0.0, bottom=bottom, right=x0, top=top)
        layouter.add_wire(net=vss, wire=m1, pin=m1pin, shape=shape)
        _l = layouter.wire_layout(
            net=vss, wire=via, bottom_height=2*canvas._m1_vssrail_width,
        )
        _m1bb = _l.bounds(mask=m1.mask)
        l = layouter.place(_l,
            x=-_m1bb.left, y=(bottom - _m1bb.bottom),
        )
        via_m2bb1 = l.bounds(mask=m2.mask)

        bottom = 2*canvas._cell_height - canvas._m1_vssrail_width
        top = 2*canvas._cell_height
        shape = _geo.Rect(left=0.0, bottom=bottom, right=x0, top=top)
        layouter.add_wire(net=vss, wire=m1, pin=m1pin, shape=shape)
        _l = layouter.wire_layout(
            net=vss, wire=via, bottom_height=canvas._m1_vssrail_width,
        )
        _m1bb = _l.bounds(mask=m1.mask)
        l = layouter.place(_l,
            x=-_m1bb.left, y=(bottom - _m1bb.bottom),
        )
        via_m2bb2 = l.bounds(mask=m2.mask)

        shape = _geo.Rect.from_rect(rect=via_m2bb1, top=via_m2bb2.top)
        layouter.add_wire(net=vss, wire=m2, shape=shape)

        # Put labels for vdd pin
        bottom = -canvas._cell_height
        top = -canvas._cell_height + canvas._m1_vddrail_width
        shape = _geo.Rect(left=0.0, bottom=bottom, right=x0, top=top)
        layouter.add_wire(net=vdd, wire=m1, pin=m1pin, shape=shape)
        _l = layouter.wire_layout(
            net=vdd, wire=via, bottom_height=canvas._m1_vddrail_width,
        )
        _m1bb = _l.bounds(mask=m1.mask)
        l = layouter.place(_l,
            x=(x0 - _m1bb.right), y=(bottom - _m1bb.bottom),
        )
        via_m2bb1 = l.bounds(mask=m2.mask)

        bottom = canvas._cell_height - canvas._m1_vddrail_width
        top = canvas._cell_height + canvas._m1_vddrail_width
        shape = _geo.Rect(left=0.0, bottom=bottom, right=x0, top=top)
        layouter.add_wire(net=vdd, wire=m1, pin=m1pin, shape=shape)
        _l = layouter.wire_layout(
            net=vdd, wire=via, bottom_height=2*canvas._m1_vddrail_width,
        )
        _m1bb = _l.bounds(mask=m1.mask)
        l = layouter.place(_l,
            x=(x0 - _m1bb.right), y=(bottom - _m1bb.bottom),
        )
        via_m2bb2 = l.bounds(mask=m2.mask)

        shape = _geo.Rect.from_rect(rect=via_m2bb1, top=via_m2bb2.top)
        layouter.add_wire(net=vdd, wire=m2, shape=shape)

        # Set boundary
        assert abs(x0 - x1) < _geo.epsilon, "Internal error"
        assert abs(x0 - x2) < _geo.epsilon, "Internal error"
        layouter.layout.boundary = _geo.Rect(
            left=0.0, bottom=-canvas._cell_height,
            right=x0, top=2*canvas._cell_height,
        )


class StdCellFactory(_fab.CellFactory[_Cell]):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, cktfab: _ckt.CircuitFactory,
        layoutfab: _lay.LayoutFactory,
        name_prefix: str="", name_suffix: str="",
        canvas: StdCellCanvas,
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab, cell_class=_Cell,
            name_prefix=name_prefix, name_suffix=name_suffix,
        )
        self._lib: _lbry.RoutingGaugeLibrary
        self.lib: _lbry.RoutingGaugeLibrary

        self._canvas = canvas
        self._cktfab = cktfab
        self._layoutfab = layoutfab

    @property
    def canvas(self) -> StdCellCanvas:
        return self._canvas

    def add_default(self) -> None:
        self.add_fillers()
        self.add_diodes()
        self.add_logicconsts()
        self.add_inverters()
        self.add_buffers()
        self.add_nands()
        self.add_ands()
        self.add_nors()
        self.add_ors()
        self.add_mux2()
        self.add_aooas()
        self.add_xors()
        self.add_latches()
        self.add_flops()
        self.add_gallery()

    def add_fillers(self):
        """Add a set of fill cells to the library.
        """
        self.new_cell(name="fill", cell_class=_Fill)
        self.new_cell(name="tie", cell_class=_Tie)
        try:
            self.new_cell(name="tie_diff", cell_class=_Tie, max_diff=True)
        except NotEnoughRoom:
            pass # Will add _w2 cell below
        try:
            self.new_cell(name="tie_poly", cell_class=_Tie, max_poly=True)
        except NotEnoughRoom:
            pass # Will add _w2 cell below
        for i in (2, 4):
            self.new_cell(name=f"fill_w{i}", cell_class=_Fill, width=i)
            self.new_cell(name=f"tie_w{i}", cell_class=_Tie, width=i)
            self.new_cell(name=f"tie_diff_w{i}", cell_class=_Tie, max_diff=True, width=i)
            self.new_cell(name=f"tie_poly_w{i}", cell_class=_Tie, max_poly=True, width=i)

    def add_diodes(self):
        """Add an antenna diode cell to the library."""
        self.new_cell(name="diode_w1", cell_class=_Diode)

    def add_logicconsts(self):
        """Add logic 0 and 1 cells
        """
        self.new_cell(name="zero_x1", cell_class=_ZeroOneDecap, zero_pin=True, one_pin=False)
        self.new_cell(name="one_x1", cell_class=_ZeroOneDecap, zero_pin=False, one_pin=True)
        self.new_cell(name="zeroone_x1", cell_class=_ZeroOneDecap, zero_pin=True, one_pin=True)
        self.new_cell(name="decap_w0", cell_class=_ZeroOneDecap, zero_pin=False, one_pin=False)

    def add_inverters(self):
        """Add a set of inverters to the library.
        """
        for drive in (0, 1, 2, 4):
            self.new_cell(name=f"inv_x{drive}", cell_class=_Inv, drive=drive)

    def add_buffers(self):
        """Add a set of buffer to the library"""
        for d0, d1 in ((0, 1), (0, 2), (1, 4)):
            self.new_cell(
                name=f"buf_x{d1}", cell_class=_Buf, drive_first=d0, drive_second=d1,
            )

    def add_nands(self):
        """Add a set of nand gates to the library"""
        for ins, d in product(range(2, 5), range(2)):
            self.new_cell(
                name=f"nand{ins}_x{d}", cell_class=_Nand, drive=d, inputs=ins,
            )

    def add_ands(self):
        """Add a set of and gates to the library"""
        for ins in range(2, 5):
            self.new_cell(
                name=f"and{ins}_x1", cell_class=_And, drive=1, inputs=ins,
            )

    def add_nors(self):
        """Add a set of nor gates to the library"""
        for ins, d in product(range(2, 5), range(2)):
            self.new_cell(
                name=f"nor{ins}_x{d}", cell_class=_Nor, drive=d, inputs=ins,
            )

    def add_ors(self):
        """Add a set of or gates to the library"""
        for ins in range(2, 5):
            self.new_cell(
                name=f"or{ins}_x1", cell_class=_Or, drive=1, inputs=ins,
            )

    def add_mux2(self):
        self.new_cell(name=f"mux2_x1", cell_class=_Mux2)

    def add_aooas(self):
        self.new_cell(name="and21nor_x0", cell_class=_And21Nor, drive=0)
        self.new_cell(name="and21nor_x1", cell_class=_And21Nor, drive=1)
        self.new_cell(name="or21nand_x0", cell_class=_Or21Nand, drive=0)
        self.new_cell(name="or21nand_x1", cell_class=_Or21Nand, drive=1)

    def add_xors(self):
        self.new_cell(name="xor2_x0", cell_class=_Xor2, inverted=False, drive=0)
        self.new_cell(name="nexor2_x0", cell_class=_Xor2, inverted=True, drive=0)

    def add_latches(self):
        self.new_cell(name="nsnrlatch_x0", cell_class=_nRnSLatch, drive=0)
        self.new_cell(name="nsnrlatch_x1", cell_class=_nRnSLatch, drive=1)

    def add_flops(self):
        self.new_cell(name="dff_x1", cell_class=_DFF, drive=1)
        self.new_cell(name="dffnr_x1", cell_class=_DFFnR, drive=1)

    def add_gallery(self):
        self.new_cell(name="Gallery", cell_class=_Gallery, cells=self.lib.cells)
