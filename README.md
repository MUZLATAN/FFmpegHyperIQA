# FFMPEG_HyperIQA
 Evaluating Image Quality Based on HyperIQA https://openaccess.thecvf.com/content_CVPR_2020/papers/Su_Blindly_Assess_Image_Quality_in_the_Wild_Guided_by_a_CVPR_2020_paper.pdf
 # What is HyperIQA
 HyperIQA is a method for evaluating image quality. It is based on the idea that human vision system is more sensitive to high-frequency content than low-frequency content. Therefore, a metric that takes into account both low-frequency and high-frequency content is needed.for more infomation click here  [hyperIQA](https://github.com/SSL92/hyperIQA)
 # requirement
 ```
Python==3.10
PyTorch
TorchVision
scipy
 ```
# important
you need install ffmpeg in your computer

# Data And Model Path
download model form here https://drive.usercontent.google.com/download?id=1OOUmnbvpGea0LIGpIWEbOyxfWx6UCiiE&export=download&authuser=0
```python
# pretrained model
./pretrained/koniq_pretrained.pkl

# input data
./data

```

# Output data directory
```
output_video/
```


# Run sample
```
python main.py 
```