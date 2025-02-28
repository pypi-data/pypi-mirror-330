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
-- Name: lab_method_code; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lab_method_code (
    lab_method_code character varying(20) NOT NULL
);

ALTER TABLE ref.lab_method_code OWNER TO postgres;

--
-- Name: TABLE lab_method_code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lab_method_code IS 'Reference table listing laboratory method codes, this is a aggregated table of dh.ref_lab_method to obtain unique codes';

--
-- Name: COLUMN lab_method_code.lab_method_code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method_code.lab_method_code IS 'Code for the lab method';

--
-- Name: lab_method_code lab_method_code_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method_code
    ADD CONSTRAINT lab_method_code_pkey PRIMARY KEY (lab_method_code);

--
-- Name: lab_method_code ref_lab_method_code_lab_method_code_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method_code
    ADD CONSTRAINT ref_lab_method_code_lab_method_code_key UNIQUE (lab_method_code);

--
-- Name: TABLE lab_method_code; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lab_method_code TO fp;

--
-- PostgreSQL database dump complete
--
