import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText


class MainWindow:
    APP_BG = "#e7e0d3"
    PANEL_BG = "#f9f5ec"
    STORY_BG = "#fcf8ef"
    ACCENT = "#5d4426"
    TEXT = "#1e1812"
    MUTED = "#6d655a"

    def __init__(self, engine) -> None:
        self.engine = engine
        self.root = tk.Tk()
        self.root.title("AI-PnP - Sereith")
        self.root.geometry("1360x860")
        self.root.minsize(1120, 700)

        self.save_name_var = tk.StringVar(value=engine.get_save_name())
        self.status_var = tk.StringVar(value="")
        self.subtitle_var = tk.StringVar(value="")
        self.player_name_var = tk.StringVar(value="")
        self.player_role_var = tk.StringVar(value="")
        self.hp_var = tk.StringVar(value="")
        self.location_var = tk.StringVar(value="")
        self.chapter_var = tk.StringVar(value="")
        self.context_var = tk.StringVar(value="")

        self.story_text: ScrolledText | None = None
        self.quest_text: ScrolledText | None = None
        self.inventory_text: ScrolledText | None = None
        self.npc_text: ScrolledText | None = None
        self.log_text: ScrolledText | None = None
        self.action_entry: ttk.Entry | None = None
        self.action_button: ttk.Button | None = None
        self.save_button: ttk.Button | None = None
        self.load_button: ttk.Button | None = None
        self.new_game_button: ttk.Button | None = None
        self.refresh_button: ttk.Button | None = None

        self._configure_style()
        self._build_layout()
        self.refresh_view()

    def launch(self) -> None:
        self.root.mainloop()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.configure(bg=self.APP_BG)
        style.configure("Root.TFrame", background=self.APP_BG)
        style.configure("Header.TFrame", background=self.APP_BG)
        style.configure(
            "Title.TLabel",
            background=self.APP_BG,
            foreground=self.ACCENT,
            font=("Segoe UI Semibold", 20),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.APP_BG,
            foreground=self.MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Card.TLabelframe",
            background=self.PANEL_BG,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.PANEL_BG,
            foreground=self.ACCENT,
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "CardLabel.TLabel",
            background=self.PANEL_BG,
            foreground=self.TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "MutedCard.TLabel",
            background=self.PANEL_BG,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Status.TLabel",
            background="#d9d0c1",
            foreground=self.TEXT,
            padding=8,
            font=("Segoe UI", 9),
        )
        style.configure("Action.TButton", padding=(12, 8))
        style.configure("Small.TButton", padding=(10, 6))

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, style="Header.TFrame", padding=(18, 16, 18, 10))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)

        title_block = ttk.Frame(header, style="Header.TFrame")
        title_block.grid(row=0, column=0, sticky="w")
        ttk.Label(title_block, text="AI-PnP", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(title_block, textvariable=self.subtitle_var, style="Subtitle.TLabel").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0),
        )

        controls = ttk.Frame(header, style="Header.TFrame")
        controls.grid(row=0, column=1, sticky="e")
        ttk.Label(controls, text="Save-Name", style="Subtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.save_name_var, width=18).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(8, 12),
        )
        self.new_game_button = ttk.Button(
            controls,
            text="Neues Spiel",
            style="Small.TButton",
            command=self._start_new_game,
        )
        self.new_game_button.grid(row=0, column=2, padx=4)
        self.save_button = ttk.Button(
            controls,
            text="Speichern",
            style="Small.TButton",
            command=self._save_game,
        )
        self.save_button.grid(row=0, column=3, padx=4)
        self.load_button = ttk.Button(
            controls,
            text="Laden",
            style="Small.TButton",
            command=self._load_game,
        )
        self.load_button.grid(row=0, column=4, padx=4)
        self.refresh_button = ttk.Button(
            controls,
            text="Aktualisieren",
            style="Small.TButton",
            command=self.refresh_view,
        )
        self.refresh_button.grid(row=0, column=5, padx=4)

        story_frame = ttk.LabelFrame(
            self.root,
            text="Erzaehlung",
            style="Card.TLabelframe",
            padding=(14, 12, 14, 14),
        )
        story_frame.grid(row=1, column=0, sticky="nsew", padx=(18, 8), pady=(0, 14))
        story_frame.rowconfigure(0, weight=1)
        story_frame.columnconfigure(0, weight=1)

        self.story_text = ScrolledText(
            story_frame,
            wrap="word",
            font=("Segoe UI", 12),
            padx=18,
            pady=16,
            relief="flat",
            borderwidth=0,
            background=self.STORY_BG,
            foreground=self.TEXT,
            insertbackground=self.TEXT,
        )
        self.story_text.grid(row=0, column=0, sticky="nsew")
        self.story_text.configure(state="disabled")
        self._configure_story_tags()

        ttk.Label(
            story_frame,
            textvariable=self.context_var,
            style="MutedCard.TLabel",
            justify="left",
            wraplength=720,
        ).grid(row=1, column=0, sticky="ew", pady=(10, 0))

        action_frame = ttk.Frame(story_frame, style="Root.TFrame", padding=(0, 12, 0, 0))
        action_frame.grid(row=2, column=0, sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        ttk.Label(action_frame, text="Was tust du?", style="Subtitle.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6),
        )
        self.action_entry = ttk.Entry(action_frame, font=("Segoe UI", 11))
        self.action_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.action_entry.bind("<Return>", self._submit_action_event)
        self.action_button = ttk.Button(
            action_frame,
            text="Senden",
            style="Action.TButton",
            command=self._submit_action,
        )
        self.action_button.grid(row=1, column=1, sticky="e")

        sidebar = ttk.Frame(self.root, style="Root.TFrame", padding=(8, 0, 18, 14))
        sidebar.grid(row=1, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(1, weight=2)
        sidebar.rowconfigure(2, weight=1)
        sidebar.rowconfigure(3, weight=2)

        status_frame = ttk.LabelFrame(sidebar, text="Charakter", style="Card.TLabelframe", padding=12)
        status_frame.grid(row=0, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)
        ttk.Label(status_frame, textvariable=self.player_name_var, style="CardLabel.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
        )
        ttk.Label(status_frame, textvariable=self.player_role_var, style="MutedCard.TLabel").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0),
        )
        ttk.Label(status_frame, textvariable=self.hp_var, style="CardLabel.TLabel").grid(
            row=2,
            column=0,
            sticky="w",
            pady=(8, 0),
        )
        ttk.Label(status_frame, textvariable=self.location_var, style="CardLabel.TLabel", wraplength=360).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(8, 0),
        )
        ttk.Label(status_frame, textvariable=self.chapter_var, style="MutedCard.TLabel", wraplength=360).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        quest_frame = ttk.LabelFrame(sidebar, text="Quests", style="Card.TLabelframe", padding=10)
        quest_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        quest_frame.rowconfigure(0, weight=1)
        quest_frame.columnconfigure(0, weight=1)
        self.quest_text = self._build_readonly_text(quest_frame, font=("Segoe UI", 10))
        self.quest_text.grid(row=0, column=0, sticky="nsew")

        lower_info = ttk.Frame(sidebar, style="Root.TFrame")
        lower_info.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        lower_info.columnconfigure(0, weight=1)
        lower_info.columnconfigure(1, weight=1)
        lower_info.rowconfigure(0, weight=1)

        inventory_frame = ttk.LabelFrame(lower_info, text="Inventar", style="Card.TLabelframe", padding=10)
        inventory_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        inventory_frame.rowconfigure(0, weight=1)
        inventory_frame.columnconfigure(0, weight=1)
        self.inventory_text = self._build_readonly_text(inventory_frame, font=("Segoe UI", 10))
        self.inventory_text.grid(row=0, column=0, sticky="nsew")

        npc_frame = ttk.LabelFrame(lower_info, text="Interaktionen", style="Card.TLabelframe", padding=10)
        npc_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        npc_frame.rowconfigure(0, weight=1)
        npc_frame.columnconfigure(0, weight=1)
        self.npc_text = self._build_readonly_text(npc_frame, font=("Segoe UI", 10))
        self.npc_text.grid(row=0, column=0, sticky="nsew")

        log_frame = ttk.LabelFrame(sidebar, text="Letzte Aktionen", style="Card.TLabelframe", padding=10)
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = self._build_readonly_text(log_frame, font=("Segoe UI", 10))
        self.log_text.grid(row=0, column=0, sticky="nsew")

        status_bar = ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel", anchor="w")
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

    def _build_readonly_text(self, parent, *, font: tuple[str, int]) -> ScrolledText:
        widget = ScrolledText(
            parent,
            wrap="word",
            height=8,
            font=font,
            padx=10,
            pady=10,
            relief="flat",
            borderwidth=0,
            background=self.PANEL_BG,
            foreground=self.TEXT,
            insertbackground=self.TEXT,
        )
        widget.configure(state="disabled")
        return widget

    def _configure_story_tags(self) -> None:
        if self.story_text is None:
            return
        self.story_text.tag_configure("story_title", font=("Segoe UI Semibold", 20), foreground=self.ACCENT)
        self.story_text.tag_configure("story_meta", font=("Segoe UI", 10), foreground=self.MUTED, spacing3=10)
        self.story_text.tag_configure("story_section", font=("Segoe UI Semibold", 11), foreground=self.ACCENT)
        self.story_text.tag_configure(
            "story_body",
            font=("Segoe UI", 12),
            foreground=self.TEXT,
            lmargin1=4,
            lmargin2=4,
            spacing3=12,
        )

    def refresh_view(self) -> None:
        player = self.engine.get_player_status()
        world = self.engine.get_world_status()
        scene = self.engine.get_current_scene()
        quests = self.engine.get_active_quests()
        inventory = self.engine.get_inventory()
        visible_npcs = self.engine.get_visible_npcs()
        recent_log = self.engine.get_recent_log(limit=8)

        self.subtitle_var.set(f"{world['chapter']} | {world['time_of_day']} | Save: {self.engine.get_save_name()}")
        self.player_name_var.set(player["name"])
        self.player_role_var.set(f"{player['ancestry']} | {player['role']} | Stufe {player['level']}")
        self.hp_var.set(f"HP: {player['hp_current']} / {player['hp_max']}")
        self.location_var.set(f"Ort: {scene['location_name']}\nSzene: {scene['title']}")
        self.chapter_var.set(f"Kapitel: {world['chapter']}\nZeit: {world['time_of_day']}")
        self.status_var.set(self.engine.get_status_message() or "Bereit.")
        self.save_name_var.set(self.engine.get_save_name())
        self.context_var.set(self._format_scene_context(scene, visible_npcs))

        self._set_story_text(scene, world)
        self._set_readonly_text(self.quest_text, self._format_quests(quests))
        self._set_readonly_text(self.inventory_text, self._format_inventory(inventory))
        self._set_readonly_text(self.npc_text, self._format_visible_npcs(visible_npcs))
        self._set_readonly_text(self.log_text, self._format_recent_log(recent_log))

        if self.action_entry is not None:
            self.action_entry.focus_set()

    def _format_scene_context(self, scene: dict, visible_npcs: list[dict]) -> str:
        objects = ", ".join(scene.get("scene_objects", [])) or "nichts Auffaelliges"
        npc_names = ", ".join(npc["name"] for npc in visible_npcs) or "niemand direkt sichtbar"
        return f"Sichtbar: {objects} | Praesente Figuren: {npc_names}"

    def _format_quests(self, quests: list[dict]) -> str:
        if not quests:
            return "Keine aktiven Quests."

        blocks: list[str] = []
        for quest in quests:
            objectives = ", ".join(self._humanize_token(item) for item in quest.get("objectives", [])) or "-"
            progress = ", ".join(self._humanize_token(item) for item in quest.get("progress_flags", [])) or "-"
            blocks.append(
                f"{quest['title']} [{quest['status']}]\n"
                f"{quest['summary']}\n"
                f"Ziele: {objectives}\n"
                f"Fortschritt: {progress}"
            )
        return "\n\n".join(blocks)

    def _format_inventory(self, inventory: list[str]) -> str:
        if not inventory:
            return "Noch kein Inventar eingetragen."
        return "\n".join(f"- {item}" for item in inventory)

    def _format_visible_npcs(self, visible_npcs: list[dict]) -> str:
        if not visible_npcs:
            return "Niemand direkt sichtbar.\n\nSpuren, Hinweise oder spaetere NPC-Details koennen hier auftauchen."

        blocks: list[str] = []
        for npc in visible_npcs:
            parts = [
                f"{npc['name']} ({npc['role']})",
                npc.get("summary", ""),
                f"Haltung: {self._humanize_token(npc.get('attitude', 'neutral'))}",
            ]
            if npc.get("last_topic"):
                parts.append(f"Letztes Thema: {self._humanize_token(npc['last_topic'])}")
            blocks.append("\n".join(part for part in parts if part))
        return "\n\n".join(blocks)

    def _format_recent_log(self, recent_log: list[dict]) -> str:
        if not recent_log:
            return "Noch keine Aktionen."

        blocks: list[str] = []
        for entry in reversed(recent_log[-6:]):
            interpretation = entry.get("interpretation", {})
            intent = self._humanize_token(interpretation.get("intent", "")) or "Aktion"
            subject = self._humanize_token(interpretation.get("subject", ""))
            header = intent if not subject else f"{intent} - {subject}"
            blocks.append(f"{header}\n{entry.get('player_action', '').strip()}")
        return "\n\n".join(blocks)

    def _humanize_token(self, value: str) -> str:
        text = (value or "").replace("_", " ").strip()
        if not text:
            return ""
        return text[:1].upper() + text[1:]

    def _set_story_text(self, scene: dict, world: dict) -> None:
        if self.story_text is None:
            return

        latest_narration = self.engine.get_last_narration()
        self.story_text.configure(state="normal")
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.END, f"{scene['title']}\n", "story_title")
        self.story_text.insert(
            tk.END,
            f"{scene['location_name']} | {world['chapter']} | {world['time_of_day']}\n\n",
            "story_meta",
        )
        if latest_narration and latest_narration != scene["description"]:
            self.story_text.insert(tk.END, "Neueste Erzaehlung\n", "story_section")
            self.story_text.insert(tk.END, f"{latest_narration}\n\n", "story_body")
            self.story_text.insert(tk.END, "Szenerahmen\n", "story_section")
        else:
            self.story_text.insert(tk.END, "Aktuelle Szene\n", "story_section")
        self.story_text.insert(tk.END, f"{scene['description']}\n", "story_body")
        self.story_text.configure(state="disabled")
        self.story_text.see("1.0")

    def _set_readonly_text(self, widget: ScrolledText | None, content: str) -> None:
        if widget is None:
            return
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content.strip())
        widget.configure(state="disabled")

    def _requested_save_name(self) -> str | None:
        save_name = self.save_name_var.get().strip()
        return save_name or None

    def _submit_action_event(self, _event) -> None:
        self._submit_action()

    def _set_busy(self, busy: bool, message: str | None = None) -> None:
        state = ["disabled"] if busy else ["!disabled"]
        for widget in (
            self.action_entry,
            self.action_button,
            self.new_game_button,
            self.save_button,
            self.load_button,
            self.refresh_button,
        ):
            if widget is not None:
                widget.state(state)
        self.root.configure(cursor="watch" if busy else "")
        if message:
            self.status_var.set(message)
        self.root.update_idletasks()

    def _submit_action(self) -> None:
        if self.action_entry is None:
            return

        action = self.action_entry.get().strip()
        if not action:
            self.status_var.set("Leere Eingabe ignoriert.")
            self.action_entry.focus_set()
            return

        self._set_busy(True, "Erzaehler antwortet...")
        try:
            result = self.engine.process_player_action(action)
            if not result["ok"]:
                self.status_var.set(result["message"])
                return
            self.action_entry.delete(0, tk.END)
            self.refresh_view()
            status = f"{result['status_message']} | Erzaehler: {result['provider']}"
            if result.get("system_note"):
                status = f"{status} | {result['system_note']}"
            self.status_var.set(status)
        except Exception as exc:
            self.status_var.set(f"Aktion konnte nicht verarbeitet werden: {exc}")
            messagebox.showerror("AI-PnP", f"Aktion konnte nicht verarbeitet werden:\n{exc}")
        finally:
            self._set_busy(False)

    def _start_new_game(self) -> None:
        self._set_busy(True, "Neue Sitzung wird vorbereitet...")
        try:
            result = self.engine.new_game(self._requested_save_name())
            self.refresh_view()
            self.status_var.set(result["message"])
        finally:
            self._set_busy(False)

    def _save_game(self) -> None:
        self._set_busy(True, "Speichere Spielstand...")
        try:
            result = self.engine.save_game(self._requested_save_name())
            if result["ok"]:
                self.refresh_view()
                self.status_var.set(result["message"])
                return
            self.status_var.set(result["message"])
            messagebox.showerror("AI-PnP", result["message"])
        finally:
            self._set_busy(False)

    def _load_game(self) -> None:
        self._set_busy(True, "Lade Spielstand...")
        try:
            result = self.engine.load_game(self._requested_save_name())
            if result["ok"]:
                self.refresh_view()
                self.status_var.set(result["message"])
                return
            self.status_var.set(result["message"])
            messagebox.showerror("AI-PnP", result["message"])
        finally:
            self._set_busy(False)
