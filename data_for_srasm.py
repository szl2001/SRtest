from multiprocessing import Pool
import pickle
import torch
import torch.nn.functional as F
import numpy as np
from e2elang.string_visitor import StringVisitor
from floatconvert.fp16_converter import FP16Converter


def worker(task_id):
    with open(f"data{task_id}.pkl", "rb") as f:
        data = pickle.load(f)

    float_converter = FP16Converter()
    str_vis = StringVisitor(float_converter)

    tokens = str_vis.tokens()
    token_map = {token: idx for idx, token in enumerate(tokens)}

    float_tokens = float_converter.tokens()
    # Convention: {<PAD>: 0}
    float_map = {token: idx + 1 for idx, token in enumerate(float_tokens)}

    encode_arr = np.vectorize(lambda x: float_map[float_converter.encode(x)])

    datasets = []
    for tree, points in data:
        sentence = [token_map[t] for t in str_vis.visit(tree)]
        sentence.append(token_map["<EOS>"])
        assert len(sentence) <= 128
        # padright = (0, 128 - len(sentence))
        # sen_tensor = F.pad(torch.tensor(sentence), padright, "constant", 0)
        sen_tensor = torch.tensor(sentence)

        for point in points:
            # point.shape: ((input_dim + 1), num_points)
            arr = encode_arr(point)
            # padright = (0, 200 - arr.shape[1])
            # arr_tensor = F.pad(torch.tensor(arr), padright, "constant", 0)

            arr_tensor = torch.tensor(arr.flatten("F"))

            datasets.append((sen_tensor, arr_tensor))

    torch.save(datasets, f"srasm{task_id}.pt")


def main():
    pool = Pool(32)
    pool.map(worker, range(10))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()