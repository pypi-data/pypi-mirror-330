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
-- Name: surv; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.surv (
    data_set character varying(30) NOT NULL,
    hole_id character varying(30) NOT NULL,
    depth_m numeric NOT NULL,
    dip real NOT NULL,
    azimuth real,
    azimuth_type character varying(50),
    azimuth_grid real NOT NULL,
    dh_survey_method_dip character varying(50),
    dh_survey_method_azimuth character varying(50),
    srid integer,
    date_surveyed_dip timestamp with time zone,
    date_surveyed_azimuth timestamp with time zone,
    dh_survey_company_dip character varying(50),
    dh_survey_company_azimuth character varying(50),
    dh_survey_operator_dip character varying(50),
    dh_survey_operator_azimuth character varying(50),
    dh_survey_instrument_dip character varying(50),
    dh_survey_instrument_azimuth character varying(50),
    comment character varying(500),
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    data_source character varying(100),
    local_grid_azimuth real,
    local_grid_id character varying(40),
    CONSTRAINT depth_check CHECK (((depth_m >= (0)::double precision))),
    CONSTRAINT dh_surv_check_azimuth CHECK (azimuth IS NULL OR ((azimuth >= (0)::double precision) AND (azimuth <= (360)::double precision))),
    CONSTRAINT dh_surv_check_degrees_grid CHECK (((azimuth_grid >= (0)::double precision) AND (azimuth_grid <= (360)::double precision))),
    CONSTRAINT dh_surv_dip_check CHECK (((dip >= (- (90)::double precision)) AND (dip <= (90)::double precision))),
    CONSTRAINT dh_surv_check_azimuth_date CHECK (azimuth IS NULL OR (date_surveyed_dip IS NOT NULL AND date_surveyed_azimuth IS NOT NULL))
);

ALTER TABLE dh.surv OWNER TO postgres;

--
-- Name: TABLE surv; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.surv IS 'Down hole drill hole survey table';

--
-- Name: COLUMN surv.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.data_set IS 'Data set for the Down hole survey, should be the same data_set as the hole_id data_set';

--
-- Name: COLUMN surv.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.hole_id IS 'Drill hole Identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id';

--
-- Name: COLUMN surv.depth_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.depth_m IS 'Depth the down hole survey was taken in metres';

--
-- Name: COLUMN surv.dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dip IS 'Dip of the down hole survey, negative (-) values are down, positive (+) are up';

--
-- Name: COLUMN surv.azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.azimuth IS 'Raw azumith of the down hole survey';

--
-- Name: COLUMN surv.azimuth_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.azimuth_type IS 'Magnetic or true azumith reading';

--
-- Name: COLUMN surv.azimuth_grid; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.azimuth_grid IS 'Azumith based on a Cartesian (grid) co-ordinate system such as UTM';

--
-- Name: COLUMN surv.dh_survey_method_dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_method_dip IS 'Method used to take the down hole survey dip, see ref.dh_survey_method';

--
-- Name: COLUMN surv.dh_survey_method_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_method_azimuth IS 'Method used to take the down hole survey azimuth, see ref.dh_survey_method';

--
-- Name: COLUMN surv.srid; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.srid IS 'Spatial Reference System Identifier, EPSG suggested see https://en.wikipedia.org/wiki/SRID';

--
-- Name: COLUMN surv.date_surveyed_dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.date_surveyed_dip IS 'Date the down hole survey dip was taken';

--
-- Name: COLUMN surv.date_surveyed_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.date_surveyed_azimuth IS 'Date the down hole survey azimuth was taken';

--
-- Name: COLUMN surv.dh_survey_company_dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_company_dip IS 'Survey company who took the down hole survey dip, see ref.company';

--
-- Name: COLUMN surv.dh_survey_company_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_company_azimuth IS 'Survey company who took the down hole survey azimuth, see ref.company';

--
-- Name: COLUMN surv.dh_survey_operator_dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_operator_dip IS 'Person who conducted the down hole survey dip, see ref.person';

--
-- Name: COLUMN surv.dh_survey_operator_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_operator_azimuth IS 'Person who conducted the down hole survey azimuth, see ref.person';

--
-- Name: COLUMN surv.dh_survey_instrument_dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_instrument_dip IS 'Instrument used to take the down hole survey dip, see ref.dh_survey_instrument';

--
-- Name: COLUMN surv.dh_survey_instrument_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.dh_survey_instrument_azimuth IS 'Instrument used to take the down hole survey azimuth, see ref.dh_survey_instrument';

--
-- Name: COLUMN surv.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.comment IS 'Any comments';

--
-- Name: COLUMN surv.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN surv.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN surv.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.data_source IS 'The source of the information for the down hole survey, ref.data_source';

--
-- Name: COLUMN surv.local_grid_azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.local_grid_azimuth IS 'Local grid azimuth';

--
-- Name: COLUMN surv.local_grid_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.surv.local_grid_id IS 'Local grid identification code, see ref.grid_id ';

--
-- Name: surv surv_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT surv_pkey PRIMARY KEY (hole_id, depth_m);

--
-- Name: surv check_depth_m_dh_surv; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_depth_m_dh_surv
    BEFORE INSERT OR UPDATE OF depth_m ON dh.surv
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_depth_m ();

--
-- Name: surv trace_insert_surv; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE OR REPLACE TRIGGER trace_insert_surv
AFTER INSERT ON dh.surv
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT
EXECUTE FUNCTION dh.trace_update_surv ();

--
-- Name: surv trace_update_surv; Type: TRIGGER; Schema: dh; Owner: postgres
--

CREATE OR REPLACE TRIGGER trace_update_surv
AFTER UPDATE ON dh.surv
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT
EXECUTE FUNCTION dh.trace_update_surv ();

--
-- Name: surv trace_delete_surv; Type: TRIGGER; Schema: dh; Owner: postgres
--

CREATE OR REPLACE TRIGGER trace_delete_surv
AFTER DELETE ON dh.surv
REFERENCING OLD TABLE AS new_table
FOR EACH STATEMENT
EXECUTE FUNCTION dh.trace_update_surv ();

--
-- Name: surv dh_dh_surv_survey_company_azimuth_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_dh_surv_survey_company_azimuth_fkey FOREIGN KEY (dh_survey_company_azimuth) REFERENCES ref.company (company);

--
-- Name: surv dh_dh_surv_survey_company_dip_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_dh_surv_survey_company_dip_fkey FOREIGN KEY (dh_survey_company_dip) REFERENCES ref.company (company);

--
-- Name: surv dh_surv_azimuth_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_azimuth_type_fkey FOREIGN KEY (azimuth_type) REFERENCES ref.azimuth_type (code);

--
-- Name: surv dh_surv_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: surv dh_surv_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: surv dh_surv_dh_survey_instrument_azimuth_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_dh_survey_instrument_azimuth_fkey FOREIGN KEY (dh_survey_instrument_azimuth) REFERENCES ref.survey_instrument (code);

--
-- Name: surv dh_surv_dh_survey_instrument_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_dh_survey_instrument_fkey FOREIGN KEY (dh_survey_instrument_dip) REFERENCES ref.survey_instrument (code);

--
-- Name: surv dh_surv_dh_survey_operator_azimuth_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_dh_survey_operator_azimuth_fkey FOREIGN KEY (dh_survey_operator_azimuth) REFERENCES ref.person (code);

--
-- Name: surv dh_surv_dh_survey_operator_dip_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_dh_survey_operator_dip_fkey FOREIGN KEY (dh_survey_operator_dip) REFERENCES ref.person (code);

--
-- Name: surv dh_surv_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: surv dh_surv_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: surv dh_surv_srid_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_srid_fkey FOREIGN KEY (srid) REFERENCES public.spatial_ref_sys (srid);

--
-- Name: surv dh_surv_survey_method_azimuth_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT dh_surv_survey_method_azimuth_fkey FOREIGN KEY (dh_survey_method_azimuth) REFERENCES ref.dh_survey_method (code);

--
-- Name: surv surv_dh_survey_method_dip_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT surv_dh_survey_method_dip_fkey FOREIGN KEY (dh_survey_method_dip) REFERENCES ref.dh_survey_method (code);

--
-- Name: surv surv_local_grid_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.surv
    ADD CONSTRAINT surv_local_grid_id_fkey FOREIGN KEY (local_grid_id) REFERENCES ref.grid_id (grid_id);

--
-- Name: TABLE surv; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.surv TO fp;

--
-- PostgreSQL database dump complete
--
