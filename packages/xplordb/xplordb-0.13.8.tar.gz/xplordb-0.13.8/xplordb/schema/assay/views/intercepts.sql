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
-- Name: intercepts; Type: VIEW; Schema: assay; Owner: postgres
--
CREATE VIEW assay.intercepts AS
WITH holes AS (
    SELECT
        collar_view.hole_id
    FROM
        dh.collar_view
),
results AS (
    SELECT
        assay.hole_id,
        assay.from_m,
        assay.to_m,
        assay. "Cu",
        assay. "Pb",
        assay. "Zn",
        assay. "Ag",
        assay. "Au",
        assay. "Co",
        assay. "Sb",
        assay. "S",
        assay. "Fe",
        assay. "As",
        assay.sample_type,
        assay.sample_method
    FROM
        dh.assay
    WHERE ((assay.sample_id)::text IN (
            SELECT
                sample.sample_id
            FROM
                dh.sample
            WHERE ((sample.hole_id)::text IN (
                    SELECT
                        holes.hole_id
                    FROM
                        holes))))
),
summary_results AS (
    SELECT
        CASE WHEN (a.from_m = lag(a.to_m) OVER n_win) THEN
            currval('dh.results_seq'::regclass)
        ELSE
            nextval('dh.results_seq'::regclass)
        END AS intercept,
        a.hole_id,
        a.from_m,
        a.to_m,
        (a.to_m - a.from_m) AS interval_,
    (abs(a. "Cu") / (10000)::double precision) AS "Cu%",
    (abs(a. "Pb") / (10000)::double precision) AS "Pb%",
(abs(a. "Zn") / (10000)::double precision) AS "Zn%",
abs(a. "Ag") AS "Ag g/t",
abs(a. "Au") AS "Au g/t",
abs(a. "Co") AS co_ppm,
abs(a. "Sb") AS sb_ppm,
abs((a. "S" / (10000)::double precision)) AS s_pct,
abs((a. "Fe" / (10000)::double precision)) AS fe_pct,
abs((a. "As" / (10000)::double precision)) AS as_pct,
a.sample_type,
a.sample_method,
c.hole_type
FROM
    results a,
    dh.collar c
    WHERE (((a. "Cu" > (1000)::double precision)
            OR ((a. "Pb" + a. "Zn") > (1000)::double precision)
            OR (a. "Ag" > (10)::double precision)
            OR (a. "Au" > (0.3)::double precision))
        AND ((a.hole_id)::text = (c.hole_id)::text))
WINDOW n_win AS (PARTITION BY a.hole_id ORDER BY a.hole_id,
    a.from_m)
),
sequence_set AS (
    SELECT
        setval('dh.results_seq'::regclass, (1)::bigint, FALSE) AS setval
),
intercepts AS (
    SELECT DISTINCT ON (summary_results.intercept)
        summary_results.hole_id,
        summary_results.intercept AS intercept_number,
        min(summary_results.from_m) OVER win AS start_m,
            max(summary_results.to_m) OVER win AS end_m,
                sum(summary_results.interval_) OVER win AS m,
                    (sum((summary_results.interval_ * summary_results. "Cu%")) OVER win / sum(summary_results.interval_) OVER win) AS "Cu%",
                            (sum((summary_results.interval_ * summary_results. "Pb%")) OVER win / sum(summary_results.interval_) OVER win) AS "Pb%",
                                    (sum((summary_results.interval_ * summary_results. "Zn%")) OVER win / sum(summary_results.interval_) OVER win) AS "Zn%",
                                            (sum((summary_results.interval_ * summary_results. "Ag g/t")) OVER win / sum(summary_results.interval_) OVER win) AS "Ag g/t",
                                                    (sum((summary_results.interval_ * summary_results. "Au g/t")) OVER win / sum(summary_results.interval_) OVER win) AS "Au g/t",
                                                            summary_results.sample_type,
                                                            summary_results.sample_method,
                                                            summary_results.hole_type
                                                        FROM
                                                            summary_results
WINDOW win AS (PARTITION BY summary_results.intercept))
SELECT
    intercepts.hole_id,
    intercepts.intercept_number,
    intercepts.start_m,
    intercepts.end_m,
    intercepts.m,
    intercepts. "Cu%",
    intercepts. "Pb%",
    intercepts. "Zn%",
    intercepts. "Ag g/t",
    intercepts. "Au g/t",
    intercepts.sample_type,
    intercepts.sample_method,
    intercepts.hole_type,
    (((((((((((((((intercepts.hole_id)::text || '  '::text) || (intercepts.m)::numeric(5, 2)) || 'm @ '::text) || (intercepts. "Cu%")::numeric(5, 2)) || '% Cu, '::text) || (intercepts. "Pb%")::numeric(5, 2)) || '% Pb, '::text) || (intercepts. "Zn%")::numeric(5, 2)) || '% Zn, '::text) || (intercepts. "Ag g/t")::numeric(5, 1)) || 'g/t Ag'::text) || ' from '::text) || intercepts.start_m) || 'm'::text) AS text
FROM
    intercepts;

ALTER TABLE assay.intercepts OWNER TO postgres;

--
-- Name: VIEW intercepts; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON VIEW assay.intercepts IS 'Example of a query to report a summary of siginificant assay intercepts';

--
-- PostgreSQL database dump complete
--
