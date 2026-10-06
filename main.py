"""攀岩训练伙伴（原型）：命令行入口。"""


def send_rate(sends: int, attempts: int) -> float:
    """完攀率：完攀次数 / 尝试次数。"""
    return sends / attempts

def main() -> None:
    print("攀岩训练伙伴 · 原型 v0")
    print(f"示例完攀率：{send_rate(3, 5):.0%}")


if __name__ == "__main__":
    main()
