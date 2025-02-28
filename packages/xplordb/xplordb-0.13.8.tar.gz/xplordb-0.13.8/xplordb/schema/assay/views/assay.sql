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

--
-- PostgreSQL database dump
--
-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
SET statement_timeout = 0;

SET lock_timeout = 0;

SET idle_in_transaction_session_timeout = 0;

SET client_encoding = 'UTF8';

SET standard_conforming_strings = ON;

SELECT
    pg_catalog.set_config('search_path', '', FALSE);

SET check_function_bodies = FALSE;

SET xmloption = content;

SET client_min_messages = warning;

SET row_security = OFF;

--
-- Name: assay; Type: VIEW; Schema: dh; Owner: postgres
--
CREATE VIEW dh.assay AS
SELECT
    row_number() OVER () AS row_number,
    s.data_set,
    s.sample_id,
    s.hole_id,
    s.from_m,
    s.to_m,
    s.weight_total,
    s.hole_diameter,
    s.sample_type,
    s.sample_method,
    s.company,
    s.date_sampled,
    s.sampled_by,
    s.comment,
    s.historic_sample_id,
    s.data_source,
    s.loaded_by,
    s.load_date,
    s.class,
    a. "Ag",
    a. "Al",
    a. "As",
    a. "Au",
    a. "Au Check",
    a. "Au-Rpt1",
    a. "Au-Rpt2",
    a. "Au-Rpt3",
    a. "Au-Rpt4",
    a. "Au1",
    a. "Au2",
    a. "Au3",
    a. "B",
    a. "Ba",
    a. "Be",
    a. "Bi",
    a. "Br",
    a. "Ca",
    a. "Cd",
    a. "Ce",
    a. "Co",
    a. "Cr",
    a. "Cs",
    a. "Cu",
    a. "Digest_Run",
    a. "Digest_Seq",
    a. "Dy",
    a. "Er",
    a. "Eu",
    a. "Fe",
    a. "Final pH",
    a. "Fusion_Run",
    a. "Fusion_Seq",
    a. "Ga",
    a. "Gd",
    a. "Ge",
    a. "Hf",
    a. "Hg",
    a. "Ho",
    a. "I",
    a. "In",
    a. "Instr_Run",
    a. "Instr_Seq",
    a. "K",
    a. "LOI 1000",
    a. "La",
    a. "Li",
    a. "Lu",
    a. "Mg",
    a. "Mn",
    a. "Mo",
    a. "Na",
    a. "Nb",
    a. "Nd",
    a. "Ni",
    a. "P",
    a. "Pass2mm",
    a. "Pass6mm",
    a. "Pass75um",
    a. "Pb",
    a. "Pb 206",
    a. "Pb 207",
    a. "Pb 208",
    a. "Pd",
    a. "Pr",
    a. "Pt",
    a. "ROAST",
    a. "Rb",
    a. "Re",
    a. "Recvd Wt.",
    a. "Rmnd2mm",
    a. "Rmnd6mm",
    a. "Rmnd75um",
    a. "S",
    a. "Sb",
    a. "Sc",
    a. "Se",
    a. "Sm",
    a. "Sn",
    a. "Sr",
    a. "Ta",
    a. "Tb",
    a. "Te",
    a. "Th",
    a. "Ti",
    a. "Tl",
    a. "Tm",
    a. "U",
    a. "V",
    a. "W",
    a. "WO3",
    a. "WT. + Frac Entire",
    a. "WT. - Frac Entire",
    a. "WT. SAMPLE",
    a. "WT. Total",
    a. "Y",
    a. "Yb",
    a. "Zn",
    a. "Zr",
    a.p75um,
    a.u,
    s.geom_trace
FROM (dh.sample s
    LEFT JOIN assay.flat_ppm a ON (((s.sample_id)::text = (a.sample_id)::text)))
WHERE (((s.class)::text = 'primary'::text)
    OR ((s.class)::text = 'primary_au'::text))
ORDER BY
    s.hole_id,
    s.from_m;

ALTER TABLE dh.assay OWNER TO postgres;

--
-- PostgreSQL database dump complete
--
