import requests
import time


def make_request_and_log(api_endpoint, log_file_path):
    with open(log_file_path, "a") as log_file:
        try:
            body = {"samples": 1}
            # If Double
            # body = {"input_value": 1}
            start_time = time.time()
            response = requests.post(f"{api_endpoint}/monte-carlo", json=body)
            duration = time.time() - start_time
            # Check if the request was successful
            if response.status_code == 200:
                current_time_string = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                log_file.write(f"{current_time_string},{duration},{response.json()['elapsed_time_s']}\n")
            else:
                log_file.write(
                    f"Failed (Status code {response.status_code}): Time taken for request: {duration} seconds\n")
        except requests.RequestException as e:
            log_file.write(f"Error: {e}\n")


def main(log_file_path, number_of_requests, url):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Time,Request Time,Computation Time\n")

    # Main loop for making the requests
    for i in range(number_of_requests):
        print(f"Making request {i + 1}/{number_of_requests}")
        make_request_and_log(url, log_file_path)
        # Wait for 1 second between requests to not overwhelm the API
        time.sleep(1)

    print(f"Completed {number_of_requests} requests. Log written to {log_file_path}")


if __name__ == "__main__":
    # Log file path
    log_file_path = "logs/log_monte_kubernetes_with_alb_subnet.csv"
    # API endpoint you want to hit
    url_dev = "http://localhost:8000"
    url_prod = "http://k8s-default-rayclust-739f2d7083-1916008357.eu-west-2.elb.amazonaws.com"
    # Number of times you want to hit the API
    number_of_requests = 100
    main(log_file_path, number_of_requests, url_prod)
