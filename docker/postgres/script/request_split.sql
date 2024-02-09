-- Full information, not efficient

SELECT
    tr.tablet_name AS tablet_CDLI,
    sr.bbox_segment,
    ar.relative_bbox AS bbox_glyph,
    mr.mzl_number,
    mr.train_label
FROM segment_ref sr
JOIN tablet_ref tr ON sr.id_tablet = tr.id_tablet
JOIN view_ref vr ON sr.id_view = vr.id_view
JOIN collection_ref cr ON sr.id_collection = cr.id_collection
JOIN annotation_ref ar ON sr.id_segment = ar.id_segment
JOIN mzl_ref mr ON ar.mzl_number = mr.mzl_number
WHERE tr.set_split = 'train'; -- 'train or test'


-- Compact one, with necessary information
SELECT 
    CONCAT(tablet_name, 
           CASE 
               WHEN vr.view_name = 'Obv' THEN '_o' 
               ELSE '_r' 
           END) AS tablet_name,
    ar.relative_bbox AS bbox_glyph,
    ar.mzl_number AS mzl_label
FROM tablet_ref tr
JOIN segment_ref sr ON tr.id_tablet = sr.id_tablet
JOIN annotation_ref ar ON sr.id_segment = ar.id_segment
JOIN view_ref vr ON sr.id_view = vr.id_view
WHERE tr.set_split = 'train'; -- train or test