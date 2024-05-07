# FFMPEG_HyperIQA
this repo contains three method about Image Quality Assessment
 # requirement
 ```
Python==3.10
PyTorch
TorchVision
scipy
modelscope
 ```
# *important*
you need install ffmpeg in your computer

# Data 
```python
# pretrained model
./pretrained/koniq_pretrained.pkl

# input data
./data

```
#config.ini
```python
[General]
# class_name = HyperIQA
# class_name = MAN
class_name = MOS
threshold=50
```
you can set three value for class_name
threshold represent quality of image, the value is bigger the quality is better


# Run sample
```
python main.py 
```

# Model Path
## HyperIQA Model
download model form [here]( https://drive.usercontent.google.com/download?id=1OOUmnbvpGea0LIGpIWEbOyxfWx6UCiiE&export=download&authuser=0)
Evaluating Image Quality Based on [HyperIQA]( https://openaccess.thecvf.com/content_CVPR_2020/papers/Su_Blindly_Assess_Image_Quality_in_the_Wild_Guided_by_a_CVPR_2020_paper.pdf)
HyperIQA is a method for evaluating image quality. It is based on the idea that human vision system is more sensitive to high-frequency content than low-frequency content. Therefore, a metric that takes into account both low-frequency and high-frequency content is needed.for more infomation click here  [hyperIQA](https://github.com/SSL92/hyperIQA)
## MOS IQA Model 
it is a api from modelscope, [reference](https://www.modelscope.cn/models/iic/cv_resnet_image-quality-assessment-mos_youtubeUGC/summary)
```python
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

img = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/dogs.jpg'
image_quality_assessment_pipeline = pipeline(Tasks.image_quality_assessment_mos, 'damo/cv_resnet_image-quality-assessment-mos_youtubeUGC')
result = image_quality_assessment_pipeline(img)[OutputKeys.SCORE]
print(result)
```
## MAN IQA Model
it is also a api from modelscope, [reference]( https://www.modelscope.cn/models/iic/cv_man_image-quality-assessment/summary)
```python
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

img = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/mog_face_detection.jpg'
image_quality_assessment_pipeline = pipeline(Tasks.image_quality_assessment_mos, 'damo/cv_man_image-quality-assessment')
result = image_quality_assessment_pipeline(img)[OutputKeys.SCORE]
print(result)
```

# Output data directory
```
output_video/
```


