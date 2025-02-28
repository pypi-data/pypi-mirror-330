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

CREATE OR REPLACE FUNCTION ref.update_lab_method_code ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN
    WITH to_insert AS (
        SELECT DISTINCT
            lab_method_code
        FROM
            ref.lab_method m
        WHERE
            NOT (EXISTS (
                    SELECT
                        NULL::text AS unknown
                    FROM
                        ref.lab_method_code c
                    WHERE
                        m.lab_method_code = c.lab_method_code))
            GROUP BY
                lab_method_code)
    INSERT INTO ref.lab_method_code (lab_method_code)
    SELECT
        *
    FROM
        to_insert;
    RETURN NEW;
END;
$function$
