import time 
start_time = time.perf_counter()
import dell_dock
import dell_NB
import dell_DT

import lenovo
import hp

import json_Hp_Dock
import json_Hp_NB
import json_Hp_DT

import json_Lenovo_Dock
import json_Lenovo_NB
import json_Lenovo_DT

import old.reorganize_data as reorganize_data


end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"took {elapsed_time:.2f} seconds to run.")
