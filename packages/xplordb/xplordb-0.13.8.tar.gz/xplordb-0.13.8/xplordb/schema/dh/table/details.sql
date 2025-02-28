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
-- Name: details; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.details (
    data_set character varying(30) NOT NULL,
    hole_id character varying(30) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    parent_hole character varying(30),
    hole_type character varying(80),
    core_type character varying(10),
    hole_diameter numeric(6, 2),
    units character varying(30),
    comment character varying,
    loaded_by character varying(50) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    program character varying,
    date_start timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone,
    date_completed timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone,
    company character varying(80),
    drilling_company character varying(80),
    drill_rig character varying(100),
    driller character varying(80),
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_details_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.details OWNER TO postgres;

--
-- Name: TABLE details; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.details IS 'Down hole drill hole details table, includes details of drilling method, parent hole for wedges, hole diameter and drill program.';

--
-- Name: COLUMN details.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.data_set IS 'Data set for the drill hole, see ref.data_set';

--
-- Name: COLUMN details.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN details.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN details.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN details.parent_hole; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.parent_hole IS 'The parent hole identification(id) number/ code from dh.collar. Relevant to wedged holes';

--
-- Name: COLUMN details.hole_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.hole_type IS 'The hole type, see ref.hole_type';

--
-- Name: COLUMN details.core_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.core_type IS 'The core specification HQ, PQ etc.';

--
-- Name: COLUMN details.hole_diameter; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.hole_diameter IS 'The diameter of the hole, record the units (usually inches, cm or mm) of measurement in the units column';

--
-- Name: COLUMN details.units; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.units IS 'Units of the hole diameter measurement, see ref.units';

--
-- Name: COLUMN details.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.comment IS 'The drilling program ';

--
-- Name: COLUMN details.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN details.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN details.program; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.program IS 'The name of the drilling program/phase the hole was a part of, see ref.program';

--
-- Name: COLUMN details.date_start; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.date_start IS 'The date the section of the drill hole was started';

--
-- Name: COLUMN details.date_completed; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.date_completed IS 'The date the section of the drill hole was completed';

--
-- Name: COLUMN details.company; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.company IS 'The company that planned and commisioned the drill hole (the operator), see ref.company';

--
-- Name: COLUMN details.drilling_company; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.drilling_company IS 'The company or contractor who drilled the hole, see ref.company';

--
-- Name: COLUMN details.drill_rig; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.drill_rig IS 'Make, model, number of the drill rig';

--
-- Name: COLUMN details.driller; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.details.driller IS 'The person who drilled the hole, the driller, see ref.person';

--
-- Name: details check_interval_overlap_dh_details; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT check_interval_overlap_dh_details
    EXCLUDE USING gist (box(point((from_m + (0.0001)::double precision), (from_m + (0.0001)::double precision)), point((to_m - (0.0001)::double precision), (to_m - (0.0001)::double precision))) WITH &&, hole_id WITH =);

--
-- Name: details dh_details_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_pkey PRIMARY KEY (hole_id, from_m);

--
-- Name: details details_driller_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT details_driller_fkey FOREIGN KEY (driller) REFERENCES ref.person (code);

--
-- Name: details details_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT details_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: details details_parent_hole_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT details_parent_hole_fkey FOREIGN KEY (parent_hole) REFERENCES dh.collar (hole_id);

--
-- Name: details dh_details_company_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);

--
-- Name: details dh_details_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: details dh_details_driller_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_driller_fkey FOREIGN KEY (driller) REFERENCES ref.person (code);

--
-- Name: details dh_details_drilling_company_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_drilling_company_fkey FOREIGN KEY (drilling_company) REFERENCES ref.company (company);

--
-- Name: details dh_details_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: details dh_details_hole_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_hole_type_fkey FOREIGN KEY (hole_type) REFERENCES ref.hole_type (code);

--
-- Name: details dh_details_person_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_person_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: details dh_details_program_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_program_fkey FOREIGN KEY (program) REFERENCES ref.program (program);

--
-- Name: details dh_details_units_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.details
    ADD CONSTRAINT dh_details_units_fkey FOREIGN KEY (units) REFERENCES ref.units (code);

--
-- PostgreSQL database dump complete
--
