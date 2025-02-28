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

CREATE OR REPLACE FUNCTION dem.alos_cap_update_example (character varying)
    RETURNS TABLE (
        data_set character varying,
        hole_id character varying,
        x double precision,
        y double precision,
        z real,
        grid_id character varying,
        hole_type character varying,
        hole_status character varying,
        survey_method character varying,
        survey_date timestamp with time zone,
        surveyed_by_company character varying,
        prospect character varying,
        comment character varying,
        loaded_by character varying,
        rl_method character varying,
        dem_z double precision)
    LANGUAGE sql
    AS $function$
    WITH intersect_collar AS (
        --
        SELECT
            hole_id,
            public.ST_Value (rast, collar.geom) AS dem_z,
            z
        FROM
            dem.capricorn,
            dh.collar
        WHERE
            public.ST_Intersects (rast, collar.geom)
            --
            AND hole_id = $1)
    UPDATE
        dh.collar
    SET
        z = dem_z,
        rl_method = 'S033E145_AVE_DSM.tif'
    FROM
        intersect_collar
    WHERE (collar.hole_id = intersect_collar.hole_id)
    AND survey_method = 'gps'
RETURNING
    data_set,
    collar.hole_id,
    x,
    y,
    collar.z,
    grid_id,
    hole_type,
    hole_status,
    survey_method,
    survey_date,
    surveyed_by_company,
    prospect,
    "comment",
    loaded_by,
    rl_method,
    dem_z;

$function$
