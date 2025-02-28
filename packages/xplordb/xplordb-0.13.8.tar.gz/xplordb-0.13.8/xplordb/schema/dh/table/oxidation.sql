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
-- Name: oxidation; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.oxidation (
    data_set character varying(10) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    oxidation integer,
    data_source character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_oxidation_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.oxidation OWNER TO postgres;

--
-- Name: TABLE oxidation; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.oxidation IS 'Down hole drill hole oxidation table';

--
-- Name: COLUMN oxidation.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.data_set IS 'Data set for the oxidation observation, sef ref.data_set';

--
-- Name: COLUMN oxidation.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN oxidation.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the oxidation observation occurs';

--
-- Name: COLUMN oxidation.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.to_m IS 'Ending distance in metres(m) down the drill hole from the collar the oxidation observation occurs';

--
-- Name: COLUMN oxidation.oxidation; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.oxidation IS 'Oxidation code relating to the observation, see ref.oxidation';

--
-- Name: COLUMN oxidation.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.data_source IS 'The source of the oxidation observation, see ref.data_source';

--
-- Name: COLUMN oxidation.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN oxidation.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN oxidation.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN oxidation.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.oxidation.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: oxidation oxidation_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT oxidation_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: oxidation dh_oxidation_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT dh_oxidation_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: oxidation dh_oxidation_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT dh_oxidation_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: oxidation dh_oxidation_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT dh_oxidation_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: oxidation dh_oxidation_oxidation_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT dh_oxidation_oxidation_fkey FOREIGN KEY (oxidation) REFERENCES ref.oxidation (code);

--
-- Name: oxidation oxidation_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT oxidation_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: oxidation oxidation_logged_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.oxidation
    ADD CONSTRAINT oxidation_logged_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: TABLE oxidation; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.oxidation TO fp;

--
-- PostgreSQL database dump complete
--
