--
-- Name: person ref_person_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.person
    ADD CONSTRAINT ref_person_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);