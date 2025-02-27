# TransBrain

TransBrain is an integrated computational framework for bidirectional translation of brain-wide phenotypes between humans and mice. Specifically, TransBrain provides a systematic approach for cross-species quantitative comparison and mechanistic investigation of both normal and pathological brain functions.

![TransBrain_FIG1](https://github.com/user-attachments/assets/1d87b730-3928-480a-98fa-7a0492754ee5)

What can TransBrain do?

1. Exploring the similarity relationships at the transcriptional level.

2. Inferring the conservation of whole-brain phenotypes.

3. Transforming and annotating whole-brain functional circuits.

4. Linking specific mouse models with human diseases.

## Further Reading

If you wish to learn more about the construction details of this method, please refer to our article: [https://www.biorxiv.org/content/10.1101/2025.01.27.635016v1](https://www.biorxiv.org/content/10.1101/2025.01.27.635016v1) (in preprint).

## Installation

To install TransBrain as a package, run:

```sh
pip install TransBrain
```

You can also directly install the conda environment from the environment.yml file:

```sh
cd TransBrain
conda env create -f environment.yml
```
Then, install TransBrain using pip.

```sh
conda activate transbrain-package
pip install -e .
```
after installation , import and use it in your script:

```python
import TransBrain as TB

# Perform cross-species mapping
human_data = TB.trans_mouse_to_human(mouse_data)
mouse_data = TB.trans_human_to_mouse(human_data)
```

This allows seamless integration into your existing workflows. 🚀

## Getting Started

We provided [**Tutorial Cases**](#tutorial-cases) demonstrating how to apply TransBrain for cross-species translation and comparison, which includes:

* Analyzing and visualizing transcriptional similarity between humans and mice.

* Characterizing the evolutionary spectrum of resting-state fMRI network phenotypes.

* Annotating the optogenetic circuits in mice using Neurosynth.

* Linking gene mutations to imaging phenotype deviations in autism.

The analysis process and figures can be viewed in the Jupyter Notebook. The necessary files and datas for completing these analysis are included in the notebook's folder.

## Python Dependencies

Code mainly depends on the Python (>= 3.8.5) scientific stack.

```
numpy V1.22.4
pandas V1.5.3
matplotlib V3.7.3
Seaborn V0.13.2
nilearn V0.10.2
scipy V1.10.1
scikit-learn V1.3.2
```
See full list in environment.yml file. 

## License
This project is covered under the Apache 2.0 License.

## Support
For questions and comments, please file a Github issue and/or email Shangzheng Huang(huangshangzheng@ibp.ac.cn)


