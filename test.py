from utils import ParameterValidator


@ParameterValidator.type("y", str)
@ParameterValidator.values(param_name="x", allowed_values=[1, 2, 3])
@ParameterValidator.values("y", allowed_values=["Hello"])
def test(x: int, y: str, z: list, a: bool = True):
    print("Hello world")


if __name__ == "__main__":
    test(1, "hell", [], True)
