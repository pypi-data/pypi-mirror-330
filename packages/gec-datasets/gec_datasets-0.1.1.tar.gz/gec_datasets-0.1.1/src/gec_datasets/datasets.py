import os
import subprocess
import requests
import tarfile
import shutil
from pathlib import Path
from gecommon import Parallel
from dataclasses import dataclass


class GECDatasets:
    def __init__(self, base_path="datasets/"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    @dataclass
    class GECData:
        srcs: list[str]
        refs: list[list[str]]

    def download(self, data_id):
        download_functions = {
            "conll13": self.download_conll13,
            "conll14": self.download_conll14,
            "bea19": self.download_bea19,
            "fce": self.download_fce,
            "jfleg": self.download_jfleg,
            "cweb": self.download_cweb,
            "wi-locness": self.download_wi_locness,
            "nucle": self.download_nucle,
            "lang8": self.download_lang8,
            "troy-1bw": self.download_troy_1bw,
            "troy-blogs": self.download_troy_blogs,
            "pie-synthetic": self.download_pie_synthetic
        }
        for d in download_functions.keys():
            if d in data_id:
                download_functions[d]()
                return
        raise ValueError(
            f"The data_id={data_id} is invalid. It should be in: {list(download_functions.keys())}."
        )

    def load(self, data_id: str) -> GECData:
        data_path = self.base_path / data_id
        src_file = data_path / "src.txt"
        if not src_file.exists():
            # E.g., "jfleg-test" -> "jfleg"
            self.download(data_id)

        if not src_file.exists():
            raise FileNotFoundError(f"Source file not found: {src_file}")
        with open(src_file, "r", encoding="utf-8") as f:
            srcs = [line.strip() for line in f]

        refs = []
        ref_index = 0
        while True:
            ref_file = data_path / f"ref{ref_index}.txt"
            if not ref_file.exists():
                break
            with open(ref_file, "r", encoding="utf-8") as f:
                refs.append([line.strip() for line in f])
            ref_index += 1

        if len(refs) > 0 and not all(len(ref) == len(srcs) for ref in refs):
            raise ValueError(
                "Mismatch in number of sentences between src.txt and ref*.txt files."
            )

        return self.GECData(srcs=srcs, refs=refs)

    def download_and_extract(self, url, dest_path, extract=True):
        dest_path = Path(dest_path)
        dest_path.mkdir(parents=True, exist_ok=True)
        tar_file = dest_path / "temp.tar.gz"

        print(f"Downloading from {url} to {tar_file}...")
        response = requests.get(url, stream=True)
        with open(tar_file, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        if extract:
            print(f"Extracting {tar_file}...")
            with tarfile.open(tar_file, "r:gz") as tar:
                tar.extractall(path=dest_path)
            tar_file.unlink()

    def m2_to_raw(self, m2_file, ref_id, output_file):
        print(f"Processing M2 file: {m2_file} with ref_id={ref_id}...")
        gec = Parallel.from_m2(m2_file, ref_id=ref_id)
        with open(output_file, "w") as f:
            f.write("\n".join(gec.trgs) + "\n")

    def m2_to_src(self, m2_file, output_file):
        with open(output_file, "w") as src_out:
            for line in open(m2_file):
                if line.startswith("S"):
                    src_out.write(" ".join(line.split(" ")[1:]))

    def download_conll13(self):
        data_id = "conll13"
        data_path = self.base_path / data_id
        url = "https://www.comp.nus.edu.sg/~nlp/conll13st/release2.3.1.tar.gz"
        self.download_and_extract(url, data_path)

        m2_file = data_path / "release2.3.1/original/data/official-preprocessed.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")

    def download_conll14(self):
        data_id = "conll14"
        data_path = self.base_path / data_id
        url = "https://www.comp.nus.edu.sg/~nlp/conll14st/conll14st-test-data.tar.gz"
        self.download_and_extract(url, data_path)

        m2_file = data_path / "conll14st-test-data/noalt/official-2014.combined.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")
        self.m2_to_raw(m2_file, 1, data_path / "ref1.txt")

    def download_bea19(self):
        data_id_dev = "bea19-dev"
        data_path = self.base_path / data_id_dev
        url = "https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz"
        self.download_and_extract(url, data_path)

        m2_file = data_path / "wi+locness/m2/ABCN.dev.gold.bea19.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")

        data_id_test = "bea19-test"
        data_path = self.base_path / data_id_test
        data_path.mkdir(parents=True, exist_ok=True)
        src_file = self.base_path / "bea19-dev/wi+locness/test/ABCN.test.bea19.orig"
        shutil.copy(src_file, data_path / "src.txt")

    def download_wi_locness(self):
        data_id_train = "wi-locness-train"
        data_path = self.base_path / data_id_train
        url = "https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz"
        self.download_and_extract(url, data_path)

        m2_file = data_path / "wi+locness/m2/ABC.train.gold.bea19.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")

    def download_jfleg(self):
        data_id_dev = "jfleg-dev"
        data_path_dev = self.base_path / data_id_dev
        data_path_dev.mkdir(parents=True, exist_ok=True)

        jfleg_repo_path = data_path_dev / "jfleg"
        if not jfleg_repo_path.exists():
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/keisks/jfleg.git",
                    str(jfleg_repo_path),
                ],
                check=True,
            )

        print(f"Processing {data_id_dev}...")
        shutil.copy(jfleg_repo_path / "dev/dev.src", data_path_dev / "src.txt")
        shutil.copy(jfleg_repo_path / "dev/dev.ref0", data_path_dev / "ref0.txt")
        shutil.copy(jfleg_repo_path / "dev/dev.ref1", data_path_dev / "ref1.txt")
        shutil.copy(jfleg_repo_path / "dev/dev.ref2", data_path_dev / "ref2.txt")
        shutil.copy(jfleg_repo_path / "dev/dev.ref3", data_path_dev / "ref3.txt")

        data_id_test = "jfleg-test"
        data_path_test = self.base_path / data_id_test
        data_path_test.mkdir(parents=True, exist_ok=True)

        print(f"Processing {data_id_test}...")
        shutil.copy(jfleg_repo_path / "test/test.src", data_path_test / "src.txt")
        shutil.copy(jfleg_repo_path / "test/test.ref0", data_path_test / "ref0.txt")
        shutil.copy(jfleg_repo_path / "test/test.ref1", data_path_test / "ref1.txt")
        shutil.copy(jfleg_repo_path / "test/test.ref2", data_path_test / "ref2.txt")
        shutil.copy(jfleg_repo_path / "test/test.ref3", data_path_test / "ref3.txt")

    def download_cweb(self):
        data_id_s_dev = "cweb-s-dev"
        data_path_s_dev = self.base_path / data_id_s_dev
        data_path_s_dev.mkdir(parents=True, exist_ok=True)

        cweb_repo_path = data_path_s_dev / "CWEB"
        if not cweb_repo_path.exists():
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/SimonHFL/CWEB.git",
                    str(cweb_repo_path),
                ],
                check=True,
            )

        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.dev.source", data_path_s_dev / "src.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.dev.ann1", data_path_s_dev / "ref0.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.dev.ann2", data_path_s_dev / "ref1.txt"
        )

        data_id_s_test = "cweb-s-test"
        data_path_s_test = self.base_path / data_id_s_test
        data_path_s_test.mkdir(parents=True, exist_ok=True)

        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.test.source", data_path_s_test / "src.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.test.ann1", data_path_s_test / "ref0.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-S.test.ann2", data_path_s_test / "ref1.txt"
        )

        data_id_g_dev = "cweb-g-dev"
        data_path_g_dev = self.base_path / data_id_g_dev
        data_path_g_dev.mkdir(parents=True, exist_ok=True)

        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.dev.source", data_path_g_dev / "src.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.dev.ann1", data_path_g_dev / "ref0.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.dev.ann2", data_path_g_dev / "ref1.txt"
        )

        data_id_g_test = "cweb-g-test"
        data_path_g_test = self.base_path / data_id_g_test
        data_path_g_test.mkdir(parents=True, exist_ok=True)

        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.test.source", data_path_g_test / "src.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.test.ann1", data_path_g_test / "ref0.txt"
        )
        shutil.copy(
            cweb_repo_path / "data/raw/CWEB-G.test.ann2", data_path_g_test / "ref1.txt"
        )

    def download_fce(self):
        url = (
            "https://www.cl.cam.ac.uk/research/nl/bea2019st/data/fce_v2.1.bea19.tar.gz"
        )

        data_id_dev = "fce-dev"
        data_path_dev = self.base_path / data_id_dev
        data_path_dev.mkdir(parents=True, exist_ok=True)
        tar_file = data_path_dev / "fce_v2.1.bea19.tar.gz"

        if not tar_file.exists():
            print(f"Downloading FCE dataset to {tar_file}...")
            self.download_and_extract(url, data_path_dev)

        dev_m2_file = data_path_dev / "fce/m2/fce.dev.gold.bea19.m2"
        self.m2_to_src(dev_m2_file, data_path_dev / "src.txt")
        self.m2_to_raw(dev_m2_file, 0, data_path_dev / "ref0.txt")

        data_id_test = "fce-test"
        data_path_test = self.base_path / data_id_test
        data_path_test.mkdir(parents=True, exist_ok=True)

        print(f"Processing {data_id_test}...")
        test_m2_file = data_path_dev / "fce/m2/fce.test.gold.bea19.m2"
        self.m2_to_src(test_m2_file, data_path_test / "src.txt")
        self.m2_to_raw(test_m2_file, 0, data_path_test / "ref0.txt")

        data_id_train = "fce-train"
        data_path_train = self.base_path / data_id_train
        data_path_train.mkdir(parents=True, exist_ok=True)

        print(f"Processing {data_id_train}...")
        train_m2_file = data_path_dev / "fce/m2/fce.train.gold.bea19.m2"
        self.m2_to_src(train_m2_file, data_path_train / "src.txt")
        self.m2_to_raw(train_m2_file, 0, data_path_train / "ref0.txt")

    def download_nucle(self):
        data_id = "nucle-train"
        data_path = self.base_path / data_id
        tar_file = data_path / "release3.3.tar.bz2"

        print(f"Extracting {tar_file}...")
        with tarfile.open(tar_file, "r:bz2") as tar:
            tar.extractall(path=data_path)
        tar_file.unlink()

        m2_file = data_path / "release3.3/bea2019/nucle.train.gold.bea19.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")

    def download_lang8(self):
        data_id = "lang8-train"
        data_path = self.base_path / data_id
        tar_file = data_path / "lang8.bea19.tar.gz"

        print(f"Extracting {tar_file}...")
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall(path=data_path)
        tar_file.unlink()

        m2_file = data_path / "lang8.train.auto.bea19.m2"
        self.m2_to_src(m2_file, data_path / "src.txt")
        self.m2_to_raw(m2_file, 0, data_path / "ref0.txt")

    def download_troy_1bw(self):
        data_id_train = "troy-1bw-train"
        data_path_train = self.base_path / data_id_train
        data_path_train.mkdir(parents=True, exist_ok=True)

        download_path = data_path_train / 'Troy-1BW.zip'
        if not download_path.exists():
            subprocess.run(
                [
                    "gdown",
                    "--fuzzy",
                    "https://drive.google.com/file/d/1aaUGLGyV3lxIbX2CIt0qw0_UM7nQUrhx/view?usp=drive_link",
                    "-O",
                    download_path
                ],
                check=True,
            )
            subprocess.run(
                [
                    "unzip",
                    download_path,
                    "-d",
                    data_path_train,
                ]
            )
        shutil.copy(
            data_path_train / "new_1bw/train_source", data_path_train / "src.txt"
        )
        shutil.copy(
            data_path_train / "new_1bw/train_target", data_path_train / "ref0.txt"
        )

        data_id_dev = "troy-1bw-dev"
        data_path_dev = self.base_path / data_id_dev
        data_path_dev.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            data_path_train / "new_1bw/test_source", data_path_dev / "src.txt"
        )
        shutil.copy(
            data_path_train / "new_1bw/test_target", data_path_dev / "ref0.txt"
        )

    def download_troy_blogs(self):
        data_id_train = "troy-blogs-train"
        data_path_train = self.base_path / data_id_train
        data_path_train.mkdir(parents=True, exist_ok=True)

        download_path = data_path_train / 'Troy-Blogs.zip'
        if not download_path.exists():
            subprocess.run(
                [
                    "gdown",
                    "--fuzzy",
                    "https://drive.google.com/file/d/1sKCxtx2k41WIdshyjQjo_gIAAbB1LWNs/view?usp=drive_link",
                    "-O",
                    download_path
                ],
                check=True,
            )
            subprocess.run(
                [
                    "unzip",
                    download_path,
                    "-d",
                    data_path_train,
                ]
            )
        shutil.copy(
            data_path_train / "blogs/train_src", data_path_train / "src.txt"
        )
        shutil.copy(
            data_path_train / "blogs/train_tgt", data_path_train / "ref0.txt"
        )

        data_id_dev = "troy-blogs-dev"
        data_path_dev = self.base_path / data_id_dev
        data_path_dev.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            data_path_train / "blogs/dev_src", data_path_dev / "src.txt"
        )
        shutil.copy(
            data_path_train / "blogs/dev_tgt", data_path_dev / "ref0.txt"
        )

    def download_pie_synthetic(self):
        data_id = "pie-synthetic-a1"
        data_path = self.base_path / data_id
        data_path.mkdir(parents=True, exist_ok=True)

        download_path = data_path / 'synthetic.zip'
        if not download_path.exists():
            subprocess.run(
                [
                    "gdown",
                    "--fuzzy",
                    "https://drive.google.com/file/d/1bl5reJ-XhPEfEaPjvO45M7w0yN-0XGOA/view",
                    "-O",
                    download_path
                ],
                check=True,
            )
            subprocess.run(
                [
                    "unzip",
                    download_path,
                    "-d",
                    data_path,
                ]
            )
        for name in ['a1', 'a2', 'a3', 'a4', 'a5']:
            data_id_this = f"pie-synthetic-{name}"
            data_path_this = self.base_path / data_id_this
            data_path_this.mkdir(parents=True, exist_ok=True)
            shutil.copy(
                data_path / f"{name}/{name}_train_incorr_sentences.txt",
                data_path_this / "src.txt"
            )
            shutil.copy(
                data_path / f"{name}/{name}_train_corr_sentences.txt",
                data_path_this / "ref0.txt"
            )