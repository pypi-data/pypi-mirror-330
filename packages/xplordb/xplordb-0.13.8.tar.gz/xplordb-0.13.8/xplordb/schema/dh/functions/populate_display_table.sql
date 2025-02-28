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
-- __authors__ = ["vlarmet"]
-- __contact__ = "vincent.larmet@apeiron.technology"
-- __date__ = "2024/03/18"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION dh.populate_display_table ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN
        --
        -- Create rows in emp_audit to reflect the operations performed on emp,
        -- making use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM display.display_collar WHERE data_set = OLD.data_set AND hole_id = OLD.hole_id;
                
        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE display.display_collar SET data_set = NEW.data_set WHERE data_set = NEW.data_set AND hole_id = NEW.hole_id;
            UPDATE display.display_collar SET hole_id = NEW.hole_id WHERE data_set = NEW.data_set AND hole_id = NEW.hole_id;
            UPDATE display.display_collar SET eoh = NEW.eoh WHERE data_set = NEW.data_set AND hole_id = NEW.hole_id;
            UPDATE display.display_collar SET planned_eoh = NEW.planned_eoh WHERE data_set = NEW.data_set AND hole_id = NEW.hole_id;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO display.display_collar VALUES(NEW.data_set, NEW.hole_id, NEW.eoh, NEW.planned_eoh, NULL, NULL);
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;

$function$
