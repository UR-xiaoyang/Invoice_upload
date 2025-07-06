# invoice management system

A modern invoice management application based on PySide6.

## Features

- **Modern UI Design**: Sleek and user-friendly interface.
- **Multi-User Management**: Supports adding, deleting, and renaming users, with invoices managed on a per-user basis.
- **Invoice Management**: Full CRUD (Create, Read, Update, Delete) operations for invoices.
- **File Caching**: Original invoice files (PDF, images) are cached for easy access.
- **Batch Scanning**: Supports batch OCR scanning of multiple invoice files.
- **OCR Integration**: Extracts data from invoices using OCR services.
- **PDF Text Extraction**: Extracts text directly from PDF files.
- **Interactive Table**: Modern table view for displaying invoices with sorting and status indicators.
- **Dynamic Buttons**: Action buttons are intelligently enabled/disabled based on selections.
- **Sidebar Navigation**: Modern collapsible sidebar for user selection.
- **Data Persistence**: Invoice data is saved locally in a `invoices.json` file.

## Installation and Running

### Method 1: Use the startup script (recommended)
```bash
./run.sh
```

### Method 2: Manual execution

1. **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python src/main.py
    ```

## Project structure

```
Invoice_upload/
├── cache/                  # Directory for cached invoice source files
├── src/                    # Source code directory
│   ├── components/         # UI component modules
│   │   ├── button_widget.py    # Bottom action buttons
│   │   ├── invoice_dialog.py   # Dialog for adding/editing invoices
│   │   ├── progress_dialog.py  # Progress dialog for batch operations
│   │   ├── sidebar_widget.py   # Left sidebar for user management
│   │   └── table_widget.py     # Main invoice display table
│   ├── services/           # Backend services
│   │   ├── ocr_service.py      # OCR processing service
│   │   ├── pdf_text_service.py # PDF text extraction service
│   │   └── verification_service.py # Invoice verification service
│   ├── styles/             # Style management module
│   │   └── styles.py       # Style definitions
│   ├── data_manager.py     # Data persistence and management
│   ├── main_window.py      # Main window class
│   └── main.py             # Main application entry point
├── invoices.json           # Data storage file
├── requirements.txt        # Project dependencies
├── run.sh                  # Startup script
├── TODO.md                 # Development plan
└── README.md               # Project description
```

## Development Progress

Please refer to the `TODO.md` file for a detailed development plan and progress.

## System Requirements

- Python 3.7+
- PySide6
- Dependencies listed in `requirements.txt`
- Linux/Windows/macOS

## Contribution

Welcome to submit issues and feature requests! 