def bind_hotkeys(root, operations, text_widget, table):
    root.bind_all("<Alt-Key-1>", lambda event: operations.parse_file(text_widget, table))
    root.bind_all("<Alt-Key-2>", lambda event: operations.add_parse_file(text_widget, table))
    root.bind_all("<Alt-Key-3>", lambda event: operations.parse_folder(text_widget, table))
    root.bind_all("<Alt-Key-4>", lambda event: operations.add_parse_folder(text_widget, table))
    root.bind_all("<Delete>", lambda event: operations.clear(text_widget, table))
