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
-- Name: qc_type; Type: TABLE; Schema: qa; Owner: postgres
--
CREATE TABLE qa.qc_type (
    code character varying(10) NOT NULL,
    description character varying(50) NOT NULL,
    lab character varying(50) NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL
);

ALTER TABLE qa.qc_type OWNER TO postgres;

--
-- Name: TABLE qc_type; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON TABLE qa.qc_type IS 'Reference table listing quality control types';

--
-- Name: COLUMN qc_type.code; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.qc_type.code IS 'Code for the quality control type';

--
-- Name: COLUMN qc_type.description; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.qc_type.description IS 'Description of the quality control type';

--
-- Name: COLUMN qc_type.lab; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.qc_type.lab IS 'Code for the laboratory that this quality control type relates to, see ref.lab';

--
-- Name: COLUMN qc_type.load_date; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.qc_type.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN qc_type.loaded_by; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.qc_type.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: qc_type qc_ref_qc_type_code_key; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.qc_type
    ADD CONSTRAINT qc_ref_qc_type_code_key UNIQUE (code);

--
-- Name: qc_type qc_type_pkey; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.qc_type
    ADD CONSTRAINT qc_type_pkey PRIMARY KEY (code);

--
-- Name: qc_type qc_ref_qc_type_loaded_by_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.qc_type
    ADD CONSTRAINT qc_ref_qc_type_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
