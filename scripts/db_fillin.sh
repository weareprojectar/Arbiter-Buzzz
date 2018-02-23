# Backing up Django DB

### 1. BM
su arbiter -c "psql -c \"\copy stockapi_bm (date, name, index, volume, individual, foreigner, institution) from '/home/arbiter/backup/bm.csv' delimiter ',';\""
echo BM backup successful

### 2. Ticker
su arbiter -c "psql -c \"\copy stockapi_ticker (date, name, code, market_type) from '/home/arbiter/backup/ticker.csv' delimiter ',';\""
echo Ticker backup successful

### 3. OHLCV
su arbiter -c "psql -c \"\copy stockapi_ohlcv (date, code, open_price, high_price, low_price, close_price, volume) from '/home/arbiter/backup/ohlcv.csv' delimiter ',';\""
echo OHLCV backup successful

### 4. Specs
su arbiter -c "psql -c \"\copy stockapi_specs (code, date, momentum, volatility, correlation, volume, momentum_score, volatility_score, correlation_score, volume_score, total_score) from '/home/arbiter/backup/specs.csv' delimiter ',';\""
echo Specs backup successful

### 5. Info
su arbiter -c "psql -c \"\copy stockapi_info (code, name, date, size_type, style_type, market_type, face_val, stock_nums, price, market_cap, market_cap_rank, industry, foreign_limit, foreign_possession, foreign_ratio, per, eps, pbr, bps, industry_per, yield_ret) from '/home/arbiter/backup/info.csv' delimiter ',';\""
echo Info backup successful

### 6. Financial
su arbiter -c "psql -c \"\copy stockapi_financial (code, name, date, revenue, profit, net_profit, consolidate_profit, asset, debt, capital) from '/home/arbiter/backup/financial.csv' delimiter ',';\""
echo Financial backup successful

### 7. FinancialRatio
su arbiter -c "psql -c \"\copy stockapi_financialratio (date, code, name, debt_ratio, profit_ratio, net_profit_ratio, consolidate_profit_ratio, net_roe, consolidate_roe, revenue_growth, profit_growth, net_profit_growth) from '/home/arbiter/backup/financialratio.csv' delimiter ',';\""
echo FinancialRatio backup successful

### 8. QuarterFinancial
su arbiter -c "psql -c \"\copy stockapi_quarterfinancial (date, code, name, revenue, profit, net_profit, consolidate_profit, profit_ratio, net_profit_ratio) from '/home/arbiter/backup/quarterfinancial.csv' delimiter ',';\""
echo QuarterFinancial backup successful

### 8. BuySell
su arbiter -c "psql -c \"\copy stockapi_kospiweeklybuy from '/home/arbiter/backup/kospiweeklybuy.csv' delimiter ',';\""
echo KospiWeeklyBuy backup successful

su arbiter -c "psql -c \"\copy stockapi_kosdaqweeklybuy from '/home/arbiter/backup/kosdaqweeklybuy.csv' delimiter ',';\""
echo KosdaqWeeklyBuy backup successful

su arbiter -c "psql -c \"\copy stockapi_kospiweeklysell from '/home/arbiter/backup/kospiweeklysell.csv' delimiter ',';\""
echo KospiWeeklySell backup successful

su arbiter -c "psql -c \"\copy stockapi_kosdaqweeklysell from '/home/arbiter/backup/kosdaqweeklysell.csv' delimiter ',';\""
echo KosdaqWeeklySell backup successful
