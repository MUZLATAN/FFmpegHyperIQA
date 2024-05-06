from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

import torch as torch
import torch.nn as nn
class MANNet(nn.Module):
    def __init__(self):
        self.image_quality_assessment_pipeline = pipeline(Tasks.image_quality_assessment_mos, 'damo/cv_man_image-quality-assessment')

    def forward(self, img):
        result = self.image_quality_assessment_pipeline(img)[OutputKeys.SCORE]
        return result