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
-- Name: capricorn; Type: TABLE; Schema: dem; Owner: postgres
--
CREATE TABLE dem.capricorn (
    rid integer NOT NULL,
    rast public.raster,
    CONSTRAINT enforce_height_rast CHECK ((public.st_height (rast) = 30)),
    CONSTRAINT enforce_nodata_values_rast CHECK ((public._raster_constraint_nodata_values (rast) = '{NULL}'::numeric[])),
    CONSTRAINT enforce_num_bands_rast CHECK ((public.st_numbands (rast) = 1)),
    CONSTRAINT enforce_out_db_rast CHECK ((public._raster_constraint_out_db (rast) = '{f}'::boolean[])),
    CONSTRAINT enforce_pixel_types_rast CHECK ((public._raster_constraint_pixel_types (rast) = '{16BSI}'::text[])),
    CONSTRAINT enforce_same_alignment_rast CHECK (public.st_samealignment (rast, '010000000065930C785634323F72BC9A78563432BFAAF3EFCDAB595D403691B5600BA638C000000000000000000000000000000000E610000001000100'::public.raster)),
    CONSTRAINT enforce_scalex_rast CHECK ((round((public.st_scalex (rast))::numeric, 10) = round(0.000277777777272717, 10))),
    CONSTRAINT enforce_scaley_rast CHECK ((round((public.st_scaley (rast))::numeric, 10) = round('-0.000277777777777772'::numeric, 10))),
    CONSTRAINT enforce_srid_rast CHECK ((public.st_srid (rast) = 4326)),
    CONSTRAINT enforce_width_rast CHECK ((public.st_width (rast) = 30))
);

ALTER TABLE dem.capricorn OWNER TO postgres;

--
-- Name: TABLE capricorn; Type: COMMENT; Schema: dem; Owner: postgres
--
COMMENT ON TABLE dem.capricorn IS 'original data is provided by JAXA https://www.eorc.jaxa.jp/ALOS/en/aw3d30';

--
-- Name: capricorn_rid_seq; Type: SEQUENCE; Schema: dem; Owner: postgres
--
CREATE SEQUENCE dem.capricorn_rid_seq
    AS integer START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE dem.capricorn_rid_seq OWNER TO postgres;

--
-- Name: capricorn_rid_seq; Type: SEQUENCE OWNED BY; Schema: dem; Owner: postgres
--
ALTER SEQUENCE dem.capricorn_rid_seq OWNED BY dem.capricorn.rid;

--
-- Name: capricorn rid; Type: DEFAULT; Schema: dem; Owner: postgres
--
ALTER TABLE ONLY dem.capricorn
    ALTER COLUMN rid SET DEFAULT nextval('dem.capricorn_rid_seq'::regclass);

--
-- Name: capricorn capricorn_pkey; Type: CONSTRAINT; Schema: dem; Owner: postgres
--
ALTER TABLE ONLY dem.capricorn
    ADD CONSTRAINT capricorn_pkey PRIMARY KEY (rid);

--
-- Name: capricorn enforce_max_extent_rast; Type: CHECK CONSTRAINT; Schema: dem; Owner: postgres
--
ALTER TABLE dem.capricorn
    ADD CONSTRAINT enforce_max_extent_rast CHECK ((public.st_envelope (rast) OPERATOR (public. @) '0103000020E61000000100000005000000AAF3EFCDAB595D40CF2A4FFAA4BF38C0AAF3EFCDAB595D403691B5600BA638C0C553AB8967655D403691B5600BA638C0C553AB8967655D40CF2A4FFAA4BF38C0AAF3EFCDAB595D40CF2A4FFAA4BF38C0'::public.geometry)) NOT VALID;

--
-- Name: capricorn_st_convexhull_idx; Type: INDEX; Schema: dem; Owner: postgres
--
CREATE INDEX capricorn_st_convexhull_idx ON dem.capricorn USING gist (public.st_convexhull (rast));

--
-- Name: TABLE capricorn; Type: ACL; Schema: dem; Owner: postgres
--
-- GRANT SELECT ON TABLE dem.capricorn TO fp;

--
-- PostgreSQL database dump complete
--
