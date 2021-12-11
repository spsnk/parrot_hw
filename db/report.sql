select "Products".name "Product", date_trunc('day', "Orders".timestamp) "Date", SUM("OrderLine".quantity) "Quantity"
FROM "OrderLine" 
INNER JOIN "Products" ON ("OrderLine".product_id = "Products".id)
INNER JOIN "Orders" ON ("OrderLine".order_id = "Orders".id)
GROUP BY "Date", "Products".name
ORDER BY "Products".name ASC, "Quantity" DESC
;
