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
-- Name: missing_samples; Type: VIEW; Schema: v; Owner: postgres
--
CREATE VIEW v.missing_samples AS
WITH sample AS (
    SELECT
        'qd'::text AS code,
        dh.data_set,
        dh.class,
        dh.sample_id
    FROM
        qa.dh
    UNION ALL
    SELECT
        'd'::text AS code,
        sample.data_set,
        sample.class,
        sample.sample_id
    FROM
        dh.sample
    UNION ALL
    SELECT
        's'::text AS code,
        sample.data_set,
        sample.class,
        sample.sample_id
    FROM
        surf.sample
    UNION ALL
    SELECT
        'qs'::text AS code,
        surf.data_set,
        surf.class,
        surf.sample_id
    FROM
        qa.surf
),
assay AS (
    SELECT
        'a'::text AS a_code,
        NULL::text AS a_data_set,
        assay.sample_id AS a_sample_id
    FROM
        assay.assay
    WHERE (assay.preferred < 3))
SELECT DISTINCT ON (s.sample_id, a.a_sample_id)
    s.code,
    s.data_set,
    s.class,
    s.sample_id,
    a.a_code,
    a.a_data_set,
    a.a_sample_id
FROM (sample s
    FULL JOIN assay a ON (((s.sample_id)::text = (a.a_sample_id)::text)))
WHERE ((s.sample_id IS NULL)
    OR (a.a_sample_id IS NULL));

ALTER TABLE v.missing_samples OWNER TO postgres;

--
-- PostgreSQL database dump complete
--
