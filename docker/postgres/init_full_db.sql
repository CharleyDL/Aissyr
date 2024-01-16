-- VIEW_REF
CREATE TABLE IF NOT EXISTS view_ref (
  id_view   SERIAL PRIMARY KEY,
  view_name VARCHAR(50) UNIQUE
);

-- COLLECTION_REF
CREATE TABLE IF NOT EXISTS collection_ref (
  id_collection SERIAL PRIMARY KEY,
  collection_name VARCHAR(50) UNIQUE
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
  segment_idx  INT PRIMARY KEY UNIQUE,
  bbox_segment VARCHAR(50),
  scale        INT,
  id_view      INT NOT NULL,
  id_tablet    INT NOT NULL,
  FOREIGN KEY (id_tablet) REFERENCES tablet_ref (id_tablet),
  FOREIGN KEY (id_view) REFERENCES view_ref (id_view)
);

-- MZL_REF
CREATE TABLE IF NOT EXISTS mzl_ref (
  mzl_number     INT PRIMARY KEY UNIQUE,
  train_label    INT,
  glyph_name     VARCHAR(50),
  glyph          VARCHAR(100),
  glyph_phonetic VARCHAR(5000)
);

-- ANNOTATION_REF
CREATE TABLE IF NOT EXISTS annotation_ref (
  id_annotation SERIAL PRIMARY KEY,
  bbox          VARCHAR(100),
  relative_bbox VARCHAR(100),
  mzl_number    INT NOT NULL,
  segment_idx   INT NOT NULL,
  FOREIGN KEY (segment_idx) REFERENCES segment_ref (segment_idx),
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
  id_annotation INT,
  mzl_number    INT,
  PRIMARY KEY (id_annotation, mzl_number),
  FOREIGN KEY (id_annotation) REFERENCES annotation_ref (id_annotation),
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number)
);

-- TABLET_INFRN
CREATE TABLE IF NOT EXISTS tablet_infrn (
  id_inference SERIAL NOT NULL,
  tablet_name  VARCHAR(50),
  picture      BYTEA,
  date         DATE,
  PRIMARY KEY (id_inference)
);

-- INFRN_RESULT
CREATE TABLE IF NOT EXISTS infrn_result (
  id_infrn_result SERIAL NOT NULL,
  bbox            VARCHAR(100),
  id_inference    INT NOT NULL,
  mzl_number      INT NOT NULL,
  PRIMARY KEY (id_infrn_result),
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number),
  FOREIGN KEY (id_inference) REFERENCES tablet_infrn (id_inference)
);