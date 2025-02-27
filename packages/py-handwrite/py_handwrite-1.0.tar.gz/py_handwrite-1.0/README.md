## Parameters
- **text** (`str`): The input text string that will be converted into a handwritten-style image.

## Returns
- **ImageFile**: An image file containing the handwritten version of the input text.

## Example Usage
```python
from py_handwrite import handwrite

text = "Hello, this is a handwritten text!"
image = handwrite(text)

# Save the output image
image.save("handwritten_text.png")

# Show the image
image.show()
```

## Dependencies
Make sure you have the `py_handwrite` module installed before using this function.

```sh
pip install py_handwrite
```