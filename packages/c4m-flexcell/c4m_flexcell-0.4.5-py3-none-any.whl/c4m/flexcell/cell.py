# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from math import ceil
from typing import Optional

from pdkmaster.technology import geometry as _geo, net as _net
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, library as _lbry, factory as _fab,
)

from .canvas import StdCellCanvas


class _Cell(_fab.FactoryCell["_scfab.StdCellFactory"]):
    def __init__(self, *, name: str, fab: "_scfab.StdCellFactory"):
        super().__init__(name=name, fab=fab)

        canvas = fab.canvas

        self._width: Optional[float] = None

        ckt = self.new_circuit()
        self._layouter = self.new_circuitlayouter()

        vdd = ckt.new_net(name="vdd", external=True)
        vss = ckt.new_net(name="vss", external=True)

        self._nwell_net: Optional[_ckt.CircuitNetT] = None if canvas._nwell is None else vdd
        self._pwell_net: Optional[_ckt.CircuitNetT] = None if canvas._pwell is None else vss

    @property
    def layouter(self) -> _lay.CircuitLayouterT:
        return self._layouter
    @property
    def lib(self) -> _lbry.RoutingGaugeLibrary:
        return self.fab.lib
    @property
    def canvas(self) -> StdCellCanvas:
        return self.fab.canvas
    @property
    def width(self) -> float:
        if self._width is None:
            raise AttributeError(f"Width of cell '{self.name}' accessed before being set")
        return self._width

    @property
    def vdd(self) -> _ckt.CircuitNetT:
        return self.circuit.nets.vdd
    @property
    def vss(self) -> _ckt.CircuitNetT:
        return self.circuit.nets.vss
    @property
    def nwell_net(self) -> Optional[_ckt.CircuitNetT]:
        return self._nwell_net
    @property
    def pwell_net(self) -> Optional[_ckt.CircuitNetT]:
        return self._pwell_net

    def set_width(self, *,
        width: Optional[float]=None, min_width: Optional[float]=None,
    ) -> float:
        if (width is None) and (min_width is None):
            raise ValueError("either width or min_width has to be provided")

        tech = self.tech
        canvas = self.canvas
        nwell = canvas._nwell
        pwell = canvas._pwell
        metal1 = canvas._metal1
        metal1pin = canvas._metal1pin
        ckt = self.circuit
        layouter = self._layouter

        if width is None:
            assert min_width is not None
            pitches = ceil((min_width - 0.5*tech.grid)/canvas._cell_horplacement_grid)
            width = pitches*canvas._cell_horplacement_grid

        g = canvas._cell_horplacement_grid
        if not tech.is_ongrid(width % g):
            raise ValueError(
                f"width of {width}µm is not a multiple of cell placement grid of {g}µm"
            )

        self._width = width

        # vdd
        net = ckt.nets["vdd"]
        left = 0.0
        bottom = canvas._cell_height - canvas._m1_vddrail_width
        right = width
        top = canvas._cell_height
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))

        if nwell is not None:
            left = -canvas._min_active_nwell_enclosure
            bottom = canvas._well_edge_height
            right = width + canvas._min_active_nwell_enclosure
            top = canvas._cell_height + canvas._min_active_nwell_enclosure
            layouter.add_wire(net=net, wire=nwell, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))

        # vss
        net = ckt.nets["vss"]
        left = 0.0
        bottom = 0.0
        right = width
        top = canvas._m1_vssrail_width
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))

        if pwell is not None:
            left = -canvas._min_active_well_enclosure
            bottom = -canvas._min_active_well_enclosure
            right = width + canvas._min_active_well_enclosure
            top = canvas._well_edge_height
            layouter.add_wire(net=net, wire=pwell, shape=_geo.Rect(
                left=left, bottom=bottom, right=right, top=top,
            ))

        # boundary
        layouter.layout.boundary = bnd = _geo.Rect(
            left=0.0, bottom=0.0, right=width, top=canvas._cell_height,
        )
        if canvas._inside is not None:
            assert canvas._inside_enclosure is not None
            for n, ins in enumerate(canvas._inside):
                shape = _geo.Rect.from_rect(rect=bnd, bias=canvas._inside_enclosure[n])
                layouter.layout.add_shape(shape=shape, layer=ins, net=None)

        return width


from . import factory as _scfab
