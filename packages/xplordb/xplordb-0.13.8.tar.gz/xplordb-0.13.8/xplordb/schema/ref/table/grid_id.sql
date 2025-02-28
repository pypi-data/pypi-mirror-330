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
-- Name: grid_id; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.grid_id (
    grid_id character varying(10) NOT NULL,
    srid integer,
    description character varying(200) NOT NULL,
    loaded_by character varying(10) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.grid_id OWNER TO postgres;

--
-- Name: TABLE grid_id; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.grid_id IS 'Reference table listing grid identification codes';

--
-- Name: COLUMN grid_id.grid_id; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.grid_id.grid_id IS 'Grid identification(id) number/ code';

--
-- Name: COLUMN grid_id.srid; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.grid_id.srid IS 'Spatial Reference System Identifier, EPSG suggested see https://en.wikipedia.org/wiki/SRID';

--
-- Name: COLUMN grid_id.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.grid_id.description IS 'Description of the grid';

--
-- Name: COLUMN grid_id.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.grid_id.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN grid_id.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.grid_id.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: grid_id grid_id_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.grid_id
    ADD CONSTRAINT grid_id_pkey PRIMARY KEY (grid_id);

--
-- Name: grid_id ref_grid_id_id_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.grid_id
    ADD CONSTRAINT ref_grid_id_id_key UNIQUE (grid_id);

--
-- Name: grid_id grid_id_srid_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.grid_id
    ADD CONSTRAINT grid_id_srid_fkey FOREIGN KEY (srid) REFERENCES public.spatial_ref_sys (srid);

--
-- Name: grid_id ref_grid_id_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.grid_id
    ADD CONSTRAINT ref_grid_id_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE grid_id; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.grid_id TO fp;

--
-- PostgreSQL database dump complete
--
