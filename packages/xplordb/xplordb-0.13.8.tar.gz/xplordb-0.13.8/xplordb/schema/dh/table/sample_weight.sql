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
-- Name: sample_weight; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.sample_weight (
    data_set character varying(20) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    sample_weight real NOT NULL,
    unit character varying(10) NOT NULL,
    comment character varying(200),
    data_source character varying(200) NOT NULL,
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326)
);

ALTER TABLE dh.sample_weight OWNER TO postgres;

--
-- Name: TABLE sample_weight; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.sample_weight IS 'Down hole drill hole sample weight. -1 weight represents an attempt was made to take a reading but was not possible.';

--
-- Name: COLUMN sample_weight.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.data_set IS 'Data set for the sample_weight observation, sef ref.data_set';

--
-- Name: COLUMN sample_weight.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN sample_weight.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the sample_weight observation occurs';

--
-- Name: COLUMN sample_weight.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.to_m IS 'Ending distance in metres(m) down the drill hole from the collar the sample_weight observation occurs';

--
-- Name: COLUMN sample_weight.sample_weight; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.sample_weight IS 'sample_weight relating to the observation. . -1 weight represents an attempt was made to take a reading but was not possible.';

--
-- Name: COLUMN sample_weight.unit; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.unit IS 'Units of the sample weight measurement';

--
-- Name: COLUMN sample_weight.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.comment IS 'Any comment';

--
-- Name: COLUMN sample_weight.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.data_source IS 'The source of the sample_weight, see ref.data_source';

--
-- Name: COLUMN sample_weight.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN sample_weight.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN sample_weight.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample_weight.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_weight.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sample_weight check_interval_overlap_dh_sample_weight; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT check_interval_overlap_dh_sample_weight
    EXCLUDE USING gist (box(point((from_m + (0.0001)::double precision), (from_m + (0.0001)::double precision)), point((to_m - (0.0001)::double precision), (to_m - (0.0001)::double precision))) WITH &&, hole_id WITH =);

--
-- Name: sample_weight dh_sample_weight_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT dh_sample_weight_pkey PRIMARY KEY (hole_id, from_m);

--
-- Name: sample_weight check_from_m_dh_sample_weight; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_sample_weight
    BEFORE INSERT OR UPDATE OF from_m ON dh.sample_weight
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: sample_weight check_to_m_dh_sample_weight; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_sample_weight
    BEFORE INSERT OR UPDATE OF to_m ON dh.sample_weight
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: sample_weight trace_row_sample_weight; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_sample_weight
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.sample_weight
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: sample_weight dh_sample_weight_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT dh_sample_weight_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sample_weight dh_sample_weight_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT dh_sample_weight_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sample_weight dh_sample_weight_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT dh_sample_weight_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: sample_weight dh_sample_weight_unit_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT dh_sample_weight_unit_fkey FOREIGN KEY (unit) REFERENCES ref.units (code);

--
-- Name: sample_weight sample_weight_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_weight
    ADD CONSTRAINT sample_weight_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
