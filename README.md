
# AI-Based Cache System for Optimizing Hotel Price Search Engine API Calls

## Overview
This project aims to optimize search engine API calls for hotel prices by using an AI-based caching system. The system determines the optimal Time to Live (TTL) for cached records based on dynamically calculated `changing_price_rate` values for each vendor and hotel.


![hotel_without_background](https://github.com/user-attachments/assets/e21044bb-3e6a-4460-86e7-6535ce709a24)



## Key Components

- **`cluster_per_vendor_ttt_los.py`**: 
  - Clusters hotel data to determine the optimal `changing_price_rate` for each vendor and hotel.
  
- **`hotels_price_cash_search_engine.py`**: 
  - Implements the AI-based cache system, calculating potential losses due to price fluctuations and optimizing API call frequency based on the `changing_price_rate`.

- **`visualize_hotels_price_cache.py`**: 
  - Visualizes clustering results and cache performance metrics.

## Workflow

1. **Data Clustering**: Run `cluster_per_vendor_ttt_los.py` to cluster data and find the best `changing_price_rate`.
2. **API Call Optimization**: Use `hotels_price_cash_search_engine.py` to optimize API calls with the AI-based cache system.
3. **Visualization**: Visualize the impact of the optimization using `visualize_hotels_price_cache.py`.

## Requirements
- Python 3.x
- Libraries: `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `numpy`

## Results


The loss heatmap indicates that the average loss is relatively low. Over time, this reduction in losses can lead to significant cost savings by minimizing the number of API calls required.


![image](https://github.com/user-attachments/assets/245e7bef-259b-4f8b-910f-00b87872721f)




