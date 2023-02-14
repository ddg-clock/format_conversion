# format_conversion
## Convert the format output from powertrace   

$ python format_conversion.py --help   
usage: format_conversion.py [-h] [--format FORMAT] --input INPUT [--output OUTPUT] [--header HEADER] [--config CONFIG]   

Formating the csv output    

optional arguments:   
  -h, --help       show this help message and exit   
  --format FORMAT  define either ieee754 or 8.20 formatting   
  --input INPUT    Input filename   
  --output OUTPUT  Output filename   
  --header HEADER  The header in the csv file to be converted   
  --config CONFIG  configuration for individual headers   

Examples:   
python format_conversion.py --input powertrace_combined_Idle.csv --output mldata.csv --config "IA_C0_ANY:ieee754 AVG_NUM_CORES:ieee754"    
python format_conversion.py --input powertrace_combined_Idle.csv --header "IA_C0_ANY AVG_NUM_CORES" --output mldata.csv --format ieee754    
