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
-- Name: minerals; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.minerals (
    data_set character varying(20) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m double precision NOT NULL,
    to_m double precision NOT NULL,
    min_1 character varying(10) NOT NULL,
    min1_per real NOT NULL,
    min_2 character varying(10),
    min2_per real,
    min_3 character varying,
    min3_per real,
    data_source character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_minerals_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision))),
    CONSTRAINT dh_minerals_check_per CHECK (((min1_per <= (100)::double precision) AND (min1_per >= (0)::double precision) AND (min2_per <= (100)::double precision) AND (min2_per >= (0)::double precision) AND (min3_per <= (100)::double precision) AND (min3_per >= (0)::double precision) AND (from_m >= (0)::double precision) AND (to_m >= (0)::double precision) AND (from_m <= (800)::double precision) AND (to_m <= (800)::double precision)))
);

ALTER TABLE dh.minerals OWNER TO postgres;

--
-- Name: TABLE minerals; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.minerals IS 'Down hole drill hole minerals table';

--
-- Name: COLUMN minerals.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.data_set IS 'Data set for the down hole mineral occurance, should be the same data_set for the hole_id';

--
-- Name: COLUMN minerals.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.hole_id IS 'Drill hole Identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id';

--
-- Name: COLUMN minerals.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the mineral occurs';

--
-- Name: COLUMN minerals.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.to_m IS 'Ending distance in metres(m) down the drill hole from the collar the mineral occurs';

--
-- Name: COLUMN minerals.min_1; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min_1 IS 'Code for mineral occurance, see ref.minerals';

--
-- Name: COLUMN minerals.min1_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min1_per IS 'Proportion of the mineral, in percent, the rock is composed of';

--
-- Name: COLUMN minerals.min_2; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min_2 IS 'Only used if required, as for min_1';

--
-- Name: COLUMN minerals.min2_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min2_per IS 'Proportion of the mineral, in percent, the rock is composed of';

--
-- Name: COLUMN minerals.min_3; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min_3 IS 'Only used if required, as for min_1';

--
-- Name: COLUMN minerals.min3_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.min3_per IS 'Proportion of the mineral, in percent, the rock is composed of';

--
-- Name: COLUMN minerals.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.data_source IS 'The source of the information for the event, see ref.data_source';

--
-- Name: COLUMN minerals.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN minerals.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN minerals.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN minerals.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.minerals.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: minerals minerals_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT minerals_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: minerals check_from_m_dh_minerals; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_minerals
    BEFORE INSERT OR UPDATE OF from_m ON dh.minerals
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: minerals check_to_m_dh_minerals; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_minerals
    BEFORE INSERT OR UPDATE OF to_m ON dh.minerals
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: minerals trace_row_minerals; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_minerals
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.minerals
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: minerals dh_minerals_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: minerals dh_minerals_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: minerals dh_minerals_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: minerals dh_minerals_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: minerals dh_minerals_min_1_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_min_1_fkey FOREIGN KEY (min_1) REFERENCES ref.minerals (code);

--
-- Name: minerals dh_minerals_min_2_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_min_2_fkey FOREIGN KEY (min_2) REFERENCES ref.minerals (code);

--
-- Name: minerals dh_minerals_min_3_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT dh_minerals_min_3_fkey FOREIGN KEY (min_3) REFERENCES ref.minerals (code);

--
-- Name: minerals minerals_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.minerals
    ADD CONSTRAINT minerals_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE minerals; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.minerals TO fp;

--
-- PostgreSQL database dump complete
--
