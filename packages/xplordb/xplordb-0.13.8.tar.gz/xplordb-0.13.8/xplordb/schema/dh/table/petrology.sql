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
-- Name: petrology; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.petrology (
    data_set character varying(30) NOT NULL,
    hole_id character varying(50),
    sample_id character varying(50) NOT NULL,
    x double precision,
    y double precision,
    z real,
    grid_id character varying(50),
    local_east real,
    local_north real,
    local_rl real,
    local_grid_id character varying(50),
    lat double precision,
    lon double precision,
    ll_rl real,
    ll_grid_id character varying(50),
    sample_type character varying(30),
    from_m real,
    to_m real,
    lith_code character varying(50),
    description_type character varying(60) NOT NULL,
    description character varying(5000),
    comment character varying(1000),
    petrology_by character varying(5) NOT NULL,
    petrology_company character varying(100) NOT NULL,
    petrology_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    data_source character varying(100),
    data_source_page character varying(50),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE dh.petrology OWNER TO postgres;

--
-- Name: TABLE petrology; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.petrology IS 'Down hole drill hole petrology table';

--
-- Name: COLUMN petrology.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.data_set IS 'Data set for the petrology description, see ref.data_set';

--
-- Name: COLUMN petrology.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN petrology.sample_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.sample_id IS 'Sample Identification(id) number or code for the petrology sample';

--
-- Name: COLUMN petrology.x; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.x IS 'Horizontal distance east from grid origin of the petrology description';

--
-- Name: COLUMN petrology.y; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.y IS 'Horizontal distance north from grid origin of the petrology description';

--
-- Name: COLUMN petrology.z; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.z IS 'Vertical distance from grid origin of the petrology description';

--
-- Name: COLUMN petrology.grid_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.grid_id IS 'Co-ordinate reference system (CRS)/ grid identification code, see ref.grid_id';

--
-- Name: COLUMN petrology.local_east; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.local_east IS 'Horizontal distance east from local grid origin of the petrology description';

--
-- Name: COLUMN petrology.local_north; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.local_north IS 'Horizontal distance north from local grid origin of the petrology description';

--
-- Name: COLUMN petrology.local_rl; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.local_rl IS 'Vertical distance from grid origin of the petrology description';

--
-- Name: COLUMN petrology.local_grid_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.local_grid_id IS 'Co-ordinate reference system (CRS)/ grid identification code, see ref.grid_id';

--
-- Name: COLUMN petrology.lat; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.lat IS 'Latitude of the petrology description';

--
-- Name: COLUMN petrology.lon; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.lon IS 'Longitude of the petrology description';

--
-- Name: COLUMN petrology.ll_rl; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.ll_rl IS 'Relative level or elevation of the petrology description ';

--
-- Name: COLUMN petrology.ll_grid_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.ll_grid_id IS 'Co-ordinate reference system (CRS)/ grid identification code, see ref.grid_id';

--
-- Name: COLUMN petrology.sample_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.sample_type IS 'Type of sample, e.g. hand speciem, drill core, RC chips etc., see ref.sample_type';

--
-- Name: COLUMN petrology.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN petrology.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN petrology.lith_code; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.lith_code IS 'Lithology code, see ref.lithology';

--
-- Name: COLUMN petrology.description_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.description_type IS 'Type of petrology description, e.g. mineragraphic, petrology';

--
-- Name: COLUMN petrology.description; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.description IS 'Description of the petrology sample';

--
-- Name: COLUMN petrology.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.comment IS 'Any comment';

--
-- Name: COLUMN petrology.petrology_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.petrology_by IS 'Person who described the petrology';

--
-- Name: COLUMN petrology.petrology_company; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.petrology_company IS 'The company who described the petrology';

--
-- Name: COLUMN petrology.petrology_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.petrology_date IS 'The date the petrology sample was sent';

--
-- Name: COLUMN petrology.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.data_source IS 'The source of the petrology description, see ref.data_source';

--
-- Name: COLUMN petrology.data_source_page; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.data_source_page IS 'The page of the data source';

--
-- Name: COLUMN petrology.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN petrology.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.petrology.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: petrology dh_petrology_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT dh_petrology_pkey PRIMARY KEY (sample_id, description_type);

--
-- Name: petrology check_from_m_dh_petrology; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_petrology
    BEFORE INSERT OR UPDATE OF from_m ON dh.petrology
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: petrology check_to_m_dh_petrology; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_petrology
    BEFORE INSERT OR UPDATE OF to_m ON dh.petrology
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: petrology dh_petrology_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT dh_petrology_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: petrology dh_petrology_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT dh_petrology_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: petrology dh_petrology_sample_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT dh_petrology_sample_type_fkey FOREIGN KEY (sample_type) REFERENCES ref.sample_type (code);

--
-- Name: petrology petrology_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT petrology_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: petrology petrology_petrology_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT petrology_petrology_by_fkey FOREIGN KEY (petrology_by) REFERENCES ref.person (code);

--
-- Name: petrology petrology_petrology_company_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.petrology
    ADD CONSTRAINT petrology_petrology_company_fkey FOREIGN KEY (petrology_company) REFERENCES ref.company (company);

--
-- PostgreSQL database dump complete
--
