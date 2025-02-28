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
-- Name: strat_name; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.strat_name (
    code character varying(9) NOT NULL,
    description character varying(100),
    number integer,
    data_set character varying(20) NOT NULL,
    data_set_2 character varying(20),
    data_set2_description character varying(50),
    loaded_by character varying(10) DEFAULT "current_user" () NOT NULL,
    load_date date DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    prospect character varying
);

ALTER TABLE ref.strat_name OWNER TO postgres;

--
-- Name: TABLE strat_name; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.strat_name IS 'Reference table listing litholgy/ geology codes';

--
-- Name: COLUMN strat_name.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.code IS 'Code for the straitigraphy/ geology';

--
-- Name: COLUMN strat_name.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.description IS 'Description of the straitigraphy code';

--
-- Name: COLUMN strat_name.number; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.number IS 'A number related to the straitigraphy for display in programs that need a number to display colour etc.';

--
-- Name: COLUMN strat_name.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.data_set IS 'Data set for the straitigraphy';

--
-- Name: COLUMN strat_name.data_set_2; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.data_set_2 IS 'Second data set for the straitigraphy';

--
-- Name: COLUMN strat_name.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN strat_name.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.strat_name.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: strat_name ref_strat_name_description_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.strat_name
    ADD CONSTRAINT ref_strat_name_description_key UNIQUE (description);

--
-- Name: strat_name ref_strat_name_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.strat_name
    ADD CONSTRAINT ref_strat_name_pkey PRIMARY KEY (code);

--
-- Name: strat_name ref_strat_name_data_set_2_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.strat_name
    ADD CONSTRAINT ref_strat_name_data_set_2_fkey FOREIGN KEY (data_set_2) REFERENCES ref.data_sets (data_set);

--
-- Name: strat_name ref_strat_name_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.strat_name
    ADD CONSTRAINT ref_strat_name_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
