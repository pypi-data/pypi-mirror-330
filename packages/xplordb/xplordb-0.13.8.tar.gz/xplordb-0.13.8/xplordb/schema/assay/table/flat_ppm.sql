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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: flat_ppm; Type: TABLE; Schema: assay; Owner: postgres
--
CREATE TABLE assay.flat_ppm (
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
    u real
);

ALTER TABLE assay.flat_ppm OWNER TO postgres;

--
-- Name: TABLE flat_ppm; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON TABLE assay.flat_ppm IS 'Flat table of assay results in parts per million(ppm). Updated with assay.flat_ppm function e.g. insert into assay.flat_ppm select * from assay.flat_ppm()';

--
-- PostgreSQL database dump complete
--
