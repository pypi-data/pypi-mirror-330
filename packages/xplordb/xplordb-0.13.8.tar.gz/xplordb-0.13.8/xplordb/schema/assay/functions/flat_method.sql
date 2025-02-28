----------------------------------------------------------------------------
-- xplordb
-- 
-- Copyright (C) 2022  Oslandia / OpenLog
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
-- 
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.
-- 
-- __authors__ = ["davidms"]
-- __contact__ = "geology@oslandia.com"
-- __date__ = "2022/02/02"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION assay.flat_method ()
    RETURNS TABLE (
        sample_id character varying,
        "Ag" text,
        "Al" text,
        "As" text,
        "Au" text,
        "Au Check" text,
        "Au-Rpt1" text,
        "Au-Rpt2" text,
        "Au-Rpt3" text,
        "Au-Rpt4" text,
        "Au1" text,
        "Au2" text,
        "Au3" text,
        "B" text,
        "Ba" text,
        "Be" text,
        "Bi" text,
        "Br" text,
        "Ca" text,
        "Cd" text,
        "Ce" text,
        "Co" text,
        "Cr" text,
        "Cs" text,
        "Cu" text,
        "Digest_Run" text,
        "Digest_Seq" text,
        "Dy" text,
        "Er" text,
        "Eu" text,
        "Fe" text,
        "Final pH" text,
        "Fusion_Run" text,
        "Fusion_Seq" text,
        "Ga" text,
        "Gd" text,
        "Ge" text,
        "Hf" text,
        "Hg" text,
        "Ho" text,
        "I" text,
        "In" text,
        "Instr_Run" text,
        "Instr_Seq" text,
        "K" text,
        "LOI 1000" text,
        "La" text,
        "Li" text,
        "Lu" text,
        "Mg" text,
        "Mn" text,
        "Mo" text,
        "Na" text,
        "Nb" text,
        "Nd" text,
        "Ni" text,
        "P" text,
        "Pass2mm" text,
        "Pass6mm" text,
        "Pass75um" text,
        "Pb" text,
        "Pb 206" text,
        "Pb 207" text,
        "Pb 208" text,
        "Pd" text,
        "Pr" text,
        "Pt" text,
        "ROAST" text,
        "Rb" text,
        "Re" text,
        "Recvd Wt." text,
        "Rmnd2mm" text,
        "Rmnd6mm" text,
        "Rmnd75um" text,
        "S" text,
        "Sb" text,
        "Sc" text,
        "Se" text,
        "Sm" text,
        "Sn" text,
        "Sr" text,
        "Ta" text,
        "Tb" text,
        "Te" text,
        "Th" text,
        "Ti" text,
        "Tl" text,
        "Tm" text,
        "U" text,
        "V" text,
        "W" text,
        "WO3" text,
        "WT. + Frac Entire" text,
        "WT. - Frac Entire" text,
        "WT. SAMPLE" text,
        "WT. Total" text,
        "Y" text,
        "Yb" text,
        "Zn" text,
        "Zr" text,
        p75um text,
        u text)
    LANGUAGE sql
    AS $function$
    WITH js_r AS (
        SELECT
            assay.sample_id,
            cast(json_object_agg(element, lab_method) AS jsonb) AS r
        FROM
            assay.assay
        WHERE
            NOT EXISTS (
                SELECT
                    NULL
                FROM
                    assay.flat_method af
                WHERE
                    assay.sample_id = af.sample_id)
                AND preferred = 1
            GROUP BY
                assay.sample_id
)
    SELECT
        sample_id,
        (r ->> 'Ag')::text AS "Ag",
        (r ->> 'Al')::text AS "Al",
        (r ->> 'As')::text AS "As",
        (r ->> 'Au')::text AS "Au",
        (r ->> 'Au
  Check')::text AS "Au Check",
        (r ->> 'Au-Rpt1')::text AS "Au-Rpt1",
        (r ->> 'Au-Rpt2')::text AS "Au-Rpt2",
        (r ->> 'Au-Rpt3')::text AS "Au-Rpt3",
        (r ->> 'Au-Rpt4')::text AS "Au-Rpt4",
        (r ->> 'Au1')::text AS "Au1",
        (r ->> 'Au2')::text AS "Au2",
        (r ->> 'Au3')::text AS "Au3",
        (r ->> 'B')::text AS "B",
        (r ->> 'Ba')::text AS "Ba",
        (r ->> 'Be')::text AS "Be",
        (r ->> 'Bi')::text AS "Bi",
        (r ->> 'Br')::text AS "Br",
        (r ->> 'Ca')::text AS "Ca",
        (r ->> 'Cd')::text AS "Cd",
        (r ->> 'Ce')::text AS "Ce",
        (r ->> 'Co')::text AS "Co",
        (r ->> 'Cr')::text AS "Cr",
        (r ->> 'Cs')::text AS "Cs",
        (r ->> 'Cu')::text AS "Cu",
        (r ->> 'Digest_Run')::text AS "Digest_Run",
        (r ->> 'Digest_Seq')::text AS "Digest_Seq",
        (r ->> 'Dy')::text AS "Dy",
        (r ->> 'Er')::text AS "Er",
        (r ->> 'Eu')::text AS "Eu",
        (r ->> 'Fe')::text AS "Fe",
        (r ->> 'Final pH')::text AS "Final pH",
        (r ->> 'Fusion_Run')::text AS "Fusion_Run",
        (r ->> 'Fusion_Seq')::text AS "Fusion_Seq",
        (r ->> 'Ga')::text AS "Ga",
        (r ->> 'Gd')::text AS "Gd",
        (r ->> 'Ge')::text AS "Ge",
        (r ->> 'Hf')::text AS "Hf",
        (r ->> 'Hg')::text AS "Hg",
        (r ->> 'Ho')::text AS "Ho",
        (r ->> 'I')::text AS "I",
        (r ->> 'In')::text AS "In",
        (r ->> 'Instr_Run')::text AS "Instr_Run",
        (r ->> 'Instr_Seq')::text AS "Instr_Seq",
        (r ->> 'K')::text AS "K",
        (r ->> 'LOI 1000')::text AS "LOI 1000",
        (r ->> 'La')::text AS "La",
        (r ->> 'Li')::text AS "Li",
        (r ->> 'Lu')::text AS "Lu",
        (r ->> 'Mg')::text AS "Mg",
        (r ->> 'Mn')::text AS "Mn",
        (r ->> 'Mo')::text AS "Mo",
        (r ->> 'Na')::text AS "Na",
        (r ->> 'Nb')::text AS "Nb",
        (r ->> 'Nd')::text AS "Nd",
        (r ->> 'Ni')::text AS "Ni",
        (r ->> 'P')::text AS "P",
        (r ->> 'Pass2mm')::text AS "Pass2mm",
        (r ->> 'Pass6mm')::text AS "Pass6mm",
        (r ->> 'Pass75um')::text AS "Pass75um",
        (r ->> 'Pb')::text AS "Pb",
        (r ->> 'Pb
  206')::text AS "Pb 206",
        (r ->> 'Pb 207')::text AS "Pb 207",
        (r ->> 'Pb 208')::text AS "Pb 208",
        (r ->> 'Pd')::text AS "Pd",
        (r ->> 'Pr')::text AS "Pr",
        (r ->> 'Pt')::text AS "Pt",
        (r ->> 'ROAST')::text AS "ROAST",
        (r ->> 'Rb')::text AS "Rb",
        (r ->> 'Re')::text AS "Re",
        (r ->> 'Recvd Wt.')::text AS "Recvd
  Wt.",
        (r ->> 'Rmnd2mm')::text AS "Rmnd2mm",
        (r ->> 'Rmnd6mm')::text AS "Rmnd6mm",
        (r ->> 'Rmnd75um')::text AS "Rmnd75um",
        (r ->> 'S')::text AS "S",
        (r ->> 'Sb')::text AS "Sb",
        (r ->> 'Sc')::text AS "Sc",
        (r ->> 'Se')::text AS "Se",
        (r ->> 'Sm')::text AS "Sm",
        (r ->> 'Sn')::text AS "Sn",
        (r ->> 'Sr')::text AS "Sr",
        (r ->> 'Ta')::text AS "Ta",
        (r ->> 'Tb')::text AS "Tb",
        (r ->> 'Te')::text AS "Te",
        (r ->> 'Th')::text AS "Th",
        (r ->> 'Ti')::text AS "Ti",
        (r ->> 'Tl')::text AS "Tl",
        (r ->> 'Tm')::text AS "Tm",
        (r ->> 'U')::text AS "U",
        (r ->> 'V')::text AS "V",
        (r ->> 'W')::text AS "W",
        (r ->> 'WO3')::text AS "WO3",
        (r ->> 'WT. + Frac Entire')::text AS "WT. + Frac Entire",
        (r ->> 'WT. -
  Frac Entire')::text AS "WT. - Frac Entire",
        (r ->> 'WT. SAMPLE')::text AS "WT. SAMPLE",
        (r ->> 'WT. Total')::text AS "WT. Total",
        (r ->> 'Y')::text AS "Y",
        (r ->> 'Yb')::text AS "Yb",
        (r ->> 'Zn')::text AS "Zn",
        (r ->> 'Zr')::text AS "Zr",
        (r ->> 'p75um')::text AS "p75um",
        (r ->> 'u')::text AS "u"
    FROM
        js_r
$function$
