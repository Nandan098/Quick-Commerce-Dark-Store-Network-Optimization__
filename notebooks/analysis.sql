--1. Which Bengaluru zones have the highest demand?

SELECT
    customer_zone,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_zone
ORDER BY total_orders DESC;


-- 2. Which hours have the highest demand?

SELECT
    EXTRACT(HOUR FROM CAST(order_time AS TIME)) AS order_hour,
    COUNT(*) AS total_orders
FROM orders
GROUP BY EXTRACT(HOUR FROM CAST(order_time AS TIME))
ORDER BY total_orders DESC;

--3. What is the average order value by zone?

SELECT
    customer_zone,
    ROUND(AVG(order_value), 2) AS avg_order_value
FROM orders
GROUP BY customer_zone
ORDER BY avg_order_value DESC;

--4. Which zones have the strongest peak-hour demand?

SELECT
    customer_zone,
    COUNT(*) AS peak_hour_orders
FROM orders
WHERE CAST(order_time AS TIME) >= '17:00:00'
  AND CAST(order_time AS TIME) < '22:00:00'
GROUP BY customer_zone
ORDER BY peak_hour_orders DESC;