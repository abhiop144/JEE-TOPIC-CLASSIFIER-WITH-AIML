import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import random

class JEEGeneratorApp:
    """
    Main Application class for the JEE Assistant Pro.
    Handles UI initialization, randomized paper generation, and data export.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("JEE Assistant Pro")
        self.root.geometry("1100x850")
        self.root.configure(bg="#f1f5f9") # Light Slate Background for a modern look
        
        # --- Color Palette (Modern Slate/Indigo Theme) ---
        self.colors = {
            "primary": "#1e293b",    # Headers
            "accent": "#4f46e5",     #  actions
            "bg": "#f1f5f9",         #  background
            "card": "#d3d3d3",       #  for containers like boxes
            "text": "#334155",       #  Main body text
            "subtext": "#64748b",    #  text labels
            "physics": "#7c3aed",    #  Physics 
            "chemistry": "#059669",  # Emerald - Chemistry 
            "maths": "#2563eb",      # Blue - Maths 
            "easy": "#10b981",       # Green - Positive 
            "medium": "#f59e0b",     # Amber - Warning 
            "hard": "#ef4444",       # Red - Critical 
            "border": "#e2e8f0"      # Borders
        }
        
        # --- Data Setup for Classification, To simplify the project i have kept the data set in a dictionary ---
        # Mapping subjects to their respective JEE Main topics
        self.topics_map = {
            "Physics": ["Mechanics", "Electrodynamics", "Optics", "Modern Physics", "Thermodynamics", "Properties of Matter"],
            "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Atomic Structure", "Chemical Bonding", "Equilibrium"],
            "Maths": ["Calculus", "Algebra", "Coordinate Geometry", "Vectors & 3D", "Trigonometry", "Probability"]
        }
        
        # A pool of strategies to be randomly selected after generation for Extra help and guidance, optional to read
        self.strategy_pool = [
            "Focus on high-weightage topics like Mechanics and Calculus first.",
            "Solve Medium difficulty questions to build confidence before tackling Hard ones.",
            "Chemistry Inorganic needs rote memorization; revise daily for 30 minutes.",
            "Use elimination techniques for Multiple Choice Questions in Physics.",
            "Avoid negative marking by only attempting questions you are 80% sure about.",
            "Mastering integration is key to scoring high in the Mathematics section.",
            "Practice previous year questions (PYQs) specifically for Modern Physics.",
            "Allocate 45 mins for Chemistry, 60 mins for Physics, and 75 mins for Maths.",
            "Maintain a formula sheet for quick revision of Thermodynamics.",
            "Coordinate Geometry can be solved faster using visualization and sketches.",
            "If a question takes more than 3 minutes, mark it for review and move on.",
            "Focus on NCERT examples for Inorganic and Organic Chemistry basics.",
            "Vector and 3D Geometry are scoring; don't skip the scalar triple product.",
            "For Hard Physics problems, start by drawing a free-body diagram.",
            "In Physical Chemistry, pay extra attention to unit conversions.",
            "Calculus requires consistent practice; solve at least 15 problems daily.",
            "Review your mocks to identify if your errors are conceptual or calculation-based.",
            "Time management is the difference between a 95 and a 99 percentile.",
            "Keep a cool head; the first 5 questions don't define the whole paper.",
            "Algebraic manipulations are often the bottleneck in complex Math problems."
        ]

        self.generated_paper = None  # Holds the current DataFrame after generation
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure custom styles for Tkinter/TTK widgets."""
        self.style = ttk.Style()
        self.style.theme_use("clam") # 'clam' allows for more flexible custom coloring
        
        # Table Styling
        self.style.configure("Treeview", 
                             background=self.colors["card"], 
                             foreground=self.colors["text"], 
                             rowheight=32, 
                             fieldbackground=self.colors["card"], 
                             font=("Segoe UI", 10))
        self.style.map("Treeview", background=[('selected', self.colors["accent"])])
        self.style.configure("Treeview.Heading", 
                             font=("Segoe UI", 11, "bold"), 
                             background=self.colors["primary"], 
                             foreground="white")

        # Custom Action Button Styling
        self.style.configure("Action.TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             padding=10, 
                             background=self.colors["accent"], 
                             foreground="white")
        self.style.map("Action.TButton", background=[('active', '#4338ca')]) # Darker indigo on hover

    def create_widgets(self):
        """Main UI layout construction."""
        # --- Top Header Section ---
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="🎯 JEE MAIN PAPER ARCHITECT", 
                 font=("Segoe UI", 20, "bold"), 
                 bg=self.colors["primary"], 
                 foreground="white", 
                 padx=30).pack(side="left", pady=20)

        # --- Tabbed Interface ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Tab 1: Generation UI
        self.tab_gen = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_gen, text=" 📝 Generator & View ")

        # Tab 2: Strategy Information Hub
        self.tab_strat = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_strat, text=" 💡 Strategy Hub ")

        self.setup_gen_tab()
        self.setup_strat_tab()

    def setup_gen_tab(self):
        """Layout for the Paper Generation tab."""
        # Container for the two top 'cards' (Controls and Summary)
        top_container = tk.Frame(self.tab_gen, bg=self.colors["bg"], pady=15)
        top_container.pack(fill="x", padx=20)

        # Card 1: Blueprint Controls
        # Note: Fixed width is set here and forced with pack_propagate(False) to fix geometry errors
        gen_card = tk.Frame(top_container, bg=self.colors["card"], 
                           highlightbackground=self.colors["border"], 
                           highlightthickness=1, padx=20, pady=15, width=350)
        gen_card.pack(side="left", fill="both", expand=False)
        gen_card.pack_propagate(False) 
        
        tk.Label(gen_card, text="Blueprint Controls", font=("Segoe UI", 12, "bold"), 
                 bg=self.colors["card"], fg=self.colors["primary"]).pack(anchor="w")
        tk.Label(gen_card, text="Configure and export your 75-question mock paper.", 
                 font=("Segoe UI", 9), bg=self.colors["card"], fg=self.colors["subtext"]).pack(anchor="w", pady=(2, 10))
        
        btn_box = tk.Frame(gen_card, bg=self.colors["card"])
        btn_box.pack(fill="x", pady=5)
        
        ttk.Button(btn_box, text="🚀 Generate", style="Action.TButton", 
                   command=self.run_generation).pack(side="left", padx=(0, 10))
        ttk.Button(btn_box, text="💾 Export CSV", command=self.save_to_csv).pack(side="left")

        # Card 2: Quick Summary (Metrics Display)
        self.stats_card = tk.Frame(top_container, bg=self.colors["card"], 
                                  highlightbackground=self.colors["border"], 
                                  highlightthickness=1, padx=20, pady=15)
        self.stats_card.pack(side="left", fill="both", expand=True, padx=(15, 0))
        
        tk.Label(self.stats_card, text="Quick Summary", font=("Segoe UI", 12, "bold"), 
                 bg=self.colors["card"], fg=self.colors["primary"]).pack(anchor="w")
        
        # Grid layout for the difficulty counters
        self.stats_grid = tk.Frame(self.stats_card, bg=self.colors["card"])
        self.stats_grid.pack(fill="x", pady=(10, 0))

        self.metric_labels = {}
        metrics = [("Easy", self.colors["easy"]), ("Medium", self.colors["medium"]), ("Hard", self.colors["hard"])]
        
        for i, (name, color) in enumerate(metrics):
            f = tk.Frame(self.stats_grid, bg=self.colors["card"])
            f.grid(row=0, column=i, sticky="nsew", padx=10)
            self.stats_grid.columnconfigure(i, weight=1) # Equally distribute space
            
            tk.Label(f, text=name, font=("Segoe UI", 9, "bold"), 
                     bg=self.colors["card"], fg=self.colors["subtext"]).pack()
            lbl = tk.Label(f, text="--", font=("Segoe UI", 16, "bold"), 
                           bg=self.colors["card"], fg=color)
            lbl.pack()
            self.metric_labels[name] = lbl

        # Placeholder label for skew distribution info
        self.dist_lbl = tk.Label(self.stats_card, text="Waiting for generation...", 
                                 font=("Segoe UI", 9, "italic"), 
                                 bg=self.colors["card"], fg=self.colors["subtext"])
        self.dist_lbl.pack(anchor="w", pady=(10, 0))

        # Bottom Section: The Results Table
        table_frame = tk.Frame(self.tab_gen, bg=self.colors["card"], 
                               highlightbackground=self.colors["border"], 
                               highlightthickness=1)
        table_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        cols = ("Q#", "Subject", "Topic", "Difficulty")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col)
            width = 80 if col == "Q#" else 200
            self.tree.column(col, width=width, anchor="center")
        
        # Table Scrollbar
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Color-coded tags to style rows by subject
        self.tree.tag_configure("physics_row", foreground=self.colors["physics"])
        self.tree.tag_configure("chemistry_row", foreground=self.colors["chemistry"])
        self.tree.tag_configure("maths_row", foreground=self.colors["maths"])

    def setup_strat_tab(self):
        """Layout for the Strategy Hub tab."""
        self.strat_container = tk.Frame(self.tab_strat, bg=self.colors["bg"], padx=30, pady=20)
        self.strat_container.pack(expand=True, fill="both")

        # Initial 'Locked' state message
        self.strat_header = tk.Label(self.strat_container, 
                                     text="Generate a paper to unlock custom strategies!", 
                                     font=("Segoe UI", 14, "italic"), 
                                     bg=self.colors["bg"], fg="#94a3b8")
        self.strat_header.pack(pady=50)

    def update_strategy_hub(self):
        """Dynamic content generation for the Strategy Hub after paper creation."""
        if self.generated_paper is None: return
        
        # Clear existing tab content
        for widget in self.strat_container.winfo_children(): widget.destroy()

        tk.Label(self.strat_container, text="🎯 Personalized Preparation Strategy", 
                 font=("Segoe UI", 18, "bold"), bg=self.colors["bg"], 
                 fg=self.colors["primary"]).pack(anchor="w", pady=(0, 10))
        
        # Count 'Hard' questions for the difficulty alert
        hard_count = (self.generated_paper['Difficulty'] == 'Hard').sum()
        alert_text = "⚠️ High Complexity Detected!" if hard_count > 28 else "✅ Balanced Paper Analysis"
        alert_color = self.colors["hard"] if hard_count > 28 else self.colors["chemistry"]
        
        tk.Label(self.strat_container, text=alert_text, 
                 font=("Segoe UI", 12, "bold"), bg=self.colors["bg"], fg=alert_color).pack(anchor="w")

        # Create a scrollable area for the strategy cards
        canvas = tk.Canvas(self.strat_container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.strat_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg"])
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Select 6 random tips from the pool
        selected_strats = random.sample(self.strategy_pool, 6)
        for i, strat in enumerate(selected_strats):
            card = tk.Frame(scrollable_frame, bg=self.colors["card"], padx=15, pady=15, 
                            highlightbackground=self.colors["border"], highlightthickness=1)
            card.pack(fill="x", pady=5)
            tk.Label(card, text=f"Tip #{i+1}", font=("Segoe UI", 10, "bold"), 
                     bg=self.colors["card"], fg=self.colors["accent"]).pack(anchor="w")
            tk.Label(card, text=strat, font=("Segoe UI", 11), bg=self.colors["card"], 
                     fg=self.colors["text"], wraplength=850, justify="left").pack(anchor="w", pady=(5, 0))

        canvas.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar.pack(side="right", fill="y")

    def run_generation(self):
        """Main logic for randomized question/difficulty selection."""
        paper_data = []
        q_id = 1
        
        # Skewed difficulty weights: generated randomly per paper
        w_easy = random.uniform(0.2, 0.4)
        w_hard = random.uniform(0.2, 0.4)
        w_med = 1.0 - (w_easy + w_hard)
        
        diff_options = ["Easy", "Medium", "Hard"]
        diff_weights = [w_easy, w_med, w_hard]
        
        for subject in ["Physics", "Chemistry", "Maths"]:
            subject_topics = self.topics_map[subject]
            for _ in range(25): # JEE standard: 25 questions per subject
                paper_data.append({
                    "Q#": q_id, 
                    "Subject": subject,
                    "Topic": random.choice(subject_topics),
                    "Difficulty": random.choices(diff_options, weights=diff_weights, k=1)[0]
                })
                q_id += 1
        
        # Store in DataFrame for easy manipulation
        self.generated_paper = pd.DataFrame(paper_data)
        
        # Update UI Table (Treeview)
        for item in self.tree.get_children(): self.tree.delete(item)
        for _, row in self.generated_paper.iterrows():
            # Apply row styling based on subject
            tag = f"{row['Subject'].lower()}_row"
            self.tree.insert("", "end", 
                             values=(row["Q#"], row["Subject"], row["Topic"], row["Difficulty"]), 
                             tags=(tag,))
        
        # Update Dashboard Metric Labels
        easy_count = (self.generated_paper['Difficulty'] == 'Easy').sum()
        med_count = (self.generated_paper['Difficulty'] == 'Medium').sum()
        hard_count = (self.generated_paper['Difficulty'] == 'Hard').sum()
        
        self.metric_labels["Easy"].config(text=str(easy_count))
        self.metric_labels["Medium"].config(text=str(med_count))
        self.metric_labels["Hard"].config(text=str(hard_count))
        
        # Display the distribution ratio for transparency
        self.dist_lbl.config(text=f"Skew Ratio: Easy {w_easy:.0%} | Med {w_med:.0%} | Hard {w_hard:.0%}", 
                             font=("Segoe UI", 9, "bold"), fg=self.colors["primary"])
        
        # Populate the Strategy Hub based on new data
        self.update_strategy_hub()
        messagebox.showinfo("Success", "75-Question blueprint generated!")

    def save_to_csv(self):
        """Standard file saving logic for exporting the blueprint."""
        if self.generated_paper is None:
            messagebox.showwarning("Warning", "Please generate a paper first.")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv")], 
                                                 initialfile="JEE_Mock_Blueprint.csv")
        if file_path:
            self.generated_paper.to_csv(file_path, index=False)
            messagebox.showinfo("Saved", "Blueprint exported successfully!")

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()
    app = JEEGeneratorApp(root)
    root.mainloop()