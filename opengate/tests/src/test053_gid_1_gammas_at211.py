#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test053_gid_helpers1 import *
from box import BoxList

paths = gate.get_default_test_paths(__file__, "", output_folder="test053")

nuclide = gate.get_nuclide_from_name("at211")
# get all daughters
daughters = gate.get_nuclide_progeny(nuclide)
print(f"Found {len(daughters)} radionuclides")

# reference from http://www.lnhb.fr/nuclear-data/module-lara/
ref = [
    {"energy": 687.2, "intensity": 0.245, "ion": "At-211"},
    # {"energy": 569.65, "intensity": 0.534, "ion": "Po-211"},
    {"energy": 897.8, "intensity": 0.507, "ion": "Po-211"},
    # {"energy": 569.698, "intensity": 97.76, "ion": "Bi-207"},
    {"energy": 1063.656, "intensity": 74.58, "ion": "Bi-207"},
]
ref = BoxList(ref)

# GammaFromIonDecayExtractor as list
keV = gate.g4_units("keV")
all_ene = []
all_w = []
is_ok = True
for d in daughters:
    ge = gate.GammaIonDecayIsomericTransitionExtractor(
        d.nuclide.Z, d.nuclide.A, verbose=False
    )
    ge.extract()

    # print
    g_ene = []
    g_w = []
    print(
        f"{d.nuclide.nuclide}  intensity={d.intensity * 100:.2f}%  ->  {len(ge.gammas)} gamma lines"
    )
    for g in ge.gammas:
        print(
            f"\t {g.transition_energy / keV:.4f} keV \t-> {g.final_intensity * 100:.4f} % "
        )
        g_ene.append(g.transition_energy)
        g_w.append(g.final_intensity)

        tol = 5
        for r in ref:
            if r.ion == d.nuclide.nuclide:
                e = g.transition_energy / keV
                if np.fabs(e - r.energy) < 1:
                    diff = (
                        np.fabs(r.intensity - g.final_intensity * 100)
                        / r.intensity
                        * 100
                    )
                    ok = diff < tol
                    gate.print_test(
                        ok,
                        f"\t ==> {e:.2f} keV   ref={r.intensity:.2f}% "
                        f" vs comp={g.final_intensity * 100:.2f}% "
                        f" -> {diff:.2f}%   (tol {tol:.2f}%)",
                    )
                    is_ok = ok and is_ok

    # add to list and take intensity into account
    g_ene = np.array(g_ene)
    g_w = np.array(g_w) * d.intensity
    all_ene.append(g_ene / keV)
    all_w.append(g_w)

gate.test_ok(is_ok)
