# utils.py
# helper functions (placeholder) - add sanitization, filename cleaning, hashing for caching etc.

def sanitize_filename(name: str) -> str:
    return ''.join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()