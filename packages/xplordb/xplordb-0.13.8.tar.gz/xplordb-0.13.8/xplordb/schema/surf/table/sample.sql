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
-- Name: sample; Type: TABLE; Schema: surf; Owner: postgres
--
CREATE TABLE surf.sample (
    data_set character varying(80) NOT NULL,
    sample_id character varying(20) NOT NULL,
    x numeric(8, 2),
    y numeric(9, 2),
    z numeric(9, 2),
    grid_id character varying(80) NOT NULL,
    line_no real,
    sample_type character varying(80),
    channel_id character varying(40),
    channel_from_m real,
    channel_to_m real,
    sample_depth_m real,
    sample_weight_kg real,
    date_sampled timestamp with time zone,
    company character varying(80),
    sampled_by character varying(5),
    sampled_by_2 character varying(5),
    geology_code character varying(20),
    geology_logged_by character varying(80),
    mesh_size character varying(20),
    survey_method character varying(80),
    survey_date timestamp with time zone,
    surveyed_by character varying(80),
    lat double precision,
    lon double precision,
    local_grid_east real,
    local_grid_north real,
    local_grid_rl real,
    lease_id character varying(80),
    prospect character varying(80),
    comment character varying(80),
    site_photo character varying(80),
    data_source character varying(300) NOT NULL,
    historic_sample_id character varying(80),
    srid integer,
    loaded_by character varying(80) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom public.geometry(PointZ, 4326),
    class character varying(16) NOT NULL,
    CONSTRAINT surf_sample_check CHECK ((channel_from_m < channel_to_m))
);

ALTER TABLE surf.sample OWNER TO postgres;

--
-- Name: TABLE sample; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON TABLE surf.sample IS 'Surafce sample table';

--
-- Name: COLUMN sample.data_set; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.data_set IS 'Data set for the surface sample, see ref.data_set';

--
-- Name: COLUMN sample.sample_id; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sample_id IS 'Sample identification(id) number/ code for the surface sample, , see ref.qc_type for quality control codes ';

--
-- Name: COLUMN sample.x; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.x IS 'Horizontal distance or angle (usually east or longitude) from grid origin of the surface sample';

--
-- Name: COLUMN sample.y; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.y IS 'Horizontal distance or angle (usually north or latitude) from grid origin of the petrology description';

--
-- Name: COLUMN sample.z; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.z IS 'Vertical distance from the local grid origin or elevation of the surface sample';

--
-- Name: COLUMN sample.grid_id; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.grid_id IS 'Grid identification(id) number/ code for the surface sample, see ref.grid_id ';

--
-- Name: COLUMN sample.line_no; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.line_no IS 'The line number of the sample, if samples were taken on numbered lines, optional';

--
-- Name: COLUMN sample.sample_type; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sample_type IS 'Sample type, see ref.sample_type';

--
-- Name: COLUMN sample.channel_id; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.channel_id IS 'Channel/ trench identification(id) number/ code for the surface sample';

--
-- Name: COLUMN sample.channel_from_m; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.channel_from_m IS 'Starting distance in metres(m) along the channel/ trench of the sample';

--
-- Name: COLUMN sample.channel_to_m; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.channel_to_m IS 'Ending distance in metres(m) along the channel/ trench of the sample';

--
-- Name: COLUMN sample.sample_depth_m; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sample_depth_m IS 'Depth the sample was taken in metres(m)';

--
-- Name: COLUMN sample.sample_weight_kg; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sample_weight_kg IS 'Weight(mass) of the surface sample';

--
-- Name: COLUMN sample.date_sampled; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.date_sampled IS 'The date the surface sample was taken';

--
-- Name: COLUMN sample.company; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.company IS 'Company who took the surface sample, see ref.company';

--
-- Name: COLUMN sample.sampled_by; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sampled_by IS 'The person who took the surface sample, see ref.person';

--
-- Name: COLUMN sample.sampled_by_2; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.sampled_by_2 IS 'The second person who also took the surface sample, see ref.person';

--
-- Name: COLUMN sample.geology_code; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.geology_code IS 'The geology code for the surface sample, see ref.lithology';

--
-- Name: COLUMN sample.geology_logged_by; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.geology_logged_by IS 'The person who described the geology/ lithology of the sample';

--
-- Name: COLUMN sample.mesh_size; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.mesh_size IS 'Mesh size of the sieve used on the surface sample in millimetres(mm) if the sample was sieved';

--
-- Name: COLUMN sample.survey_method; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.survey_method IS 'Location survey method used, see ref.survey_method';

--
-- Name: COLUMN sample.survey_date; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.survey_date IS 'Date the location survey was taken';

--
-- Name: COLUMN sample.surveyed_by; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.surveyed_by IS 'Person who surveyed the location, see ref.person';

--
-- Name: COLUMN sample.lat; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.lat IS 'Latitude of the surface sample';

--
-- Name: COLUMN sample.lon; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.lon IS 'Longitude of the surface sample';

--
-- Name: COLUMN sample.local_grid_east; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.local_grid_east IS 'Horizontal distance east from local grid origin';

--
-- Name: COLUMN sample.local_grid_north; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.local_grid_north IS 'Horizontal distance north from local grid origin';

--
-- Name: COLUMN sample.local_grid_rl; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.local_grid_rl IS 'Vertical distance from the local grid origin';

--
-- Name: COLUMN sample.lease_id; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.lease_id IS 'Lease/ tenement identification(id) code of the surface sample, see ref.lease';

--
-- Name: COLUMN sample.prospect; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.prospect IS 'Prospect of the surface sample';

--
-- Name: COLUMN sample.comment; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.comment IS 'Any comment';

--
-- Name: COLUMN sample.site_photo; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.site_photo IS 'File location of site photograph';

--
-- Name: COLUMN sample.data_source; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.data_source IS 'The source of the surface sample information, see ref.data_source';

--
-- Name: COLUMN sample.historic_sample_id; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.historic_sample_id IS 'Historic sample identification(id) number/ code for the surface sample ';

--
-- Name: COLUMN sample.srid; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.srid IS 'Spatial Reference System Identifier, EPSG suggested see https://en.wikipedia.org/wiki/SRID';

--
-- Name: COLUMN sample.loaded_by; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample.load_date; Type: COMMENT; Schema: surf; Owner: postgres
--
COMMENT ON COLUMN surf.sample.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sample surf_sample_pkey; Type: CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_pkey PRIMARY KEY (sample_id);

--
-- Name: idx_surf_sample_geom; Type: INDEX; Schema: surf; Owner: postgres
--
CREATE INDEX idx_surf_sample_geom ON surf.sample USING gist (geom);

--
-- Name: sample update_gis_surf_sample; Type: TRIGGER; Schema: surf; Owner: postgres
--
CREATE TRIGGER update_gis_surf_sample
    AFTER INSERT OR UPDATE OF x,
    y,
    z ON surf.sample
    FOR EACH ROW
    EXECUTE FUNCTION surf.update_gis_geom_sample_ll ();

--
-- Name: sample sample_class_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT sample_class_fkey FOREIGN KEY (class) REFERENCES ref.sample_class (code);

--
-- Name: sample surf_sample_company_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);

--
-- Name: sample surf_sample_data_set_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sample surf_sample_data_source_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sample surf_sample_geology_code_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_geology_code_fkey FOREIGN KEY (geology_code) REFERENCES ref.lithology (code);

--
-- Name: sample surf_sample_geology_loged_by_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_geology_loged_by_fkey FOREIGN KEY (geology_logged_by) REFERENCES ref.person (code);

--
-- Name: sample surf_sample_grid_id_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_grid_id_fkey FOREIGN KEY (grid_id) REFERENCES ref.grid_id (grid_id);

--
-- Name: sample surf_sample_loaded_by_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: sample surf_sample_sample_type_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_sample_type_fkey FOREIGN KEY (sample_type) REFERENCES ref.sample_type (code);

--
-- Name: sample surf_sample_sampled_by_fkey; Type: FK CONSTRAINT; Schema: surf; Owner: postgres
--
ALTER TABLE ONLY surf.sample
    ADD CONSTRAINT surf_sample_sampled_by_fkey FOREIGN KEY (sampled_by) REFERENCES ref.person (code);

--
-- Name: TABLE sample; Type: ACL; Schema: surf; Owner: postgres
--
-- GRANT SELECT ON TABLE surf.sample TO fp;

--
-- PostgreSQL database dump complete
--
