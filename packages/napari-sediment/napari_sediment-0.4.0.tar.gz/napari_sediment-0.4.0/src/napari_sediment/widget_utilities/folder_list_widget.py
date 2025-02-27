import os
from pathlib import Path
from qtpy.QtWidgets import QListWidget
from qtpy.QtCore import Qt


class FolderListWidget(QListWidget):
    # be able to pass the Napari viewer name (viewer)
    def __init__(self, viewer, parent=None, background_kw='_WR_', only_folders=False, ignore=None):
        """List widget to show the files in a folder.
        
        Parameters
        ----------
        viewer : str
            Napari viewer name.
        parent : QWidget, optional
            Parent widget.
        background_kw : str, optional
            Keyword to ignore files containing this name.
        only_folders : bool, optional
            Only show folders.
        ignore : list of str, optional
            List of file names to ignore.
        
        """

        super().__init__(parent)

        self.viewer = viewer
        self.background_kw = background_kw
        self.only_folders = only_folders
        self.ignore = ignore
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        #self.currentItemChanged.connect(self.open_file)

        self.folder_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        self.clear()
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            # Check that it's a LIF file
            for url in event.mimeData().urls():
                self.folder_path = str(url.toLocalFile())
                files = os.listdir(self.folder_path)  
                for f in files:
                    #if Path(f).suffix == '.oir':
                    if (f[0] != '.') and (self.background_kw not in f):
                        self.addItem(f)

    def update_from_path(self, path):
        
        if self.ignore is None:
            self.ignore = []
        self.clear()
        self.folder_path = path
        files = os.listdir(self.folder_path)  
        for f in files:
            #if Path(f).suffix == '.oir':
            if (f[0] != '.') and (self.background_kw not in f) and (f not in self.ignore):
                if self.only_folders:
                    if os.path.isdir(Path(self.folder_path).joinpath(f)):
                        self.addItem(f)
                else:
                    self.addItem(f)

    def add_elements(self, elements):

        for element in elements:
            self.addItem(element)

    def select_first_file(self):
        
        self.setCurrentRow(0)

    '''def open_file(self):
        item = self.currentItem()
        image_name = item.text()
        self.viewer.layers.clear()
        self.viewer.open(Path(self.folder_path).joinpath(image_name))'''