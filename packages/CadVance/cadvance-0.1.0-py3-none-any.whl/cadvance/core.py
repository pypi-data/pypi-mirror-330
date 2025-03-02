
import win32com.client


class CadVance:
    def __init__(self):
        """Initialize connection to AutoCAD via COM."""
        self.acad = win32com.client.Dispatch("AutoCAD.Application")
        self.acad.Visible = True  # Make AutoCAD visible

    def get_documents(self):
        """Return the current AutoCAD documents."""
        return self.acad.Documents

    def open_document(self, path):
        """Open an AutoCAD document."""
        return self.acad.Documents.Open(path)

    def save_document(self, path):
        """Save the current document."""
        self.acad.ActiveDocument.SaveAs(path)

    def close_document(self):
        """Close the current document."""
        self.acad.ActiveDocument.Close()
