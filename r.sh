curl www.baidu.com > /dev/null 2>&1
ret="$?"
if [ $ret = "6" ];then
echo "网络中断......"
exit 1
else
git pull
ret="$?"
    if [ $ret = "1" ];then
    cd app_spider
    python SendEmail.py
    
    fi
nohup python ReadDatabase.py >../log/Read.file 2>&1
sleep 5
nohup python ConsumerQQ.py > ../log/QQout.file 2>&1 &
nohup python Consumer360.py > ../log/360out.file 2>&1 &
nohup python ConsumerBaidumarket.py > ../log/markout.file 2>&1 &
nohup python ConsumerBaiduspider.py > ../log/spider.file 2>&1 &
nohup python insertData.py > ../log/inser.file 2 >&1
cd ..
fi
