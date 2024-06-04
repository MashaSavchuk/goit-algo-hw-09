import timeit

# COINS = [2, 1, 25, 50, 10, 5]
COINS = [50, 25, 10, 5, 2, 1]


def handle_error(func):
    def wrapper(total, coins):
        if total <= 0:
            raise ValueError("Total amount must be a positive integer.")
        if not coins or any(coin <= 0 for coin in coins):
            raise ValueError("Coins must be a non-empty list of positive integers.")
        if total == 0 or min(COINS) > total:
            return {}
        return func(total, coins)

    return wrapper


@handle_error
def find_coins_greedy(total, coins):
    change_coins = {}
    descending_coins_range = sorted(coins, reverse=True)
    for coin in descending_coins_range:
        count = total // coin
        total -= count * coin
        if count != 0:
            change_coins[coin] = count

    return change_coins


@handle_error
def find_min_coins(total, coins):
    dp = [float("inf")] * (total + 1)
    dp[0] = 0

    for i in range(1, total + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    change_coins = {}
    remaining_total = total
    for coin in reversed(coins):
        while (
            remaining_total - coin >= 0
            and dp[remaining_total] == dp[remaining_total - coin] + 1
        ):
            change_coins[coin] = change_coins.get(coin, 0) + 1
            remaining_total -= coin

    return change_coins


def benchmark(total):
    greedy_result = timeit.timeit(lambda: find_coins_greedy(total, COINS), number=1000)
    dynamic_result = timeit.timeit(lambda: find_min_coins(total, COINS), number=1000)
    return greedy_result, dynamic_result


if __name__ == "__main__":
    greedy_simple, dynamic_simple = benchmark(50)
    greedy_sm, dynamic_sm = benchmark(67)
    greedy_md, dynamic_md = benchmark(470)
    greedy_lg, dynamic_lg = benchmark(8852)

    greedy_sm_coin_combinations = find_coins_greedy(67, COINS)
    dynamic_sm_coin_combinations = find_coins_greedy(67, COINS)
    greedy_md_coin_combinations = find_coins_greedy(470, COINS)
    dynamic_md_coin_combinations = find_min_coins(470, COINS)
    greedy_lg_coin_combinations = find_min_coins(8852, COINS)
    dynamic_lg_coin_combinations = find_min_coins(8852, COINS)

    # Results for different exchange amounts made with the greedy algorithm
    print("{:<24}".format("Greedy algorithm:"), f"{greedy_sm:.6f} sec")
    print("{:<24}".format("Greedy algorithm:"), f"{greedy_md:.6f} sec")
    print("{:<24}".format("Greedy algorithm:"), f"{greedy_lg:.6f} sec")
    # Results for different exchange amounts made with the dynamic programming algorithm
    print("{:<24}".format("Dynamic programming:"), f"{dynamic_sm:.6f} sec")
    print("{:<24}".format("Dynamic programming:"), f"{dynamic_md:.6f} sec")
    print("{:<24}".format("Dynamic programming:"), f"{dynamic_lg:.6f} sec")

    # Coin combinations
    print(
        "Greedy allgorithm:",
        greedy_sm_coin_combinations,
        greedy_md_coin_combinations,
        greedy_lg_coin_combinations,
    )
    print(
        "Dynamic programming:",
        dynamic_sm_coin_combinations,
        dynamic_md_coin_combinations,
        dynamic_lg_coin_combinations,
    )

    # Simple
    print("{:<24}".format("Simple amount (greedy):"), f"{greedy_simple:.6f} sec")
    print("{:<24}".format("Simple amount (dynamic):"), f"{dynamic_simple:.6f} sec")
    