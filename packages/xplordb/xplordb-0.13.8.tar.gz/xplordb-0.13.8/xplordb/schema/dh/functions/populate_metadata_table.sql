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
-- __date__ = "2024/04/11"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION dh.populate_metadata_table ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN

        IF (TG_OP = 'DELETE') THEN
            DELETE FROM dh.metadata WHERE hole_id = OLD.hole_id;
                
        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE dh.metadata SET hole_id = NEW.hole_id WHERE hole_id = OLD.hole_id;

        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO dh.metadata VALUES(NEW.hole_id);
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;

$function$