# coverage web system

[覆蓋測試系統](http://10.144.1.108/)

# 使用指南

1. 選定分支
2. 選定測試項
3. 開始測試

# 來源 YAKIN

* 使用 gitlab 上的 branch (預設拿該 branch 最新版)
* 使用自行上傳的 YAKIN 包

# 上傳檔案

若要使用自己的 YAKIN，在開始跑之前，請先上傳檔案，上傳完成後，檔案將會列在已上傳的 YAKIN 中

# 產生結果 (report)

跑完測試，將會顯示在 result 分頁中，或是使用 http://host_ip:8000/ 開啟, 你也可以去歷史記錄查看

# 工作目錄

+ /home/lfsm/yakin

# 可能會遇到的問題

* 如果網站出現 404 ERROR 或是未知的問題, 請先重啟 cws 與 cws_worker

```bash
$ systemctl restart cws
$ systemctl restart cws_worker
```