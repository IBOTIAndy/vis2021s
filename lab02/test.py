import pandas as pd

path = "./kinmen_nosmoke_park.csv"
#讀取csv檔案
temp = pd.read_csv(path)
temp.head()

#, 取出想處理的部分(切割)
df = temp[["鄉鎮市", "場所禁菸規定"]]
df.head()

table=[]
#建立table來儲存
#table.append({"鄉鎮市":"a", "全面禁菸":0, "除吸菸區外全面禁菸":0})
#print(table, type(table))
#搜尋dataframe全部資料
for index, oneframe in df.iterrows():
    #print(oneframe, type(oneframe), "\n")
    flag = True #用來判斷該"鄉鎮市"記錄了沒
    for tlist in table:
        #如果該"鄉鎮市"已經建立
        if(tlist["鄉鎮市"] == oneframe["鄉鎮市"]):
            flag = False
            #增加數量
            tlist[oneframe["場所禁菸規定"]] += 1
            #print("1")
            break
    if(flag): #如果該"鄉鎮市"還沒建立
        noSmork=0
        areaSmork=0
        if(oneframe["場所禁菸規定"]=="全面禁菸"):
            noSmork=1
        else:
            areaSmork=1        
        #建立新的"鄉鎮市"並加上該公園的禁菸狀況
        table.append({"鄉鎮市":oneframe["鄉鎮市"], "全面禁菸":noSmork, "除吸菸區外全面禁菸":areaSmork})
        #print("2")
#table.pop(0)
table.pop(-1)
table

#將dict轉換成pandas的data frame
end_table = pd.DataFrame(data=table)
#發現col的排列不是預期的樣子 重新排列
end_table = end_table[["鄉鎮市", "全面禁菸", "除吸菸區外全面禁菸"]]
#end_table.reset_index(drop=True)
#存為end_park.csv (編碼為 UTF-8，且去除index)
end_table.to_csv("end_park.csv", encoding="utf-8", index=None)
