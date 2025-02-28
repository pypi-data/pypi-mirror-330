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
-- Name: person; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.person (
    code character varying(3) NOT NULL,
    person character varying(100) NOT NULL,
    type character varying(30) NOT NULL,
    company character varying(50),
    data_set character varying(50),
    active boolean NOT NULL,
    loaded_by character varying(5),
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE ref.person OWNER TO postgres;

--
-- Name: TABLE person; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.person IS 'Reference table listing person codes';

--
-- Name: COLUMN person.code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.code IS 'Code for the person';

--
-- Name: COLUMN person.person; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.person IS 'Name of the person';

--
-- Name: COLUMN person.type; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.type IS 'Person type, that is what role they act, e.g. driller, geologist, surveyor etc.';

--
-- Name: COLUMN person.company; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.company IS 'Company the person works/ contracts for, represents or owns';

--
-- Name: COLUMN person.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.data_set IS 'Project the person is related to, optional';

--
-- Name: COLUMN person.active; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.active IS 'Boolean, is the person active, yes(1) or ticked, no(0) not ticked';

--
-- Name: COLUMN person.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN person.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.person.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (code);

--
-- Name: person ref_person_code_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.person
    ADD CONSTRAINT ref_person_code_key UNIQUE (code);

--
-- Name: person ref_person_company_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.person
    ADD CONSTRAINT ref_person_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);


--
-- Name: person ref_person_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.person
    ADD CONSTRAINT ref_person_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE person; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.person TO fp;

--
-- PostgreSQL database dump complete
--
