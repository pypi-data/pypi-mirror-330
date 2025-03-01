import pkg_resources
import webbrowser
import os

def open_attention_paper():
    """Opens the 'Attention Is All You Need' paper either locally or online."""
    
    # Try to find the local file
    try:
        paper_path = pkg_resources.resource_filename("attention_paper", "data/attentionalluneed.pdf")
        if os.path.exists(paper_path):
            webbrowser.open(f"file://{paper_path}")
            return
    except Exception:
        pass  # If there's any issue, fall back to the online version

    # Open the official NeurIPS version
    neurips_link = "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf"
    print(f"Local PDF not found. Opening official NeurIPS version: {neurips_link}")
    webbrowser.open(neurips_link)
