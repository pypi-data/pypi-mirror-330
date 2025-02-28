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
-- Name: vein; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.vein (
    data_set character varying(20) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m double precision NOT NULL,
    to_m double precision NOT NULL,
    v_1 character varying(10) NOT NULL,
    v1_per real,
    v_2 character varying(10),
    v2_per real,
    v_3 character varying,
    v3_per real,
    data_source character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_vein_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision))),
    CONSTRAINT dh_vein_check_num CHECK (((v1_per <= (100)::double precision) AND (v1_per > (0)::double precision) AND (v2_per <= (100)::double precision) AND (v2_per > (0)::double precision) AND (v3_per <= (100)::double precision) AND (v3_per > (0)::double precision) AND (from_m >= (0)::double precision) AND (to_m >= (0)::double precision) AND (from_m <= (800)::double precision) AND (to_m <= (800)::double precision)))
);

ALTER TABLE dh.vein OWNER TO postgres;

--
-- Name: TABLE vein; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.vein IS 'Down hole drill hole vein observations table';

--
-- Name: COLUMN vein.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.data_set IS 'Data set for the vein observation, see ref.data_set';

--
-- Name: COLUMN vein.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN vein.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.from_m IS 'Starting distance in metres(m) down the drill hole from the collar of the vein observation';

--
-- Name: COLUMN vein.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.to_m IS 'Ending distance in metres(m) down the drill hole from the collar of the vein observation';

--
-- Name: COLUMN vein.v_1; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v_1 IS 'Vein code';

--
-- Name: COLUMN vein.v1_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v1_per IS 'Proportion of the vein, in percent, the rock is composed of';

--
-- Name: COLUMN vein.v_2; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v_2 IS 'Vein code for second set of veins';

--
-- Name: COLUMN vein.v2_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v2_per IS 'Proportion of the vein, in percent, the rock is composed of for the second set of veins';

--
-- Name: COLUMN vein.v_3; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v_3 IS 'Vein code for third set of veins';

--
-- Name: COLUMN vein.v3_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.v3_per IS 'Proportion of the vein, in percent, the rock is composed of for the third set of veins';

--
-- Name: COLUMN vein.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.data_source IS 'The source of the vein observation information, see ref.data_source';

--
-- Name: COLUMN vein.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN vein.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN vein.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN vein.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.vein.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: vein vein_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT vein_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: vein check_from_m_dh_vein; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_vein
    BEFORE INSERT OR UPDATE OF from_m ON dh.vein
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: vein check_to_m_dh_vein; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_vein
    BEFORE INSERT OR UPDATE OF to_m ON dh.vein
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: vein trace_row_vein; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_vein
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.vein
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: vein dh_vein_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: vein dh_vein_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: vein dh_vein_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: vein dh_vein_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: vein dh_vein_v_1_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_v_1_fkey FOREIGN KEY (v_1) REFERENCES ref.minerals (code);

--
-- Name: vein dh_vein_v_2_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_v_2_fkey FOREIGN KEY (v_2) REFERENCES ref.minerals (code);

--
-- Name: vein dh_vein_v_3_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT dh_vein_v_3_fkey FOREIGN KEY (v_3) REFERENCES ref.minerals (code);

--
-- Name: vein vein_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.vein
    ADD CONSTRAINT vein_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE vein; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.vein TO fp;

--
-- PostgreSQL database dump complete
--
