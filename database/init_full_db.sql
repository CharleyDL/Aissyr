/*******************************************************************************
Create Date:        Friday 12 Jan. 2024
Created by:         Charley ∆. Lebarbier
Description:        Initialize the PostgreSQL Database to insert dataset schema 
                    for AI training and save inferences from the webapp
                    HEROKU DATACLIP, in /**/ comment at top and end, use to 
                    create tables with write authorization.
Call by:            [docker-compose.yml, heroku - manually usage]
*******************************************************************************/

/*
begin;
set transaction read write;
*/

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
  set_split     VARCHAR(50) NOT NULL,
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
  train_label    INT,
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
  FOREIGN KEY (mzl_number) REFERENCES mzl_ref (mzl_number),
  FOREIGN KEY (id_segment) REFERENCES segment_ref (id_segment)
);

-- REVEAL
CREATE TABLE IF NOT EXISTS reveal (
  id_tablet INT NOT NULL,
  id_view   INT NOT NULL,
  PRIMARY KEY (id_tablet, id_view),
  FOREIGN KEY (id_tablet) REFERENCES tablet_ref (id_tablet),
  FOREIGN KEY (id_view) REFERENCES view_ref (id_view)
);

-- TABLET_INFRN
CREATE TABLE IF NOT EXISTS tablet_infrn (
  id_inference SERIAL PRIMARY KEY,
  tablet_name  VARCHAR(50) NOT NULL,
  picture      BYTEA NOT NULL,
  date_infrn   DATE NOT NULL
);

-- INFRN_RESULT
CREATE TABLE IF NOT EXISTS infrn_result (
  id_infrn_result SERIAL PRIMARY KEY,
  bbox            VARCHAR(100) NOT NULL,
  confidence      DOUBLE PRECISION NOT NULL,
  id_inference    INT NOT NULL,
  mzl_number      INT NOT NULL,
  FOREIGN KEY (id_inference) REFERENCES TABLET_INFRN (id_inference),
  FOREIGN KEY (mzl_number) REFERENCES MZL_REF (mzl_number)
);

-- ACCOUNT_USER
CREATE TABLE IF NOT EXISTS account_user (
  id_account      SERIAL PRIMARY KEY,
  title           VARCHAR(10),
  last_name       VARCHAR(100) NOT NULL,
  first_name      VARCHAR(100) NOT NULL,
  email           VARCHAR(100) UNIQUE NOT NULL,
  pwd_hash        BYTEA NOT NULL
);

-- -- ACCOUNT_PWD
-- CREATE TABLE IF NOT EXISTS account_pwd (
--   id_account      INT NOT NULL,
--   pwd_hash        BYTEA NOT NULL,
--   FOREIGN KEY (id_account) REFERENCES account_user (id_account)
-- );

-- ACCOUNT_HISTORY
CREATE TABLE IF NOT EXISTS account_history (
  id_account      INT NOT NULL,
  date_action     DATE NOT NULL,
  account_action  VARCHAR(100) NOT NULL,
  FOREIGN KEY (id_account) REFERENCES account_user (id_account)
);


/*COMMIT;*/