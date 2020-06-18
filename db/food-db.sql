CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "public"."backbone" (
    "ingredient_1" bpchar(100) NOT NULL,
    "ingredient_2" bpchar(100) NOT NULL,
    "ingredient_int" int4 NOT NULL,
    "category" bpchar(100) NOT NULL,
    "prevalence" float8 NOT NULL,
    "uuid" uuid NOT NULL DEFAULT uuid_generate_v1()
);
\copy backbone(ingredient_1, ingredient_2, ingredient_int, category, prevalence) FROM '../data/backbone.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE IF NOT EXISTS  "public"."comp_info" (
    "id" int4 NOT NULL,
    "compound_name" bpchar(100) NOT NULL,
    "cas_number" bpchar(100) NOT NULL
);
\copy comp_info(id, compound_name, cas_number) FROM '../data/comp_info.tsv' DELIMITER E'\t' CSV HEADER;

CREATE TABLE IF NOT EXISTS  "public"."ingr_comp" (
    "ingredient_id" int4 NOT NULL,
    "compound_id" int4 NOT NULL
);
\copy ingr_comp(ingredient_id, compound_id) FROM '../data/ingr_comp.tsv' DELIMITER E'\t' CSV HEADER;

CREATE TABLE IF NOT EXISTS  "public"."ingr_info_converted" (
    "id" int4 NOT NULL,
    "ingredient_name" bpchar(100) NOT NULL,
    "category" text NOT NULL
);
\copy ingr_info_converted(id, ingredient_name, category) FROM '../data/ingr_info.tsv' DELIMITER E'\t' CSV HEADER;


CREATE TABLE IF NOT EXISTS  "public"."srep-s2" (
    "ingredient_1" bpchar(100) NOT NULL,
    "ingredient_2" bpchar(100) NOT NULL,
    "shared" int4 NOT NULL,
    "uuid" uuid DEFAULT uuid_generate_v4()
);
\copy "srep-s2"(ingredient_1, ingredient_2, shared) FROM '../data/srep00196-s2.csv' DELIMITER ',' CSV HEADER;

CREATE TEMPORARY TABLE temp_table(
    "all_values" text
 );

\copy "temp_table"("all_values") FROM '../data/srep00196-s3.csv' DELIMITER ';' CSV;


CREATE TABLE "public"."srep-s3" AS
WITH T1 AS (
    SELECT
        split_part(all_values, ',', 1) as cusine,
        string_to_array(all_values, ',') as igredients
    FROM temp_table
) SELECT cusine, igredients[2:] FROM T1;
