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
-- Name: sample_class; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.sample_class (
    code character varying(16) NOT NULL,
    description character varying(200),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date date DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.sample_class OWNER TO postgres;

--
-- Name: TABLE sample_class; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.sample_class IS 'Reference table listing sample classes for the dh_sample table';

--
-- Name: COLUMN sample_class.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.sample_class.code IS 'Code for the sample class';

--
-- Name: COLUMN sample_class.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.sample_class.description IS 'Description of the sample class';

--
-- Name: COLUMN sample_class.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.sample_class.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample_class.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.sample_class.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sample_class ref_class_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.sample_class
    ADD CONSTRAINT ref_class_pkey PRIMARY KEY (code);

--
-- Name: sample_class ref_sample_class_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.sample_class
    ADD CONSTRAINT ref_sample_class_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
