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
-- Name: lease; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lease (
    data_set text,
    lease_id text NOT NULL,
    auth_id text,
    status text NOT NULL,
    stage text NOT NULL,
    grant_date timestamp with time zone,
    expire_date timestamp with time zone,
    owner text,
    owner_2 text,
    owner_3 text,
    as_date timestamp with time zone NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    geom public.geometry(MultiPolygon, 4326)
);

ALTER TABLE ref.lease OWNER TO postgres;

--
-- Name: TABLE lease; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lease IS 'Reference table listing lease information, and the geometry of the lease, historic leases and area drop offs are supported.';

--
-- Name: COLUMN lease.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.data_set IS 'Data set for the lease, see ref.data_sets';

--
-- Name: COLUMN lease.lease_id; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.lease_id IS 'Lease/ tenement identification(id) code ';

--
-- Name: COLUMN lease.auth_id; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.auth_id IS 'Lease/ tenement identification(id) code used by the relevant authority to obtain a match on a spatialy referenced table in the g. schema ';

--
-- Name: COLUMN lease.status; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.status IS 'The status of the lease, e.g. active, inactive';

--
-- Name: COLUMN lease.stage; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.stage IS 'A number indicating the time line of changes to the lease, earliest first';

--
-- Name: COLUMN lease.grant_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.grant_date IS 'Date the lease was granted';

--
-- Name: COLUMN lease.expire_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.expire_date IS 'Date the lease expires';

--
-- Name: COLUMN lease.owner; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.owner IS 'Owner of the lease, see ref.company';

--
-- Name: COLUMN lease.owner_2; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.owner_2 IS 'Owner two of the lease, see ref.company';

--
-- Name: COLUMN lease.owner_3; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.owner_3 IS 'Owner three of the lease, see ref.company';

--
-- Name: COLUMN lease.as_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.as_date IS 'Date the information was current';

--
-- Name: COLUMN lease.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN lease.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lease.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: lease lease_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT lease_pkey PRIMARY KEY (lease_id, stage, as_date);

--
-- Name: lease ref_lease_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT ref_lease_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: lease ref_lease_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT ref_lease_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: lease ref_lease_owner_2_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT ref_lease_owner_2_fkey FOREIGN KEY (owner_2) REFERENCES ref.company (company);

--
-- Name: lease ref_lease_owner_3_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT ref_lease_owner_3_fkey FOREIGN KEY (owner_3) REFERENCES ref.company (company);

--
-- Name: lease ref_lease_owner_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lease
    ADD CONSTRAINT ref_lease_owner_fkey FOREIGN KEY (OWNER) REFERENCES ref.company (company);

--
-- Name: TABLE lease; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lease TO fp;

--
-- PostgreSQL database dump complete
--
