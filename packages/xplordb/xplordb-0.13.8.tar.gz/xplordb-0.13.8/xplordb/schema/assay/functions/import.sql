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

CREATE OR REPLACE FUNCTION assay.import (character varying)
    RETURNS TABLE (
        sample_id character varying,
        sample_prep character varying,
        digest character varying,
        lab_method character varying,
        lab_element character varying,
        element character varying,
        repeat integer,
        preferred integer,
        o_method character varying,
        unit character varying,
        ar character varying,
        arr numrange,
        lab character varying,
        batch character varying,
        lower_limit real)
    LANGUAGE sql
    AS $function$
    WITH RECURSIVE batch AS (
        SELECT
            $1 AS batch_no
),
results AS (
    SELECT
        line,
        batch,
        sample_id,
        string_to_array((replace("values", '"', '')), ',')::text[] AS arr
    FROM
        assay.raw
    WHERE
        batch = (
            SELECT
                batch_no
            FROM
                batch)
),
num_values AS (
    SELECT
        max(array_length(string_to_array("values", ','), 1) - 1) AS num
FROM
    assay.raw
),
head AS (
    SELECT
        (
            SELECT
                arr[2:]
            FROM
                results
            WHERE
                line = 9) AS lab_method,
            (
                SELECT
                    arr[2:]
                FROM
                    results
                WHERE
                    line = 10) AS lab_element,
                (
                    SELECT
                        arr[2:]
                    FROM
                        results
                    WHERE
                        line = 11) AS unit,
                    (
                        SELECT
                            arr[2:]
                        FROM
                            results
                        WHERE
                            line = 12) AS lower_limit,
                        (
                            SELECT
                                arr[2:]
                            FROM
                                results
                            WHERE
                                line = 13) AS tolerance,
                            (
                                SELECT
                                    arr[2:]
                                FROM
                                    results
                                WHERE
                                    line = 14) AS digest,
                                (
                                    SELECT
                                        arr[2:]
                                    FROM
                                        results
                                    WHERE
                                        line = 15) AS temperature,
                                    (
                                        SELECT
                                            arr[2:]
                                        FROM
                                            results
                                        WHERE
                                            line = 16) AS time,
                                        (
                                            SELECT
                                                arr[2:]
                                            FROM
                                                results
                                            WHERE
                                                line = 17) AS lab,
                                            (
                                                SELECT
                                                    lab_sample_prep
                                                FROM
                                                    assay.batch
                                                WHERE
                                                    batch = (
                                                        SELECT
                                                            batch_no
                                                        FROM
                                                            batch)) AS lab_sample_prep
),
assay_batch AS (
    SELECT
        (
            SELECT
                arr[2]
            FROM
                results
            WHERE
                line = 17) AS lab,
            (
                SELECT
                    batch_no
                FROM
                    batch) AS batch,
                NULL AS dispatch_no,
                (
                    SELECT
                        arr[2]
                    FROM
                        results
                    WHERE
                        line = 4)::timestamptz AS lab_received_date,
                    (
                        SELECT
                            arr[2]
                        FROM
                            results
                        WHERE
                            line = 5)::timestamptz AS lab_completed_date,
                        NULL AS lab_sample_prep,
                        NULL::bool AS validated,
                        NULL AS validated_by,
                        NULL::timestamp AS validated_date,
                        (
                            SELECT
                                batch_no || '.csv'
                            FROM
                                batch) AS data_source,
                            'sql0.87' AS import_script,
                            (
                                SELECT
                                    arr[2]::int
                                FROM
                                    results
                                WHERE
                                    line = 3) AS lab_sample_count,
                                NULL::int AS samples_imported,
                                NULL::int AS lab_result_count,
                                NULL::int AS result_import,
                                NULL::int AS over_range_total,
                                NULL::int AS qaqc_total,
                                (
                                    SELECT
                                        arr[2]
                                    FROM
                                        results
                                    WHERE
                                        line = 1) AS batch_status,
                                    (
                                        SELECT
                                            USER) AS loaded_by,
                                        (
                                            SELECT
                                                now()) AS load_date
                                        FROM
                                            results
                                        LIMIT 1
),
insert_batch AS (
INSERT INTO assay.batch
    SELECT
        lab,
        batch,
        dispatch_no,
        lab_received_date,
        lab_completed_date,
        lab_sample_prep,
        validated,
        validated_by,
        validated_date,
        data_source,
        import_script,
        lab_sample_count,
        samples_imported,
        lab_result_count,
        result_import,
        over_range_total,
        qaqc_total,
        batch_status,
        loaded_by,
        load_date
    FROM
        assay_batch
),
--results
ass (
    sample_id, digest, lab_method, lab_element,
    --element, repeat, preferred, o_method,
    unit, ar, lab, lower_limit, count_
) AS (
    SELECT
        r.sample_id AS sample_id,
        h.digest[1] AS digest,
        h.lab_method[1] AS lab_method,
        h.lab_element[1] AS lab_element,
        --null as element, --generally this will be the same as lab_element some cases may need conversion e.g Au1 to Au
        --null as repeat, -- generate from lab_element when needed e.g Au = 1 , Au1 = 2
        --null as preferred, -- generated below in select / case
        --null as o_method,
        h.unit[1] AS unit,
        arr[2] AS ar,
        --null as arr,
        h.lab[1] AS lab,
        h.lower_limit[1] AS lower_limit,
        1 AS count_
    FROM
        results r,
        head h
    WHERE
        line > 17
    UNION
    SELECT
        r.sample_id AS sample_id,
        h.digest[count_ + 1] AS digest,
        h.lab_method[count_ + 1] AS lab_method,
        h.lab_element[count_ + 1] AS lab_element,
        --null as element, --generally this will be the same as lab_element some cases may need conversion e.g Au1 to Aut
        --null as repeat, -- generate from lab_element when needed.  Assay repeat code, 0 - result, 1 - 1st repeat, 2 - 2nd repeat
        --null as preferred, -- generated below in select / case
        --null as o_method,
        h.unit[count_ + 1] AS unit,
        arr[1 + (count_ + 1)] AS ar,
        --null as arr,
        h.lab[count_ + 1] AS lab,
        h.lower_limit[count_ + 1] AS lower_limit,
        count_ + 1 AS count_
    FROM
        results r,
        head h,
        ass
    WHERE
        line > 17
        AND count_ < (
            SELECT
                *
            FROM
                num_values))
    INSERT INTO assay.assay
    SELECT
        sample_id,
        (
            SELECT
                lab_sample_prep
            FROM
                head) AS sample_prep,
        digest,
        lab_method,
        lab_element,
        lab_element AS element,
        0 AS repeat,
        1 AS preferred, --use case statement to set Lab Blanks and Lab Standards
        m.o_method AS o_method,
        unit,
        ar,
        CASE WHEN ar LIKE '<%' THEN
            numrange(0::numeric, replace(ar, '<', '')::numeric, '[]')::numrange
        WHEN ar LIKE '>%' THEN
            numrange(replace(ar, '>', '')::numeric, NULL, '()')::numrange
        WHEN ar ~ '^[^0-9\.\-]+$' THEN
            numrange('empty')::numrange --non numbers are set to 'empty'?
ELSE
    numrange(ar::numeric, ar::numeric, '[]')
        END AS arr,
        ass.lab AS lab,
        (
            SELECT
                batch_no
            FROM
                batch) AS batch,
        lower_limit::real AS lower_limit
        --null::real as upper_limit,
        --('now'::text)::timestamp with time zone as load_date,
        --"current_user"()::varchar as loaded_by
        --,	 nextval('assay.assay_id_seq'::regclass)::int as id
    FROM
        ass
    LEFT JOIN ref.lab_method m ON (ass.lab_method = m.lab_method_code)
WHERE
    ar != ''
RETURNING
    sample_id,
    sample_prep,
    digest,
    lab_method,
    lab_element,
    element,
    repeat,
    preferred,
    o_method,
    unit,
    ar,
    arr,
    lab,
    batch,
    lower_limit;

$function$
