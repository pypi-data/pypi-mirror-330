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
-- Name: qgis_projects; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.qgis_projects (
    name text NOT NULL,
    metadata jsonb,
    content bytea
);

ALTER TABLE ref.qgis_projects OWNER TO postgres;

--
-- Name: TABLE qgis_projects; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.qgis_projects IS 'QGIS project table, in QGIS Project-Save To-PostgreSQL. http://www.bostongis.com/blog/index.php?/archives/271-New-in-QGIS-3.2-Save-Project-to-PostgreSQL.html';

--
-- Name: qgis_projects qgis_projects_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.qgis_projects
    ADD CONSTRAINT qgis_projects_pkey PRIMARY KEY (name);

--
-- PostgreSQL database dump complete
--
