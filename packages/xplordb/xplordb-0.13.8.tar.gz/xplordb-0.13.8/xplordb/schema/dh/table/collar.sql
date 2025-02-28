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
-- Name: collar; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.collar (
    data_set character varying(80) NOT NULL,
    hole_id character varying(40) NOT NULL,
    x double precision,
    y double precision,
    z real,
    eoh real,
    planned_x double precision,
    planned_y double precision,
    planned_z double precision,
    planned_eoh real,
    dip real DEFAULT -90,
    azimuth real DEFAULT 0,
    grid_id character varying(80),
    hole_type character varying(80),
    hole_status character varying(80),
    survey_method character varying(80),
    survey_date timestamp with time zone,
    surveyed_by_company character varying(80),
    local_grid_east real,
    local_grid_north real,
    local_grid_rl real,
    parent_hole character varying(80),
    precollar real,
    lease_id character varying(80),
    prospect character varying(80),
    comment character varying,
    data_source character varying(300),
    historic_hole character varying(80),
    loaded_by character varying(80) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    rl_method character varying(30),
    srid integer,
    project_srid integer,
    surveyed_by_person character varying(5),
    location_confidence_m integer,
    sub_set character varying(50),
    geom public.geometry(PointZ, 4326),
    planned_loc public.geometry(PointZ, 4326),
    geom_trace public.geometry(CompoundCurveZM, 4326),
    planned_trace public.geometry(CompoundCurveZM, 4326),
    -- projected geometries (3857 if srid is polar, else srid)
    proj_geom public.geometry(PointZ),
    proj_planned_loc public.geometry(PointZ),
    proj_geom_trace public.geometry(CompoundCurveZM),
    proj_planned_trace public.geometry(CompoundCurveZM)

);

ALTER TABLE dh.collar OWNER TO postgres;

--
-- Name: TABLE collar; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.collar IS 'Down hole drill hole collar table';

--
-- Name: COLUMN collar.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.data_set IS 'The data set/ project of the drill collar, see ref.data_sets';

--
-- Name: COLUMN collar.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.hole_id IS 'Drill hole identification(id) number/ code';

--
-- Name: COLUMN collar.x; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.x IS 'Horizontal distance or angle (usually east or longitude) from grid origin of the drill hole collar';

--
-- Name: COLUMN collar.y; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.y IS 'Horizontal distance or angle (usually north or latitude) from grid origin of the drill hole collar';

--
-- Name: COLUMN collar.z; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.z IS 'Vertical distance from the local grid origin or elevation of the drill hole collar';

--
-- Name: COLUMN collar.grid_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.grid_id IS 'Co-ordinate reference system (CRS)/ grid identification code, see ref.grid_id';

--
-- Name: COLUMN collar.hole_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.hole_type IS 'Drill hole type, see ref.hole_type';

--
-- Name: COLUMN collar.hole_status; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.hole_status IS 'The status of the drill hole, see ref.hole_status';

--
-- Name: COLUMN collar.survey_method; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.survey_method IS 'The method used to survey the collar location, see ref.survey_method';

--
-- Name: COLUMN collar.survey_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.survey_date IS 'The date the survey of the collar location was taken';

--
-- Name: COLUMN collar.surveyed_by_company; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.surveyed_by_company IS 'The company who completed the collar location survey, see ref.company';

--
-- Name: COLUMN collar.local_grid_east; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.local_grid_east IS 'Horizontal distance east from local grid origin';

--
-- Name: COLUMN collar.local_grid_north; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.local_grid_north IS 'Horizontal distance north from local grid origin';

--
-- Name: COLUMN collar.local_grid_rl; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.local_grid_rl IS 'Vertical distance from the local grid origin';

--
-- Name: COLUMN collar.parent_hole; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.parent_hole IS 'For wedged drill holes, the hole_id of the main or parent drill hole';

--
-- Name: COLUMN collar.precollar; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.precollar IS 'The down hole length of the pre-collar in metres';

--
-- Name: COLUMN collar.lease_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.lease_id IS 'Lease/ tenement identification(id) code of the drill hole location, see ref.lease';

--
-- Name: COLUMN collar.prospect; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.prospect IS 'Prospect of the drill hole collar';

--
-- Name: COLUMN collar.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.comment IS 'Any comment regarding the drill hole';

--
-- Name: COLUMN collar.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.data_source IS 'The source of the information about the drill collar, see ref.data_source';

--
-- Name: COLUMN collar.historic_hole; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.historic_hole IS 'A previous name/ id for the drill hole';

--
-- Name: COLUMN collar.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN collar.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN collar.rl_method; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.rl_method IS 'This field is needed by some drill hole plotting software';

--
-- Name: COLUMN collar.srid; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.srid IS 'Spatial Reference System Identifier, EPSG suggested see https://en.wikipedia.org/wiki/SRID';

--
-- Name: COLUMN collar.surveyed_by_person; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.surveyed_by_person IS 'Person who surveyed the drill hole collar';

--
-- Name: COLUMN collar.location_confidence_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.location_confidence_m IS 'Make, model, number of the drill rig';

--
-- Name: COLUMN collar.sub_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.sub_set IS 'Some sub-set of the drill hole collars';

--
-- Name: COLUMN collar.geom; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.geom IS 'PostGIS extension column of drill hole collar location in three dimesions (xyz)';

--
-- Name: COLUMN collar.geom_trace; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.collar.geom_trace IS 'PostGIS extension column of de-surveyed drill hole trace in three dimesions (xyz) produced by function dh.trace';

--
-- Name: collar dh_collar_hole_id_key; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collar_hole_id_key UNIQUE (hole_id);

--
-- Name: collar dh_collar_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collar_pkey PRIMARY KEY (hole_id);

--
-- Name: idx_dh_collar_geom; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX idx_dh_collar_geom ON dh.collar USING gist (geom);

--
-- Name: sidx_collar_geom_trace; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX sidx_collar_geom_trace ON dh.collar USING gist (geom_trace);

--
-- Name: collar collar_srid_update; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER collar_srid_update
    AFTER INSERT OR UPDATE OF grid_id ON dh.collar
    FOR EACH ROW
    EXECUTE FUNCTION dh.update_srid_dh ();



--
-- Name: collar geom_update_xyz; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER geom_update_xyz
    AFTER UPDATE OF geom
    ON dh.collar
    FOR EACH ROW
    WHEN (pg_trigger_depth() < 1)
    EXECUTE FUNCTION dh.geom_update_xyz ();

--
-- Name: collar trace_update_xyz; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_update_xyz
    AFTER INSERT OR UPDATE OF x,y,z,eoh,geom, hole_id
    ON dh.collar
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_xyz ();

--
-- Name: collar update_gis_dh; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER update_gis_dh
    AFTER INSERT OR UPDATE OF x,
    y,
    z,
    srid ON dh.collar
    FOR EACH ROW
    EXECUTE FUNCTION dh.update_gis_geom_dh_collar_ll ();

--
-- Name: collar planned_trace_update; Type: TRIGGER; Schema: dh; Owner: postgres
--
-- if planned_loc geometry change, extract and update coordinates
CREATE TRIGGER planned_loc_update_xyz
    AFTER UPDATE OF planned_loc
    ON dh.collar
    FOR EACH ROW
    WHEN (pg_trigger_depth() < 1)
    EXECUTE FUNCTION dh.planned_loc_update_xyz ();

CREATE TRIGGER planned_trace_update
    AFTER INSERT OR UPDATE OF planned_loc,
    planned_x, planned_y, planned_z, planned_eoh, dip, azimuth ON dh.collar
    FOR EACH ROW
    EXECUTE FUNCTION dh.planned_trace_update();

-- if planned coordinates change, update planned_loc geometry
CREATE TRIGGER update_planned_gis_dh
    AFTER INSERT OR UPDATE OF planned_x,
    planned_y,
    planned_z,
    srid ON dh.collar
    FOR EACH ROW
    EXECUTE FUNCTION dh.update_gis_planned_loc_dh_collar_ll ();


--
-- Name: collar collar_location_confidence_m_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT collar_location_confidence_m_fkey FOREIGN KEY (location_confidence_m) REFERENCES ref.location_confidence_m (code);

--
-- Name: collar dh_collar_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collar_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: collar dh_collar_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collar_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: collar dh_collar_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collar_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: collar dh_collars_grid_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_grid_id_fkey FOREIGN KEY (grid_id) REFERENCES ref.grid_id (grid_id);

--
-- Name: collar dh_collars_hole_status_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_hole_status_fkey FOREIGN KEY (hole_status) REFERENCES ref.hole_status (code);

--
-- Name: collar dh_collars_hole_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_hole_type_fkey FOREIGN KEY (hole_type) REFERENCES ref.hole_type (code);

--
-- Name: collar dh_collars_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: collar dh_collars_prospect_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_prospect_fkey FOREIGN KEY (prospect) REFERENCES ref.prospect (prospect);

--
-- Name: collar dh_collars_survey_company_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_survey_company_fkey FOREIGN KEY (surveyed_by_company) REFERENCES ref.company (company);

--
-- Name: collar dh_collars_survey_method_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_survey_method_fkey FOREIGN KEY (survey_method) REFERENCES ref.survey_method (code);

--
-- Name: collar dh_collars_surveyed_by_person_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.collar
    ADD CONSTRAINT dh_collars_surveyed_by_person_fkey FOREIGN KEY (surveyed_by_person) REFERENCES ref.person (code);

--
-- Name: TABLE collar; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.collar TO fp;

--
-- PostgreSQL database dump complete
--
