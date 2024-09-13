# build-table

須先連接到 database 

function "table_exits"
用來判斷 table 是否已經存在，為了防止建立同樣名稱的 table

function "build_table"
建立 table 名稱，命名規則為 s + 公司股票號碼 ex "s2330"

然後判斷 table 使否已經存在， 如果已經存在，則不建立 table 
反之建立 table 

# goodinfo-crawler-main
使用 selenium 進行爬蟲，點擊下來的檔案惠存放在 家目錄裡面的 Download 資料夾
使用時需要根據自己電腦的路經，進行更改，程式最後面會把該檔案刪除（因為不刪除的話會導致影響到後面讀取資料）

再來把 dataframe 的 columns 名稱改成英文
最後把資料存入資料庫

存入 table 時，會用 frist 來判斷 dataframe 的第一個值，是否為已經存在 database 中，如果沒有的話就 insert table ，
有的話函數就會回傳 1 ，代表之後的值都使已經有的，因為 dataframe 的值會從最新的到最舊的，所以看地一筆資料就知道是否需要更新
值
**更新的值會放在資料庫的最後一個 row!!**