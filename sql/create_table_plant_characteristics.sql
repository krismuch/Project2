drop table if exists PLANT_CHARACTERISTICS;

create table PLANT_CHARACTERISTICS
as
select meta.scientific_name,
       ifnull(meta.common_name, json_extract(jsond.json_data, '$.common_name')) as common_name, 
	   meta.plant_id,
	   nullif(nullif(ifnull(json_extract(jsond.json_data, '$.main_species.images[0].url'), json_extract(jsond.json_data, '$.images[0].url')),'https://upload.wikimedia.org/wikipedia/commons/7/71/Symbol_redirect_arrow_with_gradient.svg'),'https://upload.wikimedia.org/wikipedia/commons/3/31/Redirect_arrow_without_text.svg') as image_url,  --Removing extraneous URL's
	   json_extract(jsond.json_data, '$.main_species.duration') as duration, 
	   json_extract(jsond.json_data, '$.main_species.growth.temperature_minimum') as min_temp,
	   round(json_extract(jsond.json_data, '$.main_species.growth.temperature_minimum.deg_f'),2) as min_temp_deg_f,
	   round(json_extract(jsond.json_data, '$.main_species.growth.temperature_minimum.deg_c'),2) as min_temp_deg_c,
	   json_extract(jsond.json_data, '$.main_species.growth.precipitation_minimum') as min_precip,
	   round(json_extract(jsond.json_data, '$.main_species.growth.precipitation_minimum.inches'),2) as min_precip_inches,
	   round(json_extract(jsond.json_data, '$.main_species.growth.precipitation_minimum.cm'),2) as min_precip_cm,
	   json_extract(jsond.json_data, '$.main_species.growth.precipitation_maximum') as max_precip,
	   round(json_extract(jsond.json_data, '$.main_species.growth.precipitation_maximum.inches'),2) as max_precip_inches,
	   round(json_extract(jsond.json_data, '$.main_species.growth.precipitation_maximum.cm'),2) as max_precip_cm,
	   json_extract(jsond.json_data, '$.main_species.growth.frost_free_days_minimum') as frost_free_days,
	   json_extract(jsond.json_data, '$.main_species.growth.drought_tolerance') as drought_tolerance,
	   json_extract(jsond.json_data, '$.main_species.growth.ph_minimum') as min_ph,
	   json_extract(jsond.json_data, '$.main_species.growth.ph_maximum') as max_ph,
	   json_extract(jsond.json_data, '$.main_species.flower.conspicuous') as flower_conspicous,
	   json_extract(jsond.json_data, '$.main_species.flower.color') as flower_color,
	   json_extract(jsond.json_data, '$.division.name') as division_name,
	   json_extract(jsond.json_data, '$.class.name') as division_class_name,
	   json_extract(jsond.json_data, '$.order.name') as division_order_name,
	   json_extract(jsond.json_data, '$.family.name') as family_name,
	   json_extract(jsond.json_data, '$.genus.name') as genus_name,	   
	   jsond.json_data
from PLANT_META_DATA meta
	join PLANT_JSON_DATA jsond on (jsond.meta_data_id = meta.rowid)
where json_extract(jsond.json_data, '$.main_species.growth.temperature_minimum.deg_f') is not null or
      json_extract(jsond.json_data, '$.main_species.growth.precipitation_minimum.inches') is not null or
	  json_extract(jsond.json_data, '$.main_species.growth.precipitation_maximum.inches') is not null or
	  json_extract(jsond.json_data, '$.main_species.growth.frost_free_days_minimum') is not null or
	  json_extract(jsond.json_data, '$.main_species.growth.drought_tolerance') is not null or
	  json_extract(jsond.json_data, '$.main_species.growth.ph_minimum') is not null or
	  json_extract(jsond.json_data, '$.main_species.growth.ph_maximum') is not null
order by rowid;

update PLANT_CHARACTERISTICS set image_url = ifnull(image_url, 'https://barrreport.com/data/showcase/11/11351-fbe74bfb6387d2375a5e5c75377b9bde.jpg');