cd app_spider
nohup python ReadDatabase.py >log/Read.file 2>&1
sleep 5
nohup python ConsumerQQ.py > log/QQout.file 2>&1 &
nohup python Consumer360.py > log/360out.file 2>&1 &
nohup python ConsumerBaidumarket.py > log/markout.file 2>&1 &
nohup python ConsumerBaiduspider.py > log/spider.file 2>&1 &
nohup python insertData.py > log/inser.file 2 >&1
cd ..

