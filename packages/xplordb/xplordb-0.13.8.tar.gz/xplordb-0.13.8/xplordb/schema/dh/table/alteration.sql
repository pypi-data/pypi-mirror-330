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
-- Name: alteration; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.alteration (
    data_set character varying(20) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m double precision NOT NULL,
    to_m double precision NOT NULL,
    alt_1 character varying(10) NOT NULL,
    alt1_per real NOT NULL,
    alt_2 character varying(10),
    alt2_per real,
    alt_3 character varying,
    alt3_per real,
    data_source character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_alteration_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision))),
    CONSTRAINT dh_alteration_check_per CHECK (((alt1_per <= (100)::double precision) AND (alt2_per <= (100)::double precision) AND (alt3_per <= (100)::double precision)))
);

ALTER TABLE dh.alteration OWNER TO postgres;

--
-- Name: TABLE alteration; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.alteration IS 'Down hole drill hole alteration table';

--
-- Name: COLUMN alteration.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.data_set IS 'Data set for the observed alteration, see ref.data_set';

--
-- Name: COLUMN alteration.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN alteration.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN alteration.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN alteration.alt_1; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt_1 IS 'Code for the alteration occurance, see ref.alteration';

--
-- Name: COLUMN alteration.alt1_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt1_per IS 'Proportion of the alteration, in percent, the rock is composed of';

--
-- Name: COLUMN alteration.alt_2; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt_2 IS 'Code for the alteration occurance, see ref.alteration';

--
-- Name: COLUMN alteration.alt2_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt2_per IS 'Proportion of the alteration, in percent, the rock is composed of';

--
-- Name: COLUMN alteration.alt_3; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt_3 IS 'Code for the alteration occurance, see ref.alteration';

--
-- Name: COLUMN alteration.alt3_per; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.alt3_per IS 'Proportion of the alteration, in percent, the rock is composed of';

--
-- Name: COLUMN alteration.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.data_source IS 'The source of the alteration observation information, see ref.data_source';

--
-- Name: COLUMN alteration.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN alteration.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN alteration.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN alteration.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.alteration.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: alteration alteration_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT alteration_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: alteration dh_alteration_hole_id_from_m_alt_1_key; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_hole_id_from_m_alt_1_key UNIQUE (hole_id, from_m, alt_1);

--
-- Name: fki_dh_alteration_alt_1_fkey; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX fki_dh_alteration_alt_1_fkey ON dh.alteration USING btree (alt_1);

--
-- Name: interval_dh_alteration_idx; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX interval_dh_alteration_idx ON dh.alteration USING btree (hole_id, from_m, to_m);

--
-- Name: alteration check_from_m_dh_alteration; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_alteration
    BEFORE INSERT OR UPDATE OF from_m ON dh.alteration
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: alteration check_to_m_dh_alteration; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_alteration
    BEFORE INSERT OR UPDATE OF to_m ON dh.alteration
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: alteration trace_row_alteration; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_alteration
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.alteration
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: alteration dh_alteration_alt_1_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_alt_1_fkey FOREIGN KEY (alt_1) REFERENCES ref.minerals (code);

--
-- Name: alteration dh_alteration_alt_2_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_alt_2_fkey FOREIGN KEY (alt_2) REFERENCES ref.minerals (code);

--
-- Name: alteration dh_alteration_alt_3_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_alt_3_fkey FOREIGN KEY (alt_3) REFERENCES ref.minerals (code);

--
-- Name: alteration dh_alteration_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: alteration dh_alteration_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: alteration dh_alteration_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: alteration dh_alteration_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.alteration
    ADD CONSTRAINT dh_alteration_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: TABLE alteration; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.alteration TO fp;

--
-- PostgreSQL database dump complete
--
