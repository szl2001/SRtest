from multiprocessing import Pool
import pickle
import torch
from torchtext.vocab import build_vocab_from_iterator
import numpy as np
from e2elang.srasm_visitor import SRasmVisitor
from floatconvert.fp16_base10_converter import FP16Base10Converter
from pathlib import Path

source_dir = Path("/lustre/S/nanziyuan/codes/srasm/data/SRmaker/dataset/raw_tree/")
target_dir = Path("/lustre/S/nanziyuan/codes/srasm/data/SRmaker/dataset/srasm/")

PAD = "<PAD>"
EOS = "<EOS>"

def worker(task_id):
    with open(source_dir / f"data{task_id}.pkl", "rb") as f:
        data = pickle.load(f)

    float_converter = FP16Base10Converter()
    asm_vis = SRasmVisitor(float_converter)
    tokens = [asm_vis.tokens()]
    op_vocab = build_vocab_from_iterator(tokens, specials=[PAD, EOS])

    pad = torch.tensor([op_vocab["<PAD>"]])
    eos = torch.tensor([op_vocab["<EOS>"]])
    nil = torch.tensor([0])

    encode_arr = np.vectorize(float_converter.encode)

    datasets = []
    for tree, points_set in data:
        instrs = asm_vis.visit(tree)
        assert len(instrs) <= 128

        ops, operand0s, operand1s = zip(*instrs)

        # coincide with End-to-End
        ops = torch.cat((pad, torch.tensor(ops), eos))
        operand0s = torch.cat((nil, torch.tensor(operand0s), nil))
        operand1s = torch.cat((nil, torch.tensor(operand1s), nil))
        
        for points in points_set:
            # points.shape: ((1 + input_dim), num_points)
            points = torch.tensor(points)
            datasets.append((ops, operand0s, operand1s, points))

    torch.save(datasets, target_dir / f"tensor{task_id}.pt")
    if task_id == 0:
        torch.save(op_vocab, target_dir / "op_vocab.pt")


def main():
    pool = Pool(32)
    pool.map(worker, range(100))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
