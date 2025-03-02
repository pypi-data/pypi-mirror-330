import cv2
import numpy as np
import pandas as pd
from typing import List, Dict, Union, Tuple, Optional


def convert_bbox_mamasight_to_gemini(
    bbox: List[int],
    img_width: int,
    img_height: int
) -> List[int]:
    """
    Convert bounding box from mamasight format to Gemini format.
    
    Mamasight format: [x1, y1, x2, y2] in absolute pixel coordinates
    Gemini format: [y_min, x_min, y_max, x_max] normalized to 0-1000 scale
    
    Args:
        bbox (List[int]): Bounding box in mamasight format [x1, y1, x2, y2]
        img_width (int): Image width in pixels
        img_height (int): Image height in pixels
        
    Returns:
        List[int]: Bounding box in Gemini format [y_min, x_min, y_max, x_max] normalized to 0-1000
    """
    x1, y1, x2, y2 = bbox
    
    # Normalize coordinates to 0-1000 scale
    x1_norm = int((x1 / img_width) * 1000)
    y1_norm = int((y1 / img_height) * 1000)
    x2_norm = int((x2 / img_width) * 1000)
    y2_norm = int((y2 / img_height) * 1000)
    
    # Convert to Gemini format [y_min, x_min, y_max, x_max]
    return [y1_norm, x1_norm, y2_norm, x2_norm]


def convert_bbox_gemini_to_mamasight(
    bbox: List[int],
    img_width: int,
    img_height: int
) -> List[int]:
    """
    Convert bounding box from Gemini format to mamasight format.
    
    Gemini format: [y_min, x_min, y_max, x_max] normalized to 0-1000 scale
    Mamasight format: [x1, y1, x2, y2] in absolute pixel coordinates
    
    Args:
        bbox (List[int]): Bounding box in Gemini format [y_min, x_min, y_max, x_max]
        img_width (int): Image width in pixels
        img_height (int): Image height in pixels
        
    Returns:
        List[int]: Bounding box in mamasight format [x1, y1, x2, y2] in absolute pixels
    """
    y_min, x_min, y_max, x_max = bbox
    
    # Convert from normalized 0-1000 to absolute pixels
    x1_abs = int((x_min / 1000.0) * img_width)
    y1_abs = int((y_min / 1000.0) * img_height)
    x2_abs = int((x_max / 1000.0) * img_width)
    y2_abs = int((y_max / 1000.0) * img_height)
    
    # Ensure coordinates are in the correct order
    if x1_abs > x2_abs:
        x1_abs, x2_abs = x2_abs, x1_abs
    if y1_abs > y2_abs:
        y1_abs, y2_abs = y2_abs, y1_abs
    
    # Return in mamasight format [x1, y1, x2, y2]
    return [x1_abs, y1_abs, x2_abs, y2_abs]


def get_annotated_elements(
    image_path: str,
    parser_instance
) -> Tuple[np.ndarray, pd.DataFrame, Dict[str, int]]:
    """
    Get the annotated version of all icons and text boxes in a screenshot, along with
    a DataFrame containing all bounding box coordinates for detected icons.
    
    Args:
        image_path (str): Path to the input image file.
        parser_instance: Instance of the ScreenParser class from mamasight.

    Returns:
        Tuple[np.ndarray, pd.DataFrame, Dict[str, int]]: A tuple containing:
            - The annotated image as a NumPy array
            - A DataFrame containing bounding box coordinates and metadata for all detected elements
            - Image dimensions (width, height)
    """
    # Analyze the image using the parser's analyze method
    image, detections = parser_instance.analyze(image_path, use_ocr=False)
    
    # Get image dimensions
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")
    img_height, img_width = img.shape[:2]
    
    # Ensure image is a proper numpy array for OpenCV
    if not isinstance(image, np.ndarray):
        # If image is a PIL Image or something else, convert it to a numpy array
        try:
            # Try to convert from PIL Image
            if hasattr(image, 'convert'):
                image = np.array(image.convert('RGB'))
            # If it's already a numpy array but with wrong shape or type
            elif isinstance(image, np.ndarray):
                # Ensure it's a 3-channel RGB or BGR image
                if len(image.shape) == 2:  # Grayscale
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                elif image.shape[2] == 4:  # RGBA
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            else:
                # If we can't handle it, just use the original image
                image = img
        except Exception as e:
            print(f"Warning: Failed to convert image to numpy array: {e}")
            # Fall back to using the original image loaded by cv2.imread
            image = img
    
    # Make sure the image is in the right color format for OpenCV (BGR)
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Check if we need to convert from RGB to BGR
        if image[0, 0, 0] != img[0, 0, 0] and image[0, 0, 2] == img[0, 0, 0]:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Return the annotated image, the dataframe of detections, and image dimensions
    return image, detections, {"width": img_width, "height": img_height}


def ImageAnnotatorTool(
    image_path: str,
    bounding_boxes: List[Dict[str, Union[List[int], str]]],
    settings: Optional[Dict[str, Union[int, str, float]]] = None
) -> np.ndarray:
    """
    Annotate an image with bounding boxes, IDs, and arrows connecting boxes.
    
    Args:
        image_path (str): Path to the input image file.
        bounding_boxes (List[Dict]): List of dictionaries, each containing:
            - 'bbox' (List[int]): Bounding box coordinates [x1, y1, x2, y2].
            - 'color' (str): Color name for the bounding box (e.g., 'red', 'green').
            - 'id' (str): ID label for the bounding box (e.g., 'A', 'B', 'C').
            - 'description' (str, optional): Description text to display next to the bounding box.
            - 'destination_id' (str, optional): ID of the box to connect to with an arrow.
        settings (Dict, optional): Configuration settings including:
            - 'line_thickness' (int): Thickness of bounding box lines (default: 2).
            - 'text_scale' (float): Scale of text (default: 0.7).
            - 'text_thickness' (int): Thickness of text (default: 2).
            - 'arrow_color' (str): Color for arrows (default: 'blue').
            - 'arrow_thickness' (int): Thickness of arrows (default: 2).
            - 'arrow_tip_length' (float): Length of arrow tip (default: 0.03).
            - 'description_offset' (int): Vertical offset for description text (default: 15).
    
    Returns:
        np.ndarray: Annotated image as a NumPy array.
    """
    # Default settings
    default_settings = {
        'line_thickness': 2,
        'text_scale': 0.7,
        'text_thickness': 2,
        'arrow_color': 'blue',
        'arrow_thickness': 2,
        'arrow_tip_length': 0.1,
        'description_offset': 15
    }
    
    # Update default settings with provided settings
    if settings is None:
        settings = {}
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    
    # Color mapping
    color_map = {
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'purple': (255, 0, 255),
        'cyan': (255, 255, 0),
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
    
    # Load the image
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image from {image_path}")
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        # Create a blank image as fallback
        image = np.zeros((500, 500, 3), dtype=np.uint8)
    
    # Create a mapping from ID to bounding box info for arrow connections
    id_to_bbox = {}
    for box in bounding_boxes:
        if 'id' in box:
            id_to_bbox[box['id']] = box
    
    try:
        # Draw bounding boxes and IDs
        for box in bounding_boxes:
            # Extract box information
            bbox = box.get('bbox', [0, 0, 0, 0])
            color_name = box.get('color', 'red')
            box_id = box.get('id', '')
            description = box.get('description', '')
            
            # Ensure bbox has 4 elements and all are integers
            if len(bbox) != 4:
                print(f"Warning: Invalid bbox format: {bbox}")
                continue
            
            try:
                bbox = [int(coord) for coord in bbox]
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not convert bbox coordinates to integers: {bbox}, {str(e)}")
                continue
            
            # Ensure coordinates are within image bounds
            h, w = image.shape[:2]
            bbox[0] = max(0, min(bbox[0], w-1))
            bbox[1] = max(0, min(bbox[1], h-1))
            bbox[2] = max(0, min(bbox[2], w-1))
            bbox[3] = max(0, min(bbox[3], h-1))
            
            # Ensure x1 < x2 and y1 < y2
            if bbox[0] > bbox[2]:
                bbox[0], bbox[2] = bbox[2], bbox[0]
            if bbox[1] > bbox[3]:
                bbox[1], bbox[3] = bbox[3], bbox[1]
            
            # Get color in BGR format
            color = color_map.get(color_name.lower(), (0, 0, 255))  # Default to red if color not found
            
            # Draw bounding box
            cv2.rectangle(
                image, 
                (bbox[0], bbox[1]), 
                (bbox[2], bbox[3]), 
                color, 
                settings['line_thickness']
            )
            
            # Draw ID text
            text_position = (bbox[0], bbox[1] - 10)
            text_position = (max(0, text_position[0]), max(0, text_position[1]))  # Ensure text is within image
            cv2.putText(
                image,
                box_id,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                settings['text_scale'],
                color,
                settings['text_thickness']
            )
            
            # Draw description text if provided
            if description:
                description_position = (bbox[0], bbox[3] + settings['description_offset'])
                description_position = (max(0, description_position[0]), min(h-1, description_position[1]))  # Ensure text is within image
                cv2.putText(
                    image,
                    description,
                    description_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    settings['text_scale'],
                    color,
                    settings['text_thickness']
                )
        
        # Draw arrows
        for box in bounding_boxes:
            if 'destination_id' in box and box['destination_id'] in id_to_bbox:
                # Get source and destination boxes
                source_bbox = box['bbox']
                dest_box = id_to_bbox[box['destination_id']]
                dest_bbox = dest_box['bbox']
                
                # Define all corners of source bounding box
                source_corners = [
                    (source_bbox[0], source_bbox[1]),  # top-left
                    (source_bbox[2], source_bbox[1]),  # top-right
                    (source_bbox[0], source_bbox[3]),  # bottom-left
                    (source_bbox[2], source_bbox[3])   # bottom-right
                ]
                
                # Define all corners of destination bounding box
                dest_corners = [
                    (dest_bbox[0], dest_bbox[1]),  # top-left
                    (dest_bbox[2], dest_bbox[1]),  # top-right
                    (dest_bbox[0], dest_bbox[3]),  # bottom-left
                    (dest_bbox[2], dest_bbox[3])   # bottom-right
                ]
                
                # Find the closest pair of corners
                min_distance = float('inf')
                closest_source_corner = None
                closest_dest_corner = None
                
                for s_corner in source_corners:
                    for d_corner in dest_corners:
                        # Calculate Euclidean distance between corners
                        distance = np.sqrt((s_corner[0] - d_corner[0])**2 + (s_corner[1] - d_corner[1])**2)
                        if distance < min_distance:
                            min_distance = distance
                            closest_source_corner = s_corner
                            closest_dest_corner = d_corner
                
                # Get arrow color
                arrow_color_name = settings.get('arrow_color', 'blue')
                arrow_color = color_map.get(arrow_color_name.lower(), (255, 0, 0))  # Default to blue
                
                # Draw arrow between the closest corners
                cv2.arrowedLine(
                    image,
                    closest_source_corner,
                    closest_dest_corner,
                    arrow_color,
                    settings['arrow_thickness'],
                    tipLength=settings['arrow_tip_length']
                )
    except Exception as e:
        print(f"Error annotating image: {str(e)}")
        # If annotation fails, just return the original image
    
    return image