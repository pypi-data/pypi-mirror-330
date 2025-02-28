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
-- Name: dh; Type: TABLE; Schema: qa; Owner: postgres
--
CREATE TABLE qa.dh (
    data_set character varying(20) NOT NULL,
    hole_id character varying(50) NOT NULL,
    sample_id character varying(50) NOT NULL,
    depth_m real,
    from_m real,
    to_m real,
    original_sample character varying(20),
    qc_type character varying(10),
    standard_id character varying,
    date_submitted timestamp with time zone,
    comment character varying(100),
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(50) DEFAULT "current_user" () NOT NULL,
    data_source character varying(100),
    class character varying(16) NOT NULL,
    CONSTRAINT qc_dh_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision))),
    CONSTRAINT qc_dh_check_num CHECK (((from_m >= (0)::double precision) AND (to_m >= (0)::double precision) AND (from_m <= (800)::double precision) AND (to_m <= (800)::double precision) AND (depth_m >= (0)::double precision) AND (depth_m <= (800)::double precision)))
);

ALTER TABLE qa.dh OWNER TO postgres;

--
-- Name: TABLE dh; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON TABLE qa.dh IS 'Down hole drill hole quality control table';

--
-- Name: COLUMN dh.data_set; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.data_set IS 'Data set for the down hole quality control information, see ref.data_set';

--
-- Name: COLUMN dh.hole_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN dh.sample_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.sample_id IS 'Sample identification(id) number/ code for the down hole quality control item/ sample';

--
-- Name: COLUMN dh.depth_m; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.depth_m IS 'Distance in metres(m) down the drill hole from the collar the quality control item occurs (for use with standards/ reference material';

--
-- Name: COLUMN dh.from_m; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the quality control sample occurs (e.g. duplicate)';

--
-- Name: COLUMN dh.to_m; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.to_m IS 'Starting distance in metres(m) down the drill hole from the collar the quality control sample occurs (e.g. duplicate)';

--
-- Name: COLUMN dh.original_sample; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.original_sample IS 'The original sample identification(id) number/ code ';

--
-- Name: COLUMN dh.qc_type; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.qc_type IS 'Quality control category code, see qc_ref_qc_type';

--
-- Name: COLUMN dh.standard_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.standard_id IS 'The standard/ reference material identification(id) number/ code';

--
-- Name: COLUMN dh.date_submitted; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.date_submitted IS 'Date the quality control sample or item was submitted to the laboratory ';

--
-- Name: COLUMN dh.comment; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.comment IS 'Any comment';

--
-- Name: COLUMN dh.load_date; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN dh.loaded_by; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN dh.data_source; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.dh.data_source IS 'The source of the quality control information, see ref.data_source';

--
-- Name: dh dh_pkey; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT dh_pkey PRIMARY KEY (sample_id);

--
-- Name: dh check_depth_m_qc_dh; Type: TRIGGER; Schema: qa; Owner: postgres
--
CREATE TRIGGER check_depth_m_qc_dh
    BEFORE INSERT OR UPDATE OF depth_m ON qa.dh
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_depth_m ();

--
-- Name: dh check_from_m_qc_dh; Type: TRIGGER; Schema: qa; Owner: postgres
--
CREATE TRIGGER check_from_m_qc_dh
    BEFORE INSERT OR UPDATE OF from_m ON qa.dh
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: dh check_to_m_qc_dh; Type: TRIGGER; Schema: qa; Owner: postgres
--
CREATE TRIGGER check_to_m_qc_dh
    BEFORE INSERT OR UPDATE OF to_m ON qa.dh
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: dh dh_class_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT dh_class_fkey FOREIGN KEY (class) REFERENCES ref.sample_class (code);

--
-- Name: dh dh_standard_id_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT dh_standard_id_fkey FOREIGN KEY (standard_id) REFERENCES qa.sd_values (standard_id);

--
-- Name: dh qc_dh_data_set_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT qc_dh_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: dh qc_dh_data_source_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT qc_dh_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: dh qc_dh_hole_id_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT qc_dh_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: dh qc_dh_loaded_by_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT qc_dh_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: dh qc_dh_qc_type_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.dh
    ADD CONSTRAINT qc_dh_qc_type_fkey FOREIGN KEY (qc_type) REFERENCES qa.qc_type (code);

--
-- PostgreSQL database dump complete
--
