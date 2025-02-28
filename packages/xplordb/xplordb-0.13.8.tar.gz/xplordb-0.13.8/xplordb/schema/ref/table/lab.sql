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
-- Name: lab; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lab (
    lab_code character varying(20) NOT NULL,
    lab_company character varying(40) NOT NULL,
    lab_location character varying(50) NOT NULL,
    lab_address character varying(100),
    lab_email character varying(100),
    lab_phone character varying(30),
    lab_fax character varying(30),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    account_no character varying(20)
);

ALTER TABLE ref.lab OWNER TO postgres;

--
-- Name: TABLE lab; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lab IS 'Reference table listing laboratories';

--
-- Name: COLUMN lab.lab_code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_code IS 'Code for the individual laboratory';

--
-- Name: COLUMN lab.lab_company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_company IS 'Laboratory company';

--
-- Name: COLUMN lab.lab_location; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_location IS 'Laboratory location';

--
-- Name: COLUMN lab.lab_address; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_address IS 'Address of the individual laboratory';

--
-- Name: COLUMN lab.lab_email; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_email IS 'Email address of the individual laboratory';

--
-- Name: COLUMN lab.lab_phone; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_phone IS 'Phone number of the individual laboratory';

--
-- Name: COLUMN lab.lab_fax; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.lab_fax IS 'Fax of the individual laboratory';

--
-- Name: COLUMN lab.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN lab.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: lab lab_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab
    ADD CONSTRAINT lab_pkey PRIMARY KEY (lab_code);

--
-- Name: lab ref_lab_lab_code_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab
    ADD CONSTRAINT ref_lab_lab_code_key UNIQUE (lab_code);

--
-- Name: lab ref_lab_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab
    ADD CONSTRAINT ref_lab_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE lab; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lab TO fp;

--
-- PostgreSQL database dump complete
--
