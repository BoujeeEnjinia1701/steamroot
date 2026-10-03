#!/usr/bin/env python3
"""STR-CAL-001 SteamRoot sizing calculations (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and the requirement status table.
Other scripts (cad/src/concept_media.py, cad/src/sheets.py) import run() so the media quote the same numbers.

First-principles estimates with stated assumptions. Paper calculation only; nothing here is verified
by test. PRELIMINARY, NOT FOR FABRICATION. The regulatory ruling from the local boiler authority is an
open prerequisite.
"""
from __future__ import annotations
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as GEO, derived, bank_length  # noqa: E402  (shared geometry parameters, mm)
DGEO = derived(GEO)

SIGMA = 5.670e-8   # W/(m2 K4)
G = 9.81           # m/s2

# ---------------------------------------------------------------- assumptions
A = {
    # Duty
    "steam_kg_h": 30.0,          # design steam output (R3)
    "t_feed": 15.0,              # feed water temperature, C
    "t_eco_out": 85.0,           # economizer outlet, kept 15 K below boiling
    # Water and steam near 1.01 bar (saturation 100 C)
    "cp_w": 4.18, "h_fg": 2257.0, "h_f100": 419.1,         # kJ/kg
    "rho_l": 958.4, "rho_g": 0.598, "mu_l": 2.82e-4, "mu_g": 1.23e-5,
    # Soil (R1, R2)
    "rho_b": 1300.0, "w": 0.20, "c_soil": 0.84, "t_soil0": 15.0, "t_kill": 70.0, "t_steam": 100.0,
    "k_soil": 1.2,               # W/(m K), moist loam; range 0.8 to 1.6
    "hold_min": 25.0,            # hold time at 70 C (R1 asks 20 to 30 min)
    "move_min": 2.0,             # lift and reset one hood
    "switch_min": 1.0,           # steam vented while the hose is moved between hoods
    "edge_leak": 0.10,           # fraction of steam lost under the skirt (assumed; range 0.05 to 0.25)
    "k_perm": [1e-10, 1e-11, 1e-12],   # intrinsic permeability of soil, m2 (sand, sandy loam, loam)
    "ballast_kg": GEO["ballast_kg"],   # per hood, four 10 kg weights hung two a side
    # Hood construction
    "k_ins": 0.040, "h_out": 10.0, "rho_al": 2700.0, "c_al": 0.90, "rho_mw": 100.0, "c_mw": 0.84,
    # Wood fuel (20 % moisture, wet basis), dry ultimate analysis in mass %
    "C": 50.0, "H": 6.0, "O": 43.3, "N": 0.2, "ash": 0.5, "moist": 0.20,
    # Combustion and firebox
    "lambda": 2.0,               # excess air ratio for a hand-fed batch firebox (range 1.5 to 2.5)
    "f_unburned": 0.04,          # CO and char loss as a fraction of fuel energy
    "cp_fg": 1.15,               # kJ/(kg K), flue gas 300 to 700 C
    "F_rad": 0.40,               # radiative exchange factor per unit coil tube area (range 0.25 to 0.6)
    "h_conv": 20.0,              # W/(m2 K), gas to coil convection
    "t_wall": 110.0,             # coil wall temperature, C
    "k_lining": 0.12, "h_shell": 12.0,   # ceramic fiber at mean temperature; shell outside film
    "U_eco": 25.0,               # W/(m2 K), economizer overall coefficient (gas side controlled)
    # Pressure drop
    "hose_bore": 0.025, "hose_len": 6.0, "K_hose_fittings": 5.0, "dp_manifold": 500.0,  # Pa
    # Dry-coil event
    "t_dry": None,               # filled from the firebox gas temperature
    "c_ss": 0.50, "rho_ss": 8000.0, "flash_s": 30.0, "sy_316_700C": 100e6,
    # Relief valve (Napier formula, US units)
    "rv_set_psig": 15.0, "rv_accum": 0.10, "rv_K": 0.878,
    "rv_rated_lb_h": 375.0,      # Watts Series 315, 3/4 in, 15 psi set: 375 lb/h (maker's capacity table)
    # R5 and R4 study (decided by Amish 2026-09-25: study a convective evaporator bank with controlled air;
    # 2026-10-02: size it with primary and secondary air dampers, keeping R7)
    "U_bank": 30.0,              # W/(m2 K), bare-tube evaporator bank in cross flow (gas side controlled)
    "lambda_ctl": 1.5,           # excess air ratio held with the primary and secondary air dampers (range 1.5 to 2.0)
    "k_bank_lining": 0.12,       # 25 mm fibre on the bank box walls
    "draft_cd": 0.6,             # discharge coefficient of the damper openings
    "t_flue_mean": 400.0,        # mean flue gas temperature in the firebox, bank and chimney for the draft check, C
    # Hood ballast (decided 2026-10-02: handles sized to carry ballast weights)
    "ballast_dyn": 2.0,          # load factor on the handle for weights hung, knocked or lifted with the hood
    "sy_steel": 235e6,           # yield of the steel handle tube, Pa
    # Mass (kg) not derived from geometry
    "m_trailer": 160.0, "m_grate_door": 25.0, "rho_st": 7850.0, "rho_lining": 128.0, "rho_castable": 2000.0,
    "m_tank_empty": 8.0, "m_pump": 2.0, "m_battery": 6.0, "m_hose_per_m": 0.9, "m_header_etc": 18.0,
    "m_instr_safety": 8.0, "m_hood_extra": 5.5,   # manifold and handles; the handles are 30 x 30 x 2.5 steel tube on foot plates
    "m_construction": 46.0,      # skids, header post, pot stay and foot plate, saddles, coil brackets, grate stand,
                                 # gland plates, both dampers, feed lines, vent line and discharge, seal pot overflow
                                 # (42.5 kg from model volumes, python cad/src/model.py --mass) plus the roof frame and unions
    "m_bank": 26.0,              # evaporator bank box, lining, tube, supports, link (python cad/src/model.py --mass)
    # Budget
    "budget_usd": 2200.0,        # value-engineering target (a hypothetical control target, not a limit); STR-DDR-002
}


def erfinv(y):
    lo, hi = 0.0, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if math.erf(mid) < y else (lo, mid)
    return (lo + hi) / 2


def sat_temp_from_pp(p_pa):
    """Saturation temperature (C) from vapor pressure (Pa), Antoine for water 1 to 100 C."""
    p_mmhg = p_pa / 133.322
    return 1730.63 / (8.07131 - math.log10(p_mmhg)) - 233.426


def run(a=A, geo=GEO, verbose=False):
    r = {}
    out = []
    def say(s=""):
        out.append(s)

    m_s = a["steam_kg_h"] / 3600.0
    h_feed = a["cp_w"] * a["t_feed"]
    h_eco = a["cp_w"] * a["t_eco_out"]
    h_g = a["h_f100"] + a["h_fg"]
    r["Q_steam"] = m_s * (h_g - h_feed)          # kW, total heat into water
    r["Q_eco"] = m_s * (h_eco - h_feed)
    r["Q_coil"] = m_s * (h_g - h_eco)
    r["Q_eco_max"] = m_s * (a["h_f100"] - h_feed)

    # ---------------------------------------------------- A. soil heat and steam demand
    C_vol = a["rho_b"] * (a["c_soil"] + a["w"] * a["cp_w"])              # kJ/(m3 K)
    alpha = a["k_soil"] / (C_vol * 1e3)                                   # m2/s
    t_hold = a["hold_min"] * 60
    T_i = (a["t_steam"] + a["t_soil0"]) / 2
    eta_z = erfinv((a["t_kill"] - T_i) / (a["t_steam"] - T_i))
    delta = 2 * math.sqrt(alpha * t_hold) * eta_z                          # m overshoot
    r.update(C_vol=C_vol, alpha=alpha, delta=delta)
    # TRL 2 uniform 75 C model, for comparison
    E_trl2 = C_vol * 60 * 0.15 / 1000                                     # MJ/m2
    r["E_trl2"] = E_trl2
    r["ms_trl2"] = E_trl2 / (0.60 * (a["h_fg"] + a["cp_w"] * 25) / 1000)

    hl, hw, hh = geo["hood_l"] / 1000, geo["hood_w"] / 1000, geo["hood_h"] / 1000
    A_hood = hl * hw
    A_hood_skin = hl * hw + 2 * (hl + hw) * hh
    U_hood = 1 / (geo["hood_ins_t"] / 1000 / a["k_ins"] + 1 / a["h_out"])
    P_hood_wall = U_hood * A_hood_skin * (a["t_steam"] - a["t_soil0"]) / 1000   # kW
    m_hood_skin = 2 * A_hood_skin * geo["hood_skin_t"] / 1000 * a["rho_al"]
    m_hood_mw = A_hood_skin * geo["hood_ins_t"] / 1000 * a["rho_mw"]
    E_hood_store = (A_hood_skin * geo["hood_skin_t"] / 1000 * a["rho_al"] * a["c_al"] * 85
                    + m_hood_mw * a["c_mw"] * 42.5) / 1000                   # MJ per setting (inner skin + half of wool)
    skirt_m = 2 * (hl + hw) * geo["skirt_depth"] / 1000 * 0.002 * a["rho_st"]
    m_hood = m_hood_skin + m_hood_mw + skirt_m + a["m_hood_extra"]
    r.update(A_hood=A_hood, U_hood=U_hood, P_hood_wall=P_hood_wall, E_hood_store=E_hood_store, m_hood=m_hood)

    def demand(depth_m):
        """Steam per m2 and cycle numbers for one hood setting at a working depth."""
        E_soil = C_vol * (a["t_steam"] - a["t_soil0"]) * (depth_m + delta) / 1000     # MJ/m2
        ms = E_soil / (a["h_fg"] / 1000) / (1 - a["edge_leak"])                      # kg/m2 before hood losses
        for _ in range(20):   # hood wall loss and storage depend on heating time
            t_heat = A_hood * ms / a["steam_kg_h"]                                     # h
            E_hood = (P_hood_wall * t_heat * 3600 / 1000 + E_hood_store) / A_hood      # MJ/m2
            ms = (E_soil + E_hood) / (a["h_fg"] / 1000) / (1 - a["edge_leak"])
        eta = E_soil / (ms * a["h_fg"] / 1000)
        return dict(E_soil=E_soil, E_hood=E_hood, ms=ms, t_heat=t_heat * 60, eta_hood=eta)

    def rate(d, n_hoods):
        steam_lim = A_hood / ((d["t_heat"] + a["switch_min"]) / 60)
        hood_lim = n_hoods * A_hood / ((d["t_heat"] + a["hold_min"] + a["move_min"]) / 60)
        return min(steam_lim, hood_lim), ("steam" if steam_lim <= hood_lim else "hood")

    d15, d5 = demand(0.15), demand(0.05)
    r["d15"], r["d5"] = d15, d5
    for n in (1, 2, 3):
        r[f"rate15_{n}"], r[f"lim15_{n}"] = rate(d15, n)
        r[f"rate5_{n}"], r[f"lim5_{n}"] = rate(d5, n)

    # Soil permeability versus hood lift pressure
    p_lift = m_hood * G / A_hood
    u_gas = m_s / a["rho_g"] / A_hood
    r["p_lift"] = p_lift
    r["dp_soil"] = {k: a["mu_g"] * u_gas * (0.15 + delta) / k for k in a["k_perm"]}
    r["u_gas"] = u_gas

    # ---------------------------------------------------- B. fuel and combustion
    C, H, O, N, Ash = a["C"], a["H"], a["O"], a["N"], a["ash"]
    hhv_dry = 0.3491 * C + 1.1783 * H - 0.1034 * O - 0.0151 * N - 0.0211 * Ash      # Channiwala and Parikh, MJ/kg
    lhv_dry = hhv_dry - 2.442 * 9 * H / 100
    M = a["moist"]
    lhv = lhv_dry * (1 - M) - 2.442 * M
    o2_dry = C / 100 * 32 / 12 + H / 100 * 8 - O / 100
    air_st = o2_dry / 0.232 * (1 - M)                                               # kg air / kg wet fuel
    r.update(hhv_dry=hhv_dry, lhv_dry=lhv_dry, lhv=lhv, air_st=air_st)

    def firebox(lam, F, air_preheat=0.0):
        r_fg = 1 + lam * air_st                                                     # kg flue / kg fuel
        od = geo["tube_od"] / 1000
        L = math.hypot(math.pi * geo["coil_mean_d"] / 1000, geo["coil_pitch"] / 1000) * geo["coil_turns"]
        A_c = math.pi * od * L
        Tw = a["t_wall"] + 273.15
        def q_coil(Tg_C):
            Tg = Tg_C + 273.15
            return (SIGMA * F * A_c * (Tg**4 - Tw**4) + a["h_conv"] * A_c * (Tg - Tw)) / 1000
        lo, hi = 150.0, 1500.0
        for _ in range(80):
            mid = (lo + hi) / 2
            (lo, hi) = (lo, mid) if q_coil(mid) > r["Q_coil"] else (mid, hi)
        Tg = (lo + hi) / 2
        fb = geo
        A_fb = 2 * (fb["fb_l"] * fb["fb_w"] + fb["fb_l"] * fb["fb_h"] + fb["fb_w"] * fb["fb_h"]) / 1e6
        R_wall = fb["fb_lining_t"] / 1000 / a["k_lining"] + 1 / a["h_shell"]
        q_shell = (Tg - a["t_soil0"]) / R_wall / 1000                              # kW/m2
        Q_shell = q_shell * A_fb
        t_skin = a["t_soil0"] + q_shell * 1000 / a["h_shell"]
        # energy balance on the firebox: fuel + preheated air = coil + shell + gas enthalpy + unburned
        # gas leaving the firebox at Tg (single well-stirred zone)
        # m_f * [lhv*(1-f_unb) + lam*air_st*cp_air*air_preheat] = Q_coil + Q_shell + m_f*r_fg*cp*(Tg - T0)
        num = r["Q_coil"] + Q_shell
        den = lhv * 1000 * (1 - a["f_unburned"]) + lam * air_st * 1.0 * air_preheat - r_fg * a["cp_fg"] * (Tg - a["t_soil0"])
        m_f = num / den                                                              # kg/s wet fuel
        mfg = m_f * r_fg
        T_eco_in = Tg
        T_after_eco = T_eco_in - r["Q_eco"] / (mfg * a["cp_fg"])
        T_stack = T_after_eco - lam * air_st * m_f * 1.0 * air_preheat / (mfg * a["cp_fg"])
        Q_in = m_f * lhv * 1000
        Q_stack = mfg * a["cp_fg"] * (T_stack - a["t_soil0"])
        eta = r["Q_steam"] / Q_in
        lmtd = ((T_eco_in - a["t_eco_out"]) - (T_after_eco - a["t_feed"])) / math.log(
            (T_eco_in - a["t_eco_out"]) / (T_after_eco - a["t_feed"]))
        A_eco_req = r["Q_eco"] * 1000 / (a["U_eco"] * lmtd)
        return dict(Tg=Tg, m_f=m_f, wood_kg_h=m_f * 3600, Q_in=Q_in, Q_shell=Q_shell, t_skin=t_skin,
                    Q_stack=Q_stack, T_stack=T_stack, T_after_eco=T_after_eco, eta=eta, mfg=mfg, A_c=A_c,
                    A_eco_req=A_eco_req, lmtd=lmtd, Q_unb=Q_in * a["f_unburned"], r_fg=r_fg,
                    closure=Q_in + lam * air_st * m_f * air_preheat - (r["Q_coil"] + r["Q_eco"] + Q_shell + Q_stack + Q_in * a["f_unburned"]))

    base = firebox(a["lambda"], a["F_rad"])
    r["fb_v03"] = base                     # v0.3 design: no bank, lambda 2.0
    r["sens"] = {(lam, F): firebox(lam, F) for lam in (1.5, 2.0, 2.5) for F in (0.25, 0.40, 0.60)}
    r["fb_preheat"] = firebox(a["lambda"], a["F_rad"], air_preheat=135.0)
    def bank_study(lam, F, eta_t=0.65):
        """Evaporator bank in the flue between firebox and economizer needed to reach eta_t (R5 study)."""
        r_fg = 1 + lam * air_st
        Q_in = r["Q_steam"] / eta_t
        m_f = Q_in / (lhv * 1000)
        mfg = m_f * r_fg
        od = geo["tube_od"] / 1000
        L = math.hypot(math.pi * geo["coil_mean_d"] / 1000, geo["coil_pitch"] / 1000) * geo["coil_turns"]
        A_c = math.pi * od * L
        Tw = a["t_wall"] + 273.15
        A_fb = 2 * (geo["fb_l"] * geo["fb_w"] + geo["fb_l"] * geo["fb_h"] + geo["fb_w"] * geo["fb_h"]) / 1e6
        R_wall = geo["fb_lining_t"] / 1000 / a["k_lining"] + 1 / a["h_shell"]
        avail = Q_in * (1 - a["f_unburned"])
        def excess(Tg_C):   # heat released minus heat leaving the firebox zone
            Tg = Tg_C + 273.15
            q_c = (SIGMA * F * A_c * (Tg**4 - Tw**4) + a["h_conv"] * A_c * (Tg - Tw)) / 1000
            q_s = (Tg_C - a["t_soil0"]) / R_wall / 1000 * A_fb
            return avail - q_c - q_s - mfg * a["cp_fg"] * (Tg_C - a["t_soil0"]), q_c
        lo, hi = 150.0, 1500.0
        for _ in range(80):
            mid = (lo + hi) / 2
            (lo, hi) = (mid, hi) if excess(mid)[0] > 0 else (lo, mid)
        Tg = (lo + hi) / 2
        q_fb = excess(Tg)[1]
        Q_bank = max(0.0, r["Q_coil"] - q_fb)
        T1 = Tg - Q_bank / (mfg * a["cp_fg"])
        tb = a["t_steam"]
        lmtd = (Tg - T1) / math.log((Tg - tb) / (T1 - tb)) if Q_bank > 0 else float("nan")
        A_bank = Q_bank * 1000 / (a["U_bank"] * lmtd) if Q_bank > 0 else 0.0
        T_stack = T1 - r["Q_eco"] / (mfg * a["cp_fg"])
        return dict(lam=lam, F=F, eta=eta_t, Tg=Tg, q_fb=q_fb, Q_bank=Q_bank, T1=T1, A_bank=A_bank,
                    L_bank=A_bank / (math.pi * od), T_stack=T_stack, wood_kg_h=m_f * 3600)

    r["bank"] = {lam: bank_study(lam, a["F_rad"]) for lam in (1.5, 2.0)}

    def fired(g, lam, F, L_bank_m):
        """Forward model of the firebox, evaporator bank and economizer (STR-CAL-001 v0.4, section 4).
        The firing rate is found so that the coil and bank together boil the feed the economizer delivers;
        the bank is a counterflow exchanger at 100 C, the economizer a counterflow exchanger capped at
        t_eco_out. g is a geometry dictionary (coil turns, firebox height, bank tube)."""
        r_fg = 1 + lam * air_st
        od = g["tube_od"] / 1000
        L = math.hypot(math.pi * g["coil_mean_d"] / 1000, g["coil_pitch"] / 1000) * g["coil_turns"]
        A_c = math.pi * od * L
        Tw = a["t_wall"] + 273.15
        A_fb = 2 * (g["fb_l"] * g["fb_w"] + g["fb_l"] * g["fb_h"] + g["fb_w"] * g["fb_h"]) / 1e6
        R_wall = g["fb_lining_t"] / 1000 / a["k_lining"] + 1 / a["h_shell"]
        A_bank = math.pi * g["bk_tube_od"] / 1000 * L_bank_m
        A_bwall = 2 * (g["fb_l"] + g["fb_w"]) / 1000 * g["bk_h"] / 1000 if L_bank_m > 0 else 0.0
        R_bwall = g["bk_lining_t"] / 1000 / a["k_bank_lining"] + 1 / a["h_shell"]
        A_eco = math.pi * g["eco_tube_od"] / 1000 * g["eco_tube_len"] / 1000
        Cw = m_s * a["cp_w"]

        def state(m_f):
            mfg = m_f * r_fg
            Cg = mfg * a["cp_fg"]
            avail = m_f * lhv * 1000 * (1 - a["f_unburned"])
            def ex(T):
                Tk = T + 273.15
                qc = (SIGMA * F * A_c * (Tk**4 - Tw**4) + a["h_conv"] * A_c * (Tk - Tw)) / 1000
                qs = (T - a["t_soil0"]) / R_wall / 1000 * A_fb
                return avail - qc - qs - Cg * (T - a["t_soil0"]), qc, qs
            lo, hi = 100.0, 1600.0
            for _ in range(70):
                mid = (lo + hi) / 2
                (lo, hi) = (mid, hi) if ex(mid)[0] > 0 else (lo, mid)
            Tg = (lo + hi) / 2
            _, qc, qs = ex(Tg)
            eps_b = 1 - math.exp(-a["U_bank"] * A_bank / (Cg * 1000)) if A_bank > 0 else 0.0
            qb = Cg * (Tg - a["t_steam"]) * eps_b
            qbw = (Tg - a["t_soil0"]) / R_bwall / 1000 * A_bwall      # bank box wall loss, from the gas
            T1 = Tg - (qb + qbw) / Cg
            Cmin, Cmax = min(Cg, Cw), max(Cg, Cw)
            ntu = a["U_eco"] * A_eco / (Cmin * 1000)
            cr = Cmin / Cmax
            eps_e = (1 - math.exp(-ntu * (1 - cr))) / (1 - cr * math.exp(-ntu * (1 - cr)))
            qe = min(eps_e * Cmin * (T1 - a["t_feed"]), Cw * (a["t_eco_out"] - a["t_feed"]))
            return dict(Tg=Tg, qc=qc, qs=qs, qb=qb, qbw=qbw, T1=T1, qe=qe, mfg=mfg, Cg=Cg,
                        T_stack=T1 - qe / Cg, t_eo=a["t_feed"] + qe / Cw)

        lo, hi = 1e-4, 0.02
        for _ in range(70):
            mid = (lo + hi) / 2
            st_ = state(mid)
            need = r["Q_steam"] - st_["qe"]
            (lo, hi) = (lo, mid) if st_["qc"] + st_["qb"] > need else (mid, hi)
        m_f = (lo + hi) / 2
        st_ = state(m_f)
        Q_in = m_f * lhv * 1000
        Q_stack = st_["Cg"] * (st_["T_stack"] - a["t_soil0"])
        st_.update(lam=lam, F=F, m_f=m_f, wood_kg_h=m_f * 3600, Q_in=Q_in, eta=r["Q_steam"] / Q_in, A_c=A_c,
                   A_bank=A_bank, L_bank=L_bank_m, Q_shell=st_["qs"] + st_["qbw"], Q_stack=Q_stack, Q_unb=Q_in * a["f_unburned"],
                   r_fg=r_fg, t_skin=a["t_soil0"] + (st_["Tg"] - a["t_soil0"]) / R_wall / a["h_shell"],
                   closure=Q_in - (r["Q_steam"] + st_["qs"] + st_["qbw"] + Q_stack + Q_in * a["f_unburned"]),
                   V_coil=math.pi / 4 * (od - 2 * g["tube_wall"] / 1000)**2 * L * 1000,
                   V_bank=math.pi / 4 * ((g["bk_tube_od"] - 2 * g["bk_tube_wall"]) / 1000)**2 * L_bank_m * 1000)
        return st_

    L_bank = bank_length(geo)
    r["L_bank"] = L_bank
    design = fired(geo, a["lambda_ctl"], a["F_rad"], L_bank)
    r["design"] = design
    r["design_lam2"] = fired(geo, a["lambda"], a["F_rad"], L_bank)
    r["sens_bank"] = {(lam_, F_): fired(geo, lam_, F_, L_bank)["eta"] for lam_ in (1.5, 2.0, 2.5) for F_ in (0.25, 0.40, 0.60)}
    # options of the study (coil turns, firebox height, bank) at the controlled excess air
    g11 = dict(geo, coil_turns=11, fb_h=1000.0)
    r["study"] = [
        ("v0.3 design: 11 turns, 1000 mm firebox, no bank, lambda 2.0", fired(g11, 2.0, a["F_rad"], 0.0)),
        ("11 turns, 1000 mm firebox, no bank, dampers (lambda 1.5)", fired(g11, a["lambda_ctl"], a["F_rad"], 0.0)),
        (f"11 turns, 1000 mm firebox, {L_bank:.1f} m bank, lambda 1.5", fired(g11, a["lambda_ctl"], a["F_rad"], L_bank)),
        (f"Chosen: 10 turns, 960 mm firebox, {L_bank:.1f} m bank, lambda 1.5", design),
        (f"Chosen, dampers left open (lambda 2.0)", r["design_lam2"]),
        (f"9 turns, 920 mm firebox, {L_bank:.1f} m bank, lambda 1.5",
         fired(dict(geo, coil_turns=9, fb_h=920.0), a["lambda_ctl"], a["F_rad"], L_bank)),
    ]
    # efficiency needed for R4 (4 kg/m2 at 15 cm with two hoods)
    # (filled after the treatment rate is known, below)

    # stack temperature that would give 65 % at the base excess air and losses
    Q_in65 = r["Q_steam"] / 0.65
    m_f65 = Q_in65 / (lhv * 1000)
    allowed_stack = Q_in65 * (1 - a["f_unburned"]) - r["Q_steam"] - r["fb_v03"]["Q_shell"]
    r["T_stack_65"] = a["t_soil0"] + allowed_stack / (m_f65 * r["fb_v03"]["r_fg"] * a["cp_fg"])
    A_eco_avail = math.pi * geo["eco_tube_od"] / 1000 * geo["eco_tube_len"] / 1000
    r["A_eco_avail"] = A_eco_avail

    # Flue dew point at base excess air
    lam = a["lambda_ctl"]
    per_kg = {  # kmol per kg wet fuel
        "CO2": C / 100 * (1 - M) / 12,
        "H2O": (H / 100 * (1 - M) * 9 + M) / 18,
        "O2": (lam - 1) * o2_dry * (1 - M) / 32,
        "N2": lam * air_st * 0.768 / 28,
    }
    y_h2o = per_kg["H2O"] / sum(per_kg.values())
    r["y_h2o"] = y_h2o
    r["t_dew"] = sat_temp_from_pp(y_h2o * 101325)

    # the design case (bank and dampers) is what the media and the requirement table report
    fbd = dict(design)
    lmtd_e = ((design["T1"] - design["t_eo"]) - (design["T_stack"] - a["t_feed"])) / math.log(
        (design["T1"] - design["t_eo"]) / (design["T_stack"] - a["t_feed"]))
    fbd.update(A_eco_req=design["qe"] * 1000 / (a["U_eco"] * lmtd_e), lmtd=lmtd_e, T_after_eco=design["T_stack"])
    r["fb"] = fbd
    base = fbd
    # Treatment-level fuel figures
    r["wood_per_m2_15"] = base["wood_kg_h"] / r["rate15_2"]
    r["wood_per_m2_5"] = base["wood_kg_h"] / r["rate5_2"]
    r["wood_per_m2_15_lam2"] = r["design_lam2"]["wood_kg_h"] / r["rate15_2"]
    r["wood_per_m2_15_v03"] = r["fb_v03"]["wood_kg_h"] / r["rate15_2"]
    # natural draft against the damper openings
    rho_a, rho_f = 1.2, 1.2 * 288.15 / (a["t_flue_mean"] + 273.15)
    H_draft = (geo["chimney_top"] - DGEO["F"] - geo["grate_z"]) / 1000
    r["draft_pa"] = G * H_draft * (rho_a - rho_f)
    v_in = a["draft_cd"] * math.sqrt(2 * r["draft_pa"] / rho_a)
    r["air_need_mm2"] = {lam_: (r["design"]["m_f"] if lam_ == a["lambda_ctl"] else r["design_lam2"]["m_f"]) * lam_ * air_st / rho_a / v_in * 1e6
                         for lam_ in (a["lambda_ctl"], a["lambda"])}
    r["air_open_mm2"] = (geo["air_open"][0] * geo["air_open"][1], geo["air2_open"][0] * geo["air2_open"][1])
    r["H_draft"] = H_draft
    r["wood_per_m2_15_at65"] = r["bank"][2.0]["wood_kg_h"] / r["rate15_2"]
    r["eta_for_R4"] = r["Q_steam"] / (4.0 * r["rate15_2"] / 3600 * lhv * 1000)

    # ---------------------------------------------------- C. pressure drop, steam side
    Di = (geo["tube_od"] - 2 * geo["tube_wall"]) / 1000
    Ai = math.pi * Di**2 / 4
    Gm = m_s / Ai
    L_coil = math.hypot(math.pi * geo["coil_mean_d"] / 1000, geo["coil_pitch"] / 1000) * geo["coil_turns"]
    def f_darcy(Re):
        return 64 / Re if Re < 2300 else 0.316 * Re**-0.25
    Re_l, Re_g = Gm * Di / a["mu_l"], Gm * Di / a["mu_g"]
    dpdz_l = f_darcy(Re_l) / Di * Gm**2 / (2 * a["rho_l"])
    dpdz_g = f_darcy(Re_g) / Di * Gm**2 / (2 * a["rho_g"])
    n = 400
    msh = 0.0
    for i in range(n):   # Muller-Steinhagen and Heck, quality linear along the boiling length
        x = (i + 0.5) / n
        Gx = dpdz_l + 2 * (dpdz_g - dpdz_l) * x
        msh += (Gx * (1 - x)**(1 / 3) + dpdz_g * x**3) / n
    curv = max(1.0, (Re_g * (Di / 2 / (geo["coil_mean_d"] / 2000))**2)**0.05)     # Ito, turbulent helical coil
    f_boil = r["Q_coil"] and (m_s * (h_g - a["h_f100"])) / r["Q_coil"]              # fraction of coil length boiling
    dp_fric = msh * curv * L_coil * f_boil
    dp_acc = Gm**2 * (1 / a["rho_g"] - 1 / a["rho_l"])
    height = geo["coil_pitch"] * geo["coil_turns"] / 1000
    rho_h = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        rho_h += 1 / (x / a["rho_g"] + (1 - x) / a["rho_l"]) / n
    dp_grav = rho_h * G * height
    riser = (geo["header_z"] - DGEO["coil_top"]) / 1000            # coil top to the header (STR-DDR-003)
    dp_riser = f_darcy(Re_g) * curv / Di * Gm**2 / (2 * a["rho_g"]) * (riser + 0.6)
    dp_coil = dp_fric + dp_acc + dp_grav + dp_riser
    # evaporator bank upstream of the coil: subcooled water from the economizer, boiling to x_b
    Di_b = (geo["bk_tube_od"] - 2 * geo["bk_tube_wall"]) / 1000
    Gb = m_s / (math.pi * Di_b**2 / 4)
    d_ = r["design"]
    q_sub = m_s * a["cp_w"] * (a["t_steam"] - d_["t_eo"])
    x_b = max(0.0, (d_["qb"] - q_sub) / (m_s * a["h_fg"]))
    f_sub = min(1.0, q_sub / d_["qb"]) if d_["qb"] > 0 else 1.0
    Re_bl, Re_bg = Gb * Di_b / a["mu_l"], Gb * Di_b / a["mu_g"]
    gl = f_darcy(Re_bl) / Di_b * Gb**2 / (2 * a["rho_l"])
    gg = f_darcy(Re_bg) / Di_b * Gb**2 / (2 * a["rho_g"])
    msh_b = 0.0
    for i in range(n):
        x = x_b * (i + 0.5) / n
        Gx = gl + 2 * (gg - gl) * x
        msh_b += (Gx * (1 - x)**(1 / 3) + gg * x**3) / n
    curv_b = 1.10                                            # return bends of the serpentine, allowance
    dp_bank = curv_b * L_bank * (gl * f_sub + msh_b * (1 - f_sub)) + Gb**2 * x_b * (1 / a["rho_g"] - 1 / a["rho_l"])
    r.update(Gb=Gb, x_b=x_b, dp_bank=dp_bank, Di_b=Di_b)
    Ah = math.pi * a["hose_bore"]**2 / 4
    Gh = m_s / Ah
    vh = Gh / a["rho_g"]
    dp_hose = f_darcy(Gh * a["hose_bore"] / a["mu_g"]) / a["hose_bore"] * Gh**2 / (2 * a["rho_g"]) * a["hose_len"] \
        + a["K_hose_fittings"] * a["rho_g"] * vh**2 / 2
    p_hood = p_lift                     # the hood cannot hold more than its own weight per unit area
    p_header = dp_hose + a["dp_manifold"] + p_hood
    p_inlet = p_header + dp_coil + dp_bank          # bank inlet, the highest pressure on the steam side
    p_lift_ballast = (m_hood + a["ballast_kg"]) * G / A_hood
    r["p_header_ballast"] = p_header - p_hood + p_lift_ballast
    r["p_inlet_ballast"] = p_inlet - p_hood + p_lift_ballast
    p_seal = a["rho_l"] * G * DGEO["dip"] / 1000      # the overflow holds the annulus at the static mark: seal = dip leg depth
    r["p_seal_no_ovf"] = a["rho_l"] * G * geo["seal_depth"] / 1000
    r.update(Di=Di, Gm=Gm, v_coil=Gm / a["rho_g"], Re_g=Re_g, dpdz_g=dpdz_g, msh=msh, curv=curv, dp_fric=dp_fric,
             dp_acc=dp_acc, dp_grav=dp_grav, dp_riser=dp_riser, dp_coil=dp_coil, v_hose=vh, dp_hose=dp_hose,
             p_hood=p_hood, p_header=p_header, p_inlet=p_inlet, p_seal=p_seal, L_coil=L_coil)

    # ---------------------------------------------------- D. stored water, dry coil, relief valve
    V_coil = Ai * L_coil * 1000
    Di_e = (geo["eco_tube_od"] - 2 * geo["eco_tube_wall"]) / 1000
    V_eco = math.pi * Di_e**2 / 4 * geo["eco_tube_len"] / 1000 * 1000
    V_hdr = math.pi * ((geo["header_od"] - 4) / 1000)**2 / 4 * geo["header_len"] / 1000 * 1000
    V_bank = r["design"]["V_bank"]
    r.update(V_coil=V_coil, V_eco=V_eco, V_hdr=V_hdr, V_bank=V_bank, V_heated=V_coil + V_eco + V_hdr + V_bank)
    m_tube = a["rho_ss"] * math.pi / 4 * ((geo["tube_od"] / 1000)**2 - Di**2) * L_coil
    t_dry = base["Tg"]
    E_dry = m_tube * a["c_ss"] * (t_dry - 100) / 1000                               # MJ
    m_flash = E_dry * 1000 / (h_g - h_eco)
    flash_rate = m_flash / a["flash_s"] * 3600
    mult = flash_rate / a["steam_kg_h"]
    # back pressure in the pot head space while the full refeed flash leaves by the DN32 vent pipe
    Dv = (geo["vent_od"] - 2 * 3.56) / 1000
    L_v = (geo["vent_top"] - DGEO["pot_top"]) / 1000
    ref_flash = flash_rate / 3600
    vv = ref_flash / a["rho_g"] / (math.pi * Dv**2 / 4)
    r["dp_vent_flash"] = (f_darcy(ref_flash / (math.pi * Dv**2 / 4) * Dv / a["mu_g"]) * L_v / Dv + 1.5) * a["rho_g"] * vv**2 / 2
    r["p_trap"] = a["rho_l"] * G * geo["ovf_trap"] / 1000
    r["v_vent_flash"] = vv
    r.update(m_tube=m_tube, t_dry=t_dry, E_dry=E_dry, m_flash=m_flash, flash_rate=flash_rate, flash_mult=mult,
             dp_flash_coil=dp_coil * mult**2)
    hoop = lambda p: p * Di / (2 * geo["tube_wall"] / 1000)
    r.update(hoop_normal=hoop(p_inlet), hoop_shutoff=hoop(3e5))
    P1 = a["rv_set_psig"] * (1 + a["rv_accum"]) + 14.7
    def rv_area(kg_h):
        lb_h = kg_h * 2.2046
        a_in2 = lb_h / (51.5 * P1 * a["rv_K"])
        return a_in2 * 645.16
    r.update(rv_P1=P1, rv_area=rv_area(a["steam_kg_h"]), rv_d=math.sqrt(4 * rv_area(a["steam_kg_h"]) / math.pi),
             rv_area_flash=rv_area(flash_rate), rv_d_flash=math.sqrt(4 * rv_area(flash_rate) / math.pi))
    r["rv_set_bar"] = a["rv_set_psig"] * 0.0689476
    r["rv_rated_kg_h"] = a["rv_rated_lb_h"] / 2.2046

    # ---------------------------------------------------- E. mass, envelope, surfaces
    L, W, H_ = geo["fb_l"] / 1000, geo["fb_w"] / 1000, geo["fb_h"] / 1000
    A_fb = 2 * (L * W + L * H_ + W * H_)
    tl = geo["fb_lining_t"] / 1000
    V_lining = L * W * H_ - (L - 2 * tl) * (W - 2 * tl) * (H_ - 2 * tl)
    m_fb = A_fb * geo["fb_shell_t"] / 1000 * a["rho_st"] + V_lining * a["rho_lining"] + a["m_grate_door"]
    m_fb_castable = m_fb - V_lining * a["rho_lining"] + V_lining * a["rho_castable"]
    el, ew, eh = geo["eco_l"] / 1000, geo["eco_w"] / 1000, geo["eco_h"] / 1000
    m_eco = (2 * (el * ew + el * eh + ew * eh)) * 0.002 * a["rho_st"] + \
        a["rho_ss"] * math.pi / 4 * ((geo["eco_tube_od"] / 1000)**2 - Di_e**2) * geo["eco_tube_len"] / 1000
    ch_len = (geo["chimney_top"] - geo["cap_h"] + 50 - (DGEO["lid_top"])) / 1000
    m_ch = math.pi * geo["chimney_d"] / 1000 * ch_len * 0.0008 * a["rho_ss"] + 3.0
    m_water = geo["tank_volume_l"] * 1.0                             # cold water, 1 kg/L
    seal_water = math.pi / 4 * ((geo["seal_pot_od"] - 6) / 1000)**2 * (DGEO["water_line"] - DGEO["pot_bot"] - 6) / 1000 * 1000
    mass = {
        "Trailer (tare, assumed)": a["m_trailer"],
        "Firebox (shell, fiber lining, grate, door)": m_fb,
        "Monotube coil": m_tube,
        "Economizer": m_eco,
        "Chimney and cap": m_ch,
        "Header, seal pot, vent, relief valve": a["m_header_etc"],
        "Seal water": seal_water,
        "Tank, empty": a["m_tank_empty"],
        "Feed water, full tank": m_water,
        "Pump and battery": a["m_pump"] + a["m_battery"],
        "Steam hose": a["m_hose_per_m"] * geo["hose_len"] / 1000,
        f"Hoods, {int(geo['n_hoods'])} off": m_hood * geo["n_hoods"],
        "Instruments, alarms, safety kit": a["m_instr_safety"],
        "Supports and lines added for construction": a["m_construction"],
        "Evaporator bank (box, lining, tube, supports)": a["m_bank"],
    }
    r["mass"] = mass
    r["m_total"] = sum(mass.values())
    r["m_empty_tank"] = r["m_total"] - m_water - seal_water
    r["m_fb"], r["m_fb_castable"] = m_fb, m_fb_castable
    r["width"] = (geo["deck_w"] + 2 * (geo["wheel_w"] + geo["wheel_gap"])) / 1000
    r["chimney_top"] = geo["chimney_top"] / 1000
    r["t_hood_skin"] = a["t_soil0"] + U_hood * (a["t_steam"] - a["t_soil0"]) / a["h_out"]
    r["run_h"] = geo["tank_volume_l"] / a["steam_kg_h"]
    # hood handles carrying ballast: half the ballast on one handle, as one load at mid-span between standoffs
    hts, htt = geo["handle_tube"]
    I_h = (hts**4 - (hts - 2 * htt)**4) / 12                          # mm4
    Z_h = I_h / (hts / 2) * 1e-9                                       # m3
    F_side = a["ballast_kg"] / 2 * G * a["ballast_dyn"]
    span = 0.8
    r["handle_sigma"] = F_side * span / 4 / Z_h
    r["handle_sf"] = a["sy_steel"] / r["handle_sigma"]
    r["standoff_moment"] = F_side * 0.06                               # N m at the foot plate, 60 mm standoff
    r["p_lift_ballast"] = (m_hood + a["ballast_kg"]) * G / A_hood

    # ---------------------------------------------------- F. cost
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    r["bom"] = [(row["item"], float(row["qty"]), float(row["unit_cost_usd"])) for row in rows]
    r["cost"] = sum(q * c for _, q, c in r["bom"])

    # ---------------------------------------------------- G. requirement status
    def status(value, target, higher_is_better, band=0.05):
        ok = value >= target if higher_is_better else value <= target
        near = abs(value - target) <= band * target
        if ok:
            return "at risk" if near else "met"
        return "at risk" if near else "not met"
    fb = base
    req = [
        ("R1", "Soil at 70 C for 20 to 30 min at 15 cm over 80 % of footprint",
         f"front to {100*(0.15+delta):.1f} cm holds 70 C at 15 cm for {a['hold_min']:.0f} min (1D); edge and permeability untested",
         "70 C, 20 to 30 min", "not verifiable at TRL 3"),
        ("R2", "Treatment rate at 15 cm, two hoods", f"{r['rate15_2']:.2f} m2/h", "1.85 m2/h or more",
         status(r["rate15_2"], 1.85, True)),
        ("R2", "Treatment rate at 5 cm, two hoods", f"{r['rate5_2']:.2f} m2/h", "3.4 m2/h or more",
         status(r["rate5_2"], 3.4, True)),
        ("R3", "Steam output", f"30 kg/h with coil gas at {fb['Tg']:.0f} C, firing {fb['Q_in']:.1f} kW",
         "30 kg/h or more", "met"),
        ("R4", "Wood per m2 at 15 cm", f"{r['wood_per_m2_15']:.1f} kg/m2 with the bank and dampers ({r['wood_per_m2_15_lam2']:.1f} kg/m2 with the dampers open)",
         "4 kg/m2 or less", status(r["wood_per_m2_15"], 4.0, False)),
        ("R5", "Fuel to steam efficiency", f"{100*fb['eta']:.0f} % with the bank at lambda {a['lambda_ctl']} ({100*r['design_lam2']['eta']:.0f} % at lambda {a['lambda']})",
         "65 % or more", status(fb["eta"], 0.65, True)),
        ("R6", "Normal pressure at the header", f"{p_header/1e5:.3f} bar gauge",
         "0.1 bar gauge or less", status(p_header / 1e5, 0.10, False)),
        ("R6", "Normal pressure at the coil inlet (bank inlet)", f"{p_inlet/1e5:.3f} bar gauge",
         "0.15 bar gauge or less", status(p_inlet / 1e5, 0.15, False)),
        ("R7", "Water in heated section, flooded", f"{r['V_heated']:.1f} L", "8 L or less",
         status(r["V_heated"], 8.0, False)),
        ("R8", "Steaming per fill", f"{r['run_h']:.1f} h", "3 h or more", status(r["run_h"], 3.0, True)),
        ("R9", "Certified relief valve, set pressure and capacity",
         f"15 psi ({r['rv_set_bar']:.2f} bar) set; rated {r['rv_rated_kg_h']:.0f} kg/h against {flash_rate:.0f} kg/h refeed flash",
         "15 psi (1.03 bar) or less; capacity for the refeed flash",
         status(r["rv_rated_kg_h"], flash_rate, True)),
        ("R10", "Chimney, spark arrestor, handles", f"outlet {r['chimney_top']:.1f} m, 6 mm mesh, hood skin {r['t_hood_skin']:.0f} C",
         "2.2 m, 6 mm, 60 C", "met"),
        ("R11", "Mass as towed, tank and seal pot drained", f"{r['m_empty_tank']:.0f} kg ({r['m_total']:.0f} kg full)",
         "500 kg or less", status(r["m_empty_tank"], 500, False)),
        ("R11", "Overall width", f"{r['width']:.2f} m", "1.5 m or less", status(r["width"], 1.5, False, band=0.02)),
        ("R12", "Parts cost against the value-engineering target", f"${r['cost']:,.0f}", f"${a['budget_usd']:,.0f}",
         (f"over the target by ${r['cost'] - a['budget_usd']:,.0f}" if r["cost"] > a["budget_usd"]
          else f"under the target by ${a['budget_usd'] - r['cost']:,.0f}")),
    ]
    r["req"] = req

    # ---------------------------------------------------- report
    say("STR-CAL-001 SteamRoot sizing (TRL 3). All values are paper estimates.")
    say("\nA. Duty")
    say(f"  heat into water {r['Q_steam']:.2f} kW; coil {r['Q_coil']:.2f} kW; economizer {r['Q_eco']:.2f} kW "
        f"(ceiling at 100 C {r['Q_eco_max']:.2f} kW)")
    say("\nB. Soil heat and steam demand")
    say(f"  volumetric heat capacity {C_vol:.0f} kJ/(m3 K); diffusivity {alpha*1e6:.2f} mm2/s")
    say(f"  TRL 2 model (uniform 75 C, 60 % hood): {E_trl2:.1f} MJ/m2, {r['ms_trl2']:.1f} kg/m2")
    say(f"  hold overshoot below working depth: {100*delta:.2f} cm (interface {T_i:.1f} C, {a['hold_min']:.0f} min hold)")
    say(f"  hood: U {U_hood:.2f} W/(m2 K), wall loss {1000*P_hood_wall:.0f} W, storage {E_hood_store:.2f} MJ per setting, "
        f"mass {m_hood:.1f} kg, outer skin {r['t_hood_skin']:.0f} C")
    for name, d in (("15 cm", d15), ("5 cm", d5)):
        say(f"  {name}: soil {d['E_soil']:.1f} MJ/m2 + hood {d['E_hood']:.2f} MJ/m2; steam {d['ms']:.1f} kg/m2; "
            f"hood efficiency {100*d['eta_hood']:.0f} %; heat time {d['t_heat']:.1f} min per setting")
    for n in (1, 2, 3):
        say(f"  rate with {n} hood(s): 15 cm {r[f'rate15_{n}']:.2f} m2/h ({r[f'lim15_{n}']} limited); "
            f"5 cm {r[f'rate5_{n}']:.2f} m2/h ({r[f'lim5_{n}']} limited)")
    say(f"  steam-limited ceiling: 15 cm {A_hood/((d15['t_heat']+a['switch_min'])/60):.2f} m2/h; "
        f"5 cm {A_hood/((d5['t_heat']+a['switch_min'])/60):.2f} m2/h")
    say(f"  hood lift pressure {p_lift:.0f} Pa; superficial steam velocity {100*u_gas:.2f} cm/s")
    for k, dp in r["dp_soil"].items():
        say(f"  Darcy pressure through {100*(0.15+delta):.1f} cm of soil at k = {k:.0e} m2: {dp:,.0f} Pa")
    say("\nC. Fuel, combustion and efficiency")
    say(f"  wood HHV dry {hhv_dry:.2f} MJ/kg, LHV dry {lhv_dry:.2f} MJ/kg, LHV at {100*M:.0f} % moisture {lhv:.2f} MJ/kg")
    say(f"  stoichiometric air {air_st:.2f} kg/kg wet fuel; flue gas {fb['r_fg']:.1f} kg/kg at lambda {fb['lam']} (design, dampers set)")
    say(f"  coil tube length {fb['A_c']/(math.pi*geo['tube_od']/1000):.2f} m, area {fb['A_c']:.2f} m2")
    say(f"  firebox gas temperature {fb['Tg']:.0f} C; after economizer (stack) {fb['T_stack']:.0f} C")
    say(f"  firing {fb['Q_in']:.1f} kW; wood {fb['wood_kg_h']:.1f} kg/h; flue gas {1000*fb['mfg']:.1f} g/s")
    say(f"  losses: stack {fb['Q_stack']:.1f} kW, shell {fb['Q_shell']:.1f} kW, unburned {fb['Q_unb']:.1f} kW; "
        f"closure {fb['closure']:.3f} kW")
    say(f"  fuel to steam efficiency {100*fb['eta']:.1f} %; firebox skin {fb['t_skin']:.0f} C")
    say(f"  economizer: LMTD {fb['lmtd']:.0f} K, area needed {fb['A_eco_req']:.2f} m2, available {A_eco_avail:.2f} m2")
    say(f"  flue water vapor {100*y_h2o:.1f} % by volume; dew point {r['t_dew']:.0f} C")
    say(f"  stack temperature needed for 65 %: {r['T_stack_65']:.0f} C")
    say(f"  evaporator bank (model): {r['L_bank']:.2f} m of {geo['bk_tube_od']} x {geo['bk_tube_wall']} mm 316 tube, "
        f"{r['design']['A_bank']:.3f} m2, {r['V_bank'] if 'V_bank' in r else r['design']['V_bank']:.2f} L")
    say("  bank and firebox study (eta %, wood kg/h, kg/m2 at 15 cm, firebox gas C, bank kW, economizer kW, stack C, water L):")
    for name, d in r["study"]:
        g_turns = 11 if name.startswith(("v0.3", "11")) else (9 if name.startswith("9") else geo["coil_turns"])
        vol = d["V_coil"] + d["V_bank"] + 0.61 + 0.75
        say(f"    {name}: {100*d['eta']:.1f} / {d['wood_kg_h']:.1f} / {d['wood_kg_h']/r['rate15_2']:.2f} / {d['Tg']:.0f} / "
            f"{d['qb']:.2f} / {d['qe']:.2f} / {d['T_stack']:.0f} / {vol:.2f}")
    d = r["design"]
    say(f"  design: firebox gas {d['Tg']:.0f} C, coil {d['qc']:.2f} kW, bank {d['qb']:.2f} kW (gas to {d['T1']:.0f} C), "
        f"bank box wall {d['qbw']:.2f} kW, economizer {d['qe']:.2f} kW (water to {d['t_eo']:.0f} C), stack {d['T_stack']:.0f} C")
    say(f"  natural draft {r['draft_pa']:.1f} Pa over {r['H_draft']:.2f} m; air opening needed "
        + ", ".join(f"{v:,.0f} mm2 at lambda {k}" for k, v in r["air_need_mm2"].items())
        + f"; primary {r['air_open_mm2'][0]:,.0f} mm2 + secondary {r['air_open_mm2'][1]:,.0f} mm2")
    p = r["fb_preheat"]
    say(f"  with combustion air preheated by 135 K: efficiency {100*p['eta']:.1f} %, stack {p['T_stack']:.0f} C, "
        f"wood {p['wood_kg_h']:.1f} kg/h")
    for lam_, b in r["bank"].items():
        say(f"  target-seeking check (v0.3 method), lambda {lam_}, F {b['F']}: for {100*b['eta']:.0f} % firing {b['wood_kg_h']:.1f} kg/h wood, "
            f"firebox gas {b['Tg']:.0f} C, coil in firebox {b['q_fb']:.2f} kW; evaporator bank {b['Q_bank']:.2f} kW, "
            f"gas {b['Tg']:.0f} to {b['T1']:.0f} C, area {b['A_bank']:.2f} m2 ({b['L_bank']:.1f} m of 25.4 mm tube); "
            f"stack {b['T_stack']:.0f} C")
    say(f"  at 65 %, wood per m2 at 15 cm {r['wood_per_m2_15_at65']:.2f} kg/m2; efficiency needed for 4 kg/m2 "
        f"{100*r['eta_for_R4']:.1f} %")
    say("  sensitivity without the bank, efficiency % (rows lambda, columns F 0.25 / 0.40 / 0.60):")
    for lam_ in (1.5, 2.0, 2.5):
        say(f"    lambda {lam_}: " + " / ".join(f"{100*r['sens'][(lam_, F)]['eta']:.1f}" for F in (0.25, 0.40, 0.60)))
    say("  sensitivity with the bank (design), efficiency % (rows lambda, columns F 0.25 / 0.40 / 0.60):")
    for lam_ in (1.5, 2.0, 2.5):
        say(f"    lambda {lam_}: " + " / ".join(f"{100*r['sens_bank'][(lam_, F)]:.1f}" for F in (0.25, 0.40, 0.60)))
    say(f"  wood per m2 with two hoods: 15 cm {r['wood_per_m2_15']:.2f} kg/m2; 5 cm {r['wood_per_m2_5']:.2f} kg/m2")
    say("\nD. Steam-side pressure")
    say(f"  coil bore {1000*Di:.1f} mm; mass flux {Gm:.1f} kg/(m2 s); vapor velocity {r['v_coil']:.1f} m/s; Re vapor {Re_g:,.0f}")
    say(f"  all-vapor gradient {dpdz_g:.0f} Pa/m; two-phase mean {msh:.0f} Pa/m; curvature factor {curv:.2f}")
    say(f"  coil: friction {dp_fric:,.0f} Pa, acceleration {dp_acc:,.0f} Pa, gravity {dp_grav:,.0f} Pa, "
        f"outlet riser {dp_riser:,.0f} Pa; total {dp_coil:,.0f} Pa")
    say(f"  hose: velocity {vh:.1f} m/s, drop {dp_hose:,.0f} Pa; manifold {a['dp_manifold']:.0f} Pa; hood {p_hood:.0f} Pa")
    say(f"  header {p_header:,.0f} Pa ({p_header/1e5:.3f} bar); bank inlet {p_inlet:,.0f} Pa ({p_inlet/1e5:.3f} bar)")
    say(f"  evaporator bank: bore {1000*Di_b:.1f} mm, mass flux {Gb:.1f} kg/(m2 s), outlet quality {r['x_b']:.3f}, drop {dp_bank:,.0f} Pa")
    say(f"  water seal limit with the overflow {p_seal:,.0f} Pa ({p_seal/1e5:.3f} bar, dip leg {DGEO['dip']:.0f} mm); "
        f"without it {r['p_seal_no_ovf']/1e5:.3f} bar; margin at header {p_seal-p_header:,.0f} Pa")
    say(f"  with {a['ballast_kg']:.0f} kg ballast on the hood: lift {r['p_lift_ballast']:.0f} Pa, header {r['p_header_ballast']/1e5:.3f} bar, "
        f"bank inlet {r['p_inlet_ballast']/1e5:.3f} bar")
    say("\nE. Stored water, dry coil, relief valve")
    say(f"  water volumes: coil {V_coil:.2f} L, bank {V_bank:.2f} L, economizer {V_eco:.2f} L, header {V_hdr:.2f} L, total {r['V_heated']:.2f} L")
    say(f"  coil tube mass {m_tube:.1f} kg; dry at {t_dry:.0f} C stores {E_dry:.2f} MJ; flashes {m_flash:.2f} kg of water")
    say(f"  released over {a['flash_s']:.0f} s: {flash_rate:.0f} kg/h, {mult:.1f} times design flow; "
        f"coil drop would scale to about {r['dp_flash_coil']/1e5:.1f} bar")
    say(f"  hoop stress {r['hoop_normal']/1e6:.3f} MPa normal, {r['hoop_shutoff']/1e6:.1f} MPa at 3 bar pump shut-off "
        f"(316 yield at 700 C about {a['sy_316_700C']/1e6:.0f} MPa)")
    say(f"  relief valve set {a['rv_set_psig']:.0f} psi = {r['rv_set_bar']:.3f} bar; orifice for 30 kg/h "
        f"{r['rv_area']:.1f} mm2 ({r['rv_d']:.1f} mm); for the flash {r['rv_area_flash']:.0f} mm2 ({r['rv_d_flash']:.1f} mm)")
    say(f"  flash out of the vent pipe: {r['v_vent_flash']:.0f} m/s, back pressure in the pot head space {r['dp_vent_flash']:,.0f} Pa "
        f"against the {geo['ovf_trap']:.0f} mm overflow loop seal {r['p_trap']:,.0f} Pa")
    say(f"  rated capacity of the 3/4 in valve {a['rv_rated_lb_h']:.0f} lb/h = {r['rv_rated_kg_h']:.0f} kg/h; "
        f"margin over the flash {100*(r['rv_rated_kg_h']/flash_rate-1):.0f} %")
    say("\nF. Mass, envelope, cost")
    for k, v in mass.items():
        say(f"  {k:44s} {v:6.1f} kg")
    r["m_towed_no_hoods"] = r["m_empty_tank"] - m_hood * geo["n_hoods"]
    say(f"  towed without the hoods (they ride on a second vehicle for the prototype): {r['m_towed_no_hoods']:.0f} kg")
    say(f"  loaded mass {r['m_total']:.0f} kg; with tank and seal drained {r['m_empty_tank']:.0f} kg; "
        f"castable firebox would weigh {m_fb_castable:.0f} kg instead of {m_fb:.0f} kg")
    say(f"  hood handles with {a['ballast_kg']:.0f} kg ballast (load factor {a['ballast_dyn']:.0f}): bending {r['handle_sigma']/1e6:.1f} MPa, "
        f"safety factor {r['handle_sf']:.1f} on yield; standoff moment {r['standoff_moment']:.1f} N m")
    say(f"  width {r['width']:.2f} m; chimney outlet {r['chimney_top']:.2f} m; run per fill {r['run_h']:.2f} h")
    say(f"  BOM total ${r['cost']:,.2f}; value-engineering target ${a['budget_usd']:,.0f} "
        f"({'over' if r['cost'] > a['budget_usd'] else 'under'} by ${abs(a['budget_usd']-r['cost']):,.2f})")
    say(f"  water seal: dip leg {DGEO['dip']:.0f} mm below the static water line; without the overflow the annulus would rise "
        f"{DGEO['rise']:.0f} mm for an effective head of {DGEO['dip'] + DGEO['rise']:.0f} mm; the overflow holds it at {DGEO['dip']:.0f} mm")
    say("\nG. Requirement status")
    for rid, what, val, tgt, st in req:
        say(f"  {rid:4s} {st:24s} {what}: {val} (target {tgt})")
    r["report"] = "\n".join(out)
    if verbose:
        print(r["report"])
    return r


if __name__ == "__main__":
    run(verbose=True)
