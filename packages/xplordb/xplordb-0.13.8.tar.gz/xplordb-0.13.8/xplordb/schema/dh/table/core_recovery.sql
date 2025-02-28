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
-- Name: core_recovery; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.core_recovery (
    data_set character varying(30) NOT NULL,
    hole_id character varying(30) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    interval_m real,
    core_recovered_m real,
    recovery_pct real,
    rqd_m real,
    rqd_pct real,
    core_diameter character varying(10),
    core_orientated boolean,
    comment character varying(100),
    data_source character varying(50) NOT NULL,
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_core_recovery_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.core_recovery OWNER TO postgres;

--
-- Name: TABLE core_recovery; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.core_recovery IS 'Down hole drill hole core recovery table';

--
-- Name: COLUMN core_recovery.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.data_set IS 'Data set for the core recovery observation, see ref.data_set';

--
-- Name: COLUMN core_recovery.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.hole_id IS 'Drill hole identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id ';

--
-- Name: COLUMN core_recovery.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.from_m IS 'Starting distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN core_recovery.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.to_m IS 'Ending distance in metres(m) down the drill hole from the collar';

--
-- Name: COLUMN core_recovery.interval_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.interval_m IS 'The down hole depth interval or the interval between from_m and to_m';

--
-- Name: COLUMN core_recovery.core_recovered_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.core_recovered_m IS 'Down hole length of actual core recovered';

--
-- Name: COLUMN core_recovery.recovery_pct; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.recovery_pct IS 'The actual amount of core recovered in percent';

--
-- Name: COLUMN core_recovery.rqd_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.rqd_m IS 'The sum of length of solid, cylindrical core pieces greater than 100mm this relates to the RQD (rock quality designation) of the down hole core interval';

--
-- Name: COLUMN core_recovery.rqd_pct; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.rqd_pct IS 'The actual RQD (rock quality designation) which is defined in percent, i.e. rqd_m devided by interval_m';

--
-- Name: COLUMN core_recovery.core_diameter; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.core_diameter IS 'The diameter of the core in milimetres (mm)';

--
-- Name: COLUMN core_recovery.core_orientated; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.core_orientated IS 'Boolean, yes or no was the core orientated';

--
-- Name: COLUMN core_recovery.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.comment IS 'Any comment';

--
-- Name: COLUMN core_recovery.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.data_source IS 'Source of the core recovery information';

--
-- Name: COLUMN core_recovery.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN core_recovery.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN core_recovery.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN core_recovery.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.core_recovery.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: core_recovery core_recovery_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT core_recovery_pkey PRIMARY KEY (hole_id, from_m, to_m);

--
-- Name: core_recovery dh_core_recovery_hole_id_from_m_key; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT dh_core_recovery_hole_id_from_m_key UNIQUE (hole_id, from_m);

--
-- Name: interval_dh_core_recovery_idx; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX interval_dh_core_recovery_idx ON dh.core_recovery USING btree (hole_id, from_m, to_m);

--
-- Name: core_recovery check_from_m_dh_core_recovery; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_core_recovery
    BEFORE INSERT OR UPDATE OF from_m ON dh.core_recovery
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: core_recovery check_to_m_dh_core_recovery; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_core_recovery
    BEFORE INSERT OR UPDATE OF to_m ON dh.core_recovery
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: core_recovery trace_row_core_recovery; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_core_recovery
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.core_recovery
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();

--
-- Name: core_recovery data_set_foreign_key; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT data_set_foreign_key FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: core_recovery dh_core_recovery_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT dh_core_recovery_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: core_recovery dh_core_recovery_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT dh_core_recovery_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: core_recovery dh_core_recovery_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT dh_core_recovery_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: core_recovery dh_core_recovery_logged_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.core_recovery
    ADD CONSTRAINT dh_core_recovery_logged_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: TABLE core_recovery; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.core_recovery TO fp;

--
-- PostgreSQL database dump complete
--
