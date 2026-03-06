# Project Quadrant Chart Generator

Interactive bubble chart showing Project Health vs Delivery Performance.

## For End Users

### Quick Start
1. Place `Quadrant.exe` in the same folder as your Excel file (`.xlsx`)
2. Double-click `Quadrant.exe`
3. The chart opens automatically in your default browser

### Output Files
- `quadrant.html` - Interactive chart (open in any browser)
- `quadrant_output.csv` - Data table for audit/analysis

### Understanding the Chart

**Axes:**
- **X-axis (Delivery Performance)**: Average of Planning, Budget, Scope KPIs
- **Y-axis (Project Health/Risk)**: Average of Launch Indicator, Risk, Change KPIs

**Bubble Colors:**
- 🟢 **Green**: Overall score ≥ 2.5 (healthy project)
- 🟠 **Orange**: Score between 1.75 and 2.5 (attention needed)
- 🔴 **Red**: Score ≤ 1.75 (at risk)

**Bubble Size:** Larger = worse overall score

**Quadrants:**
- **Top-Right (On Track)**: Good delivery AND good health
- **Top-Left (Delivery Issues)**: Health OK but delivery struggling
- **Bottom-Right (Health Concerns)**: Delivery OK but health issues
- **Bottom-Left (Critical)**: Both delivery and health are poor

**Hover** over any bubble to see detailed KPI breakdown.

---

## For IT / Developers

### Prerequisites
- Python 3.8+ 
- pip (Python package manager)

### Installation

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install pandas openpyxl plotly pyinstaller
```

### Running from Source

```bash
python quadrant.py
```

### Building the Executable

```bash
# Single-file executable (recommended)
pyinstaller --onefile --name Quadrant quadrant.py

# The exe will be in the 'dist' folder
# Copy Quadrant.exe to the folder with your Excel files
```

### Alternative Build (faster startup)

```bash
# One-folder build (faster startup, multiple files)
pyinstaller --name Quadrant quadrant.py

# Creates dist/Quadrant/ folder with all files
```

### Configuration

Edit `quadrant_config.json` to customize:

```json
{
  "excel_filename": null,  // null = use newest .xlsx in folder
  "sheet_name": "Roadmap",
  "views": [
    {
      "name": "KPI Quadrant",
      "enabled": true,
      "project_name_column": "E",
      "phase_column": "T",
      "phase_value": "5 Réalisation",
      "kpi_columns": {
        "CS": "Launch Indicator",
        "DA": "Planning",
        ...
      },
      "x_axis": {
        "label": "Delivery Performance",
        "kpis": ["DA", "DD", "DF"]
      },
      "y_axis": {
        "label": "Project Health / Risk",
        "kpis": ["CS", "DH", "DJ"]
      },
      "scoring_map": { "J": 3, "K": 2, "L": 1 },
      "default_score": 1
    }
  ]
}
```

### Excel Column Letter to Index Conversion

The tool converts Excel column letters to 0-based indices:

| Letter | Index | Calculation |
|--------|-------|-------------|
| A      | 0     | 1 - 1 = 0 |
| B      | 1     | 2 - 1 = 1 |
| Z      | 25    | 26 - 1 = 25 |
| AA     | 26    | (1×26 + 1) - 1 = 26 |
| AB     | 27    | (1×26 + 2) - 1 = 27 |
| CS     | 96    | (3×26 + 19) - 1 = 96 |

**Formula:** For column letters like "CS":
```
C = 3rd letter → 3
S = 19th letter → 19
Index = (3 × 26 + 19) - 1 = 96
```

### KPI Scoring

| Letter | Meaning | Score |
|--------|---------|-------|
| J      | Green (Good) | 3 |
| K      | Orange (Medium) | 2 |
| L      | Red (Bad) | 1 |
| Missing/Invalid | Treated as worst | 1 |

### Troubleshooting

**"No .xlsx files found"**
- Ensure Excel file is in same folder as .exe
- Check file extension is .xlsx (not .xls)

**"No rows found with phase 'X'"**
- Verify phase_value in config matches exactly (case-sensitive)
- Check the correct sheet name is configured

**Chart looks empty**
- Verify KPI columns exist in Excel (CS, DA, DD, DF, DH, DJ)
- Check KPI values are J, K, or L

### Files Overview

```
quadrant_project/
├── quadrant.py           # Main Python script
├── quadrant_config.json  # Configuration file
├── README.md             # This file
├── build.bat             # Windows build script
└── requirements.txt      # Python dependencies
```

---

## Privacy & Security

- **No data upload**: All processing happens locally
- **No external services**: Works completely offline
- **No telemetry**: No usage tracking or analytics
