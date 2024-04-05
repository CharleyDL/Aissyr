SELECT 
    CONCAT(tr.tablet_name, 
           CASE 
               WHEN vr.view_name = 'Obv' THEN '_o' 
               ELSE '_r' 
           END) AS tablet_name,
    tr.picture AS tablet_picture,
    sr.bbox_segment
FROM tablet_ref tr
JOIN segment_ref sr ON tr.id_tablet = sr.id_tablet
JOIN view_ref vr ON sr.id_view = vr.id_view
WHERE tr.set_split = 'train'; -- train or test
-- LIMIT 10;