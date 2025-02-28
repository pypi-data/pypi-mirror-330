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
-- Name: lithology; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lithology (
    code character varying(50) NOT NULL,
    description character varying(100),
    data_set character varying(20),
    data_set_2 character varying(20),
    data_set_3 character varying(20),
    loaded_by character varying(10) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.lithology OWNER TO postgres;

--
-- Name: TABLE lithology; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lithology IS 'Reference table listing litholgy/ geology codes';

--
-- Name: COLUMN lithology.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.code IS 'Code for the lithology/ geology';

--
-- Name: COLUMN lithology.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.description IS 'Description of the lithology code';

--
-- Name: COLUMN lithology.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.data_set IS 'Data set for the lithology';

--
-- Name: COLUMN lithology.data_set_2; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.data_set_2 IS 'Second data set for the lithology';

--
-- Name: COLUMN lithology.data_set_3; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.data_set_3 IS 'Third data set for the lithology';

--
-- Name: COLUMN lithology.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN lithology.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lithology.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: lithology lithology_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT lithology_pkey PRIMARY KEY (code);

--
-- Name: lithology ref_lithology_code_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT ref_lithology_code_key UNIQUE (code);

--
-- Name: lithology ref_lithology_data_set_2_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT ref_lithology_data_set_2_fkey FOREIGN KEY (data_set_2) REFERENCES ref.data_sets (data_set);

--
-- Name: lithology ref_lithology_data_set_3_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT ref_lithology_data_set_3_fkey FOREIGN KEY (data_set_3) REFERENCES ref.data_sets (data_set);

--
-- Name: lithology ref_lithology_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT ref_lithology_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: lithology ref_lithology_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lithology
    ADD CONSTRAINT ref_lithology_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE lithology; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lithology TO fp;

--
-- PostgreSQL database dump complete
--
