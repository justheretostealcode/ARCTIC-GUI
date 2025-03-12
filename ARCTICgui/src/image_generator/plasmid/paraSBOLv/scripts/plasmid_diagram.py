"""
Plasmid diagram visualization module.
Provides functions for generating plasmid diagrams from genetic circuit descriptions.
"""
import os
import json
import matplotlib.pyplot as plt

import image_generator.plasmid.paraSBOLv.scripts.set_path
import image_generator.plasmid.paraSBOLv.parasbolv.parasbolv as psv

from image_generator.plasmid.paraSBOLv.scripts.plasmid_utils import parse_gene_info, generate_connections_from_plasmid_data, log
from image_generator.plasmid.paraSBOLv.scripts.plasmid_connection_router import ConnectionRouter
from image_generator.plasmid.paraSBOLv.scripts.plasmid_drawer import draw_constructs, draw_connections

def create_plasmid_diagram(plasmid_data, output_path="plasmid_diagram.png", 
                           show=False, save_pdf=False, vertical_gap=200, dpi=300):
    """
    Create a plasmid diagram and save it to a file.
    
    Args:
        plasmid_data: List of gene strings for each row
        output_path: Path to save the diagram image
        show: Whether to display the diagram
        save_pdf: Whether to also save as PDF
        vertical_gap: Vertical spacing between rows
        dpi: Resolution of the output image
        
    Returns:
        Path to the saved diagram
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect('equal')
    
    # Filter out None values from plasmid data
    filtered_plasmid_data = []
    for row in plasmid_data:
        filtered_row = [gene for gene in row if gene is not None]
        filtered_plasmid_data.append(filtered_row)
    
    # Row heights: top row at higher y-value, bottom row at lower y-value
    row_heights = [vertical_gap, 80]
    spacing = 50  # Spacing between constructs
    
    # Draw each row of constructs
    drawn_constructs = []
    for i, row_data in enumerate(filtered_plasmid_data):
        row_constructs = draw_constructs(ax, row_data, i, row_heights[i], spacing)
        drawn_constructs.append(row_constructs)
    
    # Generate connections directly from plasmid data
    connections_to_draw = generate_connections_from_plasmid_data(filtered_plasmid_data)
    
    # Draw the connections
    draw_connections(ax, connections_to_draw, drawn_constructs, vertical_gap)
    
    # Adjust figure bounds
    all_bounds = []
    for row in drawn_constructs:
        for construct in row:
            all_bounds.append(construct['bounds'])
    
    if all_bounds:
        # Find outer bounds
        min_x = min(bound[0][0] for bound in all_bounds)
        min_y = min(bound[0][1] for bound in all_bounds)
        max_x = max(bound[1][0] for bound in all_bounds)
        max_y = max(bound[1][1] for bound in all_bounds)
        
        # Add margins
        margin = 50
        ax.set_xlim(min_x - margin, max_x + margin)
        ax.set_ylim(min_y - margin, max_y + margin)
    
    # Remove axes
    ax.axis('off')
    
    # Save the diagram
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', transparent=True)
    
    # Save as PDF if requested
    if save_pdf:
        pdf_path = os.path.splitext(output_path)[0] + '.pdf'
        plt.savefig(pdf_path, dpi=dpi, bbox_inches='tight')
        log(f"PDF saved to: {pdf_path}")
    
    # Show if requested
    if show:
        # Try to maximize the window
        manager = plt.get_current_fig_manager()
        try:
            # Qt backend
            manager.window.showMaximized()
        except AttributeError:
            try:
                # TkAgg backend
                manager.window.state('zoomed')
            except:
                # Other backends - no maximization
                pass
        
        plt.show()
    else:
        plt.close(fig)
    
    return output_path

def parse_input_data(data_str, data_type):
    """Parse input data from string or file"""
    if not data_str:
        return None
    
    # Check if it's a file path
    if os.path.isfile(data_str):
        with open(data_str, 'r') as f:
            data_str = f.read()
    
    if data_type == 'json':
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            return None
    elif data_type == 'python':
        # Evaluate Python literal structures only (safe)
        import ast
        try:
            return ast.literal_eval(data_str)
        except (SyntaxError, ValueError):
            return None
    
    return None

def create_diagram_from_strings(plasmid_str, output_path="plasmid_diagram.png",
                              show=False, save_pdf=False, plasmid_input_type='python'):
    """Create a plasmid diagram from string representations of data"""
    # Parse input data
    plasmid_data = parse_input_data(plasmid_str, plasmid_input_type)
    
    # Create the diagram
    if plasmid_data:
        return create_plasmid_diagram(
            plasmid_data, 
            output_path, 
            show,
            save_pdf
        )
    else:
        return None

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Generate plasmid diagrams")
    parser.add_argument('--plasmid', type=str, help='Python list string or file path with plasmid data')
    parser.add_argument('--output', type=str, default='plasmid_diagram.png', help='Output file path')
    parser.add_argument('--show', action='store_true', help='Show the diagram in a window')
    parser.add_argument('--pdf', action='store_true', help='Also save as PDF')
    parser.add_argument('--gap', type=int, default=200, help='Vertical gap between rows')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for output images')
    
    args = parser.parse_args()
    
    # Use default data if no plasmid data provided
    if not args.plasmid:
        try:
            # Try to import from the local directory
            import importlib.util
            
            # Check for plasmid_data.py in the current directory
            data_path = os.path.join(os.path.dirname(__file__), "plasmid_data.py")
            if os.path.exists(data_path):
                spec = importlib.util.spec_from_file_location("plasmid_data", data_path)
                plasmid_data_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plasmid_data_module)
                
                # Create the diagram with default data
                output_path = create_plasmid_diagram(
                    plasmid_data_module.TEST_PLASMID_DATA,
                    args.output,
                    args.show,
                    args.pdf,
                    args.gap,
                    args.dpi
                )
                
                if output_path:
                    log(f"Diagram saved to: {output_path}")
                else:
                    log("Failed to create diagram")
                sys.exit(0)
            else:
                log("No plasmid data provided and plasmid_data.py not found.")
                parser.print_help()
                sys.exit(1)
        except Exception as e:
            import traceback
            log(f"Error loading default data: {e}")
            log("\nDetailed traceback:")
            traceback.print_exc()
            parser.print_help()
            sys.exit(1)
    
    # If we got here, use the provided arguments
    output_path = create_diagram_from_strings(
        args.plasmid,
        args.output,
        args.show,
        args.pdf
    )
    
    if output_path:
        log(f"Diagram saved to: {output_path}")
    else:
        log("Failed to create diagram")

