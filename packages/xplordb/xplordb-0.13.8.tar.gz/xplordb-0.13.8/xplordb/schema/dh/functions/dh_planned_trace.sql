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
-- __date__ = "2024/03/15"
-- __license__ = "AGPLv3"

CREATE OR REPLACE FUNCTION dh.dh_planned_trace (character varying, character varying)
    RETURNS void
    LANGUAGE sql
    AS $function$
  
  WITH surv as 
-- Surveys
  (
    SELECT * FROM
(SELECT hole_id, 0.0 as depth_m, dip, azimuth
 FROM dh.collar 
 WHERE hole_id = $2
UNION
SELECT hole_id , planned_eoh as depth_m, dip, azimuth
FROM dh.collar
WHERE hole_id = $2) foo
WHERE depth_m is not null
ORDER BY depth_m
 
),
-- collar projected in planar coordinates (3857 if srid is not cartesian)
proj_collar as (
SELECT hole_id, data_set, st_x(proj_planned_loc) as planned_x, st_y(proj_planned_loc) as planned_y, st_z(proj_planned_loc) as planned_z, planned_eoh from dh.collar
),
-- planar srid
planar_srid as (
  SELECT st_srid(proj_geom) as srid from dh.collar WHERE hole_id = $2 AND data_set = $1 
),

-- change survey data structure (interval-like) and compute intermediate values
from_ as(
SELECT hole_id, depth_m as d1, radians(dip+90.0) as dip1, radians(azimuth) as az1, row_number() OVER(ORDER BY depth_m) as rank FROM surv
),
to_ as(
SELECT depth_m as d2, radians(dip+90.0) as dip2, radians(azimuth) as az2, row_number() OVER(ORDER BY depth_m) - 1 as rank FROM surv
),
-- compute cl and dl
tmp1 as (
SELECT hole_id, d1, d2,
dip1, dip2, az1, az2,
d2 - d1 as cl, 
acos(cos(dip2-dip1) - (sin(dip1)*sin(dip2)) * (1 - cos(az2 - az1))) as dl
FROM from_ 
join to_
on from_.rank = to_.rank
),
-- compute rf
tmp2 as (
SELECT *,
CASE WHEN dl != 0.0 THEN tan(dl/2) * (2/dl)
ELSE 1.0
END AS rf
FROM tmp1
),
-- join x,y,z coordinates of collar
tmp3 as (
SELECT * FROM tmp2
left join (SELECT hole_id, planned_x as x, planned_y as y, planned_z as z FROM proj_collar) foo
on tmp2.hole_id = foo.hole_id
),
-- compute deltas
tmp4 as (
SELECT *,
((sin(dip1) * sin(az1)) + (sin(dip2) * sin(az2))) * (rf * (cl/2)) as d_x,
((sin(dip1) * cos(az1)) + (sin(dip2) * cos(az2))) * (rf * (cl/2))  as d_y,
-(cos(dip1) + cos(dip2) ) * (cl/2) * rf as d_z
FROM tmp3
ORDER BY d1
),
-- compute cumulative deltas
tmp5 as (
SELECT *,
sum(d_x) OVER (ORDER BY d1) as cumsum_x,
sum(d_y) OVER (ORDER BY d1) as cumsum_y,
sum(d_z) OVER (ORDER BY d1) as cumsum_z
FROM tmp4
),
-- create a new table with point's x,y,z by row and add origin point
final as (
SELECT planned_x as current_x, planned_y as current_y, planned_z as current_z, 0.0 as depth_m FROM proj_collar WHERE hole_id = $2 AND data_set = $1
UNION
SELECT x + cumsum_x as current_x, 
y + cumsum_y as current_y,
z + cumsum_z as current_z,
d2 as depth_m
FROM tmp5
ORDER BY current_z DESC
)
-- update collar table with created geometry
UPDATE dh.collar 
SET planned_trace = CASE WHEN (SELECT COUNT(*) FROM tmp5) = 0 OR (SELECT planned_eoh FROM dh.collar WHERE hole_id = $2 AND data_set = $1) is NULL OR (SELECT planned_eoh FROM dh.collar WHERE hole_id = $2 AND data_set = $1) = 0
THEN NULL
ELSE
(SELECT 
st_transform(st_forcecurve(st_makeline(st_setsrid(st_makepoint(current_x, current_y, current_z, depth_m), ((SELECT srid from planar_srid))))), 4326) as trace
 FROM final)
 END,
proj_planned_trace = CASE WHEN (SELECT COUNT(*) FROM tmp5) = 0 OR (SELECT planned_eoh FROM dh.collar WHERE hole_id = $2 AND data_set = $1) is NULL OR (SELECT planned_eoh FROM dh.collar WHERE hole_id = $2 AND data_set = $1) = 0
THEN NULL
ELSE
(SELECT 
st_transform(st_forcecurve(st_makeline(st_setsrid(st_makepoint(current_x, current_y, current_z, depth_m), (SELECT srid from planar_srid)))), (SELECT srid from planar_srid)) as trace
 FROM final)
 END
 WHERE hole_id = $2 AND data_set = $1

$function$
