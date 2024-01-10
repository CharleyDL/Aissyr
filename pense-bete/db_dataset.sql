CREATE TABLE ANNOTATION_REF (
  id_annotation INT PRIMARY KEY,
  bbox          VARCHAR(100),
  relative_bbox VARCHAR(100),
  name_tablet   VARCHAR(50) NOT NULL,
  FOREIGN KEY (name_tablet) REFERENCES TABLET_REF (name_tablet)
);

CREATE TABLE COLLECTION_REF (
  id_collection INT PRIMARY KEY,
  name_collection VARCHAR(50)
);

CREATE TABLE IDENTIFY (
  id_annotation INT,
  mzl_number    INT,
  PRIMARY KEY (id_annotation, mzl_number),
  FOREIGN KEY (id_annotation) REFERENCES ANNOTATION_REF (id_annotation),
  FOREIGN KEY (mzl_number) REFERENCES MZL_REF (mzl_number)
);

CREATE TABLE IMAGE_TABLET_REF (
  name_tablet VARCHAR(50) PRIMARY KEY,
  picture     BLOB
);

CREATE TABLE MZL_REF (
  mzl_number     INT PRIMARY KEY,
  train_label    INT,
  name_glyph     VARCHAR(50),
  glyph          VARCHAR(100),
  glyph_phonetic VARCHAR(5000)
);

CREATE TABLE REVEAL (
  name_tablet VARCHAR(50),
  id_view     INT,
  PRIMARY KEY (name_tablet, id_view),
  FOREIGN KEY (id_view) REFERENCES VIEW_REF (id_view),
  FOREIGN KEY (name_tablet) REFERENCES TABLET_REF (name_tablet)
);




CREATE TABLE SEGMENT_REF (
  segment_idx  INT PRIMARY KEY,
  bbox_segment VARCHAR(100),
  scale        INT,
  assigned     BOOLEAN,
  id_view      INT,
  name_tablet  VARCHAR(50),
  FOREIGN KEY (name_tablet) REFERENCES TABLET_REF (name_tablet),
  FOREIGN KEY (id_view) REFERENCES VIEW_REF (id_view)
);


CREATE TABLE TABLET_REF (
  name_tablet   VARCHAR(50) PRIMARY KEY,
  id_collection INT NOT NULL,
  FOREIGN KEY (id_collection) REFERENCES COLLECTION_REF (id_collection)
);

CREATE TABLE VIEW_REF (
  id_view   INT PRIMARY KEY,
  name_view VARCHAR(50)
);