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
-- Name: sample_quality; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.sample_quality (
    data_set character varying(20) NOT NULL,
    hole_id character varying(50) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    recovery_pct real NOT NULL,
    moisture_pct real,
    contamination_pct real,
    data_source character varying(50) NOT NULL,
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_sample_quality_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision))),
    CONSTRAINT dh_sample_quality_check_num CHECK (((recovery_pct <= (100)::double precision) AND (recovery_pct > (0)::double precision) AND (moisture_pct <= (100)::double precision) AND (moisture_pct > (0)::double precision) AND (contamination_pct <= (100)::double precision) AND (contamination_pct > (0)::double precision) AND (from_m >= (0)::double precision) AND (to_m >= (0)::double precision) AND (from_m <= (800)::double precision) AND (to_m <= (800)::double precision)))
);

ALTER TABLE dh.sample_quality OWNER TO postgres;

--
-- Name: TABLE sample_quality; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.sample_quality IS 'Down hole drill hole sample quality table';

--
-- Name: COLUMN sample_quality.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.data_set IS 'Data set for the sample quaility observation, see ref.data_set';

--
-- Name: COLUMN sample_quality.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id';

--
-- Name: COLUMN sample_quality.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sample_quality.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sample_quality.recovery_pct; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.recovery_pct IS 'Estimate of the proportion of the recovery, in percent, of the total sample';

--
-- Name: COLUMN sample_quality.moisture_pct; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.moisture_pct IS 'Estimate of the proportion of the moisture content of the sample, in percent, of the total sample';

--
-- Name: COLUMN sample_quality.contamination_pct; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.contamination_pct IS 'Estimate of the proportion of the contaimination, in percent, of the total sample';

--
-- Name: COLUMN sample_quality.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.data_source IS 'The source of the sample quality information, see ref.data_source';

--
-- Name: COLUMN sample_quality.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN sample_quality.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN sample_quality.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample_quality.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_quality.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sample_quality dh_sample_quality_hole_id_from_m_key; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT dh_sample_quality_hole_id_from_m_key UNIQUE (hole_id, from_m);

--
-- Name: sample_quality sample_quality_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT sample_quality_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: sample_quality dh_sample_quality_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT dh_sample_quality_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sample_quality dh_sample_quality_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT dh_sample_quality_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sample_quality dh_sample_quality_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT dh_sample_quality_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: sample_quality dh_sample_quality_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT dh_sample_quality_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: sample_quality sample_quality_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_quality
    ADD CONSTRAINT sample_quality_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE sample_quality; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.sample_quality TO fp;

--
-- PostgreSQL database dump complete
--
