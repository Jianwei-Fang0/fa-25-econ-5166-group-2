主要有三個檔案，依建立順序是：
1. merged_stage1.rmd 主要建立df_merged.csv 同時跑CV 算出R2
2. predict_stage1.rmd 是以9-11月資料訓練，並預測12月的三個值borrow_pred, return_pred, net_borrow_pred，最後建立df_m12_target.csv
3. strategy_default_stage2.rmd 是讀取df_m12_target.csv並且建立補車策略計算的檔案

使用方式：
1. 關於預測能力merged_stage1.rmd, predict_stage1.rmd 都有著墨
2. 寫補車策略直接讀取strategy_default_stage2.rmd即可

討論：
1. 現在以9-11月訓練的資料，R2很好。
2. 現在以9-11月訓練的資料去預測12月並且讓他與12月的實際流量值去做比較
3. 補車策略這裡因為都是使用同樣的模型預測結果，除了我新增strategy3 是以mean作為預測值
4. 還沒完成stage2，關於派出成本這裡還沒結論
