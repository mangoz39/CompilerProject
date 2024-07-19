import main

for i in range(1, 8):
    for j in range(1, 3):
        path = f'./data/0{i}_{j}_hidden.lsp'
        print(f"-----testcase {i}_{j}-----")
        with open(path, "r") as fp:
            content = fp.read()
            ast = main.parser.parse(content)
