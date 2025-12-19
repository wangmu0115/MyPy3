def http_error(status):  # Simple pattern: match to a literal
    match status:
        case 400:
            return "Bad request"
        case 401 | 402 | 403:
            return "Not allowed"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return f"Something's wrong with the internet: {status}"


def show_point(p):  # Patterns with a literal and variable
    match p:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y = {y}")
        case (x, 0):
            print(f"X = {x}")
        case (x, y):
            print(f"X = {x}, Y = {y}")
        case _:
            raise ValueError(f"{p} not a point.")


if __name__ == "__main__":
    print(http_error(400))
    print(http_error(402))
    print(http_error(404))
    print(http_error(418))
    print(http_error(449))
    show_point((0, 0))
    show_point((0, 9))
    show_point((42, 0))
    show_point((3.5, 2.2))
    show_point((3.5, 2.2, 1.1))
