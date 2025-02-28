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
-- Name: batch; Type: TABLE; Schema: assay; Owner: postgres
--
CREATE TABLE assay.batch (
    lab character varying(40) NOT NULL,
    batch character varying(40) NOT NULL,
    dispatch_no character varying(40),
    lab_received_date timestamp with time zone,
    lab_completed_date timestamp with time zone,
    lab_sample_prep character varying(100),
    validated boolean,
    validated_by character varying(10),
    validated_date timestamp with time zone,
    data_source character varying(100) NOT NULL,
    import_script character varying(40),
    lab_sample_count integer,
    samples_imported integer,
    lab_result_count integer,
    result_import integer,
    over_range_total integer,
    qaqc_total integer,
    batch_status character varying(40),
    loaded_by character varying(10) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL
);

ALTER TABLE assay.batch OWNER TO postgres;

--
-- Name: TABLE batch; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON TABLE assay.batch IS 'Sample batch information table';

--
-- Name: COLUMN batch.lab; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab IS 'Code for laboratory relating to the sample batch, see ref.lab';

--
-- Name: COLUMN batch.batch; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.batch IS 'The laboratory batch number/ code';

--
-- Name: COLUMN batch.dispatch_no; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.dispatch_no IS 'Dispatch number';

--
-- Name: COLUMN batch.lab_received_date; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab_received_date IS 'Date the laboratory received the sample batch';

--
-- Name: COLUMN batch.lab_completed_date; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab_completed_date IS 'Date the laboratory reported the sample batch completed';

--
-- Name: COLUMN batch.lab_sample_prep; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab_sample_prep IS 'Sample preperation details for the batch';

--
-- Name: COLUMN batch.validated; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.validated IS 'Boolean, yes or no has the assay information for the batch been validated, e.g. against a hard/ paper copy or secure digital data';

--
-- Name: COLUMN batch.validated_by; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.validated_by IS 'Person who validated the assay information for the batch';

--
-- Name: COLUMN batch.validated_date; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.validated_date IS 'Date the assay information was validated';

--
-- Name: COLUMN batch.data_source; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.data_source IS 'Source file name';

--
-- Name: COLUMN batch.import_script; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.import_script IS 'Import script used to import assay data for the batch';

--
-- Name: COLUMN batch.lab_sample_count; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab_sample_count IS 'The number of samples reported by the laboratory';

--
-- Name: COLUMN batch.samples_imported; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.samples_imported IS 'Number of samples imported';

--
-- Name: COLUMN batch.lab_result_count; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.lab_result_count IS 'Number of results as reported by the laboratory, to compare with dh.assay_batch.result_import';

--
-- Name: COLUMN batch.result_import; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.result_import IS 'Number of results imported, to compare with dh.assay_batch.result_count';

--
-- Name: COLUMN batch.over_range_total; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.over_range_total IS 'Number of Over Range values for the batch';

--
-- Name: COLUMN batch.qaqc_total; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.qaqc_total IS 'Number of QAQC values for the batch';

--
-- Name: COLUMN batch.batch_status; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.batch_status IS 'The status of the batch';

--
-- Name: COLUMN batch.loaded_by; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN batch.load_date; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.batch.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: batch assay_batch_batch_key; Type: CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT assay_batch_batch_key UNIQUE (batch);

--
-- Name: batch batch_pkey; Type: CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT batch_pkey PRIMARY KEY (batch, lab);

--
-- Name: batch assay_batch_lab_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT assay_batch_lab_fkey FOREIGN KEY (lab) REFERENCES ref.lab (lab_code);

--
-- Name: batch assay_batch_loaded_by_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT assay_batch_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: batch assay_batch_source_file_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT assay_batch_source_file_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: batch assay_batch_validated_by_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.batch
    ADD CONSTRAINT assay_batch_validated_by_fkey FOREIGN KEY (validated_by) REFERENCES ref.person (code);

--
-- PostgreSQL database dump complete
--
