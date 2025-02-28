----------------------------------------------------------------------------
-- xplordb
-- 
-- Copyright (C) 2022  Apeiron / OpenLog
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
-- __authors__ = ["vlarmet"]
-- __contact__ = "vincent.larmet@apeiron.technology"
-- __date__ = "2024/04/10"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

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

CREATE TABLE dh.metadata (
    hole_id character varying(30) NOT NULL
);


ALTER TABLE ONLY dh.metadata ADD CONSTRAINT dh_metadata_unique UNIQUE(hole_id);
ALTER TABLE ONLY dh.metadata ADD CONSTRAINT dh_metadata_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

-- trigger to synchronize metadata table with dh.collar 
CREATE TRIGGER a_populate_metadata_table
AFTER INSERT OR DELETE OR UPDATE OF hole_id
ON dh.collar
FOR EACH ROW
EXECUTE FUNCTION dh.populate_metadata_table();
