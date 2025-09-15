# 📝 Pariksha - Question Paper Drafting System for Teachers

A comprehensive web-based application for creating, editing, and generating professional question papers with advanced formatting capabilities.

## 🌟 Features

### Core Functionality
- **Interactive Question Paper Creation** - Add multiple text boxes with rich markdown support
- **Professional Header Generator** - Create standardized headers for different institutions
- **Live Preview** - Toggle preview to see how your question paper will look
- **PDF Generation** - Export professional PDFs with proper formatting
- **Save & Load** - Save papers as markdown files with metadata for future editing
- **Advanced Typography** - Customizable fonts, sizes, and line spacing
- **Windows Executable** - Standalone Windows application with no installation required

### Question Paper Elements
- **Text Boxes** - Rich markdown content with question numbers and marks
- **Professional Headers** - Institutional headers with school/university details
- **Page Breaks** - Insert page breaks for proper pagination
- **End Markers** - Mark the end of your question paper
- **Header Formatting** - Automatic centering of headers (H1, H2, H3, H4)
- **Alphabetical Lists** - Proper formatting for multiple choice options (a, b, c, d)
- **Image Support** - Drag-and-drop image insertion with base64 encoding
- **Table Generator** - Built-in table creation with customizable rows and columns

### Advanced Features
- **Bootstrap Integration** - Professional styling with responsive design
- **Markdown Support** - Full markdown syntax including tables, images, and formatting
- **Center Alignment** - Support for centered content using HTML divs
- **Float Layouts** - Left and right floating elements for complex layouts
- **Custom CSS** - Enhanced styling for professional question papers

## 🚀 Quick Start

### Option 1: Windows Executable (Recommended for Windows Users)

1. **Download the Windows build**
   - Download and extract `Pariksha_Windows_App.zip`
   - No installation required - runs standalone

2. **Run the application**
   - Double-click `Start_Pariksha.bat`
   - Wait for the application to load (30-60 seconds first time)
   - Application opens automatically in your web browser

3. **Use Header Generator**
   - Double-click `Header_Generator.bat` for professional headers
   - Choose from templates or create custom headers

### Option 2: Python Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

#### Installation Steps

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd notebook
```

2. **Install dependencies**
```bash
pip install streamlit markdown markdown-pdf
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Run header generator**
```bash
python header.py --interactive
```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 🎓 Header Generator Tool

The built-in header generator creates professional, standardized headers for question papers across different educational institutions.

### Template Types

#### 1. Standard School Template
Perfect for school-level examinations with essential details:
- School name and examination title
- Subject and class/grade information
- Duration, marks, and date
- Student information section
- General instructions

#### 2. University Template
Designed for higher education institutions:
- University and department details
- Course code and title
- Semester and year information
- Student ID section
- Academic instructions

#### 3. Board Examination Template
Formatted for board-level examinations:
- Board of education name
- Examination type and paper code
- Prominent roll number section
- Subject and standard details
- Official instructions

### Using the Header Generator

#### Command Line Usage
```bash
# Interactive mode with guided setup
python header.py --interactive

# Quick templates
python header.py --template standard
python header.py --template university
python header.py --template board

# Custom configuration
python header.py --template standard --config my_school_config.json --output school_header.md
```

#### Windows Users
- **Double-click** `Header_Generator.bat` for menu interface
- **Right-click** `Header_Generator.ps1` → "Run with PowerShell" for enhanced experience
- **Command line** access via `python header.py`

#### Configuration Files
Create JSON configuration files to customize headers:

```json
{
    "school_name": "Green Valley High School",
    "exam_name": "Mid-Term Examination - 2025",
    "subject": "Mathematics",
    "class_grade": "Grade 10",
    "duration": "3 Hours",
    "max_marks": "80",
    "date": "March 15, 2025",
    "instructions": [
        "All questions are compulsory.",
        "Use only black or blue pen.",
        "Calculator is not allowed.",
        "Draw neat diagrams wherever necessary.",
        "Show all working steps clearly."
    ]
}
```

### Integration with Main Application
Generated headers can be:
1. Copied directly into question paper text boxes
2. Saved as markdown files for reuse
3. Customized further within the main application
4. Used as templates for consistent branding

## 📖 Usage Guide

### Creating a New Question Paper

1. **Set Paper Details**
   - Enter paper name in the text input field
   - Configure font settings (style, size, line spacing)
   - Choose marks position (Beginning/End of questions)

2. **Add Content**
   - Click "➕ Add Text Box" to add question content
   - Use markdown syntax for rich formatting
   - Set question numbers and marks for each text box
   - Add page breaks where needed

3. **Format Your Content**
   - Use `#`, `##`, `###`, `####` for headers (automatically centered)
   - Create lists with `a)`, `b)`, `c)`, `d)` for multiple choice
   - Use HTML `<div style="text-align: center;">` for custom centering
   - Add images, tables, and other markdown elements

4. **Preview and Export**
   - Click "👁️ Preview" to see formatted output
   - Click "🙈 Close Preview" to hide preview
   - Click "🖨️ Print PDF" to generate and download PDF
   - Click "💾 Save" to save as markdown file

### Advanced Formatting Examples

#### Headers (Automatically Centered)
```markdown
# Main Title
## Section Title
### Subsection
#### Question Group
```

#### Multiple Choice Questions
```markdown
**[Marks: 1]** **(Q1)** This is a sample question:

a) First option
b) Second option
c) Third option
d) Fourth option
```

#### Centered Content
```html
<div style="text-align: center;">
**SECTION A**
</div>
```

#### Float Layouts
```html
<div style="float: left;">Grade: 12<br>Date: 15-09-2025</div>
<div style="float: right;">Time: 3 hours<br>Max Marks: 80</div>
<div style="overflow: hidden;"></div>
```

#### Section Headers (Centered)
```html
<p style="text-align: center;"><strong>Section Name</strong></p>
```

#### Images and Tables
- **Images**: Use the "Browse Files" button to upload and embed images
- **Tables**: Use the "Insert Table" feature with customizable rows and columns
- **Markdown Help**: Click the "📖" button for quick reference

## 📁 File Structure

```
notebook/
├── app.py                      # Main Streamlit application
├── header.py                   # Professional header generator
├── sample_header_config.json   # Example header configuration
├── README.md                   # This documentation
├── papers/                     # Saved question papers (.md files)
├── metadata/                   # Paper metadata (.json files)
├── downloads/                  # Downloaded images and assets
├── templates/                  # Custom header templates (.json files)
└── windows/                    # Windows build and distribution files
    ├── build_windows_app.py    # Windows build script
    ├── launch_app.py           # Windows launcher script
    ├── header_generator.bat    # Windows header generator (batch)
    ├── header_generator.ps1    # Windows header generator (PowerShell)
    ├── build.bat              # Quick Windows build script
    ├── build.ps1              # PowerShell build script
    └── WINDOWS_BUILD_GUIDE.md  # Windows build instructions
```

## 🪟 Windows Deployment

### Creating Windows Executable

For developers wanting to create their own Windows build:

1. **Prepare Build Environment**
```bash
pip install pyinstaller streamlit markdown markdown-pdf
```

2. **Run Build Script**
```bash
cd windows
python build_windows_app.py
```

3. **Alternative Build Methods**
```bash
# Using batch file
build.bat

# Using PowerShell
build.ps1
```

### Distribution Package

The Windows build creates `Pariksha_Windows_App/` folder containing:
- **Start_Pariksha.bat** - Main application launcher
- **Header_Generator.bat** - Header creation tool
- **Header_Generator.ps1** - PowerShell version with enhanced UI
- **Pariksha/** - Application executable and dependencies
- **USER_GUIDE.txt** - Quick start guide for end users
- **Sample configuration files** - Template customization examples

### System Requirements
- **Windows 7 or later** (64-bit recommended)
- **4GB RAM minimum** (8GB recommended)
- **500MB free disk space**
- **No Python installation required** (self-contained)

### Security Notes
- Windows Defender may initially flag the executable
- Add exception or select "Run anyway" if prompted
- All files are digitally signed for authenticity

## 🛠️ Technical Details

### Dependencies
- **streamlit** - Web application framework
- **markdown** - Markdown processing for preview
- **markdown-pdf** - PDF generation from markdown
- **json** - Metadata handling
- **tempfile** - Temporary file management
- **os** - File system operations
- **base64** - File encoding for downloads

### Architecture
- **Frontend**: Streamlit web interface with Bootstrap styling
- **Backend**: Python with markdown processing and PDF generation
- **Storage**: Local file system for papers and metadata
- **Export**: markdown-pdf library for professional PDF output

### PDF Generation Features
- Custom CSS styling for professional appearance
- Proper header formatting and centering
- Alphabetical list processing
- Image and table support
- Page break handling
- Font customization

## 🔧 Configuration

### Font Options
- Arial, sans-serif (default)
- Times New Roman, serif
- Courier New, monospace
- Custom font families

### Styling Options
- Font size: 8-24pt
- Line spacing: 1.0-3.0
- Pagination: Enabled/Disabled
- Marks position: Beginning/End

## 📝 File Formats

### Markdown Files (.md)
- Question paper content in markdown format
- Supports HTML tags for advanced formatting
- Automatically saved in `papers/` directory

### Metadata Files (.json)
- Paper configuration and settings
- Cell structure and metadata
- Font and styling preferences
- Saved in `metadata/` directory

## 🐛 Troubleshooting

### Common Issues

**PDF generation fails**
- Ensure `markdown-pdf` is installed: `pip install markdown-pdf`
- Check file permissions for temporary directories
- Verify sufficient disk space for temporary files

**Preview not showing**
- Verify all markdown syntax is correct
- Check for unclosed HTML tags
- Clear browser cache and reload

**Images not displaying**
- Ensure images are in `downloads/` directory
- Use relative paths: `./downloads/image.png`
- Check image file format (PNG, JPG, JPEG supported)

**App won't start**
- Check Python version (3.8+ required)
- Install missing dependencies: `pip install streamlit markdown markdown-pdf`
- Verify port 8501 is not in use

**Header generator issues**
- Ensure `header.py` is in the correct directory
- Check JSON configuration file syntax
- Verify write permissions for output directory

### Windows-Specific Issues

**Windows executable won't start**
- Run as Administrator if permission denied
- Add Windows Defender exception
- Check available disk space (500MB minimum)

**Header Generator batch file fails**
- Ensure Python is installed and in PATH
- Right-click → "Run as Administrator"
- Use PowerShell version for better error messages

**Browser doesn't open automatically**
- Copy URL from command window manually
- Check default browser settings
- Try different browser (Chrome, Firefox, Edge)

**File access denied errors**
- Run application as Administrator
- Move application to user directory (not Program Files)
- Check antivirus software blocking access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please ensure proper attribution when using or modifying the code.

## 🆘 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review existing documentation
3. Create an issue with detailed description and steps to reproduce

## 🔮 Future Enhancements

### Planned Features
- **Multiple export formats** - Word (.docx) and HTML export options
- **Cloud storage integration** - Google Drive, OneDrive synchronization
- **Advanced mathematical equation support** - LaTeX/MathJax integration
- **Question bank integration** - Reusable question libraries
- **Collaborative editing** - Multi-user editing capabilities
- **Advanced templates** - Subject-specific question paper templates

### Recently Added ✅
- ✅ **Professional header generator** - Multi-institutional templates
- ✅ **Windows executable** - No-installation standalone application
- ✅ **Enhanced markdown support** - Section headers and improved formatting
- ✅ **Image upload system** - Drag-and-drop with base64 encoding
- ✅ **Table generator** - Built-in table creation tools
- ✅ **Comprehensive help system** - In-app markdown reference

---

**Pariksha - Created for educators, by educators. Making question paper creation simple and professional.**