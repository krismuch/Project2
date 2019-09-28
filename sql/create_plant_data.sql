CREATE TABLE IF NOT EXISTS PLANT_META_DATA (rowid                      integer, 
                                            plant_id                   integer, 
                                            slug                       varchar(1000),
                                            scientific_name            varchar(1000),
                                            link                       varchar(1000),
                                            complete_data              boolean,
                                            common_name                varchar(1000)
                                            );

CREATE TABLE IF NOT EXISTS PLANT_JSON_DATA (meta_data_id               integer,
                                            json_data                  json
                                           );