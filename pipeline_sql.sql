CREATE OR REPLACE VIEW v_logistics_performance_analytics AS
WITH order_metrics AS(
SELECT
	 order_id,
	 order_timestamp,
	 hub_id,
	 hub_region,
	 shipping_tier,
	 item_weight_lbs,
	 route_distance_miles,
	 base_carrier_cost,
	 CASE
	 	WHEN dest_lon < -114 AND hub_region != 'West' THEN 'Cross-Country Structural Leakage'
		WHEN dest_lon BETWEEN -114 AND -98 AND hub_region != 'Mid-West' THEN 'Out-of-Region Inefficiency'
		WHEN dest_lon > -80 AND hub_region != 'East' THEN 'Out-of-Region Inefficiency'
		ELSE 'Optimized Regional Fulfillment'
	 END AS routing_efficiency_status,
	 base_carrier_cost/NULLIF(route_distance_miles, 0) AS cost_per_mile
 FROM orders	 
)

SELECT 
	order_id,
	order_timestamp,
	DATE_TRUNC('day', order_timestamp) AS order_date,
	EXTRACT(WEEK FROM order_timestamp) AS order_week,
	EXTRACT(HOUR FROM order_timestamp) AS order_hour_of_day,
	hub_id,
	hub_region,
	shipping_tier,
	item_weight_lbs,
	route_distance_miles,
	base_carrier_cost,
	routing_efficiency_status,
	ROUND(CAST(cost_per_mile AS NUMERIC), 4) AS cost_per_mile,
	CASE
		WHEN route_distance_miles > 1500 AND shipping_tier = 'Next-day' THEN 'High Breach Risk'
		WHEN route_distance_miles > 800 AND item_weight_lbs > 15 THEN 'Heavy Long-Haul Penalty'
		ELSE 'Normal Operations'
	END AS operational_risk_profile
FROM order_metrics;
	