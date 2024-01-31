SELECT 
    tr.tablet_name AS tablet_CDLI,
    tr.picture AS image,
FROM tablet_ref tr
WHERE tr.set_split = 'train'; -- 'train or test'