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
-- Name: sg; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.sg (
    data_set character varying(20) NOT NULL,
    sg_id character varying(20),
    hole_id character varying(20) NOT NULL,
    from_m numeric(6, 2) NOT NULL,
    to_m numeric(6, 2) NOT NULL,
    repeat character varying(20),
    sample_id character varying(20),
    sample_type character varying(20),
    sg_method character varying(20) NOT NULL,
    weight_wet_g numeric(6, 2),
    weight_dry_g numeric(6, 2),
    reading character varying(20) NOT NULL,
    units character varying(20) NOT NULL,
    comment character varying(100),
    data_source character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_sg_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::numeric))),
    CONSTRAINT dh_sg_check_num CHECK ((((from_m)::double precision >= (0)::double precision) AND ((to_m)::double precision >= (0)::double precision) AND ((from_m)::double precision <= (800)::double precision) AND ((to_m)::double precision <= (800)::double precision) AND ((weight_wet_g)::double precision >= (0)::double precision) AND ((weight_wet_g)::double precision >= (0)::double precision) AND ((weight_dry_g)::double precision >= (0)::double precision) AND ((weight_dry_g)::double precision >= (0)::double precision)))
);

ALTER TABLE dh.sg OWNER TO postgres;

--
-- Name: TABLE sg; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.sg IS 'Down hole drill hole specific gravity/ density table';

--
-- Name: COLUMN sg.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.data_set IS 'Data set for the specific gravity(SG) measurement, see ref.data_set';

--
-- Name: COLUMN sg.sg_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.sg_id IS 'The specific gravity(SG) identification number/ code ';

--
-- Name: COLUMN sg.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN sg.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sg.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sg.repeat; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.repeat IS 'Sample Identification(id) number/ code for the specific gravity measurement repeat';

--
-- Name: COLUMN sg.sample_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.sample_id IS 'Sample Identification(id) number/ code for the specific gravity measurement ';

--
-- Name: COLUMN sg.sample_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.sample_type IS 'Sample type that specific gravity(SG) measurement was taken, see ref.sample_type';

--
-- Name: COLUMN sg.sg_method; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.sg_method IS 'Method used to obtain the specific gravity(SG) measurement';

--
-- Name: COLUMN sg.weight_wet_g; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.weight_wet_g IS 'The weight of the sample in water';

--
-- Name: COLUMN sg.weight_dry_g; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.weight_dry_g IS 'The weight of the sample dry/ in air';

--
-- Name: COLUMN sg.reading; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.reading IS 'The specific gravity(SG) measurement';

--
-- Name: COLUMN sg.units; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.units IS 'Units of the specific gravity(SG) measurement';

--
-- Name: COLUMN sg.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.comment IS 'Any comment';

--
-- Name: COLUMN sg.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.data_source IS 'The source of the specific gravity(SG) measurement, see ref.data_source';

--
-- Name: COLUMN sg.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN sg.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN sg.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sg.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sg.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sg sg_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT sg_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: sg check_from_m_dh_sg; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_sg
    BEFORE INSERT OR UPDATE OF from_m ON dh.sg
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: sg check_to_m_dh_sg; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_sg
    BEFORE INSERT OR UPDATE OF to_m ON dh.sg
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: sg trace_row_sg; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_sg
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.sg
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: sg update_dh_sg_immersion_reading; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER update_dh_sg_immersion_reading
    AFTER INSERT OR UPDATE OF weight_dry_g,
    weight_wet_g ON dh.sg
    FOR EACH ROW
    EXECUTE FUNCTION dh.update_dh_sg_immersion ();

--
-- Name: sg dh_sg_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sg dh_sg_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sg dh_sg_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: sg dh_sg_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: sg dh_sg_sample_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_sample_type_fkey FOREIGN KEY (sample_type) REFERENCES ref.sample_type (code);

--
-- Name: sg dh_sg_unit_code_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT dh_sg_unit_code_fkey FOREIGN KEY (units) REFERENCES ref.units (code);

--
-- Name: sg sg_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT sg_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: sg sg_sg_method_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sg
    ADD CONSTRAINT sg_sg_method_fkey FOREIGN KEY (sg_method) REFERENCES ref.sg_method (code);

--
-- Name: TABLE sg; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.sg TO fp;

--
-- PostgreSQL database dump complete
--
