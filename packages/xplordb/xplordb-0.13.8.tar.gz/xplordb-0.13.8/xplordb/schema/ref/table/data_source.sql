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
-- Name: data_source; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.data_source (
    data_set character varying(20) NOT NULL,
    data_source character varying(100) NOT NULL,
    file_location character varying(300) NOT NULL,
    title character varying(300),
    author character varying(300) NOT NULL,
    report_date timestamp with time zone NOT NULL,
    comment character varying,
    loaded_by character (2) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    company character varying(200),
    pages character varying(20)
);

ALTER TABLE ref.data_source OWNER TO postgres;

--
-- Name: TABLE data_source; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.data_source IS 'Reference table detailing information data sources';

--
-- Name: COLUMN data_source.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.data_set IS 'The data set/ project of the data source, see ref.data_sets';

--
-- Name: COLUMN data_source.data_source; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.data_source IS 'The name or file name of the data source';

--
-- Name: COLUMN data_source.file_location; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.file_location IS 'The file location of the data source';

--
-- Name: COLUMN data_source.title; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.title IS 'The title of the data source or report';

--
-- Name: COLUMN data_source.author; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.author IS 'The full name of the author of the data source or report, for printing in reports and reference lists';

--
-- Name: COLUMN data_source.report_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.report_date IS 'The date of the report or data source';

--
-- Name: COLUMN data_source.comment; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.comment IS 'Any comment';

--
-- Name: COLUMN data_source.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN data_source.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN data_source.company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.company IS 'The company name the data source relates to, see ref.company';

--
-- Name: COLUMN data_source.pages; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.data_source.pages IS 'The relevant page(s) in the report or document';

--
-- Name: data_source data_source_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT data_source_pkey PRIMARY KEY (data_source);

--
-- Name: data_source ref_data_source_data_source_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT ref_data_source_data_source_key UNIQUE (data_source);

--
-- Name: data_source ref_data_source_company_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT ref_data_source_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);

--
-- Name: data_source ref_data_source_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT ref_data_source_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: data_source ref_data_source_data_source_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT ref_data_source_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: data_source ref_data_source_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.data_source
    ADD CONSTRAINT ref_data_source_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE data_source; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.data_source TO fp;

--
-- PostgreSQL database dump complete
--
