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

CREATE OR REPLACE FUNCTION dh.dog_leg (dip double precision, lead_dip double precision, azimuth_grid double precision, lead_azimuth_grid double precision)
    RETURNS double precision
    LANGUAGE plpgsql
    AS $function$
DECLARE
    dog_leg double precision;
BEGIN
    --xplordb - Mineral Exploration Database template/ system for Postgres/PostGIS. The project incorporates perl import scripts; drillling, surface and QA/QC data and more.
    --Copyright (C) 2017  Light Catcher Pty Ltd
    --This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    --This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
    --You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
    dog_leg := (acos((cos(radians(lead_dip - dip))) - ((sin(radians(dip))) * (sin(radians(lead_dip))) * (1 - (cos(radians(lead_azimuth_grid - azimuth_grid)))))));
    RETURN dog_leg;
END;
$function$
