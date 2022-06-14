SELECT
	a.stock_id AS stock_id,
	'PS' AS field,
	a.DAY AS day,
	a.
VALUE
	/ b.
VALUE
AS 
value
FROM
	t_base_stock_price a
	JOIN t_feature_finance_year b ON a.stock_id = b.stock_id 
	AND YEAR ( a.DAY ) = YEAR ( b.DAY ) 
	AND a.field = 'CLOSE' 
	AND b.field = 'SPS' ;