delete from postCodes where long = 0 or lat = 0

select 
	duocode, 
	avg(long) as long, 
	avg(lat) as lat
from 
	(
	select 
		left(postcode,2) as duocode, long, lat
	from 
		postCodes
	) as subpost
GROUP BY duocode
ORDER BY duocode
FOR JSON AUTO