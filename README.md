# 📝 Teacher Question Paper Drafting System

A comprehensive web-based application for creating, editing, and generating professional question papers with advanced formatting capabilities.

## 🌟 Features

### Core Functionality
- **Interactive Question Paper Creation** - Add multiple text boxes with rich markdown support
- **Live Preview** - Toggle preview to see how your question paper will look
- **PDF Generation** - Export professional PDFs with proper formatting
- **Save & Load** - Save papers as markdown files with metadata for future editing
- **Advanced Typography** - Customizable fonts, sizes, and line spacing

### Question Paper Elements
- **Text Boxes** - Rich markdown content with question numbers and marks
- **Page Breaks** - Insert page breaks for proper pagination
- **End Markers** - Mark the end of your question paper
- **Header Formatting** - Automatic centering of headers (H1, H2, H3, H4)
- **Alphabetical Lists** - Proper formatting for multiple choice options (a, b, c, d)

### Advanced Features
- **Bootstrap Integration** - Professional styling with responsive design
- **Markdown Support** - Full markdown syntax including tables, images, and formatting
- **Center Alignment** - Support for centered content using HTML divs
- **Float Layouts** - Left and right floating elements for complex layouts
- **Custom CSS** - Enhanced styling for professional question papers

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

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

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

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

## 📁 File Structure

```
notebook/
├── app.py                 # Main Streamlit application
├── README.md             # This documentation
├── papers/               # Saved question papers (.md files)
├── metadata/             # Paper metadata (.json files)
└── downloads/            # Downloaded images and assets
```

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

**Preview not showing**
- Verify all markdown syntax is correct
- Check for unclosed HTML tags

**Images not displaying**
- Ensure images are in `downloads/` directory
- Use relative paths: `./downloads/image.png`

**App won't start**
- Check Python version (3.8+ required)
- Install missing dependencies: `pip install streamlit markdown markdown-pdf`

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

- Multiple export formats (Word, HTML)
- Template library for common question paper formats
- Collaborative editing features
- Cloud storage integration
- Advanced mathematical equation support
- Question bank integration

---

**Created for educators, by educators. Making question paper creation simple and professional.**