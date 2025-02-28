import argparse

from . import _core


def main():
    parser = argparse.ArgumentParser(
        description="SeedKey - the Activation Tool of SeedMath"
    )

    # 添加产品选择选项组
    product_group = parser.add_mutually_exclusive_group(required=True)
    product_group.add_argument(
        "--seedmip", action="store_true", help="激活 SeedMIP 求解器"
    )
    product_group.add_argument(
        "--seedsat", action="store_true", help="激活 SeedSAT 求解器"
    )
    product_group.add_argument(
        "--seedsmt", action="store_true", help="激活 SeedSMT 求解器"
    )

    # 添加激活码参数
    parser.add_argument("activation_code", type=str, help="激活码")

    args = parser.parse_args()

    # 确定要激活的产品
    if args.seedmip:
        product = "seedmip"
    elif args.seedsat:
        product = "seedsat"
    elif args.seedsmt:
        product = "seedsmt"

    # 使用新添加的 activate 函数
    result = _core.activate(product, args.activation_code)

    if result:
        print(f"激活成功！{product} 已成功激活。")
        return 0
    else:
        print(f"激活失败！无法激活 {product}。")
        return -1


if __name__ == "__main__":
    import sys

    sys.exit(main())
