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
-- __date__ = "2024/04/16"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------


-- basic types and constraints
CREATE DOMAIN assay.azimuth AS FLOAT CHECK(VALUE BETWEEN 0 AND 360);
CREATE DOMAIN assay.dip AS FLOAT CHECK(VALUE BETWEEN -90 AND 90);
-- 0 : reversed, 1 : normal, 2 : unknown
CREATE DOMAIN assay.polarity AS INT CHECK(VALUE = 0 OR VALUE = 1  OR VALUE = 2);
CREATE DOMAIN assay.kind AS VARCHAR CHECK(VALUE = 'line' OR VALUE = 'plane');

-- composite type
CREATE TYPE assay.spherical_data AS (azimuth assay.azimuth, dip assay.dip, polarity assay.polarity, kind assay.kind);
