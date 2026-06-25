SELECT COUNT(*) FROM companies;

PRAGMA foreign_key_check;

SELECT * FROM companies LIMIT 5;

SELECT sector_name, COUNT(*) FROM companies c 
JOIN sectors s ON c.sector_id = s.sector_id 
GROUP BY sector_name;

SELECT * FROM profitandloss WHERE sales <= 0;

SELECT company_id, year, ABS(total_liabilities - total_assets) AS mismatch 
FROM balancesheet 
WHERE mismatch > 0.01;

SELECT ticker, year, net_profit FROM profitandloss p 
JOIN companies c ON p.company_id = c.company_id 
ORDER BY net_profit DESC LIMIT 10;

SELECT AVG(close_price), MAX(close_price), MIN(close_price) 
FROM stock_prices 
WHERE company_id = 1;

SELECT ticker, year, roe, roce FROM financial_ratios r
JOIN companies c ON r.company_id = c.company_id
WHERE roe > 15 AND roce > 15;

SELECT c.ticker, COUNT(p.peer_company_id) AS peer_count 
FROM peer_groups p
JOIN companies c ON p.company_id = c.company_id
GROUP BY c.ticker;