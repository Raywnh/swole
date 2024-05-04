import detectron2
import numpy as np
import cv2
import os
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode
from image_utils import WarpUtils

path = "./models/"

def get_enlarged_segment(img):
    isolated_roi, box = get_segmented_region(img)

    warper = WarpUtils(isolated_roi, img, box)
    
    transformed_roi = warper.warp_region()
    image_mask = cv2.cvtColor(transformed_roi, cv2.COLOR_BGR2GRAY)
    _, image_mask = cv2.threshold(image_mask, 1, 255, cv2.THRESH_BINARY)

    masked_roi = cv2.bitwise_and(transformed_roi, transformed_roi, mask=image_mask)
    mask_inv = cv2.bitwise_not(image_mask)
    masked_original = cv2.bitwise_and(img, img, mask=mask_inv)

    combined_image = cv2.add(masked_original, masked_roi)
    
    return combined_image


def get_segmented_region(img):
    cfg = get_cfg()
    cfg.merge_from_file("./detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

    cfg.MODEL.WEIGHTS = os.path.join(path, "model_final_9.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.4
    cfg.MODEL.DEVICE = 'cpu'
    predictor = DefaultPredictor(cfg)
    outputs = predictor(img)

    instances = outputs["instances"].to("cpu")

    if len(instances) > 0:
        highest_score_index = instances.scores.argmax()
        highest_score_instance = instances[highest_score_index:highest_score_index + 1]
        mask_res = highest_score_instance.pred_masks[0]
        box = highest_score_instance.pred_boxes
    else:
        highest_score_instance = instances
        mask_res = None
        print("Error detecting region of interest")
        return None, None
        
    # Binary mask for layer masking 
    mask_np = mask_res.numpy().astype(np.uint8)
    mask = mask_np * 255

    # The isolated region on the real image that we want to transform
    isolated_roi = cv2.bitwise_and(img, img, mask=mask)

    return isolated_roi, box