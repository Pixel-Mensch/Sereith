import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText


class MainWindow:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.root = tk.Tk()
        self.root.title("AI-PnP")
        self.root.geometry("1180x760")
        self.root.minsize(960, 640)

        self.save_name_var = tk.StringVar(value=engine.get_save_name())
        self.status_var = tk.StringVar(value="")
        self.player_var = tk.StringVar(value="")
        self.location_var = tk.StringVar(value="")
        self.hp_var = tk.StringVar(value="")

        self.story_text: ScrolledText | None = None
        self.quest_text: ScrolledText | None = None
        self.action_entry: ttk.Entry | None = None

        self._build_layout()
        self.refresh_view()

    def launch(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        controls = ttk.Frame(self.root, padding=12)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew")
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Save-Name").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.save_name_var, width=24).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(8, 12),
        )
        ttk.Button(controls, text="Neues Spiel", command=self._start_new_game).grid(row=0, column=2, padx=4)
        ttk.Button(controls, text="Speichern", command=self._save_game).grid(row=0, column=3, padx=4)
        ttk.Button(controls, text="Laden", command=self._load_game).grid(row=0, column=4, padx=4)
        ttk.Button(controls, text="Aktualisieren", command=self.refresh_view).grid(row=0, column=5, padx=4)

        story_frame = ttk.Frame(self.root, padding=(12, 0, 8, 12))
        story_frame.grid(row=1, column=0, sticky="nsew")
        story_frame.rowconfigure(0, weight=1)
        story_frame.columnconfigure(0, weight=1)

        self.story_text = ScrolledText(story_frame, wrap="word", font=("Segoe UI", 11), padx=12, pady=12)
        self.story_text.grid(row=0, column=0, sticky="nsew")
        self.story_text.configure(state="disabled")

        action_frame = ttk.Frame(story_frame, padding=(0, 10, 0, 0))
        action_frame.grid(row=1, column=0, sticky="ew")
        action_frame.columnconfigure(0, weight=1)

        self.action_entry = ttk.Entry(action_frame)
        self.action_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.action_entry.bind("<Return>", self._submit_action_event)
        ttk.Button(action_frame, text="Senden", command=self._submit_action).grid(row=0, column=1)

        sidebar = ttk.Frame(self.root, padding=(8, 0, 12, 12))
        sidebar.grid(row=1, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(1, weight=1)

        status_frame = ttk.LabelFrame(sidebar, text="Status", padding=12)
        status_frame.grid(row=0, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)

        ttk.Label(status_frame, textvariable=self.player_var, justify="left").grid(row=0, column=0, sticky="w")
        ttk.Label(status_frame, textvariable=self.hp_var, justify="left").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Label(status_frame, textvariable=self.location_var, justify="left", wraplength=260).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(6, 0),
        )

        quest_frame = ttk.LabelFrame(sidebar, text="Quests", padding=12)
        quest_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        quest_frame.rowconfigure(0, weight=1)
        quest_frame.columnconfigure(0, weight=1)

        self.quest_text = ScrolledText(quest_frame, wrap="word", height=12, font=("Segoe UI", 10), padx=8, pady=8)
        self.quest_text.grid(row=0, column=0, sticky="nsew")
        self.quest_text.configure(state="disabled")

        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w", padding=8)
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

    def refresh_view(self) -> None:
        player = self.engine.get_player_status()
        scene = self.engine.get_current_scene()
        quests = self.engine.get_active_quests()
        recent_log = self.engine.get_recent_log(limit=5)

        self.player_var.set(f"{player['name']} | {player['ancestry']} | {player['role']} | Stufe {player['level']}")
        self.hp_var.set(f"HP: {player['hp_current']} / {player['hp_max']}")
        self.location_var.set(f"Ort: {scene['location_name']}\nSzene: {scene['title']}")
        self.status_var.set(self.engine.get_status_message() or "Bereit.")
        self.save_name_var.set(self.engine.get_save_name())

        self._set_story_text(self._format_story(scene, recent_log))
        self._set_quest_text(self._format_quests(quests))

        if self.action_entry is not None:
            self.action_entry.focus_set()

    def _format_story(self, scene: dict, recent_log: list[dict]) -> str:
        sections = [
            f"{scene['title']}",
            scene["description"],
        ]
        if recent_log:
            sections.append("")
            sections.append("Letzte Zuege")
            for entry in recent_log:
                sections.append(f"> {entry.get('player_action', '').strip()}")
                sections.append(str(entry.get("narration", "")).strip())
        elif self.engine.get_last_narration() and self.engine.get_last_narration() != scene["description"]:
            sections.extend(["", self.engine.get_last_narration()])
        return "\n\n".join(part for part in sections if part)

    def _format_quests(self, quests: list[dict]) -> str:
        if not quests:
            return "Keine aktiven Quests."

        blocks: list[str] = []
        for quest in quests:
            objectives = ", ".join(quest.get("objectives", [])) or "-"
            progress = ", ".join(quest.get("progress_flags", [])) or "-"
            blocks.append(
                f"{quest['title']} [{quest['status']}]\n"
                f"{quest['summary']}\n"
                f"Ziele: {objectives}\n"
                f"Fortschritt: {progress}"
            )
        return "\n\n".join(blocks)

    def _set_story_text(self, content: str) -> None:
        if self.story_text is None:
            return
        self.story_text.configure(state="normal")
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.END, content.strip())
        self.story_text.configure(state="disabled")
        self.story_text.see(tk.END)

    def _set_quest_text(self, content: str) -> None:
        if self.quest_text is None:
            return
        self.quest_text.configure(state="normal")
        self.quest_text.delete("1.0", tk.END)
        self.quest_text.insert(tk.END, content.strip())
        self.quest_text.configure(state="disabled")

    def _requested_save_name(self) -> str | None:
        save_name = self.save_name_var.get().strip()
        return save_name or None

    def _submit_action_event(self, _event) -> None:
        self._submit_action()

    def _submit_action(self) -> None:
        if self.action_entry is None:
            return
        action = self.action_entry.get().strip()
        result = self.engine.process_player_action(action)
        if not result["ok"]:
            self.status_var.set(result["message"])
            return
        self.action_entry.delete(0, tk.END)
        self.refresh_view()
        status = result["status_message"]
        if result.get("system_note"):
            status = f"{status} | {result['system_note']}"
        self.status_var.set(status)

    def _start_new_game(self) -> None:
        result = self.engine.new_game(self._requested_save_name())
        self.refresh_view()
        self.status_var.set(result["message"])

    def _save_game(self) -> None:
        result = self.engine.save_game(self._requested_save_name())
        if result["ok"]:
            self.refresh_view()
            messagebox.showinfo("AI-PnP", result["message"])
            return
        self.status_var.set(result["message"])
        messagebox.showerror("AI-PnP", result["message"])

    def _load_game(self) -> None:
        result = self.engine.load_game(self._requested_save_name())
        if result["ok"]:
            self.refresh_view()
            messagebox.showinfo("AI-PnP", result["message"])
            return
        self.status_var.set(result["message"])
        messagebox.showerror("AI-PnP", result["message"])
