<div align="center">
<h1>Reproduce steps</h1>
<div align="center">

<div align="justify">

<h2>Dataset download</h2>

- Data download: SYNTHETIC AMASS 60FPS - DOWNLOAD SERVER 1 (source: https://dip.is.tue.mpg.de/download.php)
- Data folder structure example:

<image src="./folder_structure.png" width="600">

- Note: .pkl lists for files used in train, valid, test process can be found under files fairmotion\tasks\motion_prediction\data\XXX_fnames.txt. The current split is (0.7, 0.2, 0.1) for train, validation, test datasets. If want to change the split ratios:
  - update the lisa_resplit_data.py in the root folder based on your folder structure
  - run the lisa_resplit_data.py

<h2>Example folder setups</h2>

- Note: the variables listed here comes from the original fairmotion motion prediction task guidance: https://github.com/facebookresearch/fairmotion/tree/main/fairmotion/tasks/motion_prediction
- "PATH TO RAW DATA" = "D:\gitHub\GT\fairmotion\data\rawdata\synthetic60FPS\Synthetic_60FPS"
- "PREPROCESSED OUTPUT PATH"
  - "D:\gitHub\GT\fairmotion\data\preprocessedoutput" for preprocessing
  - "D:\gitHub\GT\fairmotion\data\preprocessedoutput\aa" for training and testing
- "PATH TO MODEL" = "D:\gitHub\GT\fairmotion\data\savedmodels"
- "PATH TO SAVE PREDICTED MOTIONS" = "D:\gitHub\GT\fairmotion\data\predictedmotions"

<h2>Example preprocess command</h2>

```
python fairmotion/tasks/motion_prediction/preprocess.py 	--input-dir "D:\gitHub\GT\fairmotion\data\rawdata\synthetic60FPS\Synthetic_60FPS" 	--output-dir "D:\gitHub\GT\fairmotion\data\preprocessedoutput" 	--split-dir ./fairmotion/tasks/motion_prediction/data/     --rep aa
```

<h2>Example Train command</h2>

```
python fairmotion/tasks/motion_prediction/training.py     --save-model-path "D:\gitHub\GT\fairmotion\data\savedmodels"    --preprocessed-path "D:\gitHub\GT\fairmotion\data\preprocessedoutput\aa"    --epochs 50    --architecture "seq2seq"
```
- Note: selectable architectures: ["seq2seq", "tied_seq2seq", "transformer", "transformer_encoder", "rnn"]
- Note: The transformer keeps meeting error: RuntimeError: CUDA out of memory. Kind of unfixable through investigations. So I Ignored here.

<h2>Example Test command</h2>

```
python fairmotion/tasks/motion_prediction/test.py --save-model-path "D:\gitHub\GT\fairmotion\data\savedmodels" --preprocessed-path "D:\gitHub\GT\fairmotion\data\preprocessedoutput\aa" --save-output-path "D:\gitHub\GT\fairmotion\data\predictedmotions" --architecture  "seq2seq"
```

- Selectable architectures: ["seq2seq", "tied_seq2seq", "transformer", "transformer_encoder", "rnn"]

<div align="center">
<h1>Below are from original fairmotion readme</h1>
<div align="center">

# fairmotion

fairmotion provides easy-to-use interfaces and tools to work with motion capture data. The objective of the library is to manage the complexity of motion representation, 3D transformations, file formats and visualization, and let users focus on high level learning tasks. 

Users can take advantage of large high-quality motion capture datasets like the [CMU](http://mocap.cs.cmu.edu/) and [AMASS](https://amass.is.tue.mpg.de/) datasets without deep knowledge of the domain or handling the idiosyncrasies of individual datasets. We implement baselines for research tasks using building blocks from the library to demonstrate its utility.

<img src="fairmotion/viz/samples/anim_viz.gif" width="500"><img src="fairmotion/viz/samples/anim_smpl.gif" width="330">

## Getting Started

### Installation

farmotion is available on PyPI for easy installation
```
pip install fairmotion
```

To install fairmotion from source, first clone the git repository, use pip to download dependencies and build the project.
```
$ git clone https://github.com/facebookresearch/fairmotion.git
$ cd fairmotion
$ pip install -e .
```
### Data Loading

Here, we load a motion capture file in the BVH file format in a python console. Similarly, there are loaders to import files from [ASF/AMC](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/ASF-AMC.html), [AMASS](https://amass.is.tue.mpg.de/dataset) and [AMASS DIP](http://dip.is.tuebingen.mpg.de/pre_download) formats.
```
from fairmotion.data import bvh

BVH_FILENAME = “PATH_TO_BVH_FILE”
motion = bvh.load(BVH_FILENAME)
```

If you recieve errors like the ones below, you can find the workaround [here](https://stackoverflow.com/questions/65202395/pyopengl-on-macos-bigsur-and-opengl-error-nullfunctionerror#:~:text=if%20name%20%3D%3D%20%27OpenGL%27%3A%0A%20%20%20%20fullName%20%3D%20%27/System/Library/Frameworks/OpenGL.framework/OpenGL%27%0Aelif%20name%20%3D%3D%20%27GLUT%27%3A%0A%20%20%20%20fullName%20%3D%20%27/System/Library/Frameworks/GLUT.framework/GLUT%27).
```
ImportError: ('Unable to load OpenGL library', 'dlopen(OpenGL, 10): image not found', 'OpenGL', None)
or
OpenGL.error.NullFunctionError: Attempt to call an undefined function glutInit, check for bool(glutInit) before calling
```
### Motion manipulation

The motion object can be manipulated in both modular and matrix forms. Here, we translate the object to a fixed global position `[1, 1, 1]` and select a time slice from frame `20` to frame `30`.
```
from fairmotion.ops import motion as motion_ops

translated_motion = motion_ops.translate(motion, np.array([1, 1, 1]))
sliced_motion = motion_ops.cut(translated_motion, 10, 20)
```
We can perform the same operations in the matrix representation of motion.
```
from fairmotion.core.motion import Motion

# motion_matrix has shape (num_frames, num_joints, 4, 4) where 4x4 is transformation matrix
motion_matrix = motion.to_matrix()

translation_matrix = np.zeros((4, 4))
translation_matrix[3, :3] = np.array([1, 1, 1])

translated_motion_matrix = motion_matrix + translation_matrix
sliced_motion_matrix = translated_motion_matrix[10:20]
sliced_motion = Motion.from_matrix(sliced_motion_matrix, motion.skel)
```
### Data saving

We can save the manipulated motion object back into the bvh file format for us to visualize the result.
```
NEW_BVH_FILENAME = "PATH_TO_NEW_BVH_FILE"
bvh.save(sliced_motion, NEW_BVH_FILENAME)
```
### Visualization

We visualize the results using the `bvh_visualizer` tool.
```
$ python fairmotion/viz/bvh_visualizer.py --bvh-files $NEW_BVH_FILENAME
```

## Tasks
The `tasks` module showcases practical usage of fairmotion modules as building blocks in developing projects.

- [Motion Prediction](https://github.com/facebookresearch/fairmotion/tree/master/fairmotion/tasks/motion_prediction)
- [Motion Graph](https://github.com/facebookresearch/fairmotion/tree/master/fairmotion/tasks/motion_graph)
- [Clustering of motion capture dataset](https://github.com/facebookresearch/fairmotion/tree/master/fairmotion/tasks/clustering)
- [Changepoint Detection](https://github.com/facebookresearch/fairmotion/tree/master/fairmotion/tasks/changepoint_detection)

fairmotion has been used in some form in the following works:

* Jungdam Won, Deepak Gopinath, and Jessica Hodgins. “A Scalable Approach to Control Diverse Behaviors for Physically Simulated Characters” to be presented at SIGGRAPH 2020 [[Project page with code and paper](https://research.fb.com/publications/a-scalable-approach-to-control-diverse-behaviors-for-physically-simulated-characters/)]
* Tanmay Shankar, and Abhinav Gupta. "Learning Robot Skills with Temporal Variational Inference." ICML 2020
* Jungdam Won, and Jehee Lee. "Learning body shape variation in physics-based characters." ACM Transactions on Graphics (TOG) 2019

## Citation
If you find fairmotion useful in your research, please cite our repository using the following BibTeX entry.
```
@Misc{gopinath2020fairmotion,
  author =       {Gopinath, Deepak and Won, Jungdam},
  title =        {fairmotion - Tools to load, process and visualize motion capture data},
  howpublished = {Github},
  year =         {2020},
  url =          {https://github.com/facebookresearch/fairmotion}
}
```
## License
fairmotion is released under the [BSD-3-Clause License](https://github.com/facebookresearch/fairmotion/blob/master/LICENSE).
