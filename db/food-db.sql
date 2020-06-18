CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE "public"."backbone" (
    "ingredient_1" bpchar(100) NOT NULL,
    "ingredient_2" bpchar(100) NOT NULL,
    "ingredient_int" int4 NOT NULL,
    "category" bpchar(100) NOT NULL,
    "prevalence" float8 NOT NULL,
    "uuid" uuid NOT NULL DEFAULT uuid_generate_v1()
);
\copy backbone(ingredient_1, ingredient_2, ingredient_int, category, prevalence) FROM '../data/backbone.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE "public"."comp_info" (
    "id" int4 NOT NULL,
    "compound_name" bpchar(100) NOT NULL,
    "cas_number" bpchar(100) NOT NULL
);
\copy comp_info(id, compound_name, cas_number) FROM '../data/comp_info_converted.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE "public"."ingr_comp" (
    "ingredient_id" int4 NOT NULL,
    "compound_id" int4 NOT NULL
);
\copy ingr_comp(ingredient_id, compound_id) FROM '../data/ingr_comp_converted.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE "public"."ingr_info_converted" (
    "id" int4 NOT NULL,
    "ingredient_name" bpchar(100) NOT NULL,
    "category" text NOT NULL
);
\copy ingr_info_converted(id, ingredient_name, category) FROM '../data/ingr_info_converted.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE "public"."srep-s2" (
    "ingredient_1" bpchar(100) NOT NULL,
    "ingredient_2" bpchar(100) NOT NULL,
    "shared" int4 NOT NULL,
    "uuid" uuid DEFAULT uuid_generate_v4()
);
\copy "srep-s2"(ingredient_1, ingredient_2, shared) FROM '../data/srep00196-s2.csv' DELIMITER ',' CSV HEADER;
