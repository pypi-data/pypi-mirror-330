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

CREATE OR REPLACE FUNCTION dh.check_to_m ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    SET search_path TO 'dh'
    AS $function$
DECLARE
    max_drillhole real;
BEGIN
    SELECT
        cast(max_depth AS real) INTO max_drillhole
    FROM
        dh.collar_view
    WHERE
        collar_view.hole_id = NEW.hole_id;
    IF cast(NEW.to_m AS real) > max_drillhole THEN
        RAISE exception 'error depth exceeds maximum hole depth';
    ELSE
        RETURN NEW;
    END IF;
END;
$function$
