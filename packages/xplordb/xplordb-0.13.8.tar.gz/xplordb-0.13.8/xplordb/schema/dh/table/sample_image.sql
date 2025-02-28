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
-- Name: sample_image; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.sample_image (
    data_set character varying(30) NOT NULL,
    hole_id character varying(30) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    tray_no integer NOT NULL,
    image_type character varying(10) NOT NULL,
    comment character varying(80),
    image_location text,
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_core_trays_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.sample_image OWNER TO postgres;

--
-- Name: TABLE sample_image; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.sample_image IS 'RC chip tray and core tray image details';

--
-- Name: COLUMN sample_image.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.data_set IS 'Data set for the drill hole, see ref.data_set';

--
-- Name: COLUMN sample_image.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN sample_image.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sample_image.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN sample_image.tray_no; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.tray_no IS 'The tray number the core is physically stored in';

--
-- Name: COLUMN sample_image.image_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.image_type IS 'What the image is of: usually RC/RAB chip trays or Diamond drill hole core trays';

--
-- Name: COLUMN sample_image.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.comment IS 'Comment ';

--
-- Name: COLUMN sample_image.image_location; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.image_location IS 'The file location of the photographed image';

--
-- Name: COLUMN sample_image.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN sample_image.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN sample_image.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample_image.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample_image.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: sample_image check_interval_overlap_dh_core_trays; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT check_interval_overlap_dh_core_trays
    EXCLUDE USING gist (box(point((from_m + (0.0001)::double precision), (from_m + (0.0001)::double precision)), point((to_m - (0.0001)::double precision), (to_m - (0.0001)::double precision))) WITH &&, hole_id WITH =);

--
-- Name: sample_image dh_core_trays_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT dh_core_trays_pkey PRIMARY KEY (hole_id, from_m, to_m, tray_no);

--
-- Name: sample_image check_from_m_dh_core_trays; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_core_trays
    BEFORE INSERT OR UPDATE OF from_m ON dh.sample_image
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: sample_image check_to_m_dh_core_trays; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_core_trays
    BEFORE INSERT OR UPDATE OF to_m ON dh.sample_image
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: sample_image trace_row_sample_image; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_sample_image
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.sample_image
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: sample_image dh_sample_image_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT dh_sample_image_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sample_image dh_sample_image_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT dh_sample_image_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: sample_image sample_image_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT sample_image_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: sample_image sample_image_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample_image
    ADD CONSTRAINT sample_image_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
