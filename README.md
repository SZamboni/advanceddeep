# Introduction
Project done for the Advanced Deep Learning course held by Hossein Azizpour during Period 1 (September and October) 2019 at KTH.
The task was to reproduce and reimplement the paper "Zero-shot Knowledge Transfer via Adversarial Belief Matching" (https://arxiv.org/pdf/1905.09768.pdf) presented at NIPS 2019. 
The project has been done by Olivier Nicolini, Matteo Tadiello and Simone Zamboni.
In this repository the report for the course project can be found.

# Author's code
The first folder is the "Authors' code". There are two more subfolders. 
In the first one, Few_shot_learning , there is the few-shot code (taken from https://github.com/polo5/FewShotKnowledgeTransfer) for the Knowledge Distillation + Attention used in the paper as a baseline against the zero-shot method. In this folder, we only downloaded the pretrained models and created a file called our main, that we used with command line options to run the six experiments with CIFAR10.
In the second folder, Zero_shot_learning, there is the code for the zero-shot learning method (taken from https://github.com/polo5/ZeroShotKnowledgeTransfer), where we downloaded the pretrained models. The code has been slightly modified in order to run it on our environment by fixing a compatibility issue with a library. This modification regards only the logger.py file. In this folder, we created seven new files, corresponding to the code for the six experiments on CIFAR10 and the one on SVHN.

# Our code
Inside the Keras folder,  our trials to implement the zero-shot algorithm on Keras can be found. We found very difficult to get the intermediate activations and train the generation with backpropagation through both the student and the teacher, so we decided to switch to Pytorch. We decided to keep the code even if does not work since we believe this was still a valuable learning experience.
Then there is the Pytorch folder. This is the folder where our working reimplementation can be found. Inside this folder there are 4 files:
 - cifar10utils.py: utils to download and get the dataloader for CIFAR-10
 - generator.py: the generator network, taken directly from the authors' code
 - wideresnet.py: a modification of https://github.com/indussky8/wide-resnet.pytorch/blob/master/networks/wide_resnet.py to have a WideResNetwork that returns the intermediate activations and the final prediction as outputs.
 - zero-shot-baseline.py: the complete code to run a zero-shot algorithm from a pretrained model. All the experiments use a variation of this file. *This is the file to be modified to run custom experiments*.
The following table shows the obtained results:

<p align="center">
  <img src="https://github.com/SZamboni/advanceddeep/blob/master/Our_code/Pytorch/Basic_experiments/table_CIFAR10_ours.png">
</p>

These four files are all you need to run a zero-shot algorithm. Modifying zero-shot-baseline.py we created our experiments and we divide the in folders.

Other 5 folders can be found inside this directory:
 - pretrained_models, containing the teachers with the code used to create them.
 - Basic_experiments, containing the code to run the six experiments reported in the paper on the CIFAR-10 dataset and the folder trained_students containing the resulting students.
- Advanced_experiments, containing the code to run the advanced experiments (different betas ecc..) on the CIFAR-10 dataset and the folder trained_students containing the resulting students.
 - Other_dataset_experiments, containing the code to a WideResNet that accepts as input one-channel images for MINST (and Fashion-MNIST), and also a generator that creates one-channel images for MNIST (and Fashion-MNIST). The code to train teachers on MNIST, FashionMNIST, SVHN and CIFAR-100, the trained teachers and the code to run a zero-shot on each of these teachers can also be found inside this repo. All the resulting students (and generators) are saved inside the folder trained_students.
 - Transition curves, where the code for the transition curves can be found. To execute it the constant.py file has to be modified by setting the path for the teacher and student models and the name of the models wanted. Inside this folder, first transition_curves.py and then print_csv.py have to be run to get the image of the average transition curve and the MTE value.

Since we have saved all the pretrained models, both ours and the authors' ones, the Github folder is quite heavy.
