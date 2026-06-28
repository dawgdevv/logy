class State:
    def __init__(self) -> None:
        self.screen = "welcome"
        self.menu_idx = 0
        self.input_prompt = ""
        self.input_value = ""
        self.input_field = ""
        self.field_idx = 0
        self.collected: dict = {}
        self.status_msg = ""
        self.status_style = "green"
        self.project_idx = 0
        self.entries: list = []
        self.entry_idx = 0
        self.entry_scroll = 0
        self.detail_scroll = 0
        self.selected_entry: dict | None = None
        self.entry_type = ""  # "daily" | "hard_problem" | "project"
