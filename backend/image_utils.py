import cv2
import numpy as np
from PIL import Image, ImageFilter

class WarpUtils:
    def __init__(self, image_roi, original_image, roi_box):
        self.image_roi = image_roi
        self.original_image = original_image
        self.roi_box = roi_box.tensor.numpy()[0].astype('int')
        self.img_width, self.img_height = self.image_roi.shape[:2]
        
    def warp_region(self):
        x1, y1, x2, y2 = self.roi_box
        h_stretch, v_stretch = self.get_warp_factor()
        
        print("Height: " + str(self.img_height) +", Width: " + str(self.img_width))
        print("Top Left: " + str(x1) + ", Top Right: " + str(x2) + ", Bottom Left: " + str(y1) + ", Bottom Right: " + str(y2))
        print("Horizontal Stretch: " + str(h_stretch) + ", Vertical Stretch: " + str(v_stretch))
        
        roi_corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        transformed_corners = [(x1, y1), (x2, y1), (x2 + h_stretch, y2 + v_stretch), (x1 - h_stretch, y2 + v_stretch)]

        transformed_roi = self.apply_perspective_warp(roi_corners, transformed_corners)
        transformed_roi_img = Image.fromarray(transformed_roi).filter(ImageFilter.ModeFilter(size=10))
        transformed_roi = np.array(transformed_roi_img)

        return transformed_roi
    
    def apply_perspective_warp(self, roi_corners, transformed_corners):
        src_points = np.array(roi_corners, dtype=np.float32)
        dst_points = np.array(transformed_corners, dtype=np.float32)

        M = cv2.getPerspectiveTransform(src_points, dst_points)

        warped_roi = cv2.warpPerspective(self.image_roi, M, (self.image_roi.shape[1], self.image_roi.shape[0]))

        return warped_roi

    def get_warp_factor(self):
        img_width, img_height = self.image_roi.shape[:2]
        x1, y1, x2, y2 = self.roi_box
        h_factor = 400
        v_factor = 200

        distance_to_left = x1
        distance_to_right = img_width - x2
        distance_to_top = y1
        distance_to_bottom = img_height - y2

        h_stretch = h_factor * (img_width / (distance_to_left + distance_to_right))
        v_stretch = v_factor * (img_height / (distance_to_top + distance_to_bottom))

        return int(h_stretch), int(v_stretch)