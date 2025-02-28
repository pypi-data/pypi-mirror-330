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
-- Name: lab_o_method; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lab_o_method (
    code character varying(10) NOT NULL,
    description character varying(50),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date character varying DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.lab_o_method OWNER TO postgres;

--
-- Name: TABLE lab_o_method; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lab_o_method IS 'Reference table listing codes for overview lab codes (grouping of generic methods e.g Fire Assay, Aqua Regia, Four Acid digest)';

--
-- Name: COLUMN lab_o_method.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_o_method.code IS 'Code for the down hole event';

--
-- Name: COLUMN lab_o_method.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_o_method.description IS 'Description of the down hole event';

--
-- Name: COLUMN lab_o_method.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_o_method.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN lab_o_method.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_o_method.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: lab_o_method ref_lab_o_code_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_o_method
    ADD CONSTRAINT ref_lab_o_code_pkey PRIMARY KEY (code);

--
-- Name: lab_o_method ref_lab_o_code_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_o_method
    ADD CONSTRAINT ref_lab_o_code_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE lab_o_method; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lab_o_method TO fp;

--
-- PostgreSQL database dump complete
--
