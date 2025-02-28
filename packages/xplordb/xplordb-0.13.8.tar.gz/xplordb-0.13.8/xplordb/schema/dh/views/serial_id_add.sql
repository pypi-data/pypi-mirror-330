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

--
-- Name: serial_id_add; Type: VIEW; Schema: dh; Owner: postgres
--
CREATE VIEW dh.serial_id_add AS SELECT DISTINCT ON (constraint_column_usage.table_name)
    (('ALTER TABLE dh.'::text || (constraint_column_usage.table_name)::text) || ' ADD id serial;'::text)
FROM
    information_schema.constraint_column_usage
WHERE (((constraint_column_usage.table_name)::text IN (
            SELECT
                tables.table_name
            FROM
                information_schema.tables
            WHERE ((tables.table_type)::text = 'BASE TABLE'::text)))
    AND ((constraint_column_usage.table_schema)::text = 'dh'::text)
    AND ((constraint_column_usage.constraint_name)::text ~~* '%pkey%'::text)
    AND ((constraint_column_usage.column_name)::text !~~ 'id_'::text))
ORDER BY
    constraint_column_usage.table_name;

ALTER TABLE dh.serial_id_add OWNER TO postgres;

--
-- Name: TABLE serial_id_add; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.serial_id_add TO fp;

--
-- PostgreSQL database dump complete
--
