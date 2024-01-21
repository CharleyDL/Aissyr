SELECT
    sr.segment_idx,
    tr.tablet_name AS tablet_CDLI,
    vr.view_name AS view_desc,
    sr.bbox_segment,
    cr.collection_name AS collection,
    mr.mzl_number,
    mr.train_label,
    ar.bbox,
    ar.relative_bbox
FROM segment_ref sr
JOIN tablet_ref tr ON sr.id_tablet = tr.id_tablet
JOIN view_ref vr ON sr.id_view = vr.id_view
JOIN collection_ref cr ON sr.id_collection = cr.id_collection
JOIN mzl_ref mr ON ar.mzl_number = mr.mzl_number
JOIN annotation_ref ar ON sr.id_segment = ar.id_segment
WHERE tr.set_ = 'test';
