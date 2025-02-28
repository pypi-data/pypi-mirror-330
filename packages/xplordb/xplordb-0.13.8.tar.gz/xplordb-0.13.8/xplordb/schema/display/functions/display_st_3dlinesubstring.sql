CREATE or REPLACE FUNCTION display.ST_3DLineSubstring(
line_geom public.GEOMETRY, start_fraction float, end_fraction float
)
RETURNS setof public.GEOMETRY AS $$
DECLARE 
srid INTEGER = st_srid(line_geom);
n_pts INTEGER;
vertex public.GEOMETRY;
next_vertex public.GEOMETRY;
vertices public.GEOMETRY [];
i INTEGER;
distance float = 0.0;
d float;
fraction float;
start_length float = st_3dlength(line_geom) * start_fraction;
end_length float = st_3dlength(line_geom) * end_fraction;
start_vertex public.GEOMETRY;
end_vertex public.GEOMETRY;
new_x float;
new_y float;
new_z float;
start_added bool = false;
BEGIN

if line_geom is null then return next
NULL;
else
n_pts := ST_NPoints(line_geom) -1;
for i in 1..n_pts LOOP
	vertex := ST_PointN(line_geom, i);
	next_vertex := ST_PointN(line_geom, i + 1);
	d := abs(ST_3DDistance(vertex, next_vertex));

	-- vertex between start and end
	if distance < end_length and distance > start_length then
	vertices := array_append(vertices, vertex);
	end if;
	
	-- first vertex
	if distance + d > start_length and start_added is false then
	fraction := (start_length - distance)/d;
	new_x := st_x(vertex) + (st_x(next_vertex) - st_x(vertex)) * fraction;
	new_y := st_y(vertex) + (st_y(next_vertex) - st_y(vertex)) * fraction;
	new_z := st_z(vertex) + (st_z(next_vertex) - st_z(vertex)) * fraction;
	start_vertex := st_setsrid(st_makepoint(new_x, new_y, new_z), srid);
	start_added := true;
	end if;

	-- last vertex
	if distance + d >= end_length then
	fraction := (end_length - distance)/d;
	new_x := st_x(vertex) + (st_x(next_vertex) - st_x(vertex)) * fraction;
	new_y := st_y(vertex) + (st_y(next_vertex) - st_y(vertex)) * fraction;
	new_z := st_z(vertex) + (st_z(next_vertex) - st_z(vertex)) * fraction;
	end_vertex := st_setsrid(st_makepoint(new_x, new_y, new_z), srid);
	EXIT;
	end if;

	distance := distance + d;
	
END LOOP;

vertices := array_append(vertices, end_vertex);
vertices := array_prepend(start_vertex, vertices);

return QUERY
select(st_makeline(vertices));
end if;
END;

$$ LANGUAGE plpgsql;

