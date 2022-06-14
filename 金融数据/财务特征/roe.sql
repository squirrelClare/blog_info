SELECT
	a.stock_id AS stock_id,
	'ROE' AS field,
	a.DAY AS day,
	a.
VALUE
	/ b.
VALUE
AS 
value
FROM
	( SELECT * FROM t_base_finance_data WHERE field = 'NET_PROFIT_IS' ) a
	JOIN ( SELECT * FROM t_base_finance_data WHERE field = 'TOT_EQUITY' ) b ON YEAR ( a.DAY ) = YEAR ( b.DAY ) 
	AND a.stock_id = b.stock_id