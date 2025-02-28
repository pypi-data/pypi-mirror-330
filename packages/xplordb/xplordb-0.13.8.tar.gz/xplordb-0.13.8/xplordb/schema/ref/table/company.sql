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
-- Name: company; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.company (
    company character varying(100) NOT NULL,
    description character varying(200) NOT NULL,
    active boolean NOT NULL,
    loaded_by character varying(10),
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    company_type character varying(30)
);

ALTER TABLE ref.company OWNER TO postgres;

--
-- Name: TABLE company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.company IS 'Reference table listing companies';

--
-- Name: COLUMN company.company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.company IS 'Company name';

--
-- Name: COLUMN company.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.description IS 'Description of the company';

--
-- Name: COLUMN company.active; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.active IS 'Boolean, is the company active, yes(1) or ticked, no(0) not ticked';

--
-- Name: COLUMN company.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN company.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN company.company_type; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.company.company_type IS 'The type of company e.g. exploration, survey, drilling, dh_survey, geophysics';

--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (company);

--
-- Name: company ref_company_company_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.company
    ADD CONSTRAINT ref_company_company_key UNIQUE (company);

--
-- Name: TABLE company; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.company TO fp;

--
-- PostgreSQL database dump complete
--
