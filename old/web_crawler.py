import time
import threading

#設定平行運行
# def subroutine_1():
#     import dell_NB
#     import dell_dock
#     import dell_DT

def subroutine_3():
    import lenovo
    import json_Lenovo_Dock
    import json_Lenovo_NB
    import json_Lenovo_DT

def subroutine_4():
    import hp
    import json_Hp_Dock
    import json_Hp_NB
    import json_Hp_DT

# def subroutine_5():
#     import reorganize_data

#分配運行核心
# Subroutine_1 = threading.Thread(target=subroutine_1)
Subroutine_3 = threading.Thread(target=subroutine_3)
Subroutine_4 = threading.Thread(target=subroutine_4)
# Subroutine_5 = threading.Thread(target=subroutine_5)

#開始執行
start_time = time.perf_counter()
# Subroutine_1.start()
Subroutine_3.start()
Subroutine_4.start()

#等待執行完畢
# Subroutine_1.join()   # 加入等待 aa() 完成的方法
Subroutine_3.join()   # 加入等待 cc() 完成的方法
Subroutine_4.join()   # 加入等待 dd() 完成的方法

#執行最後程序
# Subroutine_5.start()  # 當前面都執行完，才會開始執行

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"took {elapsed_time:.2f} seconds to run.")

