metro_areas = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
    ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
    ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]


def _main():
    print(f"{'':15} | {'latitude':>9} | {'longitude':>9}")
    for metro_area in metro_areas:
        # match 关键字后面的表达式是匹配对象（subject），即各个 case 子句中的模式尝试匹配的数据。
        match metro_area:
            # 一个 case 子句由两部分组成：一部分是模式，另一部分是使用 if 关键字指定的卫语句（guard clause，可选）。
            case [city, _, _, (lat, lon)] if lon <= 0:
                print(f"{city:15} | {lat:9.4f} | {lon:9.4f}")


if __name__ == "__main__":
    _main()
