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

CREATE OR REPLACE FUNCTION assay.flat_ppm ()
    RETURNS TABLE (
        sample_id character varying,
        "Ag" real,
        "Al" real,
        "As" real,
        "Au" real,
        "Au Check" real,
        "Au-Rpt1" real,
        "Au-Rpt2" real,
        "Au-Rpt3" real,
        "Au-Rpt4" real,
        "Au1" real,
        "Au2" real,
        "Au3" real,
        "B" real,
        "Ba" real,
        "Be" real,
        "Bi" real,
        "Br" real,
        "Ca" real,
        "Cd" real,
        "Ce" real,
        "Co" real,
        "Cr" real,
        "Cs" real,
        "Cu" real,
        "Digest_Run" real,
        "Digest_Seq" real,
        "Dy" real,
        "Er" real,
        "Eu" real,
        "Fe" real,
        "Final pH" real,
        "Fusion_Run" real,
        "Fusion_Seq" real,
        "Ga" real,
        "Gd" real,
        "Ge" real,
        "Hf" real,
        "Hg" real,
        "Ho" real,
        "I" real,
        "In" real,
        "Instr_Run" real,
        "Instr_Seq" real,
        "K" real,
        "LOI 1000" real,
        "La" real,
        "Li" real,
        "Lu" real,
        "Mg" real,
        "Mn" real,
        "Mo" real,
        "Na" real,
        "Nb" real,
        "Nd" real,
        "Ni" real,
        "P" real,
        "Pass2mm" real,
        "Pass6mm" real,
        "Pass75um" real,
        "Pb" real,
        "Pb 206" real,
        "Pb 207" real,
        "Pb 208" real,
        "Pd" real,
        "Pr" real,
        "Pt" real,
        "ROAST" real,
        "Rb" real,
        "Re" real,
        "Recvd Wt." real,
        "Rmnd2mm" real,
        "Rmnd6mm" real,
        "Rmnd75um" real,
        "S" real,
        "Sb" real,
        "Sc" real,
        "Se" real,
        "Sm" real,
        "Sn" real,
        "Sr" real,
        "Ta" real,
        "Tb" real,
        "Te" real,
        "Th" real,
        "Ti" real,
        "Tl" real,
        "Tm" real,
        "U" real,
        "V" real,
        "W" real,
        "WO3" real,
        "WT. + Frac Entire" real,
        "WT. - Frac Entire" real,
        "WT. SAMPLE" real,
        "WT. Total" real,
        "Y" real,
        "Yb" real,
        "Zn" real,
        "Zr" real,
        p75um real,
        u real)
    LANGUAGE sql
    AS $function$
    WITH js_r AS (
        SELECT
            assay.sample_id,
            cast(json_object_agg(element, CASE WHEN assay.unit::text = 'ppm'::text THEN
                        lower(arr)::real
                    WHEN assay.unit::text = 'ppb'::text THEN
                        lower(arr)::real / 1000::real
                    WHEN assay.unit::text = 'pct'::text THEN
                        lower(arr)::real * 10000::real
                    WHEN assay.unit::text = '%'::text
                        AND assay.lab_element::text != 'Pass75um'
                        AND assay.lab_element::text != 'Rmnd2mm'
                        AND assay.lab_element::text != 'Pass2mm'
                        AND assay.lab_element::text != 'Pass6mm'
                        AND assay.lab_element::text != 'LOI 1000'
                        AND assay.lab_element::text != 'Rmnd75um'
                        AND assay.lab_element::text != 'Rmnd6mm'
                        AND assay.lab_element::text IS NOT NULL THEN
                        lower(arr)::real * 10000::real
                    ELSE
                        lower(arr)::real
                    END) AS jsonb) AS r
        FROM
            assay.assay
        WHERE
            NOT EXISTS (
                SELECT
                    NULL
                FROM
                    assay.flat_ppm af
                WHERE
                    assay.sample_id = af.sample_id)
                AND preferred = 1
                AND isempty(arr) != 't'
                AND lower(arr) IS NOT NULL
            GROUP BY
                assay.sample_id
)
    SELECT
        sample_id,
        (r -> 'Ag')::text::real AS "Ag",
        (r -> 'Al')::text::real AS "Al",
        (r -> 'As')::text::real AS "As",
        (r -> 'Au')::text::real AS "Au",
        (r -> 'Au Check')::text::real AS "Au Check",
        (r -> 'Au-Rpt1')::text::real AS "Au-Rpt1",
        (r -> 'Au-Rpt2')::text::real AS "Au-Rpt2",
        (r -> 'Au-Rpt3')::text::real AS "Au-Rpt3",
        (r -> 'Au-Rpt4')::text::real AS "Au-Rpt4",
        (r -> 'Au1')::text::real AS "Au1",
        (r -> 'Au2')::text::real AS "Au2",
        (r -> 'Au3')::text::real AS "Au3",
        (r -> 'B')::text::real AS "B",
        (r -> 'Ba')::text::real AS "Ba",
        (r -> 'Be')::text::real AS "Be",
        (r -> 'Bi')::text::real AS "Bi",
        (r -> 'Br')::text::real AS "Br",
        (r -> 'Ca')::text::real AS "Ca",
        (r -> 'Cd')::text::real AS "Cd",
        (r -> 'Ce')::text::real AS "Ce",
        (r -> 'Co')::text::real AS "Co",
        (r -> 'Cr')::text::real AS "Cr",
        (r -> 'Cs')::text::real AS "Cs",
        (r -> 'Cu')::text::real AS "Cu",
        (r -> 'Digest_Run')::text::real AS "Digest_Run",
        (r -> 'Digest_Seq')::text::real AS "Digest_Seq",
        (r -> 'Dy')::text::real AS "Dy",
        (r -> 'Er')::text::real AS "Er",
        (r -> 'Eu')::text::real AS "Eu",
        (r -> 'Fe')::text::real AS "Fe",
        (r -> 'Final pH')::text::real AS "Final pH",
        (r -> 'Fusion_Run')::text::real AS "Fusion_Run",
        (r -> 'Fusion_Seq')::text::real AS "Fusion_Seq",
        (r -> 'Ga')::text::real AS "Ga",
        (r -> 'Gd')::text::real AS "Gd",
        (r -> 'Ge')::text::real AS "Ge",
        (r -> 'Hf')::text::real AS "Hf",
        (r -> 'Hg')::text::real AS "Hg",
        (r -> 'Ho')::text::real AS "Ho",
        (r -> 'I')::text::real AS "I",
        (r -> 'In')::text::real AS "In",
        (r -> 'Instr_Run')::text::real AS "Instr_Run",
        (r -> 'Instr_Seq')::text::real AS "Instr_Seq",
        (r -> 'K')::text::real AS "K",
        (r -> 'LOI 1000')::text::real AS "LOI 1000",
        (r -> 'La')::text::real AS "La",
        (r -> 'Li')::text::real AS "Li",
        (r -> 'Lu')::text::real AS "Lu",
        (r -> 'Mg')::text::real AS "Mg",
        (r -> 'Mn')::text::real AS "Mn",
        (r -> 'Mo')::text::real AS "Mo",
        (r -> 'Na')::text::real AS "Na",
        (r -> 'Nb')::text::real AS "Nb",
        (r -> 'Nd')::text::real AS "Nd",
        (r -> 'Ni')::text::real AS "Ni",
        (r -> 'P')::text::real AS "P",
        (r -> 'Pass2mm')::text::real AS "Pass2mm",
        (r -> 'Pass6mm')::text::real AS "Pass6mm",
        (r -> 'Pass75um')::text::real AS "Pass75um",
        (r -> 'Pb')::text::real AS "Pb",
        (r -> 'Pb 206')::text::real AS "Pb 206",
        (r -> 'Pb 207')::text::real AS "Pb 207",
        (r -> 'Pb 208')::text::real AS "Pb 208",
        (r -> 'Pd')::text::real AS "Pd",
        (r -> 'Pr')::text::real AS "Pr",
        (r -> 'Pt')::text::real AS "Pt",
        (r -> 'ROAST')::text::real AS "ROAST",
        (r -> 'Rb')::text::real AS "Rb",
        (r -> 'Re')::text::real AS "Re",
        (r -> 'Recvd Wt.')::text::real AS "Recvd Wt.",
        (r -> 'Rmnd2mm')::text::real AS "Rmnd2mm",
        (r -> 'Rmnd6mm')::text::real AS "Rmnd6mm",
        (r -> 'Rmnd75um')::text::real AS "Rmnd75um",
        (r -> 'S')::text::real AS "S",
        (r -> 'Sb')::text::real AS "Sb",
        (r -> 'Sc')::text::real AS "Sc",
        (r -> 'Se')::text::real AS "Se",
        (r -> 'Sm')::text::real AS "Sm",
        (r -> 'Sn')::text::real AS "Sn",
        (r -> 'Sr')::text::real AS "Sr",
        (r -> 'Ta')::text::real AS "Ta",
        (r -> 'Tb')::text::real AS "Tb",
        (r -> 'Te')::text::real AS "Te",
        (r -> 'Th')::text::real AS "Th",
        (r -> 'Ti')::text::real AS "Ti",
        (r -> 'Tl')::text::real AS "Tl",
        (r -> 'Tm')::text::real AS "Tm",
        (r -> 'U')::text::real AS "U",
        (r -> 'V')::text::real AS "V",
        (r -> 'W')::text::real AS "W",
        (r -> 'WO3')::text::real AS "WO3",
        (r -> 'WT. + Frac Entire')::text::real AS "WT. + Frac Entire",
        (r -> 'WT. - Frac Entire')::text::real AS "WT. - Frac Entire",
        (r -> 'WT. SAMPLE')::text::real AS "WT. SAMPLE",
        (r -> 'WT. Total')::text::real AS "WT. Total",
        (r -> 'Y')::text::real AS "Y",
        (r -> 'Yb')::text::real AS "Yb",
        (r -> 'Zn')::text::real AS "Zn",
        (r -> 'Zr')::text::real AS "Zr",
        (r -> 'p75um')::text::real AS "p75um",
        (r -> 'u')::text::real AS "u"
    FROM
        js_r;
$function$
