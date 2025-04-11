
/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...
SELECT c."name" AS category_name, COUNT(*)  FROM film_category fc 
LEFT JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY COUNT(*) desc


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...

SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
		COUNT(rental_id) rents_cnt
FROM  rental r 
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN film_actor fa ON i.film_id = fa.film_id
LEFT JOIN actor a ON fa.actor_id = a.actor_id
GROUP BY CONCAT(a.first_name, ' ', a.last_name)
ORDER BY COUNT(rental_id) desc
LIMIT 10


/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...
SELECT c.name,
		SUM(p.amount) revenue_per_category
FROM rental r 
LEFT JOIN payment p ON r.rental_id = p.rental_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN film_category fc ON i.film_id = fc.film_id
LEFT JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY SUM(p.amount) desc
LIMIT 1


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...
SELECT f.title FROM film f 
LEFT JOIN 
	(select DISTINCT film_id from inventory) inv ON f.film_id = inv.film_id
WHERE inv.film_id IS NULL 


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
		COUNT(*)
FROM category c 
LEFT JOIN film_category fc ON c.category_id = fc.category_id
LEFT JOIN film_actor fa ON fc.film_id = fa.film_id 
LEFT JOIN actor a ON fa.actor_id = a.actor_id
WHERE c.name = 'Children'
GROUP BY CONCAT(a.first_name, ' ', a.last_name)
ORDER BY COUNT(*) DESC
LIMIT 3 