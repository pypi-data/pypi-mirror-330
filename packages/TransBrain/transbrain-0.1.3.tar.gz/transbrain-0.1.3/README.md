# TransBrain

TransBrain is an integrated computational framework for bidirectional translation of brain-wide phenotypes between humans and mice. Specifically, TransBrain provides a systematic approach for cross-species quantitative comparison and mechanistic investigation of both normal and pathological brain functions.


What can TransBrain do?

1. Exploring the similarity relationships at the transcriptional level.

2. Inferring the conservation of whole-brain phenotypes.

3. Transforming and annotating whole-brain functional circuits.

4. Linking specific mouse models with human diseases.

## Further Reading

If you wish to learn more about the construction details of this method, please refer to our article: [https://www.biorxiv.org/content/10.1101/2025.01.27.635016v1](https://www.biorxiv.org/content/10.1101/2025.01.27.635016v1) (in preprint).


## Getting Started

We provided tutorial cases (https://github.com/ibpshangzheng/Transbrain) demonstrating how to apply TransBrain for cross-species translation and comparison, which includes:

* Analyzing and visualizing transcriptional similarity between humans and mice.

* Characterizing the evolutionary spectrum of resting-state fMRI network phenotypes.

* Annotating the optogenetic circuits in mice using Neurosynth.

* Linking gene mutations to imaging phenotype deviations in autism.

The analysis process and figures can be viewed in the Jupyter Notebook. The necessary files and datas for completing these analysis are included in the notebook's folder.

## Python Dependencies

Code mainly depends on the Python (>= 3.8.5) scientific stack.

```
matplotlib==3.7.5,
matplotlib-inline==0.1.7,
nibabel==5.2.1,
nilearn==0.10.4,
numpy==1.24.4,
openpyxl==3.1.5,
pandas==2.0.3,
scikit-learn==1.3.2,
scipy==1.10.1,
seaborn==0.13.2,
six==1.17.0,
```
See full list in environment.yml file. 

## License
This project is covered under the Apache 2.0 License.

## Support
For questions and comments, please file a Github issue and/or email Shangzheng Huang(huangshangzheng@ibp.ac.cn)


