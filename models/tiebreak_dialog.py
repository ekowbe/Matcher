"""Utilities file for a custom QDialog for tiebreaks."""

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QTextEdit, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont

# Named constant for a fixed-width font, Monaco (if it is available on the system).
# Otherwise, it will pick a "TypeWriter" style with a fixed pitch.
FW_FONT = QFont("Monaco")
FW_FONT.setStyleHint(QFont.StyleHint.TypeWriter)
FW_FONT.setFixedPitch(True)

class FixedWidthMessageDialog(QDialog):
    """Custom subclass of QDialog that displays a message in a fixed-width font and a single
        button, 'OK'.
    """

    def __init__(self, title, message, parent=None):
        """Initializer for FixedWidthMessageDialog."""

        # Call the QDialog (superclass) initializer
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle(title)
        self.user_pick = None

        # Initialize the button widget, ready to add to the layout
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept)

        # # Initialize and lay out the message box, which must be sized to the message displayed
        # msg_widget = QTextEdit()
        # msg_widget.setPlainText(message)
        # msg_widget.setFont(FW_FONT)
        # msg_widget.setReadOnly(True)
        # msg_widget.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # msg_size = msg_widget.document().size().toSize()
        # msg_widget.setFixedSize(msg_size)

        # trying a label instead of a message box
        label_widget = QLabel(message)

        # text edit
        user_input_widget = QLineEdit()
    
        # Set this dialog's layout to be a VBox (vertically-aligned widgets), and add the message
        # widget and the button to the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(label_widget)
        self.layout.addWidget(user_input_widget)
        self.layout.addWidget(button)

        # Set self.layout to be the VBox layout containing the two widgets
        self.setLayout(self.layout)

        def line_edit_delegate():
            return self.set_input(user_input_widget)

        user_input_widget.returnPressed.connect(line_edit_delegate)

    def set_input(self, user_input_edit):
        self.user_pick = int(user_input_edit.text())
