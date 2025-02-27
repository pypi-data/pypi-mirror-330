import json
import os
import tempfile
from pathlib import Path
from typing import Union

from AnyQt.QtWidgets import QLineEdit, QMessageBox
from Orange.data.io import CSVReader
from Orange.data.table import Table
from Orange.widgets import gui, widget
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import Input

class OWSaveFilepathEntry(widget.OWWidget):
    name = "Save with Filepath Entry"
    description = "Save data to a local interface. The file path is entered manually."

    priority = 1220
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        data = Input("Data", Table)
        path = Input("Path", str)

    # Persistent settings for fileId and CSV delimiter
    CSVDelimiter: str = Setting('\t') # type: ignore

    def __init__(self):
        super().__init__()
        self.info_label = gui.label(self.controlArea, self, "Initial info.")
        self.data = None
        self.save_path: str | None =None
        self.setup_ui()


    def setup_ui(self):
        """Set up the user interface."""
        # Text input for CSV delimiter
        hbox3 = gui.hBox(self.controlArea, "CSV Delimiter")
        self.le_csv_delimiter = QLineEdit(self)
        self.le_csv_delimiter.setText(self.CSVDelimiter)
        self.le_csv_delimiter.editingFinished.connect(self.update_csv_delimiter)
        hbox3.layout().addWidget(self.le_csv_delimiter) # type: ignore

        # Button to reset CSV delimiter to \t, as it can't be typed in the text input
        reset_csv_delimiter = gui.button(self.controlArea, self, "Reset Delimiter to \\t", callback=self.reset_csv_delimiter)

        self.adjustSize()
    
    def reset_csv_delimiter(self):
        """Reset the CSV delimiter to \t."""
        self.le_csv_delimiter.setText('\t')
        self.update_csv_delimiter()
    
    def update_csv_delimiter(self):
        """Update the CSV delimiter."""
        self.CSVDelimiter = self.le_csv_delimiter.text()

    @Inputs.data
    def dataset(self, data): 
        """Handle new data input."""
        self.data = data
        if self.data is not None:
            self.save_to_file()
    
    @Inputs.path
    def path(self, path):
        """Handle new path input."""
        print("path: ", path)

        if isinstance(path, str):
            path_str = path
        else:
            print("path type: ", type(path))
            print("path: ", path)
            QMessageBox.warning(self, "Invalid Path", "Invalid path input. Only string paths are supported.")
            return
        
        self.save_path = path_str
        if self.save_path is not None:
            self.save_to_file()

    def save_to_file(self):
        """Save data to a file."""
        if self.data is None:
            QMessageBox.warning(self, "No Data", "No data available to save.")
            return

        if self.save_path is None:
            self.info_label.setText("No file path specified.")
            return
        else:
            print("filepath: ", self.save_path)
            print("filepath type:", type(self.save_path))
            file_path = Path(self.save_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    class CustomReader(CSVReader):
                        DELIMITERS = self.CSVDelimiter
                    CustomReader.write(temp.name, self.data)
                os.replace(temp.name, str(file_path))
                self.info_label.setText(f"Data successfully uploaded")
                print("Data successfully saved to: ", file_path)
            except IOError as err:
                QMessageBox.critical(self, "Error", f"Failed to save file: {err}")


if __name__ == "__main__": 
    WidgetPreview(OWSaveFilepathEntry).run()
