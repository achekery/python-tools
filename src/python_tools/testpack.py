
import traceback

null, false, true = None, False, True

def test_functional(inputs, checks, klass):
    print(f"test_functional >>> {klass=}")
    obj = klass()
    for count, (name, ar, exp) in enumerate(zip(*inputs)):
        if name == klass.__name__.split("_")[0]:
            obj = klass(*ar)
            func = lambda *x, **y: (None, None)
        else:
            func = getattr(obj, name)
        check = [k for k, v in checks.items() if name in v][0]
        msg = f"when {name=}, {ar=}"
        try:
            res = func(*ar)
        except Exception as exc:
            msg += f" -> {exc=}"
            print(msg)
            traceback.print_exc()
            continue
        else:
            msg += f" -> {check=}: {res=}, {exp=}"
        match check:
            case "ignore":
                pass
            case "eq":
                assert res == exp, msg
            case "eq_when_sorted_two_deep":
                assert sorted([sorted(v) for v in res]) == sorted([sorted(v) for v in exp]), msg
            case "in_list":
                assert res in exp, msg
            case _:
                raise ValueError(f"unknown check: {check=}")
        print(f"test_functional : {msg=}")
    print(f"test_functional <<<")
    
import random
import timeit

def test_performance(klass, timer=None, repeat=100):
    print(f"test_performance >>> {klass=}, {timer=}, {repeat=}")
    if timer is None:
        timer = timeit.Timer(
            stmt='_ = [m.addAtIndex(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(2000)]',
            setup=f"m=MyLinkedList()",
            globals={"random": random, "MyLinkedList": klass},
        )
    number, time_taken = timer.autorange()
    autorange_stats = {
        "number": number,
        "time_taken": time_taken,
    }
    print(f"{autorange_stats=}")
    results = timer.repeat(repeat=repeat, number=number)
    repeat_stats = {
        "len": len(results),
        "min": min(results),
        "max": max(results),
        "avg": sum(results) / len(results),
    }
    print(f"{repeat_stats=}")
    perf_time = repeat_stats["min"] / number
    print(f"test_performance <<< {perf_time=}")
    return perf_time
