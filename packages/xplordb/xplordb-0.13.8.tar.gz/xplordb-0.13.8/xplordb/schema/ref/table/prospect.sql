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
-- Name: prospect; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.prospect (
    data_set character varying(20) NOT NULL,
    prospect character varying(50) NOT NULL,
    description character varying(300),
    company character varying(50) NOT NULL,
    active boolean NOT NULL,
    active_date_start timestamp with time zone,
    active_date_end timestamp with time zone,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date date DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    label character varying(80),
    resource character varying,
    commodity character varying(80),
    label_x double precision,
    label_y double precision,
    label_font integer,
    geom public.geometry(point, 4326),
    significance smallint,
    drill_code character varying(3),
    "group" character varying(40),
    geom_area public.geometry(polygon, 4326)
);

ALTER TABLE ref.prospect OWNER TO postgres;

--
-- Name: TABLE prospect; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.prospect IS 'Reference table listing prospects for dh.collar.prospects';

--
-- Name: COLUMN prospect.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.data_set IS 'Data set for the prospect, see ref.data_set';

--
-- Name: COLUMN prospect.prospect; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.prospect IS 'The prospect name. no spaces';

--
-- Name: COLUMN prospect.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.description IS 'Prospect description';

--
-- Name: COLUMN prospect.company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.company IS 'Company who owns the prospect';

--
-- Name: COLUMN prospect.active; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.active IS 'Boolean, is the prospect active, yes(1) or ticked, no(0) not ticked';

--
-- Name: COLUMN prospect.active_date_start; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.active_date_start IS 'The date the prospect became active';

--
-- Name: COLUMN prospect.active_date_end; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.active_date_end IS 'The date the prospect became inactive';

--
-- Name: COLUMN prospect.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN prospect.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN prospect.significance; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect.significance IS 'for display purposes i.e. only show significant prospects';

--
-- Name: COLUMN prospect."group"; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.prospect. "group" IS 'Prospect group. e.g. the state or area, i.e prospects that are near each other.';

--
-- Name: prospect prospect_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.prospect
    ADD CONSTRAINT prospect_pkey PRIMARY KEY (prospect);

--
-- Name: sidx_prospect_geom; Type: INDEX; Schema: ref; Owner: postgres
--
CREATE INDEX sidx_prospect_geom ON ref.prospect USING gist (geom);

--
-- Name: sidx_prospect_geom_area; Type: INDEX; Schema: ref; Owner: postgres
--
CREATE INDEX sidx_prospect_geom_area ON ref.prospect USING gist (geom_area);

--
-- Name: prospect prospect_company_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.prospect
    ADD CONSTRAINT prospect_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);

--
-- Name: prospect prospect_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.prospect
    ADD CONSTRAINT prospect_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: prospect prospect_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.prospect
    ADD CONSTRAINT prospect_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE prospect; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.prospect TO fp;

--
-- PostgreSQL database dump complete
--
