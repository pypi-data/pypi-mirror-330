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
-- Name: flat_method; Type: TABLE; Schema: assay; Owner: postgres
--
CREATE TABLE assay.flat_method (
    sample_id character varying(25),
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
    "Recvd
  Wt." text,
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
    u text
);

ALTER TABLE assay.flat_method OWNER TO postgres;

--
-- Name: TABLE flat_method; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON TABLE assay.flat_method IS 'Flat table of lab method for each sample. Updated with assay.flat_method function e.g. insert into assay.flat_method select * from assay.flat_method()';

--
-- PostgreSQL database dump complete
--
