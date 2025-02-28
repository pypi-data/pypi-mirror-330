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
-- Name: lith; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.lith (
    data_set character varying(30) NOT NULL,
    hole_id character varying(30) NOT NULL,
    from_m numeric NOT NULL,
    to_m numeric NOT NULL,
    lith_code_1 character varying(15),
    lith_code_2 character varying(15),
    lith_code_3 character varying(15),
    lith_code_4 character varying(15),
    comment character varying(1000),
    data_source character varying(50),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_geol_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.lith OWNER TO postgres;

--
-- Name: TABLE lith; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.lith IS 'Down hole drill hole geology/ lithologytable';

--
-- Name: COLUMN lith.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.data_set IS 'Data set for the down hole geology occurance, should be the same data_set for the hole_id';

--
-- Name: COLUMN lith.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN lith.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the geology/ lithology occurs';

--
-- Name: COLUMN lith.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.to_m IS 'Ending distance in metres(m) down the drill hole from the collar the geology/ lithology occurs';

--
-- Name: COLUMN lith.lith_code_1; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.lith_code_1 IS 'Lithology code, see ref.lithology';

--
-- Name: COLUMN lith.lith_code_2; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.lith_code_2 IS 'see ref.lithology';

--
-- Name: COLUMN lith.lith_code_3; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.lith_code_3 IS 'see ref.lithology';

--
-- Name: COLUMN lith.lith_code_4; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.lith_code_4 IS 'see ref.lithology';

--
-- Name: COLUMN lith.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.comment IS 'Any comment';

--
-- Name: COLUMN lith.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.data_source IS 'The source of the information for the lithology occurance, see ref.data_source';

--
-- Name: COLUMN lith.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN lith.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN lith.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN lith.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.lith.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: lith lith_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lith_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: lith dh_geol_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT dh_geol_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: lith dh_geol_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT dh_geol_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: lith dh_geol_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT dh_geol_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: lith dh_geol_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT dh_geol_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: lith lith_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lith_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: lith lithology_code_1_foreign_key; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lithology_code_1_foreign_key FOREIGN KEY (lith_code_1) REFERENCES ref.lithology (code);

--
-- Name: lith lithology_code_2_foreign_key; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lithology_code_2_foreign_key FOREIGN KEY (lith_code_2) REFERENCES ref.lithology (code);

--
-- Name: lith lithology_code_3_foreign_key; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lithology_code_3_foreign_key FOREIGN KEY (lith_code_3) REFERENCES ref.lithology (code);

--
-- Name: lith lithology_code_4_foreign_key; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.lith
    ADD CONSTRAINT lithology_code_4_foreign_key FOREIGN KEY (lith_code_4) REFERENCES ref.lithology (code);

--
-- Name: TABLE lith; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.lith TO fp;

--
-- PostgreSQL database dump complete
--
