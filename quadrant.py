#!/usr/bin/env python3
"""
Project Risk vs Impact Quadrant Chart Generator

Reads Excel data, calculates KPI scores, and generates an interactive
Plotly bubble chart saved as a standalone HTML file.

Usage: python quadrant.py
       or double-click Quadrant.exe (after PyInstaller build)
"""

import json
import os
import sys
import webbrowser
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_script_dir():
    """Get directory where script/exe is located."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return Path(sys.executable).parent
    else:
        # Running as Python script
        return Path(__file__).parent


def col_letter_to_index(col_letter: str) -> int:
    """
    Convert Excel column letter(s) to 0-based index.
    Examples: A=0, B=1, Z=25, AA=26, AZ=51, CS=96
    """
    result = 0
    for char in col_letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def find_excel_file(script_dir: Path, config_filename: str = None) -> Path:
    """
    Find Excel file to process.
    Priority: config filename > newest .xlsx in folder
    """
    if config_filename:
        config_path = script_dir / config_filename
        if config_path.exists():
            print(f"Using configured Excel file: {config_filename}")
            return config_path
        else:
            print(f"Warning: Configured file '{config_filename}' not found.")
    
    # Find newest .xlsx file
    xlsx_files = list(script_dir.glob("*.xlsx"))
    if not xlsx_files:
        raise FileNotFoundError("No .xlsx files found in folder.")
    
    newest = max(xlsx_files, key=lambda f: f.stat().st_mtime)
    print(f"Using newest Excel file: {newest.name}")
    return newest


def load_config(script_dir: Path) -> dict:
    """Load configuration from JSON file."""
    config_path = script_dir / "quadrant_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print("Warning: quadrant_config.json not found, using defaults.")
        return {
            "excel_filename": None,
            "sheet_name": "Roadmap",
            "views": []
        }


def parse_kpi_value(value, scoring_map: dict, default_score: int) -> tuple:
    """
    Parse KPI value and return (letter, numeric_score).
    Invalid/missing values return (None, default_score).
    """
    if pd.isna(value) or value is None:
        return (None, default_score)
    
    value_str = str(value).strip().upper()
    if value_str in scoring_map:
        return (value_str, scoring_map[value_str])
    
    return (None, default_score)


def process_view(df: pd.DataFrame, view_config: dict) -> pd.DataFrame:
    """Process data for a single view and return processed DataFrame."""
    
    # Get column indices
    project_col_idx = col_letter_to_index(view_config['project_name_column'])
    phase_col_idx = col_letter_to_index(view_config['phase_column'])
    
    # Filter by phase (skip header row)
    phase_value = view_config['phase_value']
    mask = df.iloc[:, phase_col_idx] == phase_value
    filtered_df = df[mask].copy()
    
    if filtered_df.empty:
        print(f"  Warning: No rows found with phase '{phase_value}'")
        return pd.DataFrame()
    
    print(f"  Found {len(filtered_df)} projects with phase '{phase_value}'")
    
    # Extract configuration
    kpi_columns = view_config['kpi_columns']
    scoring_map = view_config['scoring_map']
    default_score = view_config.get('default_score', 1)
    x_kpis = view_config['x_axis']['kpis']
    y_kpis = view_config['y_axis']['kpis']
    
    # Build results
    results = []
    
    for idx in filtered_df.index:
        project_name = df.iloc[idx, project_col_idx]
        if pd.isna(project_name) or not str(project_name).strip():
            continue
        
        row_data = {
            'project_name': str(project_name).strip(),
            'row_index': idx + 1  # 1-based for Excel reference
        }
        
        # Parse all KPI values
        kpi_scores = {}
        for kpi_col, kpi_name in kpi_columns.items():
            col_idx = col_letter_to_index(kpi_col)
            raw_value = df.iloc[idx, col_idx]
            letter, score = parse_kpi_value(raw_value, scoring_map, default_score)
            
            row_data[f'{kpi_col}_letter'] = letter if letter else 'N/A'
            row_data[f'{kpi_col}_score'] = score
            row_data[f'{kpi_col}_name'] = kpi_name
            kpi_scores[kpi_col] = score
        
        # Calculate X (Delivery Performance)
        x_scores = [kpi_scores[k] for k in x_kpis if k in kpi_scores]
        row_data['x_value'] = sum(x_scores) / len(x_scores) if x_scores else default_score
        
        # Calculate Y (Project Health / Risk)
        y_scores = [kpi_scores[k] for k in y_kpis if k in kpi_scores]
        row_data['y_value'] = sum(y_scores) / len(y_scores) if y_scores else default_score
        
        # Calculate overall score
        all_scores = list(kpi_scores.values())
        row_data['overall'] = sum(all_scores) / len(all_scores) if all_scores else default_score
        
        # Calculate bubble size: badness = (4 - overall), size = badness^2 * 20 + 10
        badness = 4 - row_data['overall']
        row_data['bubble_size'] = (badness ** 2) * 20 + 10
        
        # Determine color based on overall score
        color_thresholds = view_config.get('color_thresholds', {'green': 2.5, 'orange_min': 1.75})
        if row_data['overall'] >= color_thresholds['green']:
            row_data['color'] = 'green'
        elif row_data['overall'] > color_thresholds['orange_min']:
            row_data['color'] = 'orange'
        else:
            row_data['color'] = 'red'
        
        results.append(row_data)
    
    return pd.DataFrame(results)


def create_quadrant_chart(data: pd.DataFrame, view_config: dict) -> go.Figure:
    """Create a single quadrant chart for one view."""
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for this view",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    # Get config values
    x_label = view_config['x_axis']['label']
    y_label = view_config['y_axis']['label']
    thresholds = view_config.get('quadrant_thresholds', {'x': 2, 'y': 2})
    quadrant_labels = view_config.get('quadrant_labels', {
        'top_right': 'On Track',
        'top_left': 'Delivery Issues',
        'bottom_right': 'Health Concerns',
        'bottom_left': 'Critical'
    })
    kpi_columns = view_config['kpi_columns']
    
    # Build hover text
    hover_texts = []
    for _, row in data.iterrows():
        kpi_lines = []
        for kpi_col, kpi_name in kpi_columns.items():
            letter = row.get(f'{kpi_col}_letter', 'N/A')
            score = row.get(f'{kpi_col}_score', 1)
            kpi_lines.append(f"  {kpi_name} ({kpi_col}): {letter} = {score}")
        
        hover_text = (
            f"<b>{row['project_name']}</b><br>"
            f"<br>"
            f"X ({x_label}): {row['x_value']:.2f}<br>"
            f"Y ({y_label}): {row['y_value']:.2f}<br>"
            f"Overall Score: {row['overall']:.2f}<br>"
            f"<br>"
            f"<b>KPI Details:</b><br>"
            + "<br>".join(kpi_lines)
        )
        hover_texts.append(hover_text)
    
    # Create figure
    fig = go.Figure()
    
    # Add bubbles by color group for legend
    color_map = {'green': '#2ecc71', 'orange': '#f39c12', 'red': '#e74c3c'}
    color_names = {'green': 'Good (≥2.5)', 'orange': 'Medium (1.75-2.5)', 'red': 'At Risk (≤1.75)'}
    
    for color in ['green', 'orange', 'red']:
        mask = data['color'] == color
        if mask.sum() == 0:
            continue
        
        subset = data[mask]
        subset_hovers = [hover_texts[i] for i in subset.index]
        
        fig.add_trace(go.Scatter(
            x=subset['x_value'],
            y=subset['y_value'],
            mode='markers',
            name=color_names[color],
            marker=dict(
                size=subset['bubble_size'],
                color=color_map[color],
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=subset['project_name'],
            hovertemplate='%{customdata}<extra></extra>',
            customdata=subset_hovers
        ))
    
    # Add quadrant threshold lines
    fig.add_hline(y=thresholds['y'], line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=thresholds['x'], line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    label_positions = [
        (thresholds['x'] + 0.5, thresholds['y'] + 0.5, quadrant_labels['top_right']),
        (thresholds['x'] - 0.5, thresholds['y'] + 0.5, quadrant_labels['top_left']),
        (thresholds['x'] + 0.5, thresholds['y'] - 0.5, quadrant_labels['bottom_right']),
        (thresholds['x'] - 0.5, thresholds['y'] - 0.5, quadrant_labels['bottom_left']),
    ]
    
    for x_pos, y_pos, label in label_positions:
        fig.add_annotation(
            x=x_pos, y=y_pos,
            text=f"<b>{label}</b>",
            showarrow=False,
            font=dict(size=12, color='gray'),
            opacity=0.6
        )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis=dict(range=[0.5, 3.5], dtick=0.5),
        yaxis=dict(range=[0.5, 3.5], dtick=0.5),
        hovermode='closest',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=60, r=40, t=40, b=60)
    )
    
    return fig


def create_tabbed_html(figures: list, view_names: list, output_path: Path):
    """Create a single HTML file with tabs for multiple views."""
    
    # Generate div IDs and content for each figure
    tabs_html = []
    content_html = []
    
    for i, (fig, name) in enumerate(zip(figures, view_names)):
        tab_id = f"tab{i}"
        active_class = "active" if i == 0 else ""
        display_style = "block" if i == 0 else "none"
        
        tabs_html.append(f'<button class="tab-btn {active_class}" onclick="showTab(\'{tab_id}\')">{name}</button>')
        
        # Get the plotly div content
        fig_html = fig.to_html(full_html=False, include_plotlyjs=False)
        content_html.append(f'<div id="{tab_id}" class="tab-content" style="display: {display_style};">{fig_html}</div>')
    
    html_template = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Project Quadrant Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .tab-container {{
            margin-bottom: 10px;
        }}
        .tab-btn {{
            padding: 10px 20px;
            border: none;
            background-color: #ddd;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 5px 5px 0 0;
            font-size: 14px;
        }}
        .tab-btn:hover {{
            background-color: #ccc;
        }}
        .tab-btn.active {{
            background-color: #fff;
            font-weight: bold;
        }}
        .tab-content {{
            background-color: #fff;
            padding: 20px;
            border-radius: 0 5px 5px 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
    <script>
        function showTab(tabId) {{
            // Hide all tabs
            var contents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < contents.length; i++) {{
                contents[i].style.display = 'none';
            }}
            // Remove active class from all buttons
            var btns = document.getElementsByClassName('tab-btn');
            for (var i = 0; i < btns.length; i++) {{
                btns[i].classList.remove('active');
            }}
            // Show selected tab and activate button
            document.getElementById(tabId).style.display = 'block';
            event.target.classList.add('active');
            // Trigger Plotly relayout to fix sizing
            var plotDiv = document.getElementById(tabId).querySelector('.plotly-graph-div');
            if (plotDiv) {{
                Plotly.Plots.resize(plotDiv);
            }}
        }}
    </script>
</head>
<body>
    <h1>Project Quadrant Analysis</h1>
    <div class="tab-container">
        {"".join(tabs_html)}
    </div>
    {"".join(content_html)}
    <div class="footer">
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
</body>
</html>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"HTML output saved: {output_path}")


def save_csv_output(all_data: dict, output_path: Path):
    """Save processed data to CSV for audit purposes."""
    
    all_rows = []
    for view_name, df in all_data.items():
        if df.empty:
            continue
        df_copy = df.copy()
        df_copy['view'] = view_name
        all_rows.append(df_copy)
    
    if all_rows:
        combined = pd.concat(all_rows, ignore_index=True)
        combined.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"CSV output saved: {output_path}")
    else:
        print("No data to save to CSV.")


def main():
    print("="*60)
    print("Project Quadrant Chart Generator")
    print("="*60)
    
    # Get script directory
    script_dir = get_script_dir()
    print(f"Working directory: {script_dir}")
    
    # Load configuration
    config = load_config(script_dir)
    
    # Find Excel file
    try:
        excel_path = find_excel_file(script_dir, config.get('excel_filename'))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
        return
    
    # Read Excel file
    print(f"\nReading Excel file: {excel_path.name}")
    try:
        df = pd.read_excel(excel_path, sheet_name=config.get('sheet_name', 'Roadmap'), header=None)
        print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        print(f"Error reading Excel: {e}")
        input("Press Enter to exit...")
        return
    
    # Process each enabled view
    figures = []
    view_names = []
    all_data = {}
    
    for view_config in config.get('views', []):
        view_name = view_config.get('name', 'Unnamed View')
        
        if not view_config.get('enabled', True):
            print(f"\nSkipping disabled view: {view_name}")
            continue
        
        print(f"\nProcessing view: {view_name}")
        
        # Process data for this view
        processed_data = process_view(df, view_config)
        all_data[view_name] = processed_data
        
        # Create chart
        fig = create_quadrant_chart(processed_data, view_config)
        fig.update_layout(title=view_name)
        
        figures.append(fig)
        view_names.append(view_name)
    
    if not figures:
        print("\nNo enabled views found. Creating default KPI view...")
        # Create a minimal default view if no views configured
        default_view = {
            'name': 'Default View',
            'project_name_column': 'E',
            'phase_column': 'T',
            'phase_value': '5 Réalisation',
            'kpi_columns': {'CS': 'Launch', 'DA': 'Planning', 'DD': 'Budget', 
                           'DF': 'Scope', 'DH': 'Risk', 'DJ': 'Change'},
            'x_axis': {'label': 'Delivery Performance', 'kpis': ['DA', 'DD', 'DF']},
            'y_axis': {'label': 'Project Health', 'kpis': ['CS', 'DH', 'DJ']},
            'scoring_map': {'J': 3, 'K': 2, 'L': 1},
            'default_score': 1
        }
        processed_data = process_view(df, default_view)
        all_data['Default View'] = processed_data
        fig = create_quadrant_chart(processed_data, default_view)
        figures.append(fig)
        view_names.append('Default View')
    
    # Generate outputs
    html_output = script_dir / "quadrant.html"
    csv_output = script_dir / "quadrant_output.csv"
    
    # Create tabbed HTML
    create_tabbed_html(figures, view_names, html_output)
    
    # Save CSV
    save_csv_output(all_data, csv_output)
    
    # Open in browser
    print(f"\nOpening chart in browser...")
    webbrowser.open(html_output.as_uri())
    
    print("\n" + "="*60)
    print("Done! Chart opened in default browser.")
    print("="*60)
    
    # Keep window open if running as exe
    if getattr(sys, 'frozen', False):
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
