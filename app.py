import streamlit as st
import os
import base64
import markdown
import json
import tempfile
from markdown_pdf import MarkdownPdf, Section

# Set wide layout for better alignment
st.set_page_config(layout="wide")

# Custom CSS and Bootstrap integration
st.markdown("""
<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Font Awesome for icons -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet">
<style>
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    .stTextInput > div > div > div > input,
    .stNumberInput > div > div > div > input {
        background-color: white;
        color: #212529;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 0.25rem;
        padding: 0.25rem 0.5rem;
        font-size: 0.875rem;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stExpander {
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    .stExpander > div > div > div > div {
        background-color: #ffffff !important;
        color: #212529 !important;
        padding: 8px 12px !important;
    }
    .stExpander summary {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        border-bottom: 1px solid #dee2e6;
        padding: 8px 12px !important;
        font-weight: 500;
    }
    .stMarkdown {
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        margin-top: 10px;
        padding: 8px;
    }
    .stFileUploader > div > div > div > div,
    .stFileUploader > div > div > div > small,
    .stFileUploader > div > div > div > div > div,
    .stFileUploader label,
    .stFileUploader > div > div > div > div > span,
    .stFileUploader > div > div > div > span,
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"],
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div:first-child {
        display: none !important;
    }
    .stFileUploader > div > div > div,
    .stFileUploader > div > div {
        padding: 0 !important;
    }
    .stFileUploader > div > div > button {
        margin-top: 0px;
        background-color: white;
        color: #212529;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 0.25rem 0.5rem;
        font-size: 0.875rem;
    }
    .stFileUploader > div > div > button:hover {
        background-color: #e9ecef;
    }
    .stMarkdownHelp {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 0.25rem;
        margin-top: 10px;
    }
    .toolbar-btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.875rem;
    }
    .cell-toolbar {
        margin-bottom: 5px;
        margin-top: 2px;
    }
    .toolbar-input {
        width: 60px;
        font-size: 0.75rem;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
    }
    .toolbar-checkbox {
        margin: 0;
    }
    .toolbar-file-input {
        width: 80px;
        font-size: 0.75rem;
    }
    .input-group-text {
        font-size: 0.75rem;
        padding: 0.2rem 0.4rem;
    }
</style>
<!-- Bootstrap JS (for tooltips) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });
</script>
""", unsafe_allow_html=True)

st.title("Pariksha - Question Paper Drafting System for Teachers")

# Simple cell class to replace notebook functionality
class Cell:
    def __init__(self, cell_type="textbox", code="", metadata=None):
        self.type = cell_type
        self.code = code
        self.metadata = metadata or {}


def generate_pdf_from_markdown(md_content, font_style, font_size, line_spacing, pagination):
    """Generate PDF directly from markdown using markdown-pdf library"""
    try:
        import re
        import tempfile
        import os
        from markdown_pdf import MarkdownPdf, Section

        # Pre-process markdown to fix list formatting and centered headers
        processed_md = md_content

        # Fix centered headers - handle all div patterns more robustly
        # First, handle the specific multiline div pattern from the current file
        lines = processed_md.split('\n')
        processed_lines = []
        inside_center_div = False
        i = 0

        while i < len(lines):
            line = lines[i]
            line_stripped = line.strip()

            # Look for opening div tag
            if line_stripped == '<div style="text-align: center;">':
                inside_center_div = True
                i += 1
                continue

            # Look for closing div tag
            elif line_stripped == '</div>' and inside_center_div:
                inside_center_div = False
                i += 1
                continue

            # Handle content inside center div
            elif inside_center_div:
                if line_stripped.startswith('#'):
                    # This is a header - wrap it in center tags
                    processed_lines.append(f'<center>{line_stripped}</center>')
                elif line_stripped and not line_stripped.startswith('<') and not line_stripped.startswith('<!'):
                    # Non-HTML, non-empty content - keep with center div
                    processed_lines.append(f'<div style="text-align: center;">{line_stripped}</div>')
                else:
                    # HTML content, empty lines, or other - preserve as-is
                    processed_lines.append(line)
                i += 1
                continue

            # Handle content outside center divs
            else:
                processed_lines.append(line)
                i += 1

        processed_md = '\n'.join(processed_lines)

        # Additional cleanup: handle any remaining inline div-wrapped headers
        header_pattern = r'<div style="text-align: center;">\s*(#{1,6}[^<]*?)\s*</div>'
        processed_md = re.sub(header_pattern, r'<center>\1</center>', processed_md, flags=re.MULTILINE | re.DOTALL)

        # Convert alphabetical options to proper markdown lists
        # Look for patterns like "a) text", "b) text", etc. and convert to proper list format
        option_pattern = r'^([a-d])\)\s+(.+)$'
        lines = processed_md.split('\n')
        processed_lines = []
        in_options = False

        for i, line in enumerate(lines):
            # Check if this line looks like an option
            match = re.match(option_pattern, line.strip())
            if match:
                if not in_options:
                    # Start of options list
                    in_options = True
                    processed_lines.append('')  # Add blank line before list
                letter, text = match.groups()
                # Convert to proper ordered list with lowercase letters
                processed_lines.append(f'1. {text}')
            else:
                if in_options and line.strip() == '':
                    # End of options list
                    in_options = False
                processed_lines.append(line)

        processed_md = '\n'.join(processed_lines)

        # Create MarkdownPdf instance with proper configuration
        pdf = MarkdownPdf(toc_level=2)

        # Configure styling - no title or author to avoid printing them

        # Create custom CSS styling
        css_content = f"""
        @page {{
            margin: 1in;
            size: letter;
        }}
        body {{
            font-family: "{font_style}", serif;
            font-size: {font_size}pt;
            line-height: {line_spacing};
            color: #000;
            margin: 0;
            padding: 0;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-weight: bold !important;
            color: #000 !important;
            margin-top: 1em;
            margin-bottom: 0.5em;
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        h1 {{
            font-size: {font_size * 1.8}pt !important;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            text-align: center !important;
            font-weight: bold !important;
        }}
        h2 {{
            font-size: {font_size * 1.5}pt !important;
            margin-top: 1em;
            margin-bottom: 0.5em;
            text-align: center !important;
            font-weight: bold !important;
        }}
        h3 {{
            font-size: {font_size * 1.3}pt !important;
            margin-top: 0.8em;
            margin-bottom: 0.4em;
            text-align: center !important;
            font-weight: bold !important;
        }}
        h4 {{
            font-size: {font_size * 1.2}pt !important;
            margin-top: 0.7em;
            margin-bottom: 0.4em;
            text-align: center !important;
            font-weight: bold !important;
        }}
        h5, h6 {{
            font-weight: bold !important;
            text-align: center !important;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin-bottom: 8px;
            display: list-item;
            line-height: {line_spacing};
        }}
        ol li {{
            list-style-type: lower-alpha;
        }}
        ul li {{
            list-style-type: disc;
        }}
        strong, b {{
            font-weight: bold;
        }}
        em, i {{
            font-style: italic;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }}
        th {{
            font-weight: bold;
            background-color: #f5f5f5;
        }}
        .page-break {{
            page-break-after: always;
        }}
        div[style*="text-align: center"] {{
            text-align: center;
        }}
        center {{
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        center h1, center h2, center h3, center h4, center h5, center h6 {{
            text-align: center !important;
            font-weight: bold !important;
        }}
        div[style*="float: left"] {{
            float: left;
        }}
        div[style*="float: right"] {{
            float: right;
        }}
        div[style*="overflow: hidden"] {{
            overflow: hidden;
            clear: both;
        }}
        """

        # Apply CSS styling properly
        pdf.stylesheet = css_content

        # Add the processed markdown content as a section
        pdf.add_section(Section(processed_md, toc=False))

        # Generate PDF using a temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            pdf.save(temp_file.name)
            temp_file.seek(0)
            with open(temp_file.name, 'rb') as f:
                pdf_bytes = f.read()

            # Clean up the temporary file
            os.unlink(temp_file.name)

        return pdf_bytes

    except Exception as e:
        import streamlit as st
        st.error(f"PDF generation failed: {str(e)}")
        return None

def generate_html(md_content, font_style, font_size, line_spacing, pagination):
    """Generate HTML for preview"""
    import re
    import markdown

    # Pre-process markdown to fix list formatting and centered headers (same as PDF)
    processed_md = md_content

    # Fix centered headers - handle all div patterns more robustly
    lines = processed_md.split('\n')
    processed_lines = []
    inside_center_div = False
    i = 0

    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()

        # Look for opening div tag
        if line_stripped == '<div style="text-align: center;">':
            inside_center_div = True
            i += 1
            continue

        # Look for closing div tag
        elif line_stripped == '</div>' and inside_center_div:
            inside_center_div = False
            i += 1
            continue

        # Handle content inside center div
        elif inside_center_div:
            if line_stripped.startswith('#'):
                # This is a header - wrap it in center tags
                processed_lines.append(f'<center>{line_stripped}</center>')
            elif line_stripped and not line_stripped.startswith('<') and not line_stripped.startswith('<!'):
                # Non-HTML, non-empty content - keep with center div
                processed_lines.append(f'<div style="text-align: center;">{line_stripped}</div>')
            else:
                # HTML content, empty lines, or other - preserve as-is
                processed_lines.append(line)
            i += 1
            continue

        # Handle content outside center divs
        else:
            processed_lines.append(line)
            i += 1

    processed_md = '\n'.join(processed_lines)

    # Additional cleanup: handle any remaining inline div-wrapped headers
    header_pattern = r'<div style="text-align: center;">\s*(#{1,6}[^<]*?)\s*</div>'
    processed_md = re.sub(header_pattern, r'<center>\1</center>', processed_md, flags=re.MULTILINE | re.DOTALL)

    # Convert alphabetical options to proper markdown lists
    option_pattern = r'^([a-d])\)\s+(.+)$'
    lines = processed_md.split('\n')
    processed_lines = []
    in_options = False

    for i, line in enumerate(lines):
        # Check if this line looks like an option
        match = re.match(option_pattern, line.strip())
        if match:
            if not in_options:
                # Start of options list
                in_options = True
                processed_lines.append('')  # Add blank line before list
            letter, text = match.groups()
            # Convert to proper ordered list with lowercase letters
            processed_lines.append(f'1. {text}')
        else:
            if in_options and line.strip() == '':
                # End of options list
                in_options = False
            processed_lines.append(line)

    processed_md = '\n'.join(processed_lines)

    # Convert to HTML
    html_body = markdown.markdown(processed_md, extensions=['extra'])

    # Create CSS styling
    css = f"""
    body {{
        font-family: {font_style};
        font-size: {font_size}pt;
        line-height: {line_spacing};
        margin: 20px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-weight: bold !important;
        color: #000 !important;
        margin-top: 1em;
        margin-bottom: 0.5em;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }}
    h1 {{ font-size: {font_size * 1.8}pt !important; }}
    h2 {{ font-size: {font_size * 1.5}pt !important; }}
    h3 {{ font-size: {font_size * 1.3}pt !important; }}
    h4 {{ font-size: {font_size * 1.2}pt !important; }}
    img {{ max-width: 100%; height: auto; display: block; margin: 10px auto; }}
    ul, ol {{
        margin: 10px 0;
        padding-left: 30px;
    }}
    li {{
        margin-bottom: 8px;
        line-height: {line_spacing};
    }}
    ol {{
        list-style-type: lower-alpha;
    }}
    div[style*="text-align: center"] {{
        text-align: center;
    }}
    center {{
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }}
    center h1, center h2, center h3, center h4, center h5, center h6 {{
        text-align: center !important;
        font-weight: bold !important;
    }}
    div[style*="float: left"] {{
        float: left;
    }}
    div[style*="float: right"] {{
        float: right;
    }}
    div[style*="overflow: hidden"] {{
        overflow: hidden;
        clear: both;
    }}
    """

    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>{css}</style>
    </head>
    <body>{html_body}</body>
    </html>
    """
    return html

# Initialize session state
if 'paper_name' not in st.session_state:
    st.session_state.paper_name = "Untitled"
if 'font_style' not in st.session_state:
    st.session_state.font_style = "Arial"
if 'font_size' not in st.session_state:
    st.session_state.font_size = 12
if 'line_spacing' not in st.session_state:
    st.session_state.line_spacing = 1.5
if 'pagination' not in st.session_state:
    st.session_state.pagination = True
if 'marks_position' not in st.session_state:
    st.session_state.marks_position = "Beginning"
if 'show_markdown_help' not in st.session_state:
    st.session_state.show_markdown_help = {}
if 'show_preview' not in st.session_state:
    st.session_state.show_preview = False
if 'cells' not in st.session_state:
    st.session_state.cells = []

# Load existing paper
st.subheader("Load Existing Paper")
os.makedirs("metadata", exist_ok=True)
papers = [f[:-5] for f in os.listdir("metadata") if f.endswith('.json')]
selected_paper = st.selectbox("Select Paper to Load", [""] + papers, key="load_paper")
if st.button("📂 Load", key="load_btn"):
    metadata_path = os.path.join("metadata", f"{selected_paper}.json")
    try:
        with open(metadata_path, 'r') as f:
            data = json.load(f)
        st.session_state.font_style = data['font_style']
        st.session_state.font_size = data['font_size']
        st.session_state.line_spacing = data['line_spacing']
        st.session_state.pagination = data['pagination']
        st.session_state.marks_position = data.get('marks_position', 'Beginning')
        # Clear existing cells
        st.session_state.cells = []
        # Add cells from metadata
        for cell_data in data['cells']:
            cell_type = cell_data['type']
            if cell_type == 'textbox':
                cell = Cell(
                    cell_type="textbox",
                    code=cell_data['text'],
                    metadata={
                        'question_num': cell_data['question_num'],
                        'marks': cell_data['marks'],
                        'center': cell_data['center'],
                        'table_rows': cell_data['table_rows'],
                        'table_cols': cell_data['table_cols']
                    }
                )
                st.session_state.cells.append(cell)
            elif cell_type == 'pagebreak':
                cell = Cell(cell_type="pagebreak", code="📄 Page Break")
                st.session_state.cells.append(cell)
            elif cell_type == 'end':
                cell = Cell(cell_type="end", code="🏁 ----End of Paper ----")
                st.session_state.cells.append(cell)
        st.session_state.paper_name = selected_paper
        st.session_state.show_markdown_help = {f"md_help_{i}": False for i in range(len(data['cells']))}
        st.success(f"Loaded {selected_paper}")
        st.rerun()
    except Exception as e:
        st.error(f"Error loading file: {e}")

# Top options for font, size, spacing, pagination, marks position
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.selectbox("🅰️ Font Style", ["Arial", "Times New Roman", "Courier New", "Verdana"], key='font_style')
with col2:
    st.number_input("📏 Font Size", min_value=8, max_value=24, key='font_size')
with col3:
    st.number_input("↕️ Line Spacing", min_value=1.0, max_value=3.0, step=0.1, key='line_spacing')
with col4:
    st.checkbox("📄 Pagination", key='pagination')
with col5:
    st.selectbox("🏷️ Marks Position", ["Beginning", "End"], key='marks_position')

# Paper name
st.text_input("📝 Paper Name", key='paper_name')

# Add new cell at the top
st.subheader("Add New Cell")
cell_type_top = st.selectbox("Cell Type", ["Text Box", "Page Break", "End"], key="cell_type_top")
if st.button("➕ Add Cell", key="add_cell_top"):
    if cell_type_top == "Text Box":
        cell = Cell(
            cell_type="textbox",
            code="",
            metadata={
                'question_num': 1,
                'marks': 0,
                'center': False,
                'table_rows': 2,
                'table_cols': 2
            }
        )
        st.session_state.cells.append(cell)
        st.session_state.show_markdown_help[f"md_help_{len(st.session_state.cells)-1}"] = False
    elif cell_type_top == "Page Break":
        cell = Cell(cell_type="pagebreak", code="📄 Page Break")
        st.session_state.cells.append(cell)
    elif cell_type_top == "End":
        cell = Cell(cell_type="end", code="🏁 ----End of Paper ----")
        st.session_state.cells.append(cell)
    st.rerun()

# Markdown Help content
markdown_help_content = """
### Markdown Quick Reference
- **Bold**: `**text**` or `__text__`
- *Italic*: `*text*` or `_text_`
- **Header 1**: `# Header`
- **Header 2**: `## Header`
- **Bullet List**:
  ```
  - Item 1
  - Item 2
  ```
- **Numbered List**:
  ```
  1. Item 1
  2. Item 2
  ```
- **Link**: `[Link text](URL)`
- **Blockquote**: `> Quote text`
"""

# Display and edit cells
for idx, cell in enumerate(st.session_state.cells):
    with st.expander(f"Cell {idx+1}: {cell.type.capitalize()}", expanded=True):
        # Toolbar with editor controls (left) and cell controls (right)
        col_left, col_right = st.columns([3, 1])
        with col_left:
            if cell.type == 'textbox':
                col_qnum, col_marks, col_rows, col_cols, col_insert, col_center, col_browse = st.columns([1, 1, 1, 1, 1, 1, 1])
                with col_qnum:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Q#</span></div>', unsafe_allow_html=True)
                    cell.metadata['question_num'] = st.number_input(
                        "", min_value=0, value=cell.metadata.get('question_num', 1),
                        key=f"qnum_{idx}", label_visibility="collapsed"
                    )
                with col_marks:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Marks</span></div>', unsafe_allow_html=True)
                    cell.metadata['marks'] = st.number_input(
                        "", min_value=0, value=cell.metadata.get('marks', 0),
                        key=f"marks_{idx}", label_visibility="collapsed"
                    )
                with col_rows:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Rows</span></div>', unsafe_allow_html=True)
                    cell.metadata['table_rows'] = st.number_input(
                        "", min_value=1, max_value=20, value=cell.metadata.get('table_rows', 2),
                        key=f"rows_{idx}", label_visibility="collapsed"
                    )
                with col_cols:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Cols</span></div>', unsafe_allow_html=True)
                    cell.metadata['table_cols'] = st.number_input(
                        "", min_value=1, max_value=20, value=cell.metadata.get('table_cols', 2),
                        key=f"cols_{idx}", label_visibility="collapsed"
                    )
                with col_insert:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">+</span></div>', unsafe_allow_html=True)
                    if st.button("Insert Table", key=f"insert_table_{idx}", use_container_width=True):
                        rows = cell.metadata['table_rows']
                        cols = cell.metadata['table_cols']
                        header = "| " + " | ".join([f"Col{i+1}" for i in range(cols)]) + " |"
                        separator = "| " + " --- |" * cols
                        table_rows = ["| " + " | ".join([" " for _ in range(cols)]) + " |" for _ in range(rows)]
                        table_md = "\n\n" + header + "\n" + separator + "\n" + "\n".join(table_rows) + "\n\n"
                        cell.code += table_md
                        st.rerun()
                with col_center:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Center</span></div>', unsafe_allow_html=True)
                    cell.metadata['center'] = st.checkbox(
                        "", value=cell.metadata.get('center', False),
                        key=f"center_{idx}", label_visibility="collapsed"
                    )
                with col_browse:
                    st.markdown('<div class="input-group input-group-sm"><span class="input-group-text">Browse</span></div>', unsafe_allow_html=True)
                    # Toggle file uploader when button is clicked
                    show_uploader_key = f"show_uploader_{idx}"
                    if st.button("Browse Files", key=f"browse_btn_{idx}", use_container_width=True):
                        st.session_state[show_uploader_key] = not st.session_state.get(show_uploader_key, False)

                    # Show file uploader if button was clicked
                    if st.session_state.get(show_uploader_key, False):
                        uploader = st.file_uploader(
                            "Select an image file", type=["png", "jpg", "jpeg"], key=f"browse_{idx}",
                            accept_multiple_files=False
                        )
                        # Track processed files to prevent infinite rerun
                        processed_key = f"processed_file_{idx}"
                        if uploader and (processed_key not in st.session_state or st.session_state[processed_key] != uploader.name):
                            # Read file content
                            file_bytes = uploader.read()

                            # Create downloads directory and save file locally (for reference)
                            downloads_dir = "downloads"
                            os.makedirs(downloads_dir, exist_ok=True)
                            file_path = os.path.join(downloads_dir, uploader.name)
                            with open(file_path, "wb") as f:
                                f.write(file_bytes)

                            # Create base64 data URI for embedding in markdown (works in preview and PDF)
                            img_data = base64.b64encode(file_bytes).decode()
                            img_type = uploader.type.split("/")[1]
                            img_md = f"\n\n![](data:image/{img_type};base64,{img_data})\n\n"
                            cell.code += img_md

                            # Mark file as processed and hide uploader
                            st.session_state[processed_key] = uploader.name
                            st.session_state[show_uploader_key] = False
                            st.rerun()
        with col_right:
            col_up, col_down, col_delete, col_help = st.columns(4)
            with col_up:
                if st.button("↑", key=f"move_up_{idx}", disabled=idx == 0, use_container_width=True):
                    st.session_state.cells[idx], st.session_state.cells[idx-1] = st.session_state.cells[idx-1], st.session_state.cells[idx]
                    st.rerun()
            with col_down:
                if st.button("↓", key=f"move_down_{idx}", disabled=idx == len(st.session_state.cells) - 1, use_container_width=True):
                    st.session_state.cells[idx], st.session_state.cells[idx+1] = st.session_state.cells[idx+1], st.session_state.cells[idx]
                    st.rerun()
            with col_delete:
                if st.button("🗑", key=f"delete_{idx}", use_container_width=True):
                    st.session_state[f"confirm_delete_{idx}"] = True
            with col_help:
                if cell.type == 'textbox' and st.button("📖", key=f"md_help_{idx}", use_container_width=True):
                    st.session_state.show_markdown_help[f"md_help_{idx}"] = not st.session_state.show_markdown_help.get(f"md_help_{idx}", False)

        # Delete confirmation
        if st.session_state.get(f"confirm_delete_{idx}", False):
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Delete", key=f"confirm_yes_{idx}"):
                    st.session_state.cells.pop(idx)
                    del st.session_state[f"confirm_delete_{idx}"]
                    st.rerun()
            with col_no:
                if st.button("Cancel", key=f"confirm_no_{idx}"):
                    st.session_state[f"confirm_delete_{idx}"] = False
                    st.rerun()

        if cell.type == 'textbox':
            # Show markdown help if toggled
            if st.session_state.show_markdown_help.get(f"md_help_{idx}", False):
                st.markdown(markdown_help_content, unsafe_allow_html=True)

            # Markdown editor with conditional styling
#            st.markdown('<p style="font-size: small;">✏️ Text (Markdown supported)</p>', unsafe_allow_html=True)

            # Apply center alignment if center checkbox is selected
            if cell.metadata.get('center', False):
                st.markdown(f"""
                <style>
                .centered-text-editor_{idx} textarea {{
                    text-align: center !important;
                }}
                </style>
                <div class="centered-text-editor_{idx}">
                """, unsafe_allow_html=True)

            cell.code = st.text_area(
                "", value=cell.code, key=f"editor_{idx}", height=300,
                placeholder="Enter markdown content here..."
            )

            # Close the div wrapper if center alignment was applied
            if cell.metadata.get('center', False):
                st.markdown("</div>", unsafe_allow_html=True)

        elif cell.type == 'pagebreak':
            st.write("📄 Page Break (will insert a page break in the output)")

        elif cell.type == 'end':
            st.write("🏁 ----End of Paper ----")

            # Save, Preview, Print PDF buttons
            def generate_md(cells, paper_name, marks_position="Beginning"):
                md = ""
                for cell in cells:
                    if cell.type == 'textbox':
                        question_num = cell.metadata.get('question_num', 0)
                        marks = cell.metadata.get('marks', 0)
                        text = cell.code.strip()

                        # Build the question content based on marks position
                        content = ""

                        if marks_position == "Beginning":
                            # Add marks first if specified
                            if marks > 0:
                                content += f"**[Marks: {marks}]** "
                            # Add question number if specified
                            if question_num > 0:
                                content += f"**(Q{question_num})** "
                            # Add the main text content
                            if cell.metadata.get('center', False):
                                content += f"<div style=\"text-align: center;\">\n{text}\n</div>"
                            else:
                                content += text
                        else:  # marks_position == "End"
                            # Add question number first if specified
                            if question_num > 0:
                                content += f"**(Q{question_num})** "
                            # Add the main text content
                            if cell.metadata.get('center', False):
                                content += f"<div style=\"text-align: center;\">\n{text}\n</div>"
                            else:
                                content += text
                            # Add marks at the end if specified
                            if marks > 0:
                                content += f" **[Marks: {marks}]**"

                        md += content + "\n\n"

                    elif cell.type == 'pagebreak':
                        md += '<div class="page-break"></div>\n\n'
                    elif cell.type == 'end':
#                        md += '<center>----End of Paper ----</center>\n'
                        md += f"<div style=\"text-align: center;\">\n** End of Paper ** \n</div>"
                return md

            col_save, col_preview, col_pdf = st.columns(3)
            with col_save:
                if st.button("💾 Save", key="save_btn"):
                    paper_name = st.session_state.paper_name or "Untitled"
                    md_content = generate_md(st.session_state.cells, paper_name, st.session_state.marks_position)
                    dir_path = "papers"
                    os.makedirs(dir_path, exist_ok=True)
                    file_path = os.path.join(dir_path, f"{paper_name}.md")
                    with open(file_path, 'w') as f:
                        f.write(md_content)

                    # Save metadata JSON
                    metadata_dir = "metadata"
                    os.makedirs(metadata_dir, exist_ok=True)
                    metadata_path = os.path.join(metadata_dir, f"{paper_name}.json")
                    metadata = {
                        'font_style': st.session_state.font_style,
                        'font_size': st.session_state.font_size,
                        'line_spacing': st.session_state.line_spacing,
                        'pagination': st.session_state.pagination,
                        'marks_position': st.session_state.marks_position,
                        'cells': [
                            {
                                'type': cell.type,
                                'text': cell.code,
                                'question_num': cell.metadata.get('question_num', 1),
                                'marks': cell.metadata.get('marks', 0),
                                'center': cell.metadata.get('center', False),
                                'table_rows': cell.metadata.get('table_rows', 2),
                                'table_cols': cell.metadata.get('table_cols', 2)
                            } for cell in st.session_state.cells
                        ]
                    }
                    with open(metadata_path, 'w') as f:
                        json.dump(metadata, f, default=str)
                    st.success(f"Saved to {file_path} and {metadata_path}")

            with col_preview:
                # Toggle preview button
                preview_label = "🙈 Close Preview" if st.session_state.show_preview else "👁️ Preview"
                if st.button(preview_label, key="preview_btn"):
                    st.session_state.show_preview = not st.session_state.show_preview
                    st.rerun()

                # Show preview if toggled on
                if st.session_state.show_preview:
                    md_content = generate_md(st.session_state.cells, st.session_state.paper_name or "Untitled", st.session_state.marks_position)
                    html_content = generate_html(md_content, st.session_state.font_style, st.session_state.font_size, st.session_state.line_spacing, st.session_state.pagination)
                    st.components.v1.html(html_content, height=600, scrolling=True)

            with col_pdf:
                if st.button("🖨️ Print PDF", key="pdf_btn"):
                    md_content = generate_md(st.session_state.cells, st.session_state.paper_name or "Untitled", st.session_state.marks_position)
                    pdf_bytes = generate_pdf_from_markdown(
                        md_content,
                        st.session_state.font_style,
                        st.session_state.font_size,
                        st.session_state.line_spacing,
                        st.session_state.pagination
                    )
                    if pdf_bytes:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=f"{st.session_state.paper_name or 'Untitled'}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Failed to generate PDF. Please check if markdown-pdf is installed: pip install markdown-pdf")

        # Add cell button below each cell
        cell_type = st.selectbox("Cell Type", ["Text Box", "Page Break", "End"], key=f"cell_type_{idx}")
        if st.button("➕ Add Cell Below", key=f"add_cell_{idx}"):
            if cell_type == "Text Box":
                new_cell = Cell(
                    cell_type="textbox",
                    code="",
                    metadata={
                        'question_num': 1,
                        'marks': 0,
                        'center': False,
                        'table_rows': 2,
                        'table_cols': 2
                    }
                )
                st.session_state.cells.insert(idx + 1, new_cell)
                st.session_state.show_markdown_help[f"md_help_{idx+1}"] = False
            elif cell_type == "Page Break":
                new_cell = Cell(cell_type="pagebreak", code="📄 Page Break")
                st.session_state.cells.insert(idx + 1, new_cell)
            elif cell_type == "End":
                new_cell = Cell(cell_type="end", code="🏁 ----End of Paper ----")
                st.session_state.cells.insert(idx + 1, new_cell)
            st.rerun()
