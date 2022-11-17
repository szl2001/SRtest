from multiprocessing import Pool
import pickle
import torch
from torchtext.vocab import build_vocab_from_iterator
import numpy as np
from e2elang.string_visitor import StringVisitor
from floatconvert.fp16_converter import FP16Converter
from pathlib import Path

source_dir = Path("/lustre/S/nanziyuan/codes/srasm/data/SRmaker/dataset/raw_tree/")
target_dir = Path("/lustre/S/nanziyuan/codes/srasm/data/SRmaker/dataset/plain_tensor/")


def worker(task_id):
    with open(source_dir / f"data{task_id}.pkl", "rb") as f:
        data = pickle.load(f)

    float_converter = FP16Converter()
    str_vis = StringVisitor(float_converter)
    expr_vocab = build_vocab_from_iterator(
        [str_vis.tokens()], specials=["<PAD>", "<EOS>"])
    points_vocab = build_vocab_from_iterator(
        [float_converter.tokens()], specials=["<PAD>"])

    eos = torch.tensor([expr_vocab["<EOS>"]])

    encode_arr = np.vectorize(float_converter.encode)

    datasets = []
    for tree, points in data:
        sentence = expr_vocab(list(str_vis.visit(tree)))
        assert len(sentence) <= 128
        # coincide with End-to-End
        sen_tensor = torch.cat((eos, torch.tensor(sentence), eos))

        for point in points:
            # point.shape: ((input_dim + 1), num_points)
            # flatten by columns and transform to tensor
            point_tokens = encode_arr(point.flatten("F")).tolist()
            point_tensor = torch.tensor(points_vocab(point_tokens))

            datasets.append((sen_tensor, point_tensor))

    torch.save(datasets, target_dir / f"tensor{task_id}.pt")
    if task_id == 0:
        torch.save(expr_vocab, target_dir / "expr_vocab.pt")
        torch.save(points_vocab, target_dir / "points_vocab.pt")


def main():
    pool = Pool(32)
    pool.map(worker, range(100))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
