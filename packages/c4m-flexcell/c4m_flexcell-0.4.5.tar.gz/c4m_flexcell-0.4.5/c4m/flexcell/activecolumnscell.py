# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from itertools import chain
import abc
import asyncio
from threading import Thread
from typing import (
    List, Tuple, Iterator, Optional, Union, TypeVar, Generic, cast,
)

from pdkmaster.typing import MultiT, cast_MultiT, OptMultiT, cast_OptMultiT
from pdkmaster.technology import property_ as _prp, geometry as _geo, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay

from .cell import _Cell
from ._waiters import _WaiterFactory

__all__ = [
    "NSDT", "PSDT", "VssSDT", "VddSDT",
    "NMOST", "PMOST",
    "PolyContactT", "PolyKnotT",
    "M1KnotT",
    "ActiveColumnT", "PolyRowT", "M1RowT", "M1ColumnT",
    "ConstraintsT",
    "ActiveColumnsCell",
]


T = TypeVar("T")
def cast_MultiElemT(vs: MultiT[T]) -> Tuple[T, ...]:
    return cast_MultiT(vs, singular_type=(
        _ElementsElement, _MultiElementsColumn, _MultiElementsRow,
    ))
def cast_OptMultiElemT(vs: OptMultiT[T]) -> Optional[Tuple[T, ...]]:
    return cast_OptMultiT(vs, singular_type=(
        _ElementsElement, _MultiElementsColumn, _MultiElementsRow,
    ))


class _Element:
    """Base class for cell elements

    The base class provides notion of being places or not and facility to call
    callback functions when the element is placed. Child classes need to call
    the `_set_placed()` method at appropriate times.
    """
    def __init__(self, *, cell: "ActiveColumnsCell", name: str) -> None:
        if not name:
            raise ValueError("name may not be empty string")

        self._cell = cell
        self._name = name
        # self.log(f"__init__(cell={cell}), name={name}")

        self._wait_placed = cell._waiterfab.new_waiter(name=f"{self.name}:placed")

    @property
    def cell(self) -> "ActiveColumnsCell":
        return self._cell
    @property
    def name(self) -> str:
        return self._name

    @property
    def is_placed(self) -> bool:
        return self._wait_placed.released

    async def _wait4placement(self):
        # self.log("_wait4placement(): enter")
        await self._wait_placed.wait()
        # self.log("_wait4placement(): leave")

    def _set_placed(self) -> None:
        # self.log("_Element._set_placed(): enter")
        self._wait_placed.done()
        # self.log("_Element._set_placed(): leave")

    def log(self, *args):
        print(f"[{self.cell.name}:_Element[{self.name}]]", *args)


class _LayoutElement(_Element):
    """Base class for cell elements with a layout associated that will
    be placed into the cell layout."""
    def __init__(self, *, cell: "ActiveColumnsCell", name: str) -> None:
        super().__init__(cell=cell, name=name)

        wfab = cell._waiterfab

        self.__unplaced: Optional[_lay.LayoutT] = None
        self._x_waiter = wfab.new_floatwaiter(name=f"{self.name}:x")
        self._y_waiter = wfab.new_floatwaiter(name=f"{self.name}:y")
        self.__placed: Optional[_lay.LayoutT] = None

    async def _wait4x(self) -> float:
        return await self._x_waiter.wait4value()

    async def _wait4y(self) -> float:
        return await self._y_waiter.wait4value()

    @property
    def _has_unplaced(self) -> bool:
        return self.__unplaced is not None
    def _get_unplaced(self) -> _lay.LayoutT:
        if self.__unplaced is None:
            raise RuntimeError(
                f"Internal error: non-exising _unplaced accessed on elem '{self._name}'",
            )
        return self.__unplaced
    def _set_unplaced(self, layout: _lay.LayoutT) -> None:
        # self.log("_set_unplaced() enter")
        if self._has_unplaced:
            raise RuntimeError(f"Internal error: element '{self.name}' already has layout")
        self.__unplaced = layout
        self._try_place()
        # self.log("_set_unplaced() leave")
    _unplaced = property(_get_unplaced, _set_unplaced)

    @property
    def _has_x(self) -> bool:
        return self._x_waiter.has_value
    def _get_x(self) -> float:
        return self._x_waiter.value
    def _set_x(self, x: float) -> None:
        # self.log(f"setting x to {x} enter")
        self._x_waiter.value = x
        self._try_place()
        # self.log(f"setting x to {x} leave")
    _x = property(_get_x, _set_x)

    @property
    def _has_y(self) -> bool:
        return self._y_waiter.has_value
    def _get_y(self) -> float:
        return self._y_waiter.value
    def _set_y(self, y: float) -> None:
        # self.log(f"setting y to {y} enter")
        self._y_waiter.value = y
        self._try_place()
        # self.log(f"setting y to {y} leave")
    _y = property(_get_y, _set_y)

    def _try_place(self) -> bool:
        if (
            (self.__unplaced is not None)
            and self._x_waiter.has_value
            and self._y_waiter.has_value
        ):
            self.__placed = self.cell.layouter.place(
                self.__unplaced, origin=_geo.Point(
                    # Use value from intern waiters so possible overloaded properties
                    # in subclasses are ignored.
                    x=self._x_waiter.value, y=self._y_waiter.value,
                )
            )
            self._set_placed()

            return True
        else:
            return False

    @property
    def _placed(self) -> _lay.LayoutT:
        if self.__placed is None:
            raise RuntimeError(f"Internal error: elem '{self._name} is not placed yet")
        return self.__placed


class _NetElement(_LayoutElement):
    """Base class for cell elements with a net"""
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT,
    ) -> None:
        super().__init__(cell=cell, name=name)
        self.net = net


_netelem_type = TypeVar("_netelem_type", bound=_NetElement)
class _ElementsElement(_Element, Generic[_netelem_type]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[_netelem_type],
    ) -> None:
        super().__init__(cell=cell, name=name)
        self._elements = cast_MultiElemT(elements)

    @property
    def elements(self) -> Tuple[_netelem_type, ...]:
        return self._elements

    def __iter__(self) -> Iterator[_netelem_type]:
        return self.elements.__iter__()

    def __getitem__(self, key):
        return self.elements.__getitem__(key)

    def __len__(self) -> int:
        return self.elements.__len__()


class _ElementsRow(_ElementsElement[_netelem_type], Generic[_netelem_type]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[_netelem_type],
    ) -> None:
        super().__init__(cell=cell, name=name, elements=elements)

        self._y_waiter = cell._waiterfab.new_floatwaiter(name=f"{name}:y")
        self._elems_done: bool = False

    async def _wait4y(self) -> float:
        return await self._y_waiter.wait4value()

    @property
    def _has_y(self) -> bool:
        return self._y_waiter.has_value
    def _get_y(self) -> float:
        return self._y_waiter.value
    def _set_y(self, y: float):
        self._y_waiter.value = y
        if not self._elems_done:
            for elem in self:
                elem._y = y
            self._elems_done = True
        self._set_placed()
    _y = property(_get_y, _set_y)


class _ElementsColumn(_ElementsElement[_netelem_type], Generic[_netelem_type]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[_netelem_type],
    ) -> None:
        super().__init__(cell=cell, name=name, elements=elements)

        self._x_waiter = cell._waiterfab.new_floatwaiter(name=f"{name}:x")
        self._elems_done: bool = False

    async def _wait4x(self) -> float:
        return await self._x_waiter.wait4value()

    @property
    def _has_x(self) -> bool:
        return self._x_waiter.has_value
    def _get_x(self) -> float:
        return self._x_waiter.value
    def _set_x(self, x: float):
        self._x_waiter.value = x
        if not self._elems_done:
            for elem in self:
                elem._x=x
            self._elems_done = True
        self._set_placed()
    _x = property(_get_x, _set_x)


_elemrow_type = TypeVar("_elemrow_type", bound=_ElementsRow)
class _MultiElementsRow(_Element, Generic[_elemrow_type, _netelem_type]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, rows: MultiT[_elemrow_type],
    ) -> None:
        super().__init__(cell=cell, name=name)

        self._rows = cast_MultiElemT(rows)

        self._y_waiter = cell._waiterfab.new_floatwaiter(name=f"{name}:y")
        self._elems_done: bool = False

    async def _wait4y(self) -> float:
        return await self._y_waiter.wait4value()

    @property
    def _has_y(self) -> bool:
        return self._y_waiter.has_value
    def _get_y(self) -> float:
        return self._y_waiter.value
    def _set_y(self, y: float):
        self._y_waiter.value = y
        if not self._elems_done:
            for row in self:
                row._y = y
            self._elems_done = True
        self._set_placed()
    _y = property(_get_y, _set_y)

    def __iter__(self) -> Iterator[_elemrow_type]:
        return self._rows.__iter__()

    def __iter_elems__(self) -> Iterator[_netelem_type]:
        return chain(*self._rows)

    def __getitem__(self, key):
        return self._rows.__getitem__(key)


_elemcol_type = TypeVar("_elemcol_type", bound=_ElementsColumn)
class _MultiElementsColumn(_Element, Generic[_elemcol_type, _netelem_type]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, columns: MultiT[_elemcol_type],
    ) -> None:
        super().__init__(cell=cell, name=name)

        self._columns = cast_MultiElemT(columns)

        self._x_waiter = cell._waiterfab.new_floatwaiter(name=f"{cell}:x")
        self._elems_done = False

    async def _wait4x(self) -> float:
        return await self._x_waiter.wait4value()

    @property
    def _has_x(self) -> bool:
        return self._x_waiter.has_value
    def _get_x(self) -> float:
        return self._x_waiter.value
    def _set_x(self, x: float):
        self._x_waiter.value = x
        if not self._elems_done:
            for col in self:
                col._x=x
            self._elems_done = True
        self._set_placed()
    _x = property(_get_x, _set_x)

    def __iter__(self) -> Iterator[_elemcol_type]:
        return self._columns.__iter__()

    def __iter_elems__(self) -> Iterator[_netelem_type]:
        return chain(*self._columns)

    def __getitem__(self, key):
        return self._columns.__getitem__(key)


class _SD(_NetElement):
    """Element representing source/drain region of transistor"""
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, with_contact: bool,
        _implant: Optional[_prm.Implant],
        _well: Optional[_prm.Well], _well_net: Optional[_ckt.CircuitNetT],
        _bottom_enclosure: str, _bottom_implant_enclosure: Optional[_prp.Enclosure],
        _top_enclosure: str,
    ) -> None:
        super().__init__(name=name, cell=cell, net=net)
        self.with_contact = with_contact

        self._implant = _implant
        self._well = _well
        self._well_net = _well_net

        self._active_bottom: Optional[float] = None
        self._active_top: Optional[float] = None
        self._m1_bottom: Union[None, float, str] = None
        self._m1_top: Union[None, float, str] = None

        assert (_implant is None) == (_bottom_implant_enclosure is None)
        self._bottom_enclosure = _bottom_enclosure
        self._bottom_implant_enclosure = _bottom_implant_enclosure
        self._top_enclosure = _top_enclosure

        super()._set_y(0.0)

    # All _SD elements have the _has_contact property but it will only return
    # True for those that support it and have one.
    @property
    def _has_contact(self) -> bool:
        return False

    def _set_active_bottom(self, *, v: float) -> None:
        if self._active_bottom is not None:
            raise RuntimeError(
                f"Internal error: _active_bottom set twice for SD '{self.name}'"
            )
        self._active_bottom = v
        self._try_unplaced()

    def _set_active_top(self, *, v: float) -> None:
        if self._active_top is not None:
            raise RuntimeError(
                f"Internal error: _active_top set twice for SD '{self.name}'"
            )
        self._active_top = v
        self._try_unplaced()

    def _set_m1_bottom(self, *, v: Union[float, str]) -> None:
        if self._m1_bottom is not None:
            raise RuntimeError(
                f"Internal error: _m1_bottom set twice for SD '{self.name}'"
            )
        if not self.with_contact:
            raise RuntimeError(
                f"Internal error: _m1_bottom specified for SD '{self.name}' without contact"
            )
        if isinstance(v, str) and (v != "max"):
            raise RuntimeError(
                f"Internal error: _m1_bottom for SD '{self.name}' is string but not 'max'"
            )
        self._m1_bottom = v
        self._try_unplaced()

    def _set_m1_top(self, *, v: Union[float, str]) -> None:
        if self._m1_top is not None:
            raise RuntimeError(
                f"Internal error: _m1_top set twice for SD '{self.name}'"
            )
        if not self.with_contact:
            raise RuntimeError(
                f"Internal error: _m1_top specified for SD '{self.name}' without contact"
            )
        if isinstance(v, str) and (v != "max"):
            raise RuntimeError(
                f"Internal error: _m1_bottom for SD '{self.name}' is string but not 'max'"
            )
        self._m1_top = v
        self._try_unplaced()

    def _try_unplaced(self) -> None:
        cell = self.cell
        tech = cell.tech
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        active = canvas._active
        contact = canvas._contact

        # Generate a new circuit layouter as we may not add the layout yet to
        # the full layout but we are using features from the add_wire() method.
        layouter = cell.fab.layoutfab.new_circuitlayouter(
            circuit=cell.circuit, boundary=None,
        )

        if self.with_contact:
            if (
                (self._active_bottom is not None)
                and (self._active_top is not None)
                and (self._m1_bottom is not None)
                and (self._m1_top is not None)
            ):
                args = {
                    "bottom_bottom": self._active_bottom,
                    "bottom_top": self._active_top,
                }
                if isinstance(self._m1_bottom, float):
                    args["top_bottom"] = self._m1_bottom
                if isinstance(self._m1_top, float):
                    args["top_top"] = self._m1_top

                layouter.add_wire(
                    net=self.net, wire=contact, well_net=self._well_net,
                    bottom=active, bottom_implant=self._implant, bottom_well=self._well,
                    bottom_enclosure=self._bottom_enclosure,
                    bottom_implant_enclosure=self._bottom_implant_enclosure,
                    top_enclosure=self._top_enclosure,
                    **args, # pyright: ignore
                )
                self._unplaced = layouter.layout
        else:
            if (
                (not self._has_contact)
                and (self._active_bottom is not None)
                and (self._active_top is not None)
            ):
                w = ac_canvas._min_contactedgate_pitch - canvas.l - 2*tech.grid

                shape = _geo.Rect(
                    left=-0.5*w, bottom=self._active_bottom,
                    right=0.5*w, top=self._active_top,
                )
                layouter.add_wire(
                    net=self.net, wire=active, well_net=self._well_net,
                    implant=self._implant, well=self._well,
                    implant_enclosure=self._bottom_implant_enclosure,
                    shape=shape,
                )
                self._unplaced = layouter.layout


class _NSD(_SD):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, with_contact: bool,
        _bottom_enclosure: str, _top_enclosure: str,
    ) -> None:
        canvas = cell.canvas

        super().__init__(
            cell=cell, name=name, net=net, with_contact=with_contact,
            _implant=canvas._nimplant, _well=canvas._pwell, _well_net=cell.pwell_net,
            _bottom_enclosure=_bottom_enclosure, _bottom_implant_enclosure=canvas._min_nsd_enc,
            _top_enclosure=_top_enclosure,
        )
NSDT = _NSD


class _SignalNSD(_NSD):
    """this is NSD that connects to a signal"""
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, with_contact: bool,
    ) -> None:
        super().__init__(
            cell=cell, name=name, net=net, with_contact=with_contact,
            _bottom_enclosure="tall", _top_enclosure="tall",
        )
        self._contact: Optional[SignalSDContactT] = None

    @property
    def _has_contact(self) -> bool:
        return self._contact is not None
    @property
    def contact(self) -> "SignalSDContactT":
        if self._contact is None:
            self._contact = _SignalSDContact(
                cell=self.cell, name=f"{self.name}:contact", net=self.net, sd=self,
            )
        return self._contact

    # Overrule y for metal1 connections
    def _get_y(self) -> float:
        # First call _get_y and raise exception if there is not _y value.
        y = super()._get_y()
        if self.with_contact:
            lay = self._unplaced
            bb = lay.bounds(mask=self.cell.canvas._metal1.mask)
            y = bb.top - 0.5*self.cell.ac_canvas._m1row_width
        return y
    _y = property(_get_y)
SignalNSDT = _SignalNSD


class _VssSD(_NSD):
    """This is NSD with vss as net and connected to vssrail"""
    def __init__(self, *, cell: "ActiveColumnsCell", name: str) -> None:
        super().__init__(
            name=name, cell=cell, net=cell.vss, with_contact=True,
            _bottom_enclosure="tall", _top_enclosure="wide",
        )

    @staticmethod
    def _gen_layout(*, cell: _Cell) -> _lay.LayoutT:
        """This code is in separate static method so it can be shared with
        ActiveColumnsCanvas
        """
        canvas = cell.canvas

        active = canvas._active
        nimplant = canvas._nimplant
        contact = canvas._contact
        pwell = canvas._pwell

        return cell.layouter.wire_layout(
            net=cell.vss, wire=contact, well_net=cell.pwell_net,
            bottom=active, bottom_implant=nimplant, bottom_well=pwell,
            bottom_enclosure="tall", top_enclosure="wide"
        )
VssSDT = _VssSD


class _PSD(_SD):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, with_contact: bool,
        _bottom_enclosure: str, _top_enclosure: str,
    ) -> None:
        canvas = cell.canvas

        super().__init__(
            cell=cell, name=name, net=net, with_contact=with_contact,
            _implant=canvas._pimplant, _well=canvas._nwell, _well_net=cell.nwell_net,
            _bottom_enclosure=_bottom_enclosure, _bottom_implant_enclosure=canvas._min_psd_enc,
            _top_enclosure=_top_enclosure,
        )
PSDT = _PSD


class _SignalPSD(_PSD):
    """this is PSD that connects to a signal"""
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, with_contact: bool,
    ) -> None:
        super().__init__(
            cell=cell, name=name, net=net, with_contact=with_contact,
            _bottom_enclosure="tall", _top_enclosure="tall",
        )
        self._contact: Optional[SignalSDContactT] = None

    @property
    def _has_contact(self) -> bool:
        return self._contact is not None
    @property
    def contact(self) -> "SignalSDContactT":
        if self._contact is None:
            self._contact = _SignalSDContact(
                cell=self.cell, name=f"{self.name}:contact", net=self.net, sd=self,
            )
        return self._contact

    # Overrule y for metal1 connections
    def _get_y(self) -> float:
        # First call _get_y and raise exception if there is not _y value.
        y = super()._get_y()
        if self.with_contact:
            lay = self._unplaced
            bb = lay.bounds(mask=self.cell.canvas._metal1.mask)
            y = bb.bottom + 0.5*self.cell.ac_canvas._m1row_width
        return y
    _y = property(_get_y)
SignalPSDT = _SignalPSD
SignalSDT = Union[SignalNSDT, SignalPSDT]


class _VddSD(_PSD):
    """This is PSD with vdd as net and connected to vddrail"""
    def __init__(self, *, cell: "ActiveColumnsCell", name: str) -> None:
        super().__init__(
            name=name, cell=cell, net=cell.vdd, with_contact=True,
            _bottom_enclosure="tall", _top_enclosure="wide",
        )

    @staticmethod
    def _gen_layout(*, cell: _Cell) -> _lay.LayoutT:
        """This code is in separate static method so it can be shared with
        ActiveColumnsCanvas
        """
        canvas = cell.canvas

        active = canvas._active
        pimplant = canvas._pimplant
        contact = canvas._contact
        nwell = canvas._nwell

        return cell.layouter.wire_layout(
            net=cell.vdd, wire=contact, well_net=cell.nwell_net,
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            bottom_enclosure="tall", top_enclosure="wide"
        )
VddSDT = _VddSD


class _SignalSDContact(_NetElement):
    """A contact to a SignalSDT """
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT,
        sd: SignalSDT,
    ) -> None:
        if sd.with_contact:
            raise ValueError(f"SD {sd.name}: adding contact on SD with contacts not allowed")
        self.sd = sd
        super().__init__(cell=cell, name=name, net=net)

        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas
        layouter = cell.layouter

        active = canvas._active
        contact = canvas._contact
        implant = sd._implant
        well = sd._well
        well_net = sd._well_net

        self._unplaced = layouter.wire_layout(
            net=self.net, wire=contact, well_net=well_net,
            bottom=active, bottom_implant=implant, bottom_well=well,
            bottom_enclosure="tall", top_enclosure="tall",
        )
SignalSDContactT = _SignalSDContact


class _MOS(_NetElement, abc.ABC):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, w_size: str,
        _mos: _prm.MOSFET, _bulk_net: _ckt.CircuitNetT,
    ) -> None:
        # w_s = ("max", "max_fill", "min", "min_balanced")
        w_s = ("max", "min")
        if w_size not in w_s:
            raise ValueError(f"w has to be one of {w_s}")

        super().__init__(name=name, cell=cell, net=net)
        self.w_size = w_size
        self._mos = _mos
        self._bulk_net = _bulk_net

        self._w: Optional[float] = None
        self._inst = None
        self._sd1_net: Optional[_ckt.CircuitNetT] = None
        self._sd2_net: Optional[_ckt.CircuitNetT] = None

    # Disable setting of _unplaced as it will be generated when w and nets are all set
    _unplaced = property(_NetElement._get_unplaced)

    def _set_w(self, *, w: float):
        if self._w is not None:
            raise RuntimeError(
                f"Internal error: MOS '{self.name}' w set twice"
            )
        assert self._inst is None

        cell = self.cell
        canvas = cell.canvas

        self._w = w
        self._inst = inst = cell.circuit.instantiate(
            self._mos, name=self.name, l=canvas.l, w=w,
        )
        self.net.childports += inst.ports.gate
        self._bulk_net.childports += inst.ports.bulk
        if self._sd1_net is not None:
            self._sd1_net.childports += inst.ports.sourcedrain1
        if self._sd2_net is not None:
            self._sd2_net.childports += inst.ports.sourcedrain2

        self._try_unplaced()

    def _set_sd1_net(self, *, net: _ckt.CircuitNetT):
        if self._sd1_net is not None:
            raise RuntimeError(
                f"Internal error: MOS '{self.name}' sd1_net set twice"
            )

        self._sd1_net = net
        if self._inst is not None:
            net.childports += self._inst.ports.sourcedrain1

        self._try_unplaced()

    def _set_sd2_net(self, *, net: _ckt.CircuitNetT):
        if self._sd2_net is not None:
            raise RuntimeError(
                f"Internal error: MOS '{self.name}' sd2_net set twice"
            )

        self._sd2_net = net
        if self._inst is not None:
            net.childports += self._inst.ports.sourcedrain2

        self._try_unplaced()

    def _try_unplaced(self):
        if (
            (self._inst is not None)
            and (self._sd1_net is not None)
            and (self._sd2_net is not None)
        ):
            # Use _set_unplaced() method as setter for _unplaced property has been
            # disabled.
            self._set_unplaced(self.cell.layouter.inst_layout(inst=self._inst))


class _NMOS(_MOS):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, w_size: str,
    ) -> None:
        canvas = cell.canvas
        super().__init__(
            cell=cell, name=name, net=net, w_size=w_size, _mos=canvas.nmos, _bulk_net=cell.vss,
        )
NMOST = _NMOS


class _PMOS(_MOS):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT, w_size: str,
    ) -> None:
        canvas = cell.canvas
        super().__init__(
            cell=cell, name=name, net=net, w_size=w_size, _mos=canvas.pmos, _bulk_net=cell.vdd,
        )
PMOST = _PMOS


PolyContactLeftT = Union[
    "PolyContactT", "ActiveColumnT",
    "M1KnotT", "M1ColumnT", "MultiM1ColumnT",
]
class _PolyContact(_NetElement):
    """Poly to M1 contact"""
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT,
        left: MultiT[PolyContactLeftT]=(),
    ) -> None:
        self._left = left = cast_MultiElemT(left)
        super().__init__(cell=cell, name=name, net=net)

        canvas = cell.canvas

        poly = canvas._poly
        contact = canvas._contact

        self._unplaced = cell.layouter.wire_layout(
            net=net, wire=contact,
            bottom=poly, bottom_enclosure="tall", top_enclosure="tall",
        )
PolyContactT = _PolyContact


class _PolyKnot(_NetElement):
    pass
PolyKnotT = _PolyKnot


class _M1Knot(_NetElement):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, net: _ckt.CircuitNetT,
    ) -> None:
        super().__init__(cell=cell, name=name, net=net)

        cell = self.cell
        layouter = cell.layouter
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        self._unplaced = layouter.wire_layout(
            net=net, wire=canvas._metal1,
            width=ac_canvas._m1col_width, height=ac_canvas._m1row_width,
        )
M1KnotT = _M1Knot


ActiveColumnElementT = Union[
    SignalNSDT, VssSDT, SignalPSDT, VddSDT,
    NMOST, PMOST,
    PolyContactT, PolyKnotT,
]
ActiveColumnLeftT = Union[PolyContactT, "M1ColumnT", "MultiM1ColumnT"]
class _ActiveColumn(_ElementsColumn[ActiveColumnElementT]):
    """Bottom to top list of elements with elements containing active layer

    ActiveColumn is not a _NetElement object as it can have different nets.
    """
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, connect: bool,
        elements: MultiT[ActiveColumnElementT],
        left: MultiT[ActiveColumnLeftT]=(),
    ) -> None:
        super().__init__(cell=cell, name=name, elements=elements)
        self.connect = connect
        self._left = left = cast_MultiElemT(left)

        self._nmos: Optional[NMOST] = None
        self._nsd: Optional[NSDT] = None
        self._pmos: Optional[PMOST] = None
        self._psd: Optional[PSDT] = None
        self._leftjog: bool = False
        self._rightjog: bool = False

        self._prev: Optional[_ActiveColumn] = None
        self._next: Optional[_ActiveColumn] = None

        for elem in self:
            if isinstance(elem, NSDT):
                if self._nsd is not None:
                    raise ValueError(
                        f"2 NSDs in ActiveColumn '{name}': ({self._nsd.name}, {elem.name})"
                    )
                if self._nmos is not None:
                    raise ValueError(
                        f"ActiveColumn '{name}' has both NSD '{elem.name}'"
                        f" and NMOS '{self._nmos.name}' specified"
                    )
                self._nsd = elem
            elif isinstance(elem, NMOST):
                if self._nsd is not None:
                    raise ValueError(
                        f"ActiveColumn '{name}' has both NSD '{self._nsd.name}'"
                        f" and NMOS '{elem.name}' specified"
                    )
                if self._nmos is not None:
                    raise ValueError(
                        f"2 NMOSes in ActiveColumn '{name}': ({self._nmos.name}, {elem.name})"
                    )
                self._nmos = elem
            elif isinstance(elem, PSDT):
                if self._psd is not None:
                    raise ValueError(
                        f"2 PSDs in ActiveColumn '{name}': ({self._psd.name}, {elem.name})"
                    )
                if self._pmos is not None:
                    raise ValueError(
                        f"ActiveColumn '{name}' has both PSD '{elem.name}'"
                        f" and PMOS '{self._pmos.name}' specified"
                    )
                self._psd = elem
            elif isinstance(elem, PMOST):
                if self._psd is not None:
                    raise ValueError(
                        f"ActiveColumn '{name}' has both PSD '{self._psd.name}'"
                        f" and PMOS '{elem.name}' specified"
                    )
                if self._pmos is not None:
                    raise ValueError(
                        f"2 PMOSes in ActiveColumn '{name}': ({self._pmos.name}, {elem.name})"
                    )
                self._pmos = elem

    @property
    def _is_empty(self) -> bool:
        return all(
            elem is None for elem in(
                self._nmos, self._nsd, self._pmos, self._psd,
            )
        )

    def _draw_wire(self) -> None:
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas
        layouter = cell.layouter

        active = canvas._active
        nimplant = canvas._nimplant
        pimplant = canvas._pimplant
        nwell = canvas._nwell
        nwell_net = self.cell._nwell_net
        pwell = canvas._pwell
        pwell_net = self.cell._pwell_net
        poly = canvas._poly

        # Draw poly connection is needed

        if self.connect:
            nmos = self._nmos
            assert nmos is not None
            assert nmos._placed is not None
            pmos = self._pmos
            assert pmos is not None
            assert pmos._placed is not None

            npoly_bb = nmos._placed.bounds(mask=poly.mask)
            ppoly_bb = pmos._placed.bounds(mask=poly.mask)

            shape = _geo.Rect.from_rect(rect=npoly_bb, top=ppoly_bb.bottom)
            layouter.add_wire(net=nmos.net, wire=poly, shape=shape)

        # Add active rectangular to not rely on gate extension ext to make active connection

        nsd = self._nsd
        psd = self._psd
        leftcol = self._prev
        rightcol = self._next

        if nsd is not None:
            left: Optional[float] = None
            right: Optional[float] = None

            if leftcol is not None:
                nsd2 = leftcol._nsd
                nmos2 = leftcol._nmos

                if nsd2 is not None:
                    left = nsd2._x
                elif nmos2 is not None:
                    left = nmos2._x + 0.5*canvas.l + canvas._min_active_poly_space
            if left is None:
                left = cast(float, self._x) - 0.5*ac_canvas._actcont_width

            if rightcol is not None:
                nsd2 = rightcol._nsd
                nmos2 = rightcol._nmos

                if nsd2 is not None:
                    right = nsd2._x
                elif nmos2 is not None:
                    right = nmos2._x - 0.5*canvas.l - canvas._min_active_poly_space
            if right is None:
                right = cast(float, self._x) + 0.5*ac_canvas._actcont_width

            if right > left:
                # For big active to poly spacing right but for example a sd connection
                # with contacts right may be smaller than left.
                # We don't need to draw connection then.
                assert nsd._active_bottom is not None
                assert nsd._active_top is not None
                shape = _geo.Rect(
                    left=left, bottom=nsd._active_bottom, right=right, top=nsd._active_top,
                )
                layouter.add_wire(
                    net=nsd.net, wire=active, shape=shape,
                    implant=nimplant, implant_enclosure=canvas._min_nsd_enc,
                    well=pwell, well_net=pwell_net,
                )

        if psd is not None:
            left: Optional[float] = None
            right: Optional[float] = None

            if leftcol is not None:
                psd2 = leftcol._psd
                pmos2 = leftcol._pmos

                if psd2 is not None:
                    left = psd2._x
                elif pmos2 is not None:
                    left = pmos2._x + 0.5*canvas.l + canvas._min_active_poly_space
            if left is None:
                left = cast(float, self._x) - 0.5*ac_canvas._actcont_width

            if rightcol is not None:
                psd2 = rightcol._psd
                pmos2 = rightcol._pmos

                if psd2 is not None:
                    right = psd2._x
                elif pmos2 is not None:
                    right = pmos2._x - 0.5*canvas.l - canvas._min_active_poly_space
            if right is None:
                right = cast(float, self._x) + 0.5*ac_canvas._actcont_width

            if right > left:
                # For big active to poly spacing right but for example a sd connection
                # with contacts right may be smaller than left.
                # We don't need to draw connection then.
                assert psd._active_bottom is not None
                assert psd._active_top is not None
                shape = _geo.Rect(
                    left=left, bottom=psd._active_bottom, right=right, top=psd._active_top,
                )
                layouter.add_wire(
                    net=psd.net, wire=active, shape=shape,
                    implant=pimplant, implant_enclosure=canvas._min_psd_enc,
                    well=nwell, well_net=nwell_net,
                )

        # connect the sd contacts

        if (nsd is not None) and nsd._has_contact:
            assert isinstance(nsd, SignalNSDT)
            assert nsd._active_bottom is not None
            cont = nsd.contact
            assert cont.is_placed
            actbb = cont._placed.bounds(mask=active.mask)
            left = min(actbb.left, actbb.center.x - 0.5*ac_canvas._actcont_width)
            right = max(actbb.right, actbb.center.x + 0.5*ac_canvas._actcont_width)
            bottom = nsd._active_bottom
            top = actbb.top
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(
                net=cont.net, wire=active, shape=shape, implant=nimplant,
                well=pwell, well_net=pwell_net,
            )

        if (psd is not None) and psd._has_contact:
            assert isinstance(psd, SignalPSDT)
            assert psd._active_top is not None
            cont = psd.contact
            assert cont.is_placed
            actbb = cont._placed.bounds(mask=active.mask)
            left = min(actbb.left, actbb.center.x - 0.5*ac_canvas._actcont_width)
            right = max(actbb.right, actbb.center.x + 0.5*ac_canvas._actcont_width)
            bottom = actbb.bottom
            top = psd._active_top
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(
                net=cont.net, wire=active, shape=shape, implant=pimplant,
                well=nwell, well_net=nwell_net,
            )
ActiveColumnT = _ActiveColumn


PolyRowElementT = Union[PolyContactT, NMOST, PMOST, PolyKnotT]
class _PolyRow(_ElementsRow[PolyRowElementT]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[PolyRowElementT],
    ) -> None:
        """elements from left to right"""
        super().__init__(cell=cell, name=name, elements=elements)

        if len(self) <= 1:
            raise ValueError(
                f"Not enough elements for PolyRow '{name}'"
            )

        self._multipolyrow: Optional["MultiPolyRowT"] = None

    @property
    def _has_multipolyrow(self) -> bool:
        return self._multipolyrow is not None
    @property
    def multipolyrow(self) -> "MultiPolyRowT":
        if self._multipolyrow is None:
            self._multipolyrow = _MultiPolyRow(
                cell=self.cell, name=f"{self.name}:multi", rows=self,
            )
        return self._multipolyrow

    def _set_y(self, y: float) -> None:
        for elem in filter(lambda e: not isinstance(e, _MOS), self):
            elem._y = y
        self._elems_done = True
        super()._set_y(y)
    _y = property(_ElementsRow._get_y, _set_y)

    def _draw_wire(self):
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas
        layouter = cell.layouter

        poly = canvas._poly

        first = self[0]
        y = self._y
        left = min(elem._x for elem in self)
        right = max(elem._x for elem in self)

        bottom = y - 0.5*ac_canvas._polyrow_width
        top = y + 0.5*ac_canvas._polyrow_width
        if left < right:
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(net=first.net, wire=poly, shape=shape)

        for elem in self:
            if isinstance(elem, NMOST):
                assert elem._placed is not None, "Internal error"
                poly_bb = elem._placed.bounds(mask=poly.mask)
                shape = _geo.Rect.from_rect(rect=poly_bb, top=top)
                layouter.add_wire(net=first.net, wire=poly, shape=shape)
            elif isinstance(elem, PMOST):
                assert elem._placed is not None, "Internal error"
                poly_bb = elem._placed.bounds(mask=poly.mask)
                shape = _geo.Rect.from_rect(rect=poly_bb, bottom=bottom)
                layouter.add_wire(net=first.net, wire=poly, shape=shape)
PolyRowT = _PolyRow


class _MultiPolyRow(_MultiElementsRow[PolyRowT, PolyRowElementT]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, rows: MultiT[PolyRowT],
    ) -> None:
        super().__init__(cell=cell, name=name, rows=rows)

        self._prev = None
MultiPolyRowT = _MultiPolyRow


M1RowElementT = Union[SignalNSDT, SignalPSDT, SignalSDContactT, PolyContactT, M1KnotT]
class _M1Row(_ElementsRow[M1RowElementT]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[M1RowElementT],
    ) -> None:
        """elements from left to right"""
        super().__init__(cell=cell, name=name, elements=elements)

        if len(self) <= 1:
            raise ValueError(
                f"Not enough elements for M1Row '{name}'"
            )

        self._is_sdrow = any(isinstance(elem, (SignalNSDT, SignalPSDT)) for elem in self)

        self._multim1row: Optional["MultiM1RowT"] = None

    @property
    def _has_multim1row(self) -> bool:
        return self._multim1row is not None
    @property
    def multim1row(self) -> "MultiM1RowT":
        if self._multim1row is None:
            self._multim1row = _MultiM1Row(
                cell=self.cell, name=f"{self.name}:multi", rows=self,
            )
        return self._multim1row

    def _set_y(self, y: float) -> None:
        # self.log(f"_set_y(y={y}) enter")
        for elem in self:
            if isinstance(elem, (SignalNSDT, SignalPSDT)):
                assert abs(elem._y - y) < _geo.epsilon, "Internal error"
                continue
            elif isinstance(elem, PolyContactT):
                if elem._has_y:
                    assert abs(elem._y - y) < _geo.epsilon, "Internal error"
                    continue
            elem._y = y
        self._elems_done = True
        super()._set_y(y)
        # self.log(f"_set_y(y={y}) leave")
    _y = property(_ElementsRow._get_y, _set_y)

    def _draw_wire(self) -> None:
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas
        layouter = cell.layouter

        metal1 = canvas._metal1

        first = self[0]

        left = min(elem._x for elem in self)
        right = max(elem._x for elem in self)
        y = self._y

        signalsds = tuple(filter(
            lambda e: isinstance(e, (SignalNSDT, SignalPSDT)), self)
        )
        if len(signalsds) == 0:
            bottom = y - 0.5*ac_canvas._m1row_width
            top = bottom + ac_canvas._m1row_width
        else:
            bbs = tuple(
                sd._placed.bounds(mask=metal1.mask)
                for sd in signalsds
            )
            bottom = max(bb.bottom for bb in bbs)
            top = min(bb.top for bb in bbs)

        if abs(left - right) > _geo.epsilon:
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            net = first.net
            layouter.add_wire(net=net, wire=canvas._metal1, shape=shape)
M1RowT = _M1Row


class _MultiM1Row(_MultiElementsRow[M1RowT, M1RowElementT]):
    pass
MultiM1RowT = _MultiM1Row


M1ColumnElementT = Union[NSDT, PSDT, PolyContactT, M1KnotT]
M1ColumnLeftT = Union[PolyContactT, SignalSDT]
M1ColumnBottomTopT = Union[SignalSDT, M1RowT, MultiM1RowT]
class _M1Column(_ElementsColumn[M1ColumnElementT]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, elements: MultiT[M1ColumnElementT],
        left: MultiT[M1ColumnLeftT]=(),
        bottom: MultiT[M1ColumnBottomTopT], top: MultiT[M1ColumnBottomTopT],
    ) -> None:
        """elements from bottom to top"""
        super().__init__(cell=cell, name=name, elements=elements)

        self._left = left = cast_MultiElemT(left)
        for elem in left:
            if isinstance(elem, (SignalNSDT, SignalPSDT)):
                if not elem.with_contact:
                    raise TypeError(
                        f"left for M1Column '{name}' contains SD '{elem.name}' without contacts"
                    )
        self._bottom = bottom = cast_MultiElemT(bottom)
        self._top = top = cast_MultiElemT(top)

        if not (
            (len(self) >= 2) or ((len(self) == 1) and isinstance(self, _M1Pin))
        ):
            raise ValueError(
                f"Not enough elements for M1Column '{name}'",
            )

        net = None
        for elem in self:
            if net is None:
                net = elem.net
            else:
                if elem.net != net:
                    raise ValueError(
                        f"Not all element for M1Column '{name}' are on the same net",
                    )

            if isinstance(elem, _SD):
                if not elem.with_contact:
                    raise ValueError(
                        f"SD '{elem.name}' for M1Column '{name}' does not have contacts",
                    )
                if isinstance(elem, VssSDT):
                    raise TypeError(
                        f"M1Column '{name}': VssSD '{elem.name}' not allowed"
                    )
                if isinstance(elem, VddSDT):
                    raise TypeError(
                        f"M1Column '{name}': VddSD '{elem.name}' not allowed"
                    )

        self._multim1column: Optional["MultiM1ColumnT"] = None

    @property
    def bottom(self) -> Tuple[M1ColumnBottomTopT]:
        return self._bottom
    @property
    def top(self) -> Tuple[M1ColumnBottomTopT]:
        return self._top
    @property
    def _has_multim1column(self) -> bool:
        return self._multim1column is not None
    @property
    def multim1column(self) -> "MultiM1ColumnT":
        if self._multim1column is None:
            self._multim1column = _MultiM1Column(
                cell=self.cell, name=f"{self.name}:multi", columns=self,
            )
        return self._multim1column

    def _set_x(self, x: float) -> None:
        for elem in self:
            if isinstance(elem, (NSDT, PSDT)):
                assert abs(elem._x - x) <= _geo.epsilon
            else:
                elem._x = x
        self._elems_done = True
        super()._set_x(x)
    _x = property(_ElementsColumn._get_x, _set_x)

    def _draw_wire(self, *, m1pin: Optional[_prm.Marker]=None) -> None:
        # m1pin can be set by child class
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas
        layouter = cell.layouter

        metal1 = canvas._metal1
        m1_halfw = 0.5*ac_canvas._m1row_width
        m1_space = canvas.min_m1_space
        m1vss_space = canvas._min_m1vssrail_space
        m1vdd_space = canvas._min_m1vddrail_space

        first: M1ColumnElementT = self[0]
        if len(self.bottom) == 0:
            if m1pin is not None:
                bottom = canvas._m1_vssrail_width + m1vss_space
            else:
                bottom = first._y - m1_halfw
        else:
            bottom = max(botelem._y for botelem in self.bottom) + m1_halfw + m1_space

        if len(self.top) == 0:
            last: M1ColumnElementT = self[-1]
            if m1pin is not None:
                top = canvas._cell_height - canvas._m1_vddrail_width - m1vdd_space
            else:
                top = last._y + m1_halfw
        else:
            top = min(topelem._y for topelem in self.top) - m1_halfw - m1_space

        net = first.net
        x = self._x
        assert x is not None
        left = x - 0.5*ac_canvas._m1col_width
        right = x + 0.5*ac_canvas._m1col_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal1, pin=m1pin, shape=shape)
M1ColumnT = _M1Column


class _M1Pin(_M1Column):
    def _draw_wire(self) -> None:
        canvas = self.cell.canvas

        return super()._draw_wire(m1pin=canvas._metal1pin)


class _MultiM1Column(_MultiElementsColumn[M1ColumnT, M1ColumnElementT]):
    def __init__(self, *,
        cell: "ActiveColumnsCell", name: str, columns: MultiT[M1ColumnT],
    ) -> None:
        super().__init__(cell=cell, name=name, columns=columns)

        self._prev: Optional[_MultiM1Column] = None
        self._place_polycontact = False
MultiM1ColumnT = _MultiM1Column


class _Constraints:
    def __init__(self, *,
        cell: "ActiveColumnsCell",
        activecolumns: MultiT[ActiveColumnT],
        polyrows: MultiT[MultiPolyRowT],
        m1rows: MultiT[MultiM1RowT],
        m1columns: MultiT[MultiM1ColumnT],
    ) -> None:
        self.cell = cell
        self.activecolumns = activecolumns = cast_MultiElemT(activecolumns)
        self.polyrows = cast_MultiElemT(polyrows)
        self.m1rows = cast_MultiElemT(m1rows)
        self.m1columns = cast_MultiElemT(m1columns)

        if len(activecolumns) == 0:
            raise ValueError(f"No active column specificed")
        firstcol = activecolumns[0]
        lastcol = activecolumns[-1]

        if firstcol._is_empty:
            raise ValueError(
                f"First ActiveColumn '{firstcol.name}' is an empty column",
            )
        if lastcol._is_empty:
            raise ValueError(
                f"Last ActiveColumn '{lastcol.name}' is an empty column",
            )

        self._n_actcols = len(self.activecolumns)
        self._n_polyrows = len(self.polyrows)
        self._n_m1rows = len(self.m1rows)
        self._n_m1cols = len(self.m1columns)

    @property
    def _poly_y0(self) -> float:
        if self._n_polyrows == 0:
            raise RuntimeError(
                "Internal error: _poly_y0 requested for zero rows",
            )
        ac_canvas = self.cell.ac_canvas

        return (
            ac_canvas._midrow_height
            - 0.5*(self._n_polyrows - 1)*ac_canvas._min_polyrow_pitch
        )
    @property
    def _poly_bottom(self) -> float:
        ac_canvas = self.cell.ac_canvas

        return self._poly_y0 - 0.5*ac_canvas._polyrow_width
    @property
    def _poly_top(self) -> float:
        ac_canvas = self.cell.ac_canvas

        return (
            self._poly_bottom
            + (self._n_polyrows - 1)*ac_canvas._min_polyrow_pitch
            + ac_canvas._polyrow_width
        )
    @property
    def _metal1_y0(self) -> float:
        if self._n_m1rows == 0:
            raise RuntimeError(
                "Internal error: _metal1_y0 requested for zero rows",
            )
        ac_canvas = self.cell.ac_canvas

        return (
            ac_canvas._midrow_height
            - 0.5*(self._n_m1rows - 1)*ac_canvas._min_m1row_pitch
        )

    async def _do_layout(self) -> bool:
        tasks: List[asyncio.Task] = []

        # Determine the source and drain nets of the transistor based on
        # sd left and right from it.
        # self.log("_do_layout: calling _set_transistor_nets")
        self._set_transistor_nets()

        # Compute the w for the max size transistors; this value depends
        # on the number of poly rows in the design.
        # self.log("_do_layout: calling _size_transistors")
        self._size_transistors()

        # Determine top and bottom edge of the sd regions.
        # It will be determined based on the size of (optional)
        # left and right transistor
        # self.log("_do_layout: calling _size_sd")
        self._size_sd()

        # Place the poly rows.
        # They are placed around middle height of the cell.
        # self.log("_do_layout: calling _place_polyrows")
        self._place_polyrows()

        # Set the prev for the activre columns.
        # Put first column on fixed x location. x computation of the other
        # columns may be delayed until other elements on which the column
        # depends are placed.
        # Run in coroutine as it may wait for placement of other elements
        # in functions below.
        # self.log("_do_layout: calling _place_actcols")
        tasks.append(asyncio.create_task(self._place_actcols()))

        # Set the prev for the m1 columns.
        # Put first column on fixed location, x computation of other columns
        # may be delayed until other elements are placed.
        # self.log("_do_layout: calling _setprev_m1cols")
        # self._setprev_m1cols()

        # Place the m1 columns.
        # If the columns contain a polypad without a determined x coord that
        # x coordinate will also be set.
        # Run in coroutine as it may wait for placement of other elements
        # in functions below.
        # self.log("_do_layout: calling _place_m1cols()")
        tasks.append(asyncio.create_task(self._place_m1cols()))

        # Place the sd contacts.
        # Derive x value from the SD
        tasks.append(asyncio.create_task(self._place_sdcontacts_sds()))

        # Place the poly pads that are not in a metal 1 row.
        # self.log("_do_layout: calling _place_polypads")
        tasks.extend((
            asyncio.create_task(self._place_polypads_m1row(m1row=m1row))
            for m1row in chain(*self.m1rows)
        ))
        tasks.extend((
            asyncio.create_task(self._place_polypads_m1col(m1col=m1col))
            for m1col in chain(*self.m1columns)
        ))

        # Place the M1 rows which are not connected to sd or polypad.
        # self.log("_do_layout: calling _place_m1rows")
        self._place_m1rows()

        # Run the tasks
        done, running = await asyncio.wait(tasks, timeout=1.0)
        for t in done:
            e = t.exception()
            if e is not None:
                self.log("Exception raised")
                raise e
        if running:
            self.log("Timeout reached")
            self.log("  Running tasks:")
            for task in running:
                self.log(f"  * {task.get_stack()}")
            self.log("  Waiters:")
            for w in filter(lambda wait: wait.waiting, self.cell._waiterfab.waiters):
                self.log(f"  * {w.name}")
            raise RuntimeError("Timeout reached")

        # Draw the wires for all the rows and columns
        # It is assumed that all elements are placed so the shape of the wires
        # can be computed.
        # self.log("_do_layout: calling _draw_wires")
        self._draw_wires()

        # Set the width of the cell.
        # This also adds the rails etc.
        # self.log("_do_layout: calling _size_width")
        self._size_width()

        return True

    def _set_transistor_nets(self) -> None:
        for i, actcol in enumerate(self.activecolumns):
            leftcol = None if i == 0 else self.activecolumns[i - 1]
            rightcol = None if i == (self._n_actcols - 1) else self.activecolumns[i + 1]

            nmos = actcol._nmos
            if nmos is not None:
                assert (leftcol is not None) and (leftcol._nsd is not None)
                nmos._set_sd1_net(net=leftcol._nsd.net)

                assert (rightcol is not None) and (rightcol._nsd is not None)
                nmos._set_sd2_net(net=rightcol._nsd.net)

            pmos = actcol._pmos
            if pmos is not None:
                assert (leftcol is not None) and (leftcol._psd is not None)
                pmos._set_sd1_net(net=leftcol._psd.net)

                assert (rightcol is not None) and (rightcol._psd is not None)
                pmos._set_sd2_net(net=rightcol._psd.net)

    def _size_transistors(self) -> None:
        """_size_transistors() assumes the nets of the transistor has been set before
        """
        cell = self.cell
        tech = cell.tech
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        active = canvas._active

        nact_top = canvas._well_edge_height - ac_canvas._min_nact_nwell_space
        pact_bottom = canvas._well_edge_height + ac_canvas._min_pact_nwell_enclosure
        if self._n_polyrows > 0:
            active = canvas._active
            contact = canvas._contact

            space = canvas._min_active_poly_space
            try:
                ch_space = tech.computed.min_space(primitive1=active, primitive2=contact)
            except:
                pass
            else:
                space = max(
                    space, ch_space - 0.5*(ac_canvas._polyrow_width - contact.width),
                )
            nact_top = min(
                nact_top, self._poly_bottom - space,
            )
            pact_bottom = max(
                pact_bottom, self._poly_top + space,
            )

        w_nmos_max = nact_top - ac_canvas._nact_bottom
        w_pmos_max = ac_canvas._pact_top - pact_bottom

        for actcol in self.activecolumns:
            nmos = actcol._nmos
            if nmos is not None:
                if nmos.w_size == "min":
                    nmos._set_w(w=canvas._nmos_min_w)
                elif nmos.w_size == "max":
                    nmos._set_w(w=w_nmos_max)
                else:
                    raise NotImplementedError(f"nmos w_size '{nmos.w_size}'")
                # We assume nets have been set before so the transistor has an unplaced layout
                act_bb = nmos._unplaced.bounds(mask=active.mask)
                nmos._y = canvas._ac_canvas._nact_bottom - act_bb.bottom

            pmos = actcol._pmos
            if pmos is not None:
                if pmos.w_size == "min":
                    pmos._set_w(w=canvas._pmos_min_w)
                elif pmos.w_size == "max":
                    pmos._set_w(w=w_pmos_max)
                else:
                    raise NotImplementedError(f"pmos w_size '{pmos.w_size}'")
                # We assume nets have been set before so the transistor has an unplaced layout
                act_bb = pmos._unplaced.bounds(mask=active.mask)
                pmos._y = canvas._ac_canvas._pact_top - act_bb.top

    def _size_sd(self) -> None:
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        active = canvas._active
        metal1 = canvas._metal1

        dpoly_etch = 0.5*(ac_canvas._polyrow_width - ac_canvas._m1row_width) - canvas.min_m1_space
        m1_top_max = self._poly_bottom + dpoly_etch
        m1_bottom_min = self._poly_top - dpoly_etch
        for i, actcol in enumerate(self.activecolumns):
            leftcol = None if i == 0 else self.activecolumns[i - 1]
            rightcol = None if i == (self._n_actcols - 1) else self.activecolumns[i + 1]

            # Set previous and next column
            actcol._prev = leftcol
            actcol._next = rightcol

            nsd = actcol._nsd
            psd = actcol._psd

            # Set active bottom/top
            if nsd is not None:
                bottom: Optional[float] = None
                top: Optional[float] = None

                left_nmos = None if leftcol is None else leftcol._nmos
                left_nsd = None if leftcol is None else leftcol._nsd
                right_nmos = None if rightcol is None else rightcol._nmos
                if left_nmos is not None:
                    _lay = left_nmos._unplaced
                    _act_bb = _lay.bounds(mask=active.mask)

                    bottom = left_nmos._y + _act_bb.bottom
                    top = left_nmos._y + _act_bb.top
                elif left_nsd is not None:
                    bottom = left_nsd._active_bottom
                    top = left_nsd._active_top
                if right_nmos is not None:
                    _lay = right_nmos._unplaced
                    _act_bb = _lay.bounds(mask=active.mask)

                    bottom2 = right_nmos._y + _act_bb.bottom
                    top2 = right_nmos._y + _act_bb.top

                    bottom = bottom2 if bottom is None else min(bottom, bottom2)
                    top = top2 if top is None else max(top, top2)
                if (left_nmos is not None) and (right_nmos is not None):
                    actcol._leftjog = (
                        (right_nmos.w_size == "max")
                        and (left_nmos.w_size != "max")
                    )
                    actcol._rightjog = (
                        (left_nmos.w_size == "max")
                        and (right_nmos.w_size != "max")
                    )
                if left_nmos is not None:
                    actcol._leftjog = actcol._leftjog or nsd._has_contact
                if right_nmos is not None:
                    actcol._rightjog = actcol._rightjog or nsd._has_contact
                assert (bottom is not None) and (top is not None)
                nsd._set_active_bottom(v=bottom)
                nsd._set_active_top(v=top)

            if psd is not None:
                bottom: Optional[float] = None
                top: Optional[float] = None

                left_pmos = None if leftcol is None else leftcol._pmos
                left_psd = None if leftcol is None else leftcol._psd
                right_pmos = None if rightcol is None else rightcol._pmos
                if left_pmos is not None:
                    _lay = left_pmos._unplaced
                    _act_bb = _lay.bounds(mask=active.mask)

                    bottom = left_pmos._y + _act_bb.bottom
                    top = left_pmos._y + _act_bb.top
                elif left_psd is not None:
                    bottom = left_psd._active_bottom
                    top = left_psd._active_top
                if right_pmos is not None:
                    _lay = right_pmos._unplaced
                    _act_bb = _lay.bounds(mask=active.mask)

                    bottom2 = right_pmos._y + _act_bb.bottom
                    top2 = right_pmos._y + _act_bb.top

                    bottom = bottom2 if bottom is None else min(bottom, bottom2)
                    top = top2 if top is None else max(top, top2)
                if (left_pmos is not None) and (right_pmos is not None):
                    actcol._leftjog = actcol._leftjog or (
                        (right_pmos.w_size == "max")
                        and (left_pmos.w_size != "max")
                    )
                    actcol._rightjog = actcol._rightjog or (
                        (left_pmos.w_size == "max")
                        and (right_pmos.w_size != "max")
                    )
                if left_pmos is not None:
                    actcol._leftjog = actcol._leftjog or psd._has_contact
                if right_pmos is not None:
                    actcol._rightjog = actcol._rightjog or psd._has_contact

                assert (bottom is not None) and (top is not None)
                psd._set_active_bottom(v=bottom)
                psd._set_active_top(v=top)

            # Set the metal1 bottom/top
            if nsd is not None:
                if isinstance(nsd, SignalNSDT):
                    if nsd.with_contact:
                        nsd._set_m1_bottom(v=(canvas._m1_vssrail_width + canvas._min_m1vssrail_space))
                        assert nsd._active_top is not None
                        if m1_top_max < nsd._active_top:
                            nsd._set_m1_top(v=m1_top_max)
                        else:
                            nsd._set_m1_top(v="max")
                elif isinstance(nsd, VssSDT):
                    nsd._set_m1_top(v=canvas._m1_vssrail_width)
                    nsd._set_m1_bottom(v="max")
                else:
                    raise RuntimeError(
                        f"Internal error: unsupported nsd type {type(nsd)}"
                    )

            if psd is not None:
                if isinstance(psd, SignalPSDT):
                    if psd.with_contact:
                        psd._set_m1_top(
                            v=(canvas._cell_height - canvas._m1_vddrail_width - canvas._min_m1vddrail_space),
                        )
                        assert psd._active_bottom is not None
                        if m1_bottom_min > psd._active_bottom:
                            psd._set_m1_bottom(v=m1_bottom_min)
                        else:
                            psd._set_m1_bottom(v="max")
                elif isinstance(psd, VddSDT):
                    psd._set_m1_bottom(
                        v=(canvas._cell_height - canvas._m1_vddrail_width),
                    )
                    psd._set_m1_top(v="max")
                else:
                    raise RuntimeError(
                        f"Internal error: unsupported psd type {type(psd)}"
                    )

    async def _place_actcols(self) -> None:
        # self.log("_place_actcols(): enter")
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        poly = canvas._poly

        x: Optional[float] = None
        prev_rightjog: bool = False
        prev_gap = False
        for actcol in self.activecolumns:
            # self.log(f"_place_actcols(): computing x for {actcol.name}")
            if x is None:
                x = ac_canvas._firstcol_dx
            else:
                dxs = [0.5*ac_canvas._min_contactedgate_pitch]
                if actcol._leftjog or prev_rightjog:
                    dxs.append(ac_canvas._min_actjog_dx)
                is_gap = (
                    ((actcol._nsd is None) and (actcol._nmos is None))
                    or ((actcol._psd is None) and (actcol._pmos is None))
                )
                if prev_gap or is_gap:
                    dxs.append(ac_canvas._min_actgap_dx)
                prev_gap = is_gap
                x += max(dxs)
            prev_rightjog = actcol._rightjog

            left_vals: List[float] = []
            for elem in actcol._left:
                elem_x = await elem._wait4x()
                v = None
                if isinstance(elem, _PolyContact):
                    if (actcol._nmos is not None) or (actcol._pmos is not None):
                        bb = elem._placed.bounds(mask=poly.mask)
                        v = bb.right + poly.min_space + 0.5*canvas.l
                    if (
                        ((actcol._nsd is not None) and (actcol._nsd.with_contact))
                        or ((actcol._psd is not None) and (actcol._psd.with_contact))
                    ):
                        v2 = elem_x + ac_canvas._min_m1col_pitch
                        v = v2 if v is None else max(v, v2)
                elif isinstance(elem, (M1ColumnT, MultiM1ColumnT)):
                    v = elem_x + ac_canvas._min_m1col_pitch
                else:
                    raise RuntimeError(f"Internal error: type '{type(elem)}'")
                assert v is not None, "Internal error"
                left_vals.append(v)
            actcol._x = x = max((x, *left_vals))
            # self.log(f"_place_actcols(): computed x {x} for {actcol.name}")
        # self.log("_place_actcols(): leave")

    def _place_polyrows(self) -> None:
        ac_canvas = self.cell.ac_canvas

        for i, multipolyrow in enumerate(self.polyrows):
            multipolyrow._y = self._poly_y0 + i*ac_canvas._min_polyrow_pitch

    async def _place_sdcontacts_sds(self) -> None:
        # self.log("_place_sdcontacts_sds(): enter")
        for actcol in self.activecolumns:
            for sd in (actcol._nsd, actcol._psd):
                if (sd is not None) and (sd._has_contact):
                    sd.contact._x = await sd._wait4x() # type: ignore
        # self.log("_place_sdcontacts_sds(): leave")

    async def _place_polypads_m1row(self, *, m1row: _M1Row) -> None:
        # self.log("_place_polypads_m1row(): enter")
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        for elem in filter(lambda e: isinstance(e, PolyContactT), m1row):
            # self.log(f"_place_polypads_m1row(): computing x for {elem.name}")
            assert not elem._has_x
            assert isinstance(elem, PolyContactT), "Impossible!"
            left_xs: List[float] = []
            for l in elem._left:
                l_x = await l._wait4x()
                if isinstance(l, PolyContactT):
                    left_xs.append(
                        l_x
                        + ac_canvas._polycont_width
                        + canvas._poly.min_space
                    )
                elif isinstance(l, ActiveColumnT):
                    left_xs.append(
                        l_x
                        + 0.5*canvas.l
                        + canvas._poly.min_space
                        + 0.5*ac_canvas._polycont_width
                    )
                elif isinstance(l, (M1KnotT, M1ColumnT, MultiM1ColumnT)):
                    left_xs.append(l_x + ac_canvas._min_m1col_pitch)
                else:
                    raise NotImplementedError(f"Internal error: type '{type(elem)}'")
            elem._x = max(left_xs)
            # self.log(f"_place_polypads_m1row(): computed x {elem._x} for {elem.name}")
        # self.log("_place_polypads(): leave")

    async def _place_polypads_m1col(self, *, m1col: _M1Column) -> None:
        # self.log(f"_place_polypads_m1col(): m1col '{m1col.name}' enter")
        x = await m1col._wait4x()
        for elem in filter(
            lambda e: isinstance(e, PolyContactT) and not e._has_x,
            m1col,
        ):
            elem._x = x
        # self.log(f"_place_polypads_m1col(): m1col '{m1col.name}' leave")

    def _place_m1rows(self) -> None:
        if len(self.m1rows) == 0:
            return

        cell = self.m1rows[0].cell
        ac_canvas = cell.ac_canvas

        bot_y = None
        top_y = None
        bot_rows: List[MultiM1RowT] = []
        mid_rows: List[MultiM1RowT] = []
        top_rows: List[MultiM1RowT] = []
        for mrow in self.m1rows:
            is_bot = False
            is_top = False
            for elem in chain(*mrow):
                if isinstance(elem, SignalNSDT):
                    # Assume contact only on smallest active width
                    mrow._y = elem._y
                    bot_y = elem._y if bot_y is None else min(bot_y, elem._y)
                    break
                elif isinstance(elem, SignalPSDT):
                    # Assume contact only on smallest active width
                    mrow._y = elem._y
                    top_y = elem._y if top_y is None else max(top_y, elem._y)
                    break
                elif isinstance(elem, SignalSDContactT):
                    is_bot = isinstance(elem.sd, SignalNSDT)
                    is_top = isinstance(elem.sd, SignalPSDT)
            else:
                if any(isinstance(elem, PolyContactT) and elem._has_y for elem in chain(*mrow)):
                    mid_rows.append(mrow)
                elif is_bot:
                    assert not is_top
                    bot_rows.append(mrow)
                elif is_top:
                    top_rows.append(mrow)
                else:
                    mid_rows.append(mrow)

        for mrow in bot_rows:
            assert bot_y is not None
            bot_y += ac_canvas._min_m1row_pitch
            mrow._y = bot_y

        todo: List[MultiM1RowT] = []
        prev_y: Optional[float] = None
        for mrow in mid_rows:
            for elem in chain(*mrow):
                if isinstance(elem, PolyContactT) and elem._has_y:
                    prev_y = mrow._y = elem._y
                    assert prev_y is not None
                    for i, mrow2 in enumerate(reversed(todo)):
                        mrow2._y = prev_y - (i + 1)*ac_canvas._min_m1row_pitch
                    todo = []
                    break
            else:
                if prev_y is not None:
                    prev_y += ac_canvas._min_m1row_pitch
                    mrow._y = prev_y
                else:
                    todo.append(mrow)
        n = len(todo)
        y0 = ac_canvas._midrow_height - 0.5*(n - 1)*ac_canvas._min_m1row_pitch
        for i, mrow in enumerate(todo):
            mrow._y = y0 + i*ac_canvas._min_m1row_pitch

        for mrow in reversed(top_rows):
            assert top_y is not None
            top_y -= ac_canvas._min_m1row_pitch
            mrow._y = top_y

    async def _place_m1cols(self) -> None:
        # self.log("_place_m1cols(): enter")
        cell = self.cell
        canvas = cell.canvas
        ac_canvas = cell.ac_canvas

        x: Optional[float] = None
        for multim1col in self.m1columns:
            # self.log(f"_place_m1cols(): computing x of {multim1col.name}")
            x = (
                # First column can contact to polypad so use _firstcol_dx
                ac_canvas._firstcol_dx if (x is None)
                else x + ac_canvas._min_m1col_pitch
            )
            assert not multim1col.is_placed, "Internal error"

            for col in multim1col:
                for elem in col._left:
                    x = max(x, (await elem._wait4x()) + ac_canvas._min_m1col_pitch)

            prev_sd = None
            for elem in multim1col.__iter_elems__():
                if isinstance(elem, PolyContactT):
                    left_xs: List[float] = []
                    for l in elem._left:
                        l_x = await l._wait4x()
                        if isinstance(l, PolyContactT):
                            left_xs.append(
                                l_x
                                + ac_canvas._polycont_width
                                + canvas._poly.min_space
                            )
                        elif isinstance(l, ActiveColumnT):
                            added = False
                            if (l._nmos is not None) or (l._pmos is not None):
                                left_xs.append(
                                    l_x
                                    + 0.5*canvas.l
                                    + canvas._poly.min_space
                                    + 0.5*ac_canvas._polycont_width
                                )
                                added = True
                            if (
                                ((l._nsd is not None) and l._nsd._has_contact)
                                or ((l._psd is not None) and l._psd._has_contact)
                            ):
                                left_xs.append(l_x + ac_canvas._min_m1row_pitch)
                                added = True
                            if not added:
                                raise ValueError(
                                    f"left Activecolumn '{l.name}' for PolyContact '{elem.name}'"
                                    "did not result in x constraint"
                                )
                    assert x is not None
                    x = max((x, *left_xs))
                elif isinstance(elem, (SignalNSDT, SignalPSDT)):
                    assert elem.with_contact, "Internal error: unchecked error"
                    elem_x = await elem._wait4x()

                    if (prev_sd is not None) and abs(cast(float, prev_sd._x) - elem_x) > _geo.epsilon:
                        raise ValueError(
                            f"MultiM1Column: different x for"
                            f" SignalNSDT '{prev_sd.name}' SignalPSDT '{elem.name}'"
                        )

                    prev_sd = elem

                    if x > elem_x + _geo.epsilon:
                        raise ValueError(
                            f"SignalSDT '{elem.name}' in MultiM1Column x too low"
                        )
                    x = elem_x
            multim1col._x = x
            # self.log(f"_place_m1cols(): computed x {x} for {multim1col.name}")
        # self.log("_place_m1cols(): leave")

    def _draw_wires(self) -> None:
        for elemselem in chain(
            self.activecolumns, *self.polyrows, *self.m1rows, *self.m1columns,
        ):
            elemselem._draw_wire()

    def _size_width(self) -> None:
        cell = self.cell
        canvas = cell.canvas

        active = canvas._active

        lastcol = self.activecolumns[-1]
        assert (lastcol._nmos is None) and (lastcol._pmos is None)
        nsd = lastcol._nsd
        psd = lastcol._psd
        assert (nsd is not None) or (psd is not None)
        min_widths: List[float] = []
        if nsd is not None:
            lay = nsd._placed
            bb = lay.bounds(mask=active.mask)
            min_widths.append(bb.right + 0.5*canvas._min_active_space)
        if psd is not None:
            lay = psd._placed
            bb = lay.bounds(mask=active.mask)
            min_widths.append(bb.right + 0.5*canvas._min_active_space)
        assert len(min_widths) > 0

        self.cell.set_width(min_width=max(min_widths))

    def log(self, *args):
        print(f"[{self.cell.name}:Constraints]", *args)
ConstraintsT = _Constraints


class _ActiveColumnsCanvas:
    def __init__(self, *, fab: "_scfab.StdCellFactory"):
        canvas = fab.canvas
        tech = canvas.tech

        # originally this assumed that PMOS was in a nwell and NMOS in substrate
        # therefor the properties computed here are referenced to nwell.
        active = canvas._active
        poly = canvas._poly
        contact = canvas._contact
        metal1  = canvas._metal1

        nmos = canvas._nmos
        pmos = canvas._pmos

        l = canvas.l
        vssrail_top = canvas._m1_vssrail_width
        vddrail_bottom = canvas._cell_height - canvas._m1_vddrail_width

        # Temporary cell to dervice values
        cell = _Cell(name="_internal_", fab=fab)

        # vss_sd

        vss_sd_l = _VssSD._gen_layout(cell=cell)

        vss_sd_act_bb = vss_sd_l.bounds(mask=active.mask)
        vss_sd_m1_bb = vss_sd_l.bounds(mask=metal1.mask)

        # vdd_sd

        vdd_sd_l = _VddSD._gen_layout(cell=cell)

        vdd_sd_act_bb = vdd_sd_l.bounds(mask=active.mask)
        vdd_sd_m1_bb = vdd_sd_l.bounds(mask=metal1.mask)

        # Compute placement values

        self._vss_sd_y = vssrail_top - vss_sd_m1_bb.top
        self._vdd_sd_y = vddrail_bottom - vdd_sd_m1_bb.bottom

        self._nact_bottom = vss_sd_act_bb.bottom + self._vss_sd_y
        self._pact_top = vdd_sd_act_bb.top + self._vdd_sd_y

        self._actcont_width = max(
            canvas._min_active_width,
            tech.computed.min_width(active, up=True, min_enclosure=True),
        )
        self._actcont_height = tech.computed.min_width(
            active, up=True, min_enclosure=False,
        )
        self._polyrow_width = tech.computed.min_width(
            poly, up=True, min_enclosure=False,
        )
        self._polycont_width = tech.computed.min_width(
            poly, up=True, min_enclosure=True,
        )
        self._m1row_width = tech.computed.min_width(
            metal1, down=True, min_enclosure=False,
        )
        self._m1col_width = tech.computed.min_width(
            metal1, down=True, up=True, min_enclosure=True,
        )

        dx_act = 0.5*canvas._min_active_space + 0.5*self._actcont_width
        dx_poly = 0.5*poly.min_space + 0.5*self._polycont_width
        try:
            s = tech.computed.min_space(active, poly)
        except:
            pass
        else:
            dx_poly = max(dx_poly, -0.5*canvas._min_active_space + s + 0.5*self._polycont_width)
        dx_m1 = 0.5*canvas.min_m1_space + 0.5*self._m1col_width
        self._firstcol_dx = tech.on_grid(
            max(dx_act, dx_poly, dx_m1), rounding="ceiling",
        )

        p = self._m1row_width + canvas.min_m1_space
        # The y of m1 row maybe used to place sd contact above poly contact
        # ensure that the m1 pitch does account for that
        try:
            s = tech.computed.min_space(active, poly)
        except:
            pass
        else:
            p = max(p, 0.5*self._polyrow_width + s + 0.5*self._actcont_height)
        self._min_m1row_pitch = tech.on_grid(p, rounding="ceiling", mult=2)

        self._min_polyrow_pitch = max(
            self._polyrow_width + poly.min_space,
            # y values of poly pads may be used as y values for m1 rows
            # this means that the polyrow pitch also has be at least equal
            # to the minimum m1 row pitch
            self._min_m1row_pitch,
        )
        self._min_m1col_pitch = self._m1col_width + canvas.min_m1_space
        self._min_polycont_hpitch = tech.computed.min_pitch(
            poly, up=True, min_enclosure=False,
        )

        self._min_contactedgate_pitch = tech.on_grid(
            max(
                l + 2*max(nmos.computed.min_contactgate_space, pmos.computed.min_contactgate_space)
                + contact.width,
                self._min_m1col_pitch,
            ),
            mult=2, rounding="ceiling",
        )
        self._min_gate_pitch = tech.on_grid(
            l + max(nmos.computed.min_gate_space, pmos.computed.min_gate_space),
            mult=2, rounding="ceiling",
        )
        # Min dx for active column that has a jog
        self._min_actjog_dx = max(
            0.5*self._min_contactedgate_pitch,
            tech.on_grid(
                0.5*l
                + canvas._min_active_poly_space
                + 0.5*self._actcont_width,
                rounding="ceiling",
            ),
        )
        # Min dx for gap in active
        self._min_actgap_dx = tech.on_grid(
            0.5*(self._actcont_width + canvas._min_active_space),
            rounding="ceiling",
        )

        enc = canvas._min_active_nwell_space
        if canvas._min_nsd_enc is not None:
            enc = max(enc, canvas._min_nsd_enc.second)
        if canvas._pimplant is not None:
            try:
                s = tech.computed.min_space(nmos.gate4mosfet, canvas._pimplant)
            except AttributeError:
                # Rule does not exist -> do nothing
                pass
            else:
                enc = max(enc, s)
        self._min_nact_nwell_space = enc

        enc = canvas._min_active_nwell_enclosure
        if canvas._min_psd_enc is not None:
            enc = max(enc, canvas._min_psd_enc.second)
        if canvas._nimplant is not None:
            try:
                s = tech.computed.min_space(pmos.gate4mosfet, canvas._nimplant)
            except AttributeError:
                # Rule does not exists -> do nothing
                pass
            else:
                enc = max(enc, s)
        self._min_pact_nwell_enclosure = enc

        # Set mid hieght of cell in middle of nact top and pact bottom
        self._midrow_height = tech.on_grid(
            canvas._well_edge_height
            + 0.5*(self._min_pact_nwell_enclosure - self._min_nact_nwell_space)
        )


class ActiveColumnsCellFrame(_Cell):
    """Subclasses of this class need to call _draw_frame() after they have set
    the of the cell.
    """
    def __init__(self, *, name: str, fab: "_scfab.StdCellFactory", draw_implants: bool=True):
        super().__init__(name=name, fab=fab)

        canvas = fab.canvas
        if canvas._ac_canvas is None:
            canvas._ac_canvas = _ActiveColumnsCanvas(fab=fab)

        self._draw_implants = draw_implants
        self._vsstap_lay: Optional[_lay.LayoutT] = None
        self._vddtap_lay: Optional[_lay.LayoutT] = None

    @property
    def ac_canvas(self) -> _ActiveColumnsCanvas:
        return self.canvas._ac_canvas
    @property
    def draw_implants(self) -> bool:
        return self._draw_implants
    @property
    def vsstap_lay(self) -> _lay.LayoutT:
        if self._vsstap_lay is None:
            raise TypeError(
                f"Accessing vsstap_lay on cell '{self.name}' before set_width has been called"
            )
        return self._vsstap_lay
    @property
    def vddtap_lay(self) -> _lay.LayoutT:
        if self._vddtap_lay is None:
            raise TypeError(
                f"Accessing vsstap_lay on cell '{self.name}' before set_width has been called"
            )
        return self._vddtap_lay

    def set_width(self, **args) -> float:
        width = super().set_width(**args)

        tech = self.tech
        canvas = self.canvas
        ac_canvas = self.ac_canvas
        layouter = self.layouter

        pwell = canvas._pwell
        nwell = canvas._nwell
        active = canvas._active
        nimplant = canvas._nimplant
        if canvas._min_active_nimplant_enc is None:
            assert nimplant is None, "Internal error"
            nenc = None
        else:
            nenc = canvas._min_active_nimplant_enc.wide()
            if (nenc.first + _geo.epsilon) < 0.5*canvas._min_active_space:
                nenc = _prp.Enclosure((0.5*canvas._min_active_space, nenc.second))
        pimplant = canvas._pimplant
        if canvas._min_active_pimplant_enc is None:
            assert pimplant is None, "Internal error"
            penc = None
        else:
            penc = canvas._min_active_pimplant_enc.wide()
            if (penc.first + _geo.epsilon) < 0.5*canvas._min_active_space:
                penc = _prp.Enclosure((0.5*canvas._min_active_space, penc.second))
        active = canvas._active
        contact = canvas._contact

        tap_height = ac_canvas._actcont_width

        # ptap
        act_left = 0.5*canvas._min_active_space
        act_right = width - act_left
        act_bottom = 0.5*canvas._min_active_space
        act_top = act_bottom + tap_height
        self._vsstap_lay = lay = layouter.add_wire(
            net=self.vss, well_net=self.pwell_net, wire=contact,
            bottom=active, bottom_well=pwell, bottom_enclosure="wide",
            bottom_implant=pimplant, bottom_implant_enclosure=penc,
            bottom_left=act_left, bottom_bottom=act_bottom,
            bottom_right=act_right, bottom_top=act_top,
        )
        if pimplant is not None:
            bb = lay.bounds(mask=pimplant.mask)
            args = {}
            if (bb.bottom - _geo.epsilon) > 0.0:
                args["bottom"] = 0.0
            if (bb.left - _geo.epsilon) > 0.0:
                args["left"] = 0.0
                args["right"] = width
            if args:
                shape = _geo.Rect.from_rect(rect=bb, **args)
                layouter.add_portless(prim=pimplant, shape=shape)

        # ntap
        act_left = 0.5*canvas._min_active_space
        act_right = width - act_left
        act_top = canvas._cell_height - 0.5*canvas._min_active_space
        act_bottom = act_top - tap_height
        self._vddtap_lay = lay = layouter.add_wire(
            net=self.vdd, well_net=self.nwell_net, wire=contact,
            bottom=active, bottom_well=nwell, bottom_enclosure="wide",
            bottom_implant=nimplant, bottom_implant_enclosure=nenc,
            bottom_left=act_left, bottom_bottom=act_bottom,
            bottom_right=act_right, bottom_top=act_top,
        )
        if nimplant is not None:
            bb = lay.bounds(mask=nimplant.mask)
            args = {}
            if (bb.top + _geo.epsilon) < canvas._cell_height:
                args["top"] = canvas._cell_height
            if (bb.left - _geo.epsilon) > 0.0:
                args["left"] = 0.0
                args["right"] = width
            if args:
                shape = _geo.Rect.from_rect(rect=bb, **args)
                layouter.add_portless(prim=nimplant, shape=shape)

        if self.draw_implants:
            # transistor nimplant
            if nimplant is not None:
                assert canvas._min_active_nimplant_enc is not None
                assert canvas._min_nsd_enc is not None
                enc = canvas._min_active_nimplant_enc.first
                left = min(0.0, 0.5*canvas._min_active_space - enc)
                right = max(width, width - 0.5*canvas._min_active_space + enc)
                bottom = ac_canvas._nact_bottom - canvas._min_nsd_enc.second
                top = canvas._well_edge_height
                shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                lay = layouter.add_portless(prim=nimplant, shape=shape)

            # transistor pimplant
            if pimplant is not None:
                assert canvas._min_active_pimplant_enc is not None
                assert canvas._min_psd_enc is not None
                enc = canvas._min_active_pimplant_enc.first
                left = min(0.0, 0.5*canvas._min_active_space - enc)
                right = max(width, width - 0.5*canvas._min_active_space + enc)
                top = ac_canvas._pact_top + canvas._min_psd_enc.second
                bottom = canvas._well_edge_height
                shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                layouter.add_portless(prim=pimplant, shape=shape)

        return width


class ActiveColumnsCell(ActiveColumnsCellFrame, abc.ABC):
    def __init__(self, *, name: str, fab: "_scfab.StdCellFactory"):
        super().__init__(name=name, fab=fab)

        self._waiterfab = _WaiterFactory(name=f"{name}:waiterfab")

        generator = self.build_generator()
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            class DoLayoutThread(Thread):
                def run(self):
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(generator._do_layout())

            thread = DoLayoutThread()
            thread.start()
            thread.join()
        else:
            loop.run_until_complete(generator._do_layout())

    @abc.abstractmethod
    def build_generator(self) -> ConstraintsT:
        pass

    def signal_nsd(self, *, name: str, net: _ckt.CircuitNetT, with_contact: bool) -> SignalNSDT:
        return _SignalNSD(cell=self, name=name, net=net, with_contact=with_contact)

    def vss_sd(self, *, name: str) -> VssSDT:
        return _VssSD(cell=self, name=name)

    def signal_psd(self, *, name: str, net: _ckt.CircuitNetT, with_contact: bool) -> SignalPSDT:
        return _SignalPSD(cell=self, name=name, net=net, with_contact=with_contact)

    def vdd_sd(self, *, name: str) -> VddSDT:
        return _VddSD(cell=self, name=name)

    def nmos(self, *, name: str, net: _ckt.CircuitNetT, w_size: str) -> NMOST:
        return _NMOS(cell=self, name=name, net=net, w_size=w_size)

    def pmos(self, *, name: str, net: _ckt.CircuitNetT, w_size: str) -> PMOST:
        return _PMOS(cell=self, name=name, net=net, w_size=w_size)

    def polypad(self, *,
        name: str, net: _ckt.CircuitNetT, left: MultiT[PolyContactLeftT]=(),
    ) -> PolyContactT:
        return _PolyContact(cell=self, name=name, net=net, left=left)

    def polyknot(self, *, name: str, net: _ckt.CircuitNetT) -> PolyKnotT:
        return _PolyKnot(cell=self, name=name, net=net)

    def m1knot(self, *, name: str, net: _ckt.CircuitNetT) -> M1KnotT:
        return _M1Knot(cell=self, name=name, net=net)

    def activecolumn(self, *,
        name: str, connect: bool, elements: MultiT[ActiveColumnElementT],
        left: MultiT[ActiveColumnLeftT]=(),
    ) -> ActiveColumnT:
        return _ActiveColumn(
            cell=self, name=name, connect=connect, elements=elements, left=left,
        )

    def polyrow(self, *,
        name: str, elements: MultiT[PolyRowElementT],
    ) -> PolyRowT:
        return _PolyRow(cell=self, name=name, elements=elements)

    def multipolyrow(self, *, name: str, rows: MultiT[PolyRowT]) -> MultiPolyRowT:
        return _MultiPolyRow(cell=self, name=name, rows=rows)

    def m1row(self, *,
        name: str, elements: MultiT[M1RowElementT],
    ) -> M1RowT:
        return _M1Row(cell=self, name=name, elements=elements)
    def multim1row(self, *, name: str, rows: MultiT[M1RowT]) -> MultiM1RowT:
        return _MultiM1Row(cell=self, name=name, rows=rows)

    def m1column(self, *,
        name: str, elements: MultiT[M1ColumnElementT],
        left: MultiT[M1ColumnLeftT]=(),
        bottom: MultiT[M1ColumnBottomTopT]=(), top: MultiT[M1ColumnBottomTopT]=(),
    ) -> M1ColumnT:
        return _M1Column(
            cell=self, name=name, elements=elements,
            left=left, bottom=bottom, top=top,
        )

    def m1pin(self, *,
        name: str, elements: MultiT[M1ColumnElementT],
        left: MultiT[M1ColumnLeftT]=(),
        bottom: MultiT[M1ColumnBottomTopT]=(), top: MultiT[M1ColumnBottomTopT]=(),
    ) -> M1ColumnT:
        return _M1Pin(
            cell=self, name=name, elements=elements,
            left=left, bottom=bottom, top=top,
        )

    def multim1column(self, *, name: str, columns: MultiT[M1ColumnT]) -> MultiM1ColumnT:
        return _MultiM1Column(cell=self, name=name, columns=columns)

    def constraints(self, *,
        activecolumns: MultiT[ActiveColumnT],
        polyrows: MultiT[MultiPolyRowT],
        m1rows: MultiT[MultiM1RowT],
        m1columns: MultiT[MultiM1ColumnT],
    ) -> ConstraintsT:
        return _Constraints(
            cell=self,
            activecolumns=activecolumns,
            polyrows=polyrows,
            m1rows=m1rows,
            m1columns=m1columns,
        )


from . import factory as _scfab
