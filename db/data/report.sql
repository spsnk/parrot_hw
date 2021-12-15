SELECT p.name AS "product",
    SUM (oc.quantity) AS "units",
    SUM (oc.quantity * oc.unitary_price) AS "revenue"
FROM ordercontents oc
    INNER JOIN products p ON (oc.product_id = p.id)
    INNER JOIN orders o ON (o.id = oc.order_id)
WHERE o.date_created BETWEEN '2021-12-10' AND '2021-12-11'
GROUP BY p.name
ORDER BY p.name ASC,
    units DESC
