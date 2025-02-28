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
-- Name: struc; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.struc (
    data_set character varying(20) NOT NULL,
    hole_id character varying(70) NOT NULL,
    structure character varying(100) NOT NULL,
    depth_m real NOT NULL,
    dip real,
    azimuth real,
    alpha real,
    beta real,
    data_source character varying(200) NOT NULL,
    comment character varying(1000),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    CONSTRAINT dh_struc_alpha_check CHECK (((alpha >= (0)::double precision) AND (alpha <= (90)::double precision))),
    CONSTRAINT dh_struc_azimuth_check CHECK (((azimuth >= (0)::double precision) AND (azimuth <= (360)::double precision))),
    CONSTRAINT dh_struc_beta_check CHECK (((beta >= (0)::double precision) AND (beta <= (360)::double precision))),
    CONSTRAINT dh_struc_dip_check CHECK (((dip >= (0)::double precision) AND (dip <= (90)::double precision)))
);

ALTER TABLE dh.struc OWNER TO postgres;

--
-- Name: TABLE struc; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.struc IS 'Down hole drill hole structure table';

--
-- Name: COLUMN struc.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.data_set IS 'The data set of the structural measurment/observation, see ref.data_sets';

--
-- Name: COLUMN struc.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.hole_id IS 'Drill hole identification(id) number/ code';

--
-- Name: COLUMN struc.structure; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.structure IS 'The type of structure measured/ observed, see ref.struc';

--
-- Name: COLUMN struc.depth_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.depth_m IS 'Depth (in metres) the down hole structural measurment was taken';

--
-- Name: COLUMN struc.dip; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.dip IS 'The dip of the structure as measured or calculated from alpha and beta core angles';

--
-- Name: COLUMN struc.azimuth; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.azimuth IS 'The azimuth of the structure as measured or calculated from alpha and beta core angles';

--
-- Name: COLUMN struc.alpha; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.alpha IS 'Taken where the structure corresponds with the reference ellipse';

--
-- Name: COLUMN struc.beta; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.beta IS 'Taken from where the orientation line cross refence line';

--
-- Name: COLUMN struc.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.data_source IS 'The source of the structural measurement, see ref.data_source';

--
-- Name: COLUMN struc.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.comment IS 'Any comment';

--
-- Name: COLUMN struc.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN struc.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN struc.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN struc.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.struc.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: struc struc_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT struc_pkey PRIMARY KEY (hole_id, depth_m, structure);

--
-- Name: struc check_depth_m_dh_struc; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_depth_m_dh_struc
    BEFORE INSERT OR UPDATE OF depth_m ON dh.struc
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_depth_m ();

--
-- Name: struc dh_struc_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT dh_struc_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: struc dh_struc_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT dh_struc_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: struc dh_struc_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT dh_struc_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: struc dh_struc_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT dh_struc_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: struc dh_struc_structure_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT dh_struc_structure_fkey FOREIGN KEY (structure) REFERENCES ref.struc (code);

--
-- Name: struc struc_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.struc
    ADD CONSTRAINT struc_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE struc; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.struc TO fp;

--
-- PostgreSQL database dump complete
--
