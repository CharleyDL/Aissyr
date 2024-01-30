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
