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
-- Name: rl_method; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.rl_method (
    code character varying(50) NOT NULL,
    description character varying(50),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date date DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    file_location character varying
);

ALTER TABLE ref.rl_method OWNER TO postgres;

--
-- Name: TABLE rl_method; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.rl_method IS 'Reference table listing the elevation (rl) determination method codes. Only use if different to survey method.';

--
-- Name: COLUMN rl_method.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.rl_method.code IS 'Code for the elevation (rl) determination method';

--
-- Name: COLUMN rl_method.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.rl_method.description IS 'Description of the elevation (rl) determination method code';

--
-- Name: COLUMN rl_method.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.rl_method.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN rl_method.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.rl_method.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: rl_method ref_hole_rl_survey_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.rl_method
    ADD CONSTRAINT ref_hole_rl_survey_pkey PRIMARY KEY (code);

--
-- Name: rl_method ref_rl_method_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.rl_method
    ADD CONSTRAINT ref_rl_method_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
