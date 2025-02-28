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
-- Name: event; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.event (
    data_set character varying(20) NOT NULL,
    hole_id character varying(50) NOT NULL,
    event character varying(4) NOT NULL,
    depth_m real NOT NULL,
    data_source character varying(100),
    comment character varying(100),
    logged_by character varying(5) DEFAULT "current_user" () NOT NULL,
    logged_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE dh.event OWNER TO postgres;

--
-- Name: TABLE event; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.event IS 'Down hole drill hole point events';

--
-- Name: COLUMN event.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.data_set IS 'Data set for the down hole event, should be the same data_set for the hole_id';

--
-- Name: COLUMN event.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.hole_id IS 'Drill hole Identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id';

--
-- Name: COLUMN event.event; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.event IS 'The event that occurs in the drill hole, see ref.event';

--
-- Name: COLUMN event.depth_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.depth_m IS 'Down hole depth where the event occurs in metres';

--
-- Name: COLUMN event.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.data_source IS 'The source of the information for the event, see ref.data_source';

--
-- Name: COLUMN event.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.comment IS 'Any comments';

--
-- Name: COLUMN event.logged_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.logged_by IS 'The person who logged the data, see ref.person';

--
-- Name: COLUMN event.logged_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.logged_date IS 'The date the data was logged';

--
-- Name: COLUMN event.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN event.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.event.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: event event_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (hole_id, depth_m);

--
-- Name: event check_depth_m_dh_event; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_depth_m_dh_event
    BEFORE INSERT OR UPDATE OF depth_m ON dh.event
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_depth_m ();

--
-- Name: event dh_event_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT dh_event_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: event dh_event_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT dh_event_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: event dh_event_event_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT dh_event_event_fkey FOREIGN KEY (event) REFERENCES ref.event (code);

--
-- Name: event dh_event_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT dh_event_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: event dh_event_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.event
    ADD CONSTRAINT dh_event_loaded_by_fkey FOREIGN KEY (logged_by) REFERENCES ref.person (code);

--
-- Name: TABLE event; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.event TO fp;

--
-- PostgreSQL database dump complete
--
