/* Table MZL_REF already exist */

CREATE TABLE TABLET_INFRN (
  id_inference INT NOT NULL,
  name_tablet  VARCHAR(50),
  picture      BLOB,
  date         DATE,
  PRIMARY KEY (id_inference)
);

CREATE TABLE INFRN_RESULT (
  id_infrn_result INT NOT NULL,
  bbox            VARCHAR(100),
  id_inference    INT NOT NULL,
  mzl_number      INT NOT NULL,
  PRIMARY KEY (id_infrn_result),
  FOREIGN KEY (mzl_number) REFERENCES MZL_REF (mzl_number),
  FOREIGN KEY (id_inference) REFERENCES TABLET_INFRN (id_inference)
);
