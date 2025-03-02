import ast

def is_point_in_rectangle(rect_pos, rect_dims, target_pos):
  """
  Checks if a target position is inside a rectangle.

  Args:
      rect_pos (tuple): The (x, y) position of the top-left corner of the rectangle.
      rect_dims (tuple): The (width, height) dimensions of the rectangle.
      target_pos (tuple): The (x, y) position to check.

  Returns:
      bool: True if the target position is inside the rectangle, False otherwise.
  """
  rect_x, rect_y = rect_pos
  rect_width, rect_height = rect_dims
  target_x, target_y = target_pos

  return (rect_x <= target_x < rect_x + rect_width) and (rect_y <= target_y < rect_y + rect_height)



def extract_list_from_file(fileName):
    with open(fileName, "r") as file:
        file_content = file.read()
        # Safely evaluate the dictionary using `ast.literal_eval`
        return ast.literal_eval(file_content)


