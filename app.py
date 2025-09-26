import tkinter as tk
import re

FUNCTION_WORDS = {
	"the", "a", "an", "is", "to", "and", "or", "but", "of", "in", "on",
	"for", "at", "by", "with", "from", "as", "that", "this", "it", "be",
	"are", "was", "were", "am", "not", "no", "do", "does", "did", "so",
	"if", "then", "than", "too", "very", "can", "will", "just", "you", "i",
    "he", "she", "they", "them", "his", "her", "their", "them", "we", "us", 
    "our", "ours",
	".", ",", "!", "?", ":", ";", "-"
}

def highlight_duplicates(text_widget: tk.Text) -> None:
	# Remove previous highlights
	text_widget.tag_remove("dup_highlight", "1.0", "end")
	# Get current text (exclude trailing newline)
	text = text_widget.get("1.0", "end-1c")
	if not text:
		return
	# Find tokens that include: words possibly interleaved with punctuation (e.g., e.g., i.e., word---word)
	# and standalone punctuation runs (e.g., --- ,,, !!!) so these can also be matched as substrings
	words = re.findall(r"[A-Za-z0-9_']+(?:[.,;:!?\-]+[A-Za-z0-9_']+)*|[.,;:!?\-]+", text, flags=re.IGNORECASE)
	if not words:
		return
	# Work with unique lowercase words excluding stopwords
	unique_words = {w.lower() for w in words if w and w.lower() not in FUNCTION_WORDS}
	# For each word, count overlapping substring occurrences; highlight if count >= 2
	for word in unique_words:
		if not word:
			continue
		pattern = re.compile(rf"(?={re.escape(word)})", flags=re.IGNORECASE)
		matches = [m for m in pattern.finditer(text)]
		if len(matches) < 2:
			continue
		word_len = len(word)
		for m in matches:
			start_char = m.start()
			end_char = start_char + word_len
			start_idx = f"1.0 + {start_char} chars"
			end_idx = f"1.0 + {end_char} chars"
			text_widget.tag_add("dup_highlight", start_idx, end_idx)

def on_text_modified(event: tk.Event) -> None:
	text_widget: tk.Text = event.widget  # type: ignore[assignment]
	highlight_duplicates(text_widget)
	text_widget.edit_modified(False)

def show_context_menu(event: tk.Event, root: tk.Tk, text: tk.Text, context_menu: tk.Menu) -> str:
	text.focus_set()
	# Enable Cut/Copy only when selection exists
	selection_exists = bool(text.tag_ranges("sel"))
	state = "normal" if selection_exists else "disabled"
	context_menu.entryconfigure(0, state=state)  # Cut
	context_menu.entryconfigure(1, state=state)  # Copy
	try:
		_ = root.clipboard_get()
		context_menu.entryconfigure(2, state="normal")  # Paste
	except Exception:
		context_menu.entryconfigure(2, state="disabled")  # Paste
	context_menu.tk_popup(event.x_root, event.y_root)
	context_menu.grab_release()
	return "break"

def main() -> None:
	root = tk.Tk()
	root.title("Highlighter")
	root.geometry("480x360")
	# Force Tk scaling to 1.0 (you can change if desired)
	root.tk.call("tk", "scaling", 1.0)
	# Container with Text and a vertical Scrollbar
	container = tk.Frame(root)
	container.pack(fill="both", expand=True)

	scrollbar = tk.Scrollbar(container, orient="vertical")
	scrollbar.pack(side="right", fill="y")

	text = tk.Text(container, wrap="word", undo=True, autoseparators=True, yscrollcommand=scrollbar.set)
	text.pack(side="left", fill="both", expand=True)
	scrollbar.config(command=text.yview)

	# Configure font
	chosen = "Segoe UI"
	font_pt_size = 18
	font_px_size = int(round(font_pt_size))
	if font_px_size <= 0:
		font_px_size = 16
	text.configure(font=(chosen, -font_px_size))

	# Configure tag
	text.tag_configure("dup_highlight", background="#8cf5b7")
	text.bind("<<Modified>>", on_text_modified)
	text.bind("<Control-z>", lambda e: (text.edit_undo(), "break")[1])

	# Context menu (right-click) for Cut, Copy, Paste
	menu_font = (chosen, 14)
	context_menu = tk.Menu(text, tearoff=0, font=menu_font)
	context_menu.add_command(label="Cut", command=lambda: text.event_generate("<<Cut>>"))
	context_menu.add_command(label="Copy", command=lambda: text.event_generate("<<Copy>>"))
	context_menu.add_command(label="Paste", command=lambda: text.event_generate("<<Paste>>"))
	text.bind("<Button-3>", lambda e: show_context_menu(e, root, text, context_menu))
	highlight_duplicates(text)
	text.edit_modified(False)
	root.mainloop()

if __name__ == "__main__":
	main()
