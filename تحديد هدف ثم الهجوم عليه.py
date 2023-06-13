import random
import string
import time
import hashlib
import concurrent.futures

addresses = set()

# Add the desired addresses directly to the set
addresses.add("bc1q2zraufq3t7se07xcwwlgvytdsyh2y6t25r3rnq")
addresses.add("bc1q2zraufq3t7se07xcwwlgvytdsyh2y6t25r3rnq")

start_time = time.time()
total_count = 0
match_found = False

def generate():
    private_key = ''.join(random.choices(string.hexdigits, k=64))
    public_key = hashlib.sha256(private_key.encode()).hexdigest()

    # Convert the public key to a Bech32 address
    bech32_address = "bc1" + public_key[:42]

    if bech32_address in addresses:
        print("")
        print("\033[92m>> Match Found: {}\033[0m".format(bech32_address))
        success_string = "Address: {}\n\nPrivate Key: {}".format(bech32_address, private_key)
        print(success_string)
        global match_found
        match_found = True
        return bech32_address

    global total_count
    total_count += 1

def start_workers(num_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(generate) for _ in range(num_workers)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result

def print_stats():
    elapsed_time_in_minutes = (time.time() - start_time) / 60
    speed_per_minute = total_count / elapsed_time_in_minutes
    print("Total Addresses Generated:", total_count)
    print("Addresses per Minute:", "{:.2f}".format(speed_per_minute))

def run_brute_force(num_workers):
    print("Multithread Bitcoin Brute Force (Bech32 Only)")
    print("---------------------(mustafa)-----------------------")

    if num_workers <= 0:
        print('Invalid number of workers. Must be a positive integer.')
        exit(1)

    print("Number of Workers:", num_workers)

    match_address = start_workers(num_workers)

    if match_address:
        global match_found
        match_found = True

    print_stats()

    if not match_found:
        print("No match found in the provided addresses.")

def run_program(num_workers):
    run_brute_force(num_workers)

# Set the desired number of workers here
num_workers = 1000000

run_program(num_workers)
