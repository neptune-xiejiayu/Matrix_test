import os


def save_html_report(src_path, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(src_path):
        dest = os.path.join(dest_dir, os.path.basename(src_path))
        with open(src_path, 'rb') as rf, open(dest, 'wb') as wf:
            wf.write(rf.read())
        return dest
    return None
