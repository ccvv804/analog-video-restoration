# [miccunifi](https://github.com/miccunifi)의 Swin-UNet을 이용한 아날로그 비디오 복구 도구
Media Integration and Communication Center에서 개발하고 공개한 도구를 대충 개조했습니다.

고품질 또는 전문적인 변환 시스템으로 아날로그 비디오를 변환했으나 비디오테이프 데미지 등으로 영상 표출에 문제가 있는 경우 영상을 복구하려고 시도하는 툴입니다. 

부작용이 상당히 강한 도구이니 신중하게 사용하세요.
## 특징?
* 비정상적인 영상 떨림 억제 시도?
* 비정상적인 드롭아웃 보정 시도?
* 적극적인 노이즈 억제
## 시연 영상?
https://user-images.githubusercontent.com/54245389/236802520-ec6c92b8-2ab9-43ff-8efd-47cc8f275442.mp4

https://github.com/ccvv804/analog-video-restoration/assets/54245389/bbf23ca7-81d8-4214-b04a-748ba8f1a159
## 설치 방법? 
* Windows 11 PowerShell 기준입니다. 리눅스는 조금 다를 수 있습니다.
### 요구사항
* 아무런 수정 없이는 엔비디아 RTX 그래픽카드가 필요합니다.
  * CPU나 AMD 라데온 RX 그래픽카드에서는 torch 설치 버전 변경하고 프로그램 코드 수정이 필요합니다.
  * patch size 512는 8GB 정도의 VRAM이 필요한 것으로 보입니다.
  * patch size 640는 10GB 정도의 VRAM이 필요한 것으로 보입니다.
  * patch size 704는 12GB 정도의 VRAM이 필요한 것으로 보입니다.
  * patch size 768는 12GB 정도의 VRAM에서는 작업할 수 없습니다.
* git, Python 3.10, ffmpeg, ffprobe가 필요합니다.
  * 윈도우라면 PATH 등록이 필요합니다. git과 파이썬은 설치 단계에서 PATH 등록이 가능합니다.
  * ffmpeg 하고 ffprobe의 PATH 설정이 어려운 경우 ```analog-video-restoration``` 폴더에 ```ffmpeg.exe```하고 ```ffprobe.exe```를 두면 됩니다.
### 프로그램 설치
```sh
git clone https://github.com/ccvv804/analog-video-restoration
cd analog-video-restoration
python -m venv venv
.\venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install opencv-python
pip install pytorch-lightning
pip install einops
```
### 모델 설치
[Google Drive](https://drive.google.com/drive/folders/1omIk6qHKqbvO7T09Ixiez7zq08S7OaxE?usp=share_link)에서 모델을 다운로드 받고 ```analog-video-restoration``` 폴더에 ```pretrained_models``` 라는 폴더를 만들고 들어간 다음 ```video_swin_unet``` 라는 폴더를 만들고 들어간 다음 ```best.ckpt```을 넣습니다. 

## 사용 방법?
```sh
.\venv\Scripts\activate
python src/run.py -p 512 -i test1.mkv
```
### 옵션 설명
 * ```-i``` : 처리할 동영상 파일을 지정합니다.
 * ```-p``` : patch size를 의미하며 512 이상의 64 배수이어야 하며 크면 클수록 더 많은 VRAM이 필요합니다. 기본값은 512
 * ```-v``` : 동영상이 이미 디인터레이스 처리되어 프로그레시브인 경우에 사용하면 됩니다. 기본 미적용.
   * 복구가 소극적으로 진행될 수 있으나 부작용 또한 약해집니다.
 * ```-d``` : 더블 프레임레이트를 적용하는 경우 사용하시면 됩니다. 기본 미적용.
## 이하는 원본 README입니다.
***
# Restoration of Analog Videos Using Swin-UNet

This application is part of the **ReInHerit Toolkit**.

![ReInHerit Smart Video Restoration logo](smartvideorestoration_logo.jpg "ReInHerit Smart Video Restoration logo")

## Table of Contents
* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Training](#training)
  * [Test](#test) 
* [Authors](#authors)
* [Citation](#citation)

## About The Project
![restoration example](readme.png)

This is the **official repository** of "[**Restoration of Analog Videos Using Swin-UNet**](https://dl.acm.org/doi/10.1145/3503161.3547730)" **[Demo ACM MM 2022]**.

In this work, we present an approach to restore analog videos of historical archives. These videos often contain severe visual degradation due to the deterioration of their tape supports that require costly and slow manual interventions to recover the original content. The proposed method uses a multi-frame approach and is able to deal also with severe tape mistracking, which results in completely scrambled frames. Tests on real-world videos from a major historical video archive show the effectiveness of our approach.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

We strongly recommend the use of the [**Anaconda**](https://www.anaconda.com/) package manager in order to avoid dependency/reproducibility problems.
A conda installation guide for Linux systems can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

### Installation
 
1. Clone the repo
```sh
git clone https://github.com/miccunifi/analog-video-restoration.git
```
2. Install Python dependencies
```sh
conda create -n analog_video_restoration -y python=3.9
conda activate analog_video_restoration
pip install -r requirements.txt
```

## Usage

### Training

1. Make your training dataset have the following structure:
```
<dataset-name>
     └─── train
           └─── input
                └─── 000
                      | 00000.jpg
                      | 00001.jpg
                      | ...

                └───  001
                      | 00000.jpg
                      | 00001.jpg
                      | ...
                ...

           └─── gt
                └─── 000
                      | 00000.jpg
                      | 00001.jpg
                      | 00002.jpg
                      | ...

                └───  001
                      | 00000.jpg
                      | 00001.jpg
                      | ...
                ...

           └─── val
              └─── input
                └─── 000
                      | 00000.jpg
                      | 00001.jpg
                      | ...

                └───  001
                      | 00000.jpg
                      | 00001.jpg
                      | ...
                ...

              └─── gt
                   └─── 000
                         | 00000.jpg
                         | 00001.jpg
                         | 00002.jpg
                         | ...

                   └───  001
                         | 00000.jpg
                         | 00001.jpg
                         | ...
                   ...
```

2. Get your [Comet](https://www.comet.com/site/) api key for online logging of the losses and metrics

3. Run the training code with
```
python src/train.py --experiment-name video_swin_unet --data-base-path <path-to-dataset> --devices 0 --api-key <your-Comet-api-key> --batch-size 2 --num-epochs 100 --num-workers 20 --pixel-loss-weight 200 --perceptual-loss-weight 1
```

### Test

1. If needed, download the pretrained model from [Google Drive](https://drive.google.com/drive/folders/1omIk6qHKqbvO7T09Ixiez7zq08S7OaxE?usp=share_link) and copy it inside the folder ```pretrained_models/video_swin_unet/```

2. Extract the frames of the video in .jpg images and save them in a folder
```
mkdir <folder-name>
ffmpeg -i <video-file-name> -qscale:v 2 <folder-name>/%00d.jpg
```

3. Run inference on the folder with
```
python src/real_world_test.py --experiment-name video_swin_unet --data-base-path <path-to-folder> --results-path results --patch-size 512 --fps 60
```

## Authors
* [**Lorenzo Agnolucci**](https://scholar.google.com/citations?user=hsCt4ZAAAAAJ&hl=en)
* [**Leonardo Galteri**](https://scholar.google.com/citations?user=_n2R2bUAAAAJ&hl=en)
* [**Marco Bertini**](https://scholar.google.it/citations?user=SBm9ZpYAAAAJ&hl=en)
* [**Alberto Del Bimbo**](https://scholar.google.it/citations?user=bf2ZrFcAAAAJ&hl=en)

## Citation
If you find this work useful for your research, please consider citing:
<pre>
@inproceedings{10.1145/3503161.3547730,
  author = {Agnolucci, Lorenzo and Galteri, Leonardo and Bertini, Marco and Del Bimbo, Alberto},
  title = {Restoration of Analog Videos Using Swin-UNet},
  year = {2022},
  isbn = {9781450392037},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3503161.3547730},
  doi = {10.1145/3503161.3547730},
  abstract = {In this paper we present a system to restore analog videos of historical archives. These videos often contain severe visual degradation due to the deterioration of their tape supports that require costly and slow manual interventions to recover the original content. The proposed system uses a multi-frame approach and is able to deal also with severe tape mistracking, which results in completely scrambled frames. Tests on real-world videos from a major historical video archive show the effectiveness of our demo system.},
  booktitle = {Proceedings of the 30th ACM International Conference on Multimedia},
  pages = {6985–6987},
  numpages = {3},
  keywords = {old videos restoration, analog videos, unet, swin transformer},
  location = {Lisboa, Portugal},
  series = {MM '22}
}
</pre>
