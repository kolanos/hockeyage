import random, bisect

def weighted_choice(items):
    """items is a list of tuples in the form (item, weight)"""
    weight_total = sum((item[1] for item in items))
    n = random.uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item

def weighted_choice_bisect(items):
    added_weights = []
    last_sum = 0
    for item, weight in items:
        last_sum += weight
        added_weights.append(last_sum)
    return items[bisect.bisect(added_weights, random.random() * last_sum)][0]

def weighted_choice_compile(items):
    """returns a function that fetches a random item from items

    items is a list of tuples in the form (item, weight)"""
    weight_total = sum((item[1] for item in items))
    def choice(uniform = random.uniform):
        n = uniform(0, weight_total)
        for item, weight in items:
            if n < weight:
                return item
            n = n - weight
        return item
    return choice

def weighted_choice_bisect_compile(items):
    """returns a function that makes a weighted random choice from items."""
    added_weights = []
    last_sum = 0
    for item, weight in items:
        last_sum += weight
        added_weights.append(last_sum)
    def choice(rnd=random.random, bis=bisect.bisect):
        return items[bis(added_weights, rnd() * last_sum)][0]
    return choice
