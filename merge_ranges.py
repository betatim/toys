from operator import itemgetter

periods = [(1,4), (8, 9), (7, 10), (1,2), (2,3), (11,12), (5,5), (6,8)]


def merge(periods, sort_key, start, end):
    periods = sorted(periods, key=sort_key)

    merged = [periods[0]]
    for period in periods:
        s = start(period)
        e = end(period)

        ee = end(merged[-1])
        if s <= ee:
            if e > ee:
                merged[-1] = (start(merged[-1]), e)
            else:
                merged[-1] = (start(merged[-1]), ee)

        else:
            merged.append(period)

    return merged
        

if __name__ == "__main__":
    import timeit
    print periods
    print "becomes"
    print merge(periods, itemgetter(0), itemgetter(0), itemgetter(-1))

    print min(timeit.repeat("merge(periods, itemgetter(0), itemgetter(0), itemgetter(-1))", "from merge_ranges import merge, periods; from operator import itemgetter"))
