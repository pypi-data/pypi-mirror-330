# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Dict, Optional, Any

from pdkmaster.typing import OptMultiT, cast_OptMultiT, cast_OptMultiT_n
from pdkmaster.technology import (
    property_ as _prp, geometry as _geo, primitive as _prm, technology_ as _tch,
)
from pdkmaster.design import routinggauge as _rg


__all__ = ["StdCellCanvas"]


class StdCellCanvas:
    """The CellCanvas class describes the rules a generated standard cell has to
    fullfil.

    Parameters:
        tech: the technology to use for the standard cells
            Assumption on the stack composition are made:
                * at least 3 metal layers
                * only one top layer for contact and vias and one bottom
                    layer for the vias and these need to be of type MetalWire
        nmos: the nmos transistor to use in the cells
            By default the minimum l for the nmos will be used.
            It is currently assumed that the active and the poly wire is the same
            for the nmos and the pmos gates.
        pmos: the pmos transistor to use in the cells
            Currently it is assumed the pmos is in a n-type well.
        l: the transistor length to use for the nmos/pmos.
            By default the minimum l for the provided transistors will be used.
            When the default value is used the minimum l of the nmos and pmos
            have to be the same.
        nimplant: implant to use for n-diffusion wires and nwell taps
        pimplant: implant to use for p-diffusion wires and bulk/pwell taps
        inside: optional layer(s) to draw around the full cell.
        inside_enclosure: enclosure value to use for drawing the inside, the
            cell boundary box is up-sized with enclosure value and that
            rectangle is used for the drawing the layer.
            One value can be given for all inside layers or a value for each
            inside layer. By default 0 enclosure is taken and the shape of the
            drawn layers is the cell boundary box.
        min_m1_space: Provide custom Metal1 spacing.
            Currently implementation of the compaction may violate width
            independent Metal1 spacing rules. This options allows to give
            global minimum space that avoids these violations. Unfortunately
            this is global parameter and increases spacing everywhere.
    """
    def __init__(self, *,
        tech: _tch.Technology,
        nmos: _prm.MOSFET, nmos_min_w: float,
        pmos: _prm.MOSFET, pmos_min_w: float,
        l: Optional[float]=None,
        cell_height: float,
        cell_horplacement_grid: float,
        m1_vssrail_width: float,
        m1_vddrail_width: float,
        well_edge_height: float,
        nimplant: Optional[_prm.Implant]=None,
        pimplant: Optional[_prm.Implant]=None,
        inside: OptMultiT[_prm.DesignMaskPrimitiveT]=None,
        inside_enclosure: OptMultiT[_prp.Enclosure]=None,
        min_m1_space: Optional[float]=None,
    ):
        if nmos not in tech.primitives:
            raise ValueError(
                f"provided nmos transistor {nmos.name} not of technology '{tech.name}'",
            )
        if nimplant is None:
            try:
                nimplant = nmos.implant[0]
            except:
                pass
            else:
                assert nimplant.type_ == _prm.nImpl
        else:
            if nimplant.type_ != _prm.nImpl:
                raise ValueError(
                    f"nimplant '{nimplant.name}' is not n type",
                )
            if nimplant not in nmos.implant:
                raise NotImplementedError(
                    f"nimplant '{nimplant.name}' not part of nmos implants"
                )

        if pmos not in tech.primitives:
            raise ValueError(
                f"provided pmos transistor {pmos.name} not of technology '{tech.name}'",
            )
        if pimplant is None:
            try:
                pimplant = pmos.implant[0]
            except:
                pass
            else:
                assert pimplant.type_ == _prm.pImpl
        else:
            if pimplant.type_ != _prm.pImpl:
                raise ValueError(
                    f"pimplant '{pimplant.name}' is not p type",
                )
            if pimplant not in pmos.implant:
                raise NotImplementedError(
                    f"pimplant '{pimplant.name}' not part of pmos implants"
                )

        if (nimplant is None) and (pimplant is None):
            raise ValueError("both nimplant and pimplant are None")

        if l is None:
            l = nmos.computed.min_l
            if nmos.computed.min_l != pmos.computed.min_l:
                raise NotImplementedError(
                    "Differing minimal l of nmos and pmos"
                )
        else:
            if l//_geo.epsilon < nmos.computed.min_l//_geo.epsilon:
                raise ValueError(
                    f"l {l}um smaller than min. nmos transistor l {nmos.computed.min_l}um",
                )
            if l//_geo.epsilon < pmos.computed.min_l//_geo.epsilon:
                raise ValueError(
                    f"l {l}um smaller than min. pmos transistor l {nmos.computed.min_l}um",
                )

        inside = cast_OptMultiT(inside)
        if inside is None:
            if inside_enclosure is not None:
                raise ValueError("inside_enclosure provided with inside")
        else:
            if inside_enclosure is None:
                inside_enclosure = _prp.Enclosure(0.0)
            inside_enclosure = cast_OptMultiT_n(inside_enclosure, n=len(inside))

        self._tech = tech
        self._nmos = nmos
        self._pmos = pmos
        self._l = l
        self._nimplant = nimplant
        self._pimplant = pimplant
        self._inside = inside
        self._inside_enclosure = inside_enclosure

        self._nmos_min_w = nmos_min_w
        self._pmos_min_w = pmos_min_w
        self._cell_height = cell_height
        self._cell_horplacement_grid = cell_horplacement_grid
        self._m1_vssrail_width = m1_vssrail_width
        self._m1_vddrail_width = m1_vddrail_width
        self._well_edge_height = well_edge_height

        # Derived values
        nwell = pmos.well
        if nwell is None:
            raise NotImplementedError("pmos not in a well")
        self._nwell: _prm.Well = nwell
        pwell = nmos.well
        self._pwell: Optional[_prm.Well] = pwell

        self._active = active = nmos.gate.active
        if active != pmos.gate.active:
            raise NotImplementedError(
                "Different active wire for nmos and pmos transistor"
            )
        idx = active.well.index(nwell)
        self._min_active_nwell_enclosure = pmos.computed.min_active_well_enclosure.max()
        if pwell is not None:
            s = nmos.computed.min_active_well_enclosure.max()
        elif nmos.computed.min_active_substrate_enclosure is not None:
            s = nmos.computed.min_active_substrate_enclosure.max()
        else:
            s = tech.computed.min_space(primitive1=active, primitive2=nwell)
        self._min_active_nwell_space: float = s

        self._poly = poly = nmos.gate.poly
        if poly != pmos.gate.poly:
            raise NotImplementedError(
                "Different poly wire for nmos and pmos transistor"
            )

        vs = [active.min_space]
        if inside is not None:
            for in_ in inside:
                ins = active.in_(in_)
                try:
                    s = tech.computed.min_space(ins)
                except:
                    pass
                else:
                    vs.append(s)
        self._min_active_space = max(vs)
        vs = [active.min_width]
        if inside is not None:
            ins = active.in_(inside)
            try:
                w = tech.computed.min_width(ins)
            except:
                pass
            else:
                vs.append(w)
        self._min_active_width = max(vs)

        self._min_active_poly_space = tech.computed.min_space(active, poly)

        ins = () if inside is None else inside
        self._nactive = nactive = active if nimplant is None else active.in_((nimplant, *ins))
        self._pactive = pactive = active if pimplant is None else active.in_((pimplant, *ins))

        self._min_nactive_pactive_space = v = tech.computed.min_space(nactive, pactive)
        self._min_nactive_pactive_space_maxenc = tech.computed.min_space(
            nactive, pactive, max_enclosure=True,
        )

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
        self._min_active_nimplant_enc = act_enc
        if gate_enc is None:
            if act_enc is None:
                self._min_nsd_enc = None
            else:
                self._min_nsd_enc = act_enc
        else:
            assert act_enc is not None
            self._min_nsd_enc = _prp.Enclosure((
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
        self._min_active_pimplant_enc = act_enc
        if gate_enc is None:
            if act_enc is None:
                self._min_psd_enc = None
            else:
                self._min_psd_enc = act_enc
        else:
            assert act_enc is not None
            self._min_psd_enc = _prp.Enclosure((
                act_enc.first, max(act_enc.min(), gate_enc.second),
            ))

        self._vias = vias = tuple(tech.primitives.__iter_type__(_prm.Via))
        self._contact = cont = vias[0]
        min_contact_active_space = None
        try:
            min_contact_active_space = tech.computed.min_space(
                primitive1=cont, primitive2=active,
            )
        except AttributeError:
            pass
        # Contact on poly to implant spacing
        # TODO: See if it can be done with drawing implants over pads
        idx = cont.bottom.index(poly)
        polyenc = cont.min_bottom_enclosure[idx].min()
        def get_implants():
            if nimplant is not None:
                yield nimplant
            if pimplant is not None:
                yield pimplant
        for impl in get_implants():
            try:
                s = tech.computed.min_space(
                    primitive1=cont.in_(poly), primitive2=impl,
                )
            except AttributeError:
                pass
            else:
                idx = active.implant.index(impl)
                enc = active.min_implant_enclosure[idx].max()
                try:
                    enc = max(enc, nmos.min_gateimplant_enclosure[0].max())
                except:
                    pass
                else:
                    if min_contact_active_space is None:
                        min_contact_active_space = enc + s + polyenc
                    else:
                        min_contact_active_space = max(
                            min_contact_active_space,
                            enc + s + polyenc,
                        )
        self._min_contact_active_space = min_contact_active_space
        idx = cont.bottom.index(active)
        self._min_contact_active_enclosure = cont.min_bottom_enclosure[idx]
        idx = cont.bottom.index(poly)
        self._min_contact_poly_enclosure = cont.min_bottom_enclosure[idx]
        self._via1 = via1 = vias[1]
        self._via2 = via2 = vias[2]
        for v in (cont, via1, via2):
            if len(v.top) != 1:
                raise NotImplementedError(
                    f"Number of top layers for contact/via '{v.name}' not 1"
                )
        for v in (via1, via2):
            if len(v.bottom) != 1:
                raise NotImplementedError(
                    f"Number of bottom layers for via '{v.name}' not 1"
                )
        metal1 = cont.top[0]
        if not isinstance(metal1, _prm.MetalWire):
            raise ValueError(
                "top contact layer is not of type 'MetalWire' but of type "
                f"'{type(metal1)}'"
            )
        self._metal1 = metal1
        self._metal1pin = metal1.pin
        self._min_contact_metal1_enclosure = cont.min_top_enclosure[0]
        metal2 = via1.top[0]
        if not isinstance(metal2, _prm.MetalWire):
            raise ValueError(
                "top via1 layer is not of type 'MetalWire' but of type "
                f"'{type(metal2)}'"
            )
        self._metal2 = metal2
        self._metal2pin = metal2.pin
        metal3 = via2.top[0]
        if not isinstance(metal3, _prm.MetalWire):
            raise ValueError(
                "top via2 layer is not of type 'MetalWire' but of type "
                f"'{type(metal3)}'"
            )
        self._metal3 = metal3
        self._metal3pin = metal3.pin

        # Custom minimum spacing rules. Width dependent rules may need a non-minimal metal1
        # space; this includes normal width contacted width and the DC rails
        w_m1 = max(
            tech.computed.min_width(metal1, down=True, up=False, min_enclosure=False),
            tech.computed.min_width(metal1, down=True, up=True, min_enclosure=True),
        )
        self.min_m1_space = min_m1_space = (
            min_m1_space
            if min_m1_space is not None
            else tech.computed.min_space(metal1, width=w_m1)
        )
        self._min_m1vssrail_space = max(
            min_m1_space,
            tech.computed.min_space(metal1, width=2*m1_vssrail_width),
        )
        self._min_m1vddrail_space = max(
            min_m1_space,
            tech.computed.min_space(metal1, width=2*m1_vddrail_width),
        )

        enc = via1.min_bottom_enclosure[0].min()
        self._pin_width = tech.computed.min_width(
            metal1, up=True, down=True, min_enclosure=True,
        )

        self._min_tap_chs = 2 # Should be high enough for min. diffusion area

        # ActiveColumsCell specific values
        self._ac_canvas: Any = None

    @property
    def tech(self) -> _tch.Technology:
        return self._tech
    @property
    def nmos(self) -> _prm.MOSFET:
        return self._nmos
    @property
    def pmos(self) -> _prm.MOSFET:
        return self._pmos
    @property
    def l(self) -> float:
        return self._l
    @property
    def nimplant(self) -> Optional[_prm.Implant]:
        return self._nimplant
    @property
    def pimplant(self) -> Optional[_prm.Implant]:
        return self._pimplant

    @property
    def routinggauge(self) -> _rg.RoutingGauge:
        vias = tuple(self.tech.primitives.__iter_type__(_prm.Via))
        topvia = vias[-1]
        assert len(topvia.top) == 1
        topmetal = vias[-1].top[0]
        assert isinstance(topmetal, _prm.MetalWire)
        return _rg.RoutingGauge(
            tech=self.tech,
            # metal1 layer is used only for Pin
            # => bottom layer is _metal2
            bottom=self._metal2, bottom_direction="horizontal", top=topmetal,
            pingrid_pitch=self._cell_horplacement_grid, row_height=self._cell_height,
        )

    @staticmethod
    def compute_dimensions_lambda(lambda_: float) -> Dict[str, Any]:
        return {
            "nmos_min_w": 20*lambda_,
            "pmos_min_w": 40*lambda_,
            "cell_height": 200*lambda_,
            "cell_horplacement_grid": 20*lambda_,
            "m1_vssrail_width": 24*lambda_,
            "m1_vddrail_width": 24*lambda_,
            "well_edge_height": 96*lambda_,

        }