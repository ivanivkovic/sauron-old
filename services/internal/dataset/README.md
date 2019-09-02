Dataset is a microservice designed to continuously store online datasets and store them in a target MySQL database for internal consumption.

sources.json config file explanation:

@type specifies string data type - currently supported: csv

@name specifies data name, as referenced by other applications

@url specifies online URL location of the data

@keys defines data key / column names and MySQL specs of the given data set

@version specifies data type version

@remove_rows dictates if any (and how many) first rows would be removed (some files may contain column names that aren't quite descriptive)

@file_type indicates which file type the source is (currently supporting CSV and JSON)

 
