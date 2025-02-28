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
-- Name: data_sets; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.data_sets (
    data_set character varying(30) NOT NULL,
    full_name character varying(100),
    comment character varying(500),
    prospects character varying(500),
    owner1 character varying(100),
    owner2 character varying(100),
    lease_numbers character varying(20),
    loaded_by character varying DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.data_sets OWNER TO postgres;

--
-- Name: TABLE data_sets; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.data_sets IS 'Reference table listing data sets';

--
-- Name: COLUMN data_sets.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.data_set IS 'Data set code';

--
-- Name: COLUMN data_sets.full_name; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.full_name IS 'The full formated name of the Data Set';

--
-- Name: COLUMN data_sets.comment; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.comment IS 'Any comments about the data set';

--
-- Name: COLUMN data_sets.prospects; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.prospects IS 'List of prospects/ projects related to the data set';

--
-- Name: COLUMN data_sets.owner1; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.owner1 IS 'The primary owner of the data set project';

--
-- Name: COLUMN data_sets.owner2; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.owner2 IS 'Other owner of the data set project';

--
-- Name: COLUMN data_sets.lease_numbers; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.lease_numbers IS 'Tenement/ lease identification';

--
-- Name: COLUMN data_sets.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN data_sets.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_sets.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: data_sets data_sets_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_sets
    ADD CONSTRAINT data_sets_pkey PRIMARY KEY (data_set);

--
-- Name: data_sets ref_data_sets_data_set_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_sets
    ADD CONSTRAINT ref_data_sets_data_set_key UNIQUE (data_set);

--
-- Name: data_sets ref_data_sets_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY ref.data_sets
    ADD CONSTRAINT ref_data_sets_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: data_sets ref_data_sets_owner1_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY ref.data_sets
    ADD CONSTRAINT ref_data_sets_owner1_fkey FOREIGN KEY (owner1) REFERENCES ref.company (company);

--
-- Name: data_sets ref_data_sets_owner2_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY ref.data_sets
    ADD CONSTRAINT ref_data_sets_owner2_fkey FOREIGN KEY (owner2) REFERENCES ref.company (company);

--
-- Name: TABLE data_sets; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.data_sets TO fp;

--
-- PostgreSQL database dump complete
--
