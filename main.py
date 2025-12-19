import argparse
from parser import parse_text
import tomlkit


def to_toml(data):
    def convert(d):
        if isinstance(d, dict):
            t = tomlkit.table()
            for k, v in d.items():
                if isinstance(v, dict):
                    t.add(k, convert(v))
                elif isinstance(v, list):
                    t.add(k, v)
                else:
                    t.add(k, v)
            return t
        else:
            return d
    return convert(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    data = parse_text(text)
    toml_data = to_toml(data)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(toml_data))


if __name__ == "__main__":
    main()
