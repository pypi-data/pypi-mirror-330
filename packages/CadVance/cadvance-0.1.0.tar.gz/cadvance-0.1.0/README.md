
# CadVance

**CadVance** is a Python package designed for automating AutoCAD tasks using COM (Component Object Model). This package enables you to interact with AutoCAD, automate drawing creation, and manage AutoCAD documents programmatically.

## Features

- **Automated Drawing**: Easily create and manipulate AutoCAD drawings directly from Python.
- **Shape Drawing**: Draw basic shapes like lines, circles, and rectangles.
- **Document Management**: Save, open, and close AutoCAD documents.
- **COM Automation**: Leverage AutoCAD's COM API to automate tasks.
- **Customization**: Easily extend the library to suit your automation needs.

## Installation

### 1. Install via pip:

The easiest way to install **CadVance** is through pip:

```bash
pip install cadvance
```

### 2. Install from Source:

If you'd like to install **CadVance** from the source, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/CadVance.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CadVance
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Initialize AutoCAD Automation

```python
from cadvance.automation import CadVance

# Initialize CadVance to interact with AutoCAD
cad = CadVance()

# Draw a line from coordinates (0, 0, 0) to (100, 100, 0)
cad.draw_line((0, 0, 0), (100, 100, 0))

# Save the document as a .dwg file
cad.save_document("C:\path\to\save\yourdrawing.dwg")

# Close the document
cad.close_document()
```

### Example

```python
from cadvance.automation import CadVance

# Create CadVance object
cad = CadVance()

# Draw a line
cad.draw_line((0, 0, 0), (200, 200, 0))

# Save the drawing
cad.save_document("C:\Users\Public\AutoCAD_Test.dwg")

# Close the document
cad.close_document()
```

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To contribute to **CadVance**:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add feature'`)
5. Push to the branch (`git push origin feature-name`)
6. Create a pull request

## Acknowledgments

- **AutoCAD**: For providing the COM API that allows Python to interact with AutoCAD.
- **Python**: For being an easy-to-use language for automation tasks.
- **PyWin32**: For enabling COM support in Python.

## Contact

For inquiries or support, feel free to reach out to me at [peterjonespeter22@gmail.com].

This project is maintained by **Jones Peter**.

---

> **Note**: This project is not affiliated with Autodesk AutoCAD in any way.
