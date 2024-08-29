import os
import json
import csv

CONVERTION_RATE_REAL = 0.1
CONVERTION_RATE_HIGHER_PRICE = 0.1
COMMISION = 0.05
TRESHOLD_SKIP_MINUTES = 60 * 600
PRICE_THRESHOLD_MULTIPLIER= 2


def calculate_loss_for_hotel(hotel_data, changing_price_rate):
    # print(changing_price_rate)
    changing_price_rate = changing_price_rate * 60
    total_loss = 0.0
    previous_price = None
    last_update_time = None
    cached_price = 0
    counter_equal_prices = 0
    count_skips = 0
    counter_of_samples = 0

    for timestamp, current_price in hotel_data:
        if previous_price is not None and last_update_time is not None:
            # Calculate the time difference between the current timestamp and the last update time

            time_difference = timestamp - last_update_time

            if (abs(time_difference)) > TRESHOLD_SKIP_MINUTES or cached_price * PRICE_THRESHOLD_MULTIPLIER < current_price or cached_price / PRICE_THRESHOLD_MULTIPLIER > current_price:
                cached_price = current_price
                last_update_time = timestamp
                count_skips += 1
                continue
            counter_of_samples += 1
            
            if time_difference >= changing_price_rate:
                # Time difference exceeds or equals the threshold, update the price
                cached_price = current_price
                last_update_time = timestamp

            else:
                if cached_price == current_price:
                    counter_equal_prices += 1
                    continue
                elif cached_price > current_price:
                    # Higher reported price scenario
                    convertion_rate_higher_ratio = (current_price / cached_price) * CONVERTION_RATE_HIGHER_PRICE
                    potential_loss = abs(current_price * CONVERTION_RATE_REAL - cached_price * convertion_rate_higher_ratio)
                    total_loss += potential_loss
                elif cached_price < current_price:
                    # Lower reported price scenario
                    commission = cached_price * COMMISION
                    loss = max(0, current_price - cached_price - commission)
                    total_loss += loss
        else:
            # First record or initialization
            cached_price = current_price
            last_update_time = timestamp

        # Set previous_price to the cached price for the next iteration
        previous_price = cached_price
    # print("The number of matches is = ", str(counter_equal_prices))
    # print(count_skips)
    return int(total_loss/counter_of_samples if counter_of_samples > 0 else 0)

def process_json_files(json_files, files):
    avg_loss = 0
    counter = 0
    results = {}
    for json_file in json_files:
        # print(json_file)
        split = json_file.split('\\')                       
        split = split[1]
        full_cluster_path = cluster_folder + '/' + split
        #open the cluster file
        try:
            with open(full_cluster_path, 'r') as f:
                try:
                    cluster_data = json.load(f)
                except:
                    continue
        except:
            continue
        for item in cluster_data[0]:
            real_value = str(cluster_data[0][item])
            real_avg = cluster_data[1][real_value]
            cluster_data[0][item] = real_avg
        clusters_with_prices = cluster_data[0]
            # hotel_cluster = cluster_data[]
        # print(full_cluster_path)
        # print(split)        
        with open(json_file, 'r') as file:
            data = json.load(file)
            vendor_name = os.path.basename(json_file).split('.')[0]
            results[vendor_name] = {}

            for hotel_entry in data:
                for hotel_name, hotel_data in hotel_entry.items():
                    try:
                        cluster_price = clusters_with_prices[hotel_name]
                    except:
                        cluster_price = 250
                    loss = calculate_loss_for_hotel(hotel_data,cluster_price)
                    counter += 1
                    avg_loss += loss
                    results[vendor_name][hotel_name] = int(loss)
    print("The average loss is = ", str(avg_loss/counter))
    return results

def write_results_to_csv(results, output_file):
    hotel_names = sorted({hotel for vendor in results.values() for hotel in vendor.keys()})
    vendor_names = sorted(results.keys())

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hotel/Vendor'] + vendor_names)

        for hotel in hotel_names:
            row = [hotel]
            for vendor in vendor_names:
                row.append(results[vendor].get(hotel, 0.0))
            writer.writerow(row)



# Example usage:
json_dir = 'all_combos_and_timelines'  # Directory containing JSON files
list_of_rates = [50,100,150,200,250,300,350]
changing_rate_minuts = 201
changing_price_rate = changing_rate_minuts * 60  # Example threshold in seconds (5 hours), replace with your value
output_file = 'hotel_losses_' + str(changing_rate_minuts) + '.csv'
cluster_folder = 'clustered_data_by_vendor_ttt_los'

# List all JSON files in the directory
json_files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if file.endswith('.json')]
files = os.listdir(json_dir)


results = process_json_files(json_files,files)
write_results_to_csv(results, output_file)

print(f'Results written to {output_file}')
