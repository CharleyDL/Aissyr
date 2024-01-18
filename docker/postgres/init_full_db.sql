/*******************************************************************************
Create Date:        Friday 12 Jan. 2024
Created by:         Charley ∆. Lebarbier
Description:        Initialize the PostgreSQL Database to insert dataset schema 
                    for AI training and save inferences from the webapp
Call by:            [docker-compose.yml]
*******************************************************************************/

-- VIEW_REF
CREATE TABLE IF NOT EXISTS view_ref (
  id_view   SERIAL PRIMARY KEY,
  view_name VARCHAR(50) UNIQUE NOT NULL
);

-- COLLECTION_REF
CREATE TABLE IF NOT EXISTS collection_ref (
  id_collection SERIAL PRIMARY KEY,
  collection_name VARCHAR(50) UNIQUE NOT NULL
);

-- TABLET_REF
CREATE TABLE IF NOT EXISTS tablet_ref (
  id_tablet     SERIAL PRIMARY KEY,
  tablet_name   VARCHAR(50) UNIQUE NOT NULL,
  picture       BYTEA NOT NULL,
  id_collection INT NOT NULL,
  FOREIGN KEY (id_collection) REFERENCES collection_ref (id_collection)
);

-- SEGMENT_REF
CREATE TABLE IF NOT EXISTS segment_ref (
  id_segment    SERIAL PRIMARY KEY,
  segment_idx   INT NOT NULL,
  bbox_segment  VARCHAR(50) NOT NULL,
  scale         DOUBLE PRECISION,
  id_collection INT NOT NULL,
  id_tablet     INT NOT NULL,
  id_view       INT NOT NULL,
  FOREIGN KEY (id_collection) REFERENCES collection_ref (id_collection),
  FOREIGN KEY (id_tablet) REFERENCES tablet_ref (id_tablet),
  FOREIGN KEY (id_view) REFERENCES view_ref (id_view)
);

-- MZL_REF
CREATE TABLE IF NOT EXISTS mzl_ref (
  mzl_number     INT PRIMARY KEY UNIQUE,
  train_label    INT NOT NULL,
  glyph_name     VARCHAR(50),
  glyph          VARCHAR(100),
  glyph_phonetic VARCHAR(5000)
);

-- ANNOTATION_REF
CREATE TABLE IF NOT EXISTS annotation_ref (
  id_annotation SERIAL PRIMARY KEY,
  bbox          VARCHAR(100) NOT NULL,
  relative_bbox VARCHAR(100) NOT NULL,
  mzl_number    INT NOT NULL,
  id_segment    INT NOT NULL,
  FOREIGN KEY (id_segment) REFERENCES segment_ref (id_segment),
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number)
);

-- REVEAL
CREATE TABLE IF NOT EXISTS reveal (
  id_tablet INT NOT NULL,
  id_view   INT NOT NULL,
  PRIMARY KEY (id_tablet, id_view),
  FOREIGN KEY (id_view) REFERENCES view_ref (id_view),
  FOREIGN KEY (id_tablet) REFERENCES tablet_ref (id_tablet)
);

-- IDENTIFY
CREATE TABLE IF NOT EXISTS identify (
  id_annotation INT NOT NULL,
  mzl_number    INT NOT NULL,
  PRIMARY KEY (id_annotation, mzl_number),
  FOREIGN KEY (id_annotation) REFERENCES annotation_ref (id_annotation),
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number)
);

-- TABLET_INFRN
CREATE TABLE IF NOT EXISTS tablet_infrn (
  id_inference SERIAL NOT NULL,
  tablet_name  VARCHAR(50) NOT NULL,
  picture      BYTEA NOT NULL,
  date         DATE NOT NULL,
  PRIMARY KEY (id_inference)
);

-- INFRN_RESULT
CREATE TABLE IF NOT EXISTS infrn_result (
  id_infrn_result SERIAL NOT NULL,
  bbox            VARCHAR(100) NOT NULL,
  id_inference    INT NOT NULL,
  mzl_number      INT NOT NULL,
  PRIMARY KEY (id_infrn_result),
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number),
  FOREIGN KEY (id_inference) REFERENCES tablet_infrn (id_inference)
);